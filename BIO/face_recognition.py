#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Jakub Kubik (xkubik32)
# BIO - faces recognition
# 04.11.2022

"""

live video face recognition (most important part of project)

"""

import logging
from typing import Tuple
import time

import cv2
import pandas as pd
import numpy as np

from deepface import DeepFace
from deepface.detectors import FaceDetector
from deepface.commons import functions, distance as dst

from settings import (
    DB_PATH,
    DETECTOR_BACKEND,
    RECOGNITION_MODEL_NAME,
    DISTANCE_METHODS,
    DISTANCE_METRIC,
)

distance_function = DISTANCE_METHODS[DISTANCE_METRIC]

from utils import (
    create_embeddings_from_db_people_imgs,
    compute_fps,
    get_name_from_path,
    get_people_imgs_paths,
)


def find_face_best_match(df: pd.core.frame.DataFrame, face: np.ndarray, input_shape: Tuple[int], recognition_model) -> Tuple[str, np.float64]:
    """Compute embedding from face image and find best match among stored imgages (df) and return best img score and name."""

    def computeDistance(row: pd.core.series.Series) -> np.float64:
        """compute distance between detected face and stored face."""
        db_img_embedding = row["embedding"]
        if DISTANCE_METRIC == "euclidean_l2":
            distance = distance_function(dst.l2_normalize(detected_img_embedding), dst.l2_normalize(db_img_embedding))
        else:
            distance = distance_function(detected_img_embedding, db_img_embedding)

        return distance

    img_pixels = functions.preprocess_face(
        img=face,
        target_size=input_shape,
        enforce_detection=False,
        detector_backend=DETECTOR_BACKEND,
    )
    detected_img_embedding = recognition_model.predict(img_pixels)[0, :]
    df["distance"] = df.apply(computeDistance, axis=1)
    df = df.sort_values(by=["distance"])
    candidate = df.iloc[0]
    employee_name = candidate["employee"]
    best_distance = candidate["distance"]

    return employee_name, best_distance


def live_video_face_recognition():
    """Main function for live video face recognition."""
    # get path to all imgs stored i db folder
    db_people_paths = get_people_imgs_paths(DB_PATH)

    # webcam initialization - TODO maybe change to external camera
    cap = cv2.VideoCapture(0)
    # cap = cv2.VideoCapture("tests/basic/basic.mp4")
    # cap = cv2.VideoCapture("tests/multiple_persons/big_bang.mp4")
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1024)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1024)

    # face detector initialization
    face_detector = FaceDetector.build_model(DETECTOR_BACKEND)
    logging.info(f"Face_detector model: {DETECTOR_BACKEND} is initialized")

    # face recognition model initialization
    recognition_model = DeepFace.build_model(RECOGNITION_MODEL_NAME)
    logging.info(f"Recognition model: {RECOGNITION_MODEL_NAME} is initialized")

    # input shapes initialization
    input_shape = functions.find_input_shape(recognition_model)

    # create embeddings from stored people imgs
    df = create_embeddings_from_db_people_imgs(
        db_people_paths, recognition_model, input_shape
    )
    logging.info(df)

    # threshold for embedding vectors comparison
    threshold = dst.findThreshold(RECOGNITION_MODEL_NAME, DISTANCE_METRIC)

    # infinite loop because of processing video frame after frame

    counter = 0

    detected_faces_counter = 0
    total_distance = 0
    start_time = time.time()

    while True:
        # capture image
        success, img = cap.read()
        if not success:
            break

        # detect all faces in image
        try:
            faces = FaceDetector.detect_faces(
                face_detector, DETECTOR_BACKEND, img, align=False
            )
        except:  # to avoid exception if no face detected
            faces = []
            cv2.imshow("Image", img)

        if not faces:  # nothing to do
            continue

        counter += 1

        # try to recognize detected faces one after another
        for face, (x, y, w, h) in faces:

            # draw rectangle around recognized face to image
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # get detected face embedding vector, compare it to db and select the best matching
            try:
                employee_name, best_distance = find_face_best_match(
                    df, face, input_shape, recognition_model
                )
            except Exception:  # toto mozno este poriesit ked sa mi bude fakt moc chciet
                continue

            # set name if best embedding vector precision is enough
            label = "unknown"
            detected_faces_counter += 1
            total_distance += best_distance

            if best_distance <= threshold:
                label = get_name_from_path(employee_name)

            cv2.putText(img, label, (x, y), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 2)

        # compute and add fps to image
        fps = compute_fps()
        cv2.putText(
            img, f"FPS: {int(fps)}", (20, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 2
        )

        # show final image
        cv2.imshow("Image", img)

        # press q to quit
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

        if counter % 10 == 0:
            print(f"Average FPS from start: {counter / (time.time() - start_time)}")
            print(f"Average distance of detected faces with most similar faces from start: {total_distance / detected_faces_counter or 1}")
            print(f"Best distance: {best_distance}. Threshold for face recognition: {threshold}")

    end_time = time.time()
    print(f"Total average FPS: {counter / (end_time - start_time)}")
    print(f"Total average distance of detected faces with most similar faces: {total_distance / detected_faces_counter or 1}")
