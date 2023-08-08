# -*- coding: utf-8 -*-
# Author: Jan Jakub Kubik
# Date: 10.04.2022

import numpy as np  
import pandas as pd  
from sklearn.svm import OneClassSVM
from sklearn.model_selection import train_test_split 

from datasets import agregate_to_intervals, MINUTES


def prepare_dataset(filename):
    data = agregate_to_intervals(filename, MINUTES)
    #print(data)

    df = pd.DataFrame(data)

    # normalize the read_data - which leads to better accuracy and reduces numerical instability.
    df["packet_nmb"] = df["packet_nmb"].apply(lambda x: x)  
    df["packet_nmb"] = abs(np.log(df["packet_nmb"])).astype(float)
    df["avg_inter_arrival_time"] = df["avg_inter_arrival_time"].apply(lambda x: x)
    df["avg_inter_arrival_time"] = abs(np.log(df["avg_inter_arrival_time"])).astype(float)
    df["avg_packet_size"] = abs(np.log(df["avg_packet_size"])).astype(float)

    return df


def compute_accuracy(model, train_data, validation_data):
    values_preds = model.predict(train_data) 
    print(values_preds)

    suma = 0
    for x in values_preds:
        if x == 1:
            suma += x
    
    print(suma)
    print("Train data accuracy:")
    print("---------------" * 2)
    print(f"{suma / len(values_preds) * 100}%")



    values_preds = model.predict(validation_data) 
    print(values_preds)

    suma = 0
    for x in values_preds:
        if x == 1:
            suma += x
    
    print(suma)
    print("Validation data accuracy:")
    print("---------------" * 2)
    print(f"{suma / len(values_preds) * 100}%")


def create_model(dataset, comp_acc=False):
    train_data, validation_data = train_test_split(dataset, train_size = 0.66)  

    model = OneClassSVM(nu=0.001, kernel="poly", gamma="auto").fit(train_data)

    if comp_acc: 
        compute_accuracy(model, train_data, validation_data)

    return model 


def main():
    filename_1_ms = "datasets/104_mega/104_mega_master_slaves.csv"
    filename_1_sm = "datasets/104_mega/104_mega_slaves_master.csv"
    filename_2_ms = "datasets/10122018/10122018_master_slaves.csv"
    filename_2_sm = "datasets/10122018/10122018_slaves_master.csv"

    dataset_1_ms = prepare_dataset(filename_1_ms)
    dataset_1_sm = prepare_dataset(filename_1_sm)
    dataset_2_ms = prepare_dataset(filename_2_ms)
    dataset_2_sm = prepare_dataset(filename_2_sm)

    create_model(dataset_1_ms, comp_acc=True)
    create_model(dataset_1_sm, comp_acc=True)
    create_model(dataset_2_ms, comp_acc=True)
    create_model(dataset_2_sm, comp_acc=True)


if __name__ == "__main__":
    main()
