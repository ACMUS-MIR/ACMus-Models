"""
Created on 25.02.2020 

@author: goh
"""

import librosa
import numpy as np


def extractSTFT(file, classID, **extractParams):
    """ Extract stft or mel spec features from audio file.
    Args:
        file (string): input audio file name
        classID (int): Assign y label for training, can be zero for inference
        extractParams (dict): Dict with additional extraction parameters
    Returns:
        [features, classes, file]:  feature matrix (x), class matrix (y), input file name (important for parallel extraction)
    """
    winsize = extractParams["winsize"] if "winsize" in extractParams else 2048
    hopsize = extractParams["hopsize"] if "hopsize" in extractParams else 1024
    logSpec = extractParams["logSpec"] if "logSpec" in extractParams else False
    desired_sample_rate = extractParams["desired_sample_rate"] if "desired_sample_rate" in extractParams else 0
    mel_bands = extractParams["mel_bands"] if "mel_bands" in extractParams else 0
    patchsize = extractParams["patchsize"] if "patchsize" in extractParams else 10
    patchhop = extractParams["patchhop"] if "patchhop" in extractParams else patchsize

    if desired_sample_rate > 0:
        sr = desired_sample_rate
    else:
        sr = None

    x, sr = librosa.load(file, mono=True, sr=sr)

    # normalize audio
    x = x/np.max(np.abs(x))

    X = np.abs(librosa.stft(x, hop_length=hopsize, win_length=winsize, n_fft=winsize).T)

    if mel_bands > 0:
        mel_basis = librosa.filters.mel(
            sr=sr,
            n_fft=winsize,
            n_mels=mel_bands,
            fmin=0,
            fmax=int(sr/2.0),
            htk=False
        ).T
        X = np.dot(X, mel_basis)

    if logSpec is True:
        X = librosa.amplitude_to_db(X, ref=np.max)

    patches = extract_2D_patches_from_features(X, patchsize, patchhop)
    classes = np.ones(patches.shape[0]) * classID

    return [patches.astype(np.float32), classes.astype(np.int16), file]


def extract_2D_patches_from_features(features, blocksize, hopsize):
    """ Extract a 3D tensor of 2D patches from features. Useful for instance
        for training a convolutional neural network (CNN)
    Args:
        features (2d ndarray): features (num_frames x num_features)
        blocksize (int): Block size / window size in frames
                        -> determines the height of the spectrogram patches
                           (the patch width is the number of features)
        hopsize (int): Hopsize in frames
    Returns:
        tensor (4d ndarray): Tensor with feature patches (num_patches x blocksize x num_features x 1 channel)
    """
    num_frames, num_features = features.shape
    if blocksize > num_frames or hopsize > num_frames:
        print("extract_2D_patches_from_features: blocksize bigger than num frames:", num_frames)
        raise RuntimeError("extract_2D_patches_from_features: blocksize bigger than num frames "+str(num_frames))

    num_patches = int(np.fix((num_frames - (blocksize - hopsize)) / hopsize))
    patch_tensor = np.zeros((num_patches, blocksize, num_features, 1))
    for i in range(num_patches):
        patch_tensor[i, :, :, :] = np.expand_dims(features[i*hopsize:i*hopsize+blocksize, :], axis=-1)
    return patch_tensor


def normalizeFeatures(features, normFile):
    full_feature_set = np.load(normFile)
    normMat = full_feature_set['normMat']
    features -= normMat[0]
    features /= normMat[1]