#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Jan Jakub Kubik (xkubik32)
# BIO - faces recognition - helping functions
# 04.11.2022


import time
import os
import re
import logging
from typing import List, Tuple

from deepface.commons import functions

from tqdm import tqdm
import pandas as pd

from settings import DETECTOR_BACKEND, PTIME


def compute_fps() -> float:
    """Compute frames per second."""
    global PTIME
    cTime = time.time()
    fps = 1 / (cTime - PTIME)
    PTIME = cTime  # side effect

    return fps


def get_name_from_path(path: str) -> str:
    """Extract img name from path."""
    label = path.split("/")[-1].replace(".jpeg", "")
    label = re.sub("[0-9]", "", label)

    return label


def get_people_imgs_paths(db_path: str) -> List[str]:
    """Get full paths to all imgs stored in db folder."""
    db_people_paths = []
    # check passed db folder exists
    if os.path.isdir(db_path) == True:
        for r, _, f in os.walk(db_path):  # r=root, d=directories, f = files
            for file in f:
                if ".jpeg" in file:
                    # exact_path = os.path.join(r, file)
                    exact_path = r + "/" + file
                    # logging.info(exact_path)
                    db_people_paths.append(exact_path)

    if not db_people_paths:
        logging.info(
            f"WARNING: There is no image in this path {db_path}. Face recognition will not be performed."
        )

    return db_people_paths


def create_embeddings_from_db_people_imgs(
    db_people_paths: List[str], recognition_model, input_shape: Tuple[int]
) -> pd.core.frame.DataFrame:
    """Compute embeddings from imgs paths."""
    pbar = tqdm(range(0, len(db_people_paths)), desc="Finding embeddings")
    embeddings = []
    # for employee in db_people_paths:
    for index in pbar:
        employee = db_people_paths[index]
        pbar.set_description("Finding embedding for %s" % (employee.split("/")[-1]))
        embedding = []

        # preprocess_face returns single face. this is expected for source images in db.
        img = functions.preprocess_face(
            img=employee,
            target_size=input_shape,
            enforce_detection=False,
            detector_backend=DETECTOR_BACKEND,
        )
        img_representation = recognition_model.predict(img)[0, :]

        embedding.append(employee)
        embedding.append(img_representation)
        embeddings.append(embedding)

    logging.info(embeddings)
    df = pd.DataFrame(embeddings, columns=["employee", "embedding"])

    return df
