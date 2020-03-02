# ACMus-Models
Respository with some of the models trained in ACMus publications.

## References

For ensemle size detection best CNN model was taken from:
[Ensemble size classification in Colombian Andean string music recordings](https://acmus-mir.github.io/publication/cmmr19/)

For speech music classification best CNN model was taken from - refer to baseline on T3:
[Analyzing the potential of pre-trained embeddings for audio classification tasks](https://acmus-mir.github.io/publication/embeddings20/)

## How to use

### Clone this repository

Models and commandline scripts are included for ensemble size classification and speech/music detection
as well as example files. Further data can be found at [Zenodo ACMUS-MIR](https://zenodo.org/record/3268961#.XlPH5iiyhaQ) 

### Install required packages

Install reuqired packages with pip or conda using the provided requirement.txt file for python 3.6.

Option A: Create new environment and install dependencies using conda:
```
# Create new env
$ conda create -n acmus_models python=3.6
# Activate it
$ conda activate acmus_models
# Install from requirements file
(acmus_models)$ pip install --user --requirement requirements.txt
```

Option B: Install using pip only:
```
$ pip install -r requirements.txt
```

Option C: Install main packages manually:
```
$ pip install tensorflow==1.12
$ pip install librosa==0.7.2
```

### Run *_inference_main.py

Either "ensemble_size_inference_main.py" or "speech_music_inference_main.py" for each task. Arguments are "-i" for
input file or folder with files. These folders should contain only audio files! The prediction results are
written to a csv file. The output file name can be set using "-o".

```
$ python ensemble_size_inference_main.py -i example_files/ -o output.csv
```

## License

MIT License

Copyright (c) 2020 ACMus - Advancing Computational Musicology

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.