"""
Created on 01.07.2019 

@author: goh
"""

import os
import csv

import glob


pattern = "*.txt"
path = "path_to/acmus/rhythm_set/Beat_annotations/"

instrumental_format_dataset = "instrumental_format" in path


def getFilesWithPatternsFromFolder(folders, patterns):
    if not isinstance(patterns, list):
        patterns = [patterns]
    if not isinstance(folders, list):
        folders = [folders]

    files = []
    for folder in folders:
        for pattern in patterns:
            files += glob.glob(os.path.join(folder, pattern))
    files.sort()
    return files


def get_beats_from_file(file):
    beats = []

    with open(file) as f:
        print("reading", file)
        data = f.readlines()
        for line in data:
            try:
                onset = float(line.strip())
                beats.append(onset)
            except:
                continue

    return beats


def get_bpm_from_beats(beats):
    bpm = (len(beats)-1)/(beats[-1]-beats[0])*60
    # round
    return int(bpm+0.5)


# quick test if method is correct
beats_test = []

test_onset = 2
offset = 30
while test_onset < offset:
    beats_test.append(test_onset)
    test_onset += 0.5

bpm_test = get_bpm_from_beats(beats_test)
if bpm_test != 120:
    print("ERROR: bpm is corrupted, result should be 120")
    exit(-1)


files = getFilesWithPatternsFromFolder(path, pattern)

if instrumental_format_dataset is True:
    fieldnames = ['file', 'bpm']
    csv_file = open(os.path.join(path, "bpm.csv"), mode='w', newline='')
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter=';')
    writer.writeheader()

    for file in files:
        basename = os.path.basename(file).replace(".txt", ".wav")

        beats = get_beats_from_file(file)
        if len(beats) == 0:
            print("ERROR: couldn't parse beats in file", file)
            continue

        bpm = get_bpm_from_beats(beats)

        writer.writerow({'file': basename, 'bpm': str(bpm)})

    csv_file.flush()
    csv_file.close()
else:
    fieldnames = ['file', 'bpm0', 'bpm1']
    csv_file = open(os.path.join(path, "bpm.csv"), mode='w', newline='')
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter=';')
    writer.writeheader()

    bpm0 = 0
    bpm1 = 1

    for file in files:
        basename = os.path.basename(file).replace(".txt", ".wav")

        # simple case only one annotation
        if "(0)" in basename:
            beats = get_beats_from_file(file)
            if len(beats) == 0:
                print("couldn't parse beats in file", file)
                continue

            bpm0 = get_bpm_from_beats(beats)
        elif "(1)" in basename:
            if len(beats) == 0:
                print("couldn't parse beats in file", file)
                continue

            bpm1 = get_bpm_from_beats(beats)
            writer.writerow({'file': basename.replace("(1)", ""), 'bpm0': str(bpm0), 'bpm1': str(bpm1)})
        else:
            beats = get_beats_from_file(file)
            if len(beats) == 0:
                print("ERROR: couldn't parse beats in file", file)
                continue

            bpm0 = get_bpm_from_beats(beats)
            writer.writerow({'file': basename, 'bpm0': str(bpm0), 'bpm1': str(0)})

    csv_file.flush()
    csv_file.close()
