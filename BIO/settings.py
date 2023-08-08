#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Jan Jakub Kubik (xkubik32)
# BIO - faces recognition - settings
# 04.11.2022

import os

from deepface.commons import distance as dst

PTIME = 0


DB_PATH = os.getcwdb().decode() + "/database"
DETECTOR_BACKEND = "ssd"
# RECOGNITION_MODEL_NAME = "Facenet"
# RECOGNITION_MODEL_NAME = "ArcFace"
RECOGNITION_MODEL_NAME = "SFace"

# euclidean_l2 mozno ale asi neni treba
DISTANCE_METHODS = {
    "cosine": dst.findCosineDistance,
    "euclidean": dst.findEuclideanDistance,
    "euclidean_l2": dst.findEuclideanDistance,
}
# DISTANCE_METRIC = "cosine"
# DISTANCE_METRIC = "euclidean"
DISTANCE_METRIC = "euclidean_l2"
