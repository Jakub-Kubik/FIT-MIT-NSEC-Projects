# -*- coding: utf-8 -*-
# Author: Jan Jakub Kubik
# Date: 10.04.2022

import numpy as np 
import pandas as pd

pd.options.mode.chained_assignment = None  # default="warn"

from models import prepare_dataset, create_model
from datasets import create_graph
 
import pandas as pd  


def get_model_and_dataset(filename, cutting=False):
    if cutting:
        dataset = prepare_dataset(filename)[6:]
    else:
        dataset = prepare_dataset(filename)

    #print(dataset)
    model = create_model(dataset)

    return model, dataset


def test_model(model, dataset):
    start_index = int(len(dataset)/2)

    # DDOS setup
    df_1 = dataset.iloc[:start_index,:]
    df_2 = dataset.iloc[start_index:,:]
    df_2["packet_nmb"] = abs(np.exp(df_2["packet_nmb"])).astype(float)
    df_2["packet_nmb"] = df_2["packet_nmb"].apply(lambda x: x * 2)
    df_2["packet_nmb"] = abs(np.log(df_2["packet_nmb"])).astype(float)

    df_2["avg_inter_arrival_time"] = abs(np.exp(df_2["avg_inter_arrival_time"])).astype(float)
    df_2["avg_inter_arrival_time"] = df_2["avg_inter_arrival_time"].apply(lambda x: x * 0.5)
    df_2["avg_inter_arrival_time"] = abs(np.log(df_2["avg_inter_arrival_time"])).astype(float)

    df_2["avg_packet_size"] = abs(np.exp(df_2["avg_packet_size"])).astype(float)
    df_2["avg_packet_size"] = df_2["avg_packet_size"].apply(lambda x: x * 0.3)
    df_2["avg_packet_size"] = abs(np.log(df_2["avg_packet_size"])).astype(float)


    df_3 = pd.concat([df_1, df_2])
    create_graph(df_3.to_dict("records"))
    results = model.predict(df_3)
    res_pos = results[:start_index]
    #print(results)

    print(f"number of items: {int(len(dataset))}")
    suma = 0
    for x in res_pos:
        if x == 1:
            suma += x
    
    print("Positive data accuracy:")
    print("---------------" * 2)
    print(f"{suma / len(res_pos) * 100}%")
    print(f"total {len(res_pos)}")
    print(f"total TP: {suma}")
    print(f"total FP: {len(res_pos) - suma}")
    print("============" * 10)

    res_neg = results[start_index:]
    suma = 0
    for x in res_neg:
        if x == -1:
            suma += 1
    
    print("Negative data accuracy:")
    print("---------------" * 2)
    print(f"{suma / len(res_neg) * 100}%")
    print(f"total {len(res_neg)}")
    print(f"total TN: {suma}")
    print(f"total FN: {len(res_neg) - suma}")



def main():
    filename_1_ms = "datasets/104_mega/104_mega_master_slaves.csv"
    filename_1_sm = "datasets/104_mega/104_mega_slaves_master.csv"
    filename_2_ms = "datasets/10122018/10122018_master_slaves.csv"
    filename_2_sm = "datasets/10122018/10122018_slaves_master.csv"
    
    model_1, dataset_1_ms = get_model_and_dataset(filename_1_ms)
    model_2, dataset_1_sm = get_model_and_dataset(filename_1_sm)
    model_3, dataset_2_ms = get_model_and_dataset(filename_2_ms, cutting=True)
    model_4, dataset_2_sm = get_model_and_dataset(filename_2_sm, cutting=True)

    print("******************" * 5)
    print("Testing model 1 master --> slaves")
    print("******************" * 5)
    test_model(model_1, dataset_1_ms)

    print("******************" * 5)
    print("Testing model 2 slaves --> master")
    print("******************" * 5)
    test_model(model_2, dataset_1_sm)

    print("******************" * 5)
    print("Testing model 3 master --> slaves")
    print("******************" * 5)
    test_model(model_3, dataset_2_ms)

    print("******************" * 5)
    print("Testing model 4 slaves --> master")
    print("******************" * 5)
    test_model(model_4, dataset_2_sm)


if __name__ == "__main__":
    main()
