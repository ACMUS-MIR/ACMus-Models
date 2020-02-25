"""
Created on 25.02.2020 

@author: goh
"""

import argparse

from predict_file import inference


parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", required=True,
                    help="input audio file or folder.")
parser.add_argument("-o", "--output", required=True,
                    help="output file with predictions.")
args = parser.parse_args()

input_file = args.input
output_file = args.output

extract_params = {}
extract_params["winsize"] = 512
extract_params["hopsize"] = 512
extract_params["patchsize"] = 34
extract_params["patchhop"] = 17
extract_params["desired_sample_rate"] = 12000
extract_params["logSpec"] = True

class_dict = {0: 'solo', 1: 'duo', 2: 'trio', 3: 'quartett', 4: 'large ensemble'}

model_file = "models/ensemble.h5"
norm_file = "models/ensemble.npz"


if __name__ == '__main__':
    inference(args.input, model_file, norm_file, class_dict, extract_params)
    print("Finished")
