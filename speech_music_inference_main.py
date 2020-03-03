"""
Created on 25.02.2020 

@author: goh
"""

import argparse

from predict_files import inference
from write_result_file import write_result_csv


parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", required=True,
                    help="input audio file or folder.")
parser.add_argument("-o", "--output", required=True,
                    help="output file with predictions.")
args = parser.parse_args()

input_file = args.input
output_file = args.output

extract_params = {}
extract_params["winsize"] = 1024
extract_params["hopsize"] = 342
extract_params["patchsize"] = 140
extract_params["patchhop"] = 140
extract_params["desired_sample_rate"] = 22050
extract_params["mel_bands"] = 80
extract_params["logSpec"] = True

class_dict = {0: 'Speech', 1: 'Choir', 2: 'Solo Singing', 3: 'Music'}

model_file = "models/speech_music.h5"
norm_file = "models/speech_music.npz"


if __name__ == '__main__':
    results = inference(args.input, model_file, norm_file, class_dict, extract_params)
    write_result_csv(output_file, results)
    print("Finished")
