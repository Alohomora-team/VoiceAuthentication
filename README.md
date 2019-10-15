# speaker-verification-toolkit
This module contains some tools to make a simple speaker verification.

You can **download** it with PyPI:
```r
$ pip install speaker-verification-toolkit
```

To import and use in your own projects:
```python
import speaker_verification_toolkit.tools as svt
```

#### Example code
```python
import speaker_verification_toolkit.tools as svt
import librosa

# Example:
# Comparing 2 voices audio .
data1, sr = librosa.load('voice1.wav', sr=16000, mono=True)
data2, sr = librosa.laod('voice2.wav', sr=16000, mono=True)

data1 = svt.rms_silence_filter(data1)
data2 = svt.rms_silence_filter(data2)

data1 = svt.extract_mfcc(data1)
data2 = svt.extract_mfcc(data2)

print(
    'The difference between voice1 and voice2 is',
    svt.compute_distance(data1,data2)
)
```

## Usage

```python
find_nearest_voice_data(voice_data_list, voice_sample)
```
Find the nearest voice data based on this voice sample. Could be used to make the naive Accept/Reject decision.
More explanations about Accept/Reject decision can be found in [[1]](#1) (see [references](#references)).

> ***voice_data_list***: a list containing all voices data from the dataset.
>
> ***voice_sample***: the voice sample reference.

> ***returns***: the index of the element from voice_data_list that represents the nearest voice data.
---

```python
compute_distance(sample1, sample2)
```
Compute the distance between sample1 and sample2 using O(n) DTW algorithm [[2]](#2) (see [references](#references)).

> ***sample1***: the mfcc data extracted from the audio signal 1.
>
> ***sample2***: the mfcc data extracted from the audio signal 2.

> ***returns***: Float number representing the minimum distance between sample1 and sample2.
---

```python
extract_mfcc(signal_data, samplerate=16000, winlen=0.025, winstep=0.01)
```
Compute MFCC features from an audio signal. Explanations about mfcc can be found in [[1]](#1) (see [references](#references))

> ***signal***: the audio signal from which to compute features. Should be an N*1 array.
>
> ***samplerate***: the sample rate of the signal we are working with, in Hz.
>
> ***winlen***: the length of the analysis window in seconds. Default is 0.025s (25 milliseconds).
>
> ***winstep***: the step between successive windows in seconds. Default is 0.01s (10 milliseconds).

> ***returns***: A numpy array of size (NUMFRAMES by numcep) containing features. Each row holds 1 feature vector.
---

```python
extract_mfcc_from_wav_file(path, samplerate=16000, winlen=0.025, winstep=0.01)
```
Compute MFCC features from a wav file. Explanations about mfcc can be found in [[1]](#1) (see [references](#references))

> ***path***: the wav file path to be open.
>
> ***samplerate***: the wanted sample rate, in Hz. Default is 16000. If you want no resampling fill this argument with None.
>
> ***winlen***: the length of the analysis window in seconds. Default is 0.025s (25 milliseconds).
>
> ***winstep***: the step between successive windows in seconds. Default is 0.01s (10 milliseconds).

> ***returns***: A numpy array of size (NUMFRAMES by numcep) containing features. Each row holds 1 feature vector.
---

```python
rms_silence_filter(data, samplerate=16000, segment_length=None, threshold=0.001135)
```
Cut off silence parts from the signal audio data. **Doesn't work with signals data affected by environment noise**.
You should consider apply a noise filter before using this silence filter or make sure that environment noise is small enough to be considered as silence.

>***data***: the audio signal data
>
>***samplerate***: the audio signal sample rate. If no segment_length is given, segment_length will be equals samplerate/100 (around 0.01 secs per segment).
>
>***segment_length***: the number of frames per segment. I.e. for a sample rate SR, a segment length equal SR/100 will represent a chunk containing 0.01 seconds of audio.
>
>***threshold***: the threshold value. Values less than or equal will be cut off. The default value was defined at [[3]](#3) (see [references](#references)).

>***returns***: the param "data" without silence parts.

# References

##### [1]
 > Lindasalwa Muda, Mumtaj Begam and I. Elamvazuthi, "Voice Recognition Algorithms using Mel Frequency Cepstral Coefficient (MFCC) and Dynamic Time Warping (DTW) Techniques", Journal of Computing, Volume 2, Issue 3

##### [2]
 > Stan Salvador and Philip Chan, "FastDTW: Toward Accurate Dynamic Time Warping in Linear Time and Space", Dept. of Computer Sciences, Florida Institute of Technology Melbourne

##### [3]
 > Muhammad Asadullah & Shibli Nisar, "A SILENCE REMOVAL AND ENDPOINT DETECTION APPROACH FOR SPEECH PROCESSING", National University of Computer and Emerging Sciences, Peshawar