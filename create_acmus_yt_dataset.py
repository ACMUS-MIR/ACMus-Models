"""
Script for automated download and convertion of audio from youtube. Input is an XLS file with a 'link' column, that
contains the links. The script was initially created for the creation of the ACMUS youtube dataset. For more
information visit: https://acmus-mir.github.io/

Created on 31.03.2021
@author: kehlcn

required python packages:

pydub
numpy
pandas
pytube3

"""


import os
import argparse
import pandas
import numpy as np
from pydub import AudioSegment
# from tube_dl import Youtube --> not working
from youtube_dl import YoutubeDL


def _get_links_from_xml(fpath):
    if not os.path.exists(fpath):
        print("Could not find file. Please check the filepath.")

    root = pandas.read_excel(fpath)
    name_id = _get_xml_colname("name", root)
    link_id = _get_xml_colname("Original", root)
    nlist = root[name_id].tolist()
    nlist = [x for x in nlist if not pandas.isnull(x)]
    ytlist = root[link_id].tolist()
    ytlist = [x for x in ytlist if not pandas.isnull(x)]
    return ytlist, nlist


def _get_xml_colname(name, pandas_xml_file):
    val_index = None
    for item in list(pandas_xml_file):
        if name in item:
            colname = item
    return colname


def _download(list_of_links, list_of_names, fs, out_path):
    assert len(list_of_links) == len(list_of_names), "Number of links does not match number of file names in the list."

    if not os.path.exists(out_path):
        os.mkdir(out_path)

    for i in range(len(list_of_links)):
        # download from yt
        audio_dl = YoutubeDL({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'wav'
            }],
            'postprocessor_args': [
                '-ar', str(fs)
            ],
            'prefer_ffmpeg': True,
            'audioquality': '0',
            'extractaudio': True,
            'keepvideo': False
        })
        audio_dl.download(list_of_links[i])
        #YoutubeDL(list_of_links[i]).formats.filter(only_audio=True)[0].download(convert='wav')
        #audio_dl.prepare_filename(os.path.join(out_path, list_of_names[i]))
        #wav_file = _extract_audio(in_file, sample_rate, 2)
        #track = AudioSegment(wav_file)
        #output_file_path = os.path.join(out_path, filename)
        #track.export(output_file_path, format="wav")



def _convert_to_desired_audio_in_folder(fs, targetpath):
    z = fs + targetpath
    # Youtube(list_of_links[i]).formats.filter(only_audio=True)[0].download(convert='wav')
    # audio_dl.prepare_filename(os.path.join(out_path, list_of_names[i]))
    # wav_file = _extract_audio(in_file, sample_rate, 2)
    # track = AudioSegment(wav_file)
    # output_file_path = os.path.join(out_path, filename)
    # track.export(output_file_path, format="wav")


def _extract_audio(in_file, fs, num_channels):
    head, tail = os.path.split(in_file)
    suffix = tail[tail.rfind('.'):]
    wavfile = []
    try:
        if not ".npz" in suffix:
            if suffix == '.wav':
                track = AudioSegment.from_wav(in_file)
            elif suffix == '.mp3':
                track = AudioSegment.from_mp3(in_file)
            elif suffix == '.ogg':
                track = AudioSegment.from_ogg(in_file)
            else:
                track = AudioSegment.from_file(in_file, suffix[1:])

            track = track.set_frame_rate(fs)
            track = track.set_channels(num_channels)

            # convert to numpy array
            aud_array = np.array(track.get_array_of_samples())
            aud_array = np.reshape(aud_array, (len(aud_array), 1)).astype(float)
            wavfile = aud_array / np.max(np.abs(aud_array))
    except:
        print("ERROR CONVERTING " + str(in_file))
    return wavfile


if __name__ == '__main__':

    # Parse input args
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="Path to the list file (xml) of youtube links")
    parser.add_argument("-sr", "--samplerate", help="Samplerate for created wav files. ")
    args = parser.parse_args()
    file_path = args.file
    sr = args.samplerate
    foldername = "Youtube Set"

    # start processing
    print("Start Creation of Dataset...")
    linklist, namelist = _get_links_from_xml(file_path)
    head, tail = os.path.split(file_path)
    targetpath = os.path.join(head, foldername)
    _download(linklist, namelist, sr, targetpath)
    _convert_to_desired_audio_in_folder(sr, targetpath)
    print("Sucessfully created " + foldername + " dataset")

