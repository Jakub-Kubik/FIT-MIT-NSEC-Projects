# -*- coding: utf-8 -*-
# Author: Jan Jakub Kubik
# Date: 01.04.2022
 
import csv

import matplotlib.pyplot as plt

MINUTES = 5

csv_fields = ["src_ip", "src_port", "dst_ip", "dst_port", "time", "bytes"]


def split_flows(read_csv_file, master_ip):
    """Split flows (create new file) for: master --> slaves flow and slaves --> master flow."""

    print(f"file: {read_csv_file}")

    write_master_slaves_csv_file = read_csv_file[:-4] + "_master_slaves.csv"
    write_slaves_master_csv_file = read_csv_file[:-4] + "_slaves_master.csv"
    #print(write_slaves_master_csv_file)
    #print(write_slaves_master_csv_file)

    reader = csv.DictReader(open(read_csv_file), delimiter=";", fieldnames=csv_fields)
    writer_master_slave = csv.DictWriter(open(write_master_slaves_csv_file, "w"), delimiter=";", fieldnames=csv_fields)
    writer_slave_master = csv.DictWriter(open(write_slaves_master_csv_file, "w"), delimiter=";", fieldnames=csv_fields)

    for row in reader:
        if row["src_ip"] == master_ip:
            writer_master_slave.writerow(row)
        else:
            writer_slave_master.writerow(row)

    return write_master_slaves_csv_file, write_slaves_master_csv_file


def agregate_to_intervals(read_csv_file, minutes):
    """Agregate fields to time intervals."""

    print(f"file: {read_csv_file}")

    reader = csv.DictReader(open(read_csv_file), delimiter=";", fieldnames=csv_fields)

    stats = []

    prev_packet_time = 0
    data_for_stats = {
        "number_of_packets": 0,
        "inter_arrival_times": [],
        "packet_sizes": [],
    }

    time_index = 1
    for i, row in enumerate(reader):
        if float(row["time"]) > time_index * 60 * minutes:
            # print(data_for_stats["inter_arrival_times"])
            # print(data_for_stats["packet_sizes"])
            # print(data_for_stats["number_of_packets"])

            stats.append({
                "packet_nmb": data_for_stats["number_of_packets"],
                "avg_inter_arrival_time": sum(data_for_stats["inter_arrival_times"]) / data_for_stats["number_of_packets"],
                "avg_packet_size": sum(data_for_stats["packet_sizes"])
            })

            data_for_stats = {
                "number_of_packets": 0,
                "inter_arrival_times": [],
                "packet_sizes": [],
            }
            time_index += 1

        else:
            data_for_stats["number_of_packets"] += 1
            data_for_stats["inter_arrival_times"].append(float(row["time"]) - prev_packet_time)
            data_for_stats["packet_sizes"].append(int(row["bytes"]))

            prev_packet_time = float(row["time"])

    return stats


def create_graph(stats):
    time = []
    count = []
    for i, x in enumerate(stats):
        time.append(x["time"])
        count.append(x["count"])

    plt.plot(time, count, color="red")
    plt.xlabel(f"seconds")
    plt.ylabel("number of peers")
    plt.show()

import json

def main():
    #print(len(stats_master_slaves_1))
    #print(len(stats_slaves_master_1))
    #print(len(stats_master_slaves_2))
    #print(len(stats_slaves_master_2))

    data = []
    with open('peers_info_ipv4.json', 'r') as f:
        for i, row in enumerate(f):
            print(i + 1)
            d = json.loads(row)
            data.append({
                'count': i+1,
                'time': d['check_time']
            })

    print(data)
    create_graph(data)


if __name__ == "__main__":
    main()
