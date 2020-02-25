"""
Created on 25.02.2020 

@author: goh
"""

from extract_features import extractSTFT, normalizeFeatures

from tensorflow.keras import models
import numpy as np


def predict_file(input_file, model_file, norm_file, extract_params):
    res = extractSTFT(input_file, 0, **extract_params)
    features = res[0]

    norm_file = model_file.replace(".h5", ".npz")

    normalizeFeatures(features, norm_file)

    model = models.load_model(model_file)
    results = model.predict(features)

    result_per_file = np.mean(results, axis=0)

    pred = np.argmax(result_per_file)
    return pred, result_per_file[pred]
