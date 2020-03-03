"""
Created on 25.02.2020 

@author: goh
"""

from extract_features import extractSTFT, normalizeFeatures

from tensorflow.keras import models
import numpy as np
import os
import sys


def inference(input, model_file, norm_file, class_dict, extract_params):
    """ Get predictions for file or folder.
    Args:
        input (string): file or folder to get predictions for
        model_file (string): model file that should be used
        norm_file (string): file with normalization values for features
        class_dict (dict): dict with index (int) as key and corresponding label (string)
        extract_params (dict): dict with paramaters for extracting features (fft size etc.)
    Returns:
        List with all files and tuple with results per file (file name, class label, confidence)
    """
    results = []

    model = models.load_model(model_file)

    if os.path.isfile(input):
        res = predict_file(input, model, norm_file, class_dict, extract_params)
        results.append(res)
    else:
        results = predict_folder(input, model, norm_file, class_dict, extract_params)

    return results


def predict_file(input_file, model, norm_file, class_dict, extract_params):
    """ Get predictions for file.
    Args:
        input_file (string): file to get predictions for
        model (keras model): model hat should be used
        norm_file (string): file with normalization values for features
        class_dict (dict): dict with index (int) as key and corresponding label (string)
        extract_params (dict): dict with paramaters for extracting features (fft size etc.)
    Returns:
        [file name, class label and confidence]
    """
    res = extractSTFT(input_file, 0, **extract_params)

    features = res[0]

    normalizeFeatures(features, norm_file)

    results = model.predict(features)

    result_per_file = np.mean(results, axis=0)

    pred = np.argmax(result_per_file)
    print(os.path.basename(input_file), "is", class_dict[pred], "with", result_per_file[pred], "confidence")

    return [input_file, class_dict[pred], result_per_file[pred]]


def predict_folder(input_file, model, norm_file, class_dict, extract_params):
    """ Get predictions for file or folder.
    Args:
        input (string): file or folder to get predictions for
        model (string): model that should be used
        norm_file (string): file with normalization values for features
        class_dict (dict): dict with index (int) as key and corresponding label (string)
        extract_params (dict): dict with paramaters for extracting features (fft size etc.)
    Returns:
        List with all files and tuple with results per file (file name, class label, confidence)
    """
    fileList = []
    for root, dirs, files in os.walk(input_file):
        for file in files:
            fileList.append(os.path.join(root, file))

    print("Found", len(fileList), "files")

    results = []

    for file in fileList:
        try:
            res = predict_file(file, model, norm_file, class_dict, extract_params)
        except:
            e = sys.exc_info()[0]
            print("Error on file", file, e)
            continue

        results.append(res)

    return results
