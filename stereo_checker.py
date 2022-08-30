"""
Created on 21.07.2020 

@author: goh
"""

import argparse
import glob
import os
import csv
import essentia
import essentia.standard


parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", required=True,
                    help="input folder")
parser.add_argument("-o", "--output", required=True,
                    help="output file")
parser.add_argument("-p", "--pattern", required=True,
                    help="pattern for files (*.wav)")
args = parser.parse_args()

folder = args.input
output = args.output
pattern = args.pattern


if __name__ == '__main__':
    files = glob.glob(os.path.join(folder, pattern))
    print("Found", len(files), "files")

    outdict = {}

    for file in files:
        loader = essentia.standard.AudioLoader(filename=file)
        data = loader()
        samples = data[0]

        threshold = 0.99

        detector = essentia.standard.FalseStereoDetector(correlationThreshold=threshold)

        isFalseStereo, correlation = detector(samples)

        # manually check these files
        if correlation > 0.80 and correlation < threshold:
            isFalseStereo = 2

        outdict[file] = [isFalseStereo, round(correlation, 3)]

    outdict = dict(sorted(outdict.items()))

    print("writing results to", output)

    for file, stereo in outdict.items():
        print(os.path.basename(file), stereo[0], stereo[1])

    with open(output, 'w', newline='') as file:
        fieldnames = ['file', 'mono', 'correlation']
        writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=';')

        writer.writeheader()
        for file, mono in outdict.items():
            writer.writerow({'file': os.path.basename(file), 'mono': mono[0], 'correlation': mono[1]})

    print("done")

