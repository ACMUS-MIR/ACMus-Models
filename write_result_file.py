"""
Created on 25.02.2020 

@author: goh
"""

import csv


def write_result_csv(output_file, results):
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(["file", "prediction", "confidence"])
        for row in results:
            writer.writerow([row[0], row[1], str(row[2])])
