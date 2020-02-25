"""
Created on 25.02.2020 

@author: goh
"""

from extract_features import extractSTFT, normalizeFeatures

from tensorflow.keras import models
import numpy as np
import os


def inference(input, model_file, norm_file, class_dict, extract_params):
    if os.path.isfile(input):
        predict_file(input, model_file, norm_file, class_dict, extract_params)
    else:
        predict_folder(input, model_file, norm_file, class_dict, extract_params)


def predict_file(input_file, model_file, norm_file, class_dict, extract_params):
    res = extractSTFT(input_file, 0, **extract_params)
    features = res[0]

    normalizeFeatures(features, norm_file)

    model = models.load_model(model_file)
    results = model.predict(features)

    result_per_file = np.mean(results, axis=0)

    pred = np.argmax(result_per_file)
    print(os.path.basename(input_file), "is", class_dict[pred], "with", result_per_file[pred], "confidence")

    return pred, result_per_file[pred]


def predict_folder(input_file, model_file, norm_file, class_dict, extract_params):
    fileList = []
    for root, dirs, files in os.walk(input_file):
        for file in files:
            fileList.append(os.path.join(root, file))

    print("Found", len(fileList), "files")

    for file in fileList:
        pred, conf = predict_file(file, model_file, norm_file, class_dict, extract_params)
