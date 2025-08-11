import essentia.streaming as ess
import essentia
import os
import sys


def predict(input_path): 

    # Configure Key Detection Algorithm
    framecutter = ess.FrameCutter(frameSize=4096, hopSize=2048, silentFrames='noise')
    windowing = ess.Windowing(type='blackmanharris62')
    spectrum = ess.Spectrum()
    spectralpeaks = ess.SpectralPeaks(orderBy='magnitude',
                                    magnitudeThreshold=0.00001,
                                    minFrequency=20,
                                    maxFrequency=3500,
                                    maxPeaks=60)

    # Use default HPCP parameters 
    hpcp = ess.HPCP()
    hpcp_key = ess.HPCP(size=36, # We will need higher resolution for Key estimation.
                        referenceFrequency=440, # Assume tuning frequency is 44100.
                        bandPreset=False,
                        minFrequency=20,
                        maxFrequency=3500,
                        weightType='cosine',
                        nonLinear=False,
                        windowSize=1.)

    key = ess.Key(profileType='diatonic', 
                numHarmonics=2,
                pcpSize=36,
                slope=0.6,
                usePolyphony=True,
                useThreeChords=True)

    # Use pool to store data.
    pool = essentia.Pool()

    # Connect streaming algorithms.
    loader.audio >> framecutter.signal
    framecutter.frame >> windowing.frame >> spectrum.frame
    spectrum.spectrum >> spectralpeaks.spectrum
    spectralpeaks.magnitudes >> hpcp.magnitudes
    spectralpeaks.frequencies >> hpcp.frequencies
    spectralpeaks.magnitudes >> hpcp_key.magnitudes
    spectralpeaks.frequencies >> hpcp_key.frequencies
    hpcp_key.hpcp >> key.pcp
    hpcp.hpcp >> (pool, 'tonal.hpcp')
    key.key >> (pool, 'tonal.key_key')
    key.scale >> (pool, 'tonal.key_scale')
    key.strength >> (pool, 'tonal.key_strength')

    
    # Get file list from input_path
    fileList = []
    for root, dirs, files in os.walk(input_path):
        for file in files:
            fileList.append(os.path.join(root, file))

    print("Found", len(fileList), "files")

    results = {}

    for file in fileList:
        try:
            loader = ess.MonoLoader(filename=file)
            # Run streaming network.
            essentia.run(loader)
            res = pool['tonal.key_key'] + " " + pool['tonal.key_scale']
            results[file] = res
            print("Estimated key for " + file + ":" + pool['tonal.key_key'] + " " + pool['tonal.key_scale'])
        except:
            e = sys.exc_info()[0]
            print("Error on file", file, e)
            continue

    return results

    
    
    

    