import librosa
from fastdtw import fastdtw
from python_speech_features import mfcc
import numpy

def find_nearest_voice_data(voice_data_list, voice_sample):
    '''
    Find the nearest voice data based on this voice sample. Could be used to make the naive Accept/Reject decision.

    :param voice_data_list: a list containing all voices data from the dataset
    :param voice_sample: the voice sample reference
    :returns: the index of the element from voice_data_list that represents the nearest voice data
    '''
    if len(voice_data_list) < 1:
        raise Exception('voice_data_list should be not empty')

    optimal_index = -1
    current_index = 0
    lowest_distance = 10**10

    for cur_data in voice_data_list:
        current_measure = compute_distance(cur_data, voice_sample)
        if lowest_distance > current_measure:
            lowest_distance = current_measure
            optimal_index = current_index

        current_index += 1

    return optimal_index

def compute_distance(sample1, sample2):
    '''
    Compute the distance between sample1 and sample2 using O(n) DTW algorithm

    :param sample1: the mfcc data extracted from the audio signal 1.
    :param sample2: the mfcc data extracted from the audio signal 2.
    :returns: Float number representing the minimum distance between sample1 and sample2.
    '''
    distance, _ = fastdtw(sample1, sample2)
    return distance

def extract_mfcc(signal_data, samplerate=16000, winlen=0.025, winstep=0.01):
    '''
    Compute MFCC features from an audio signal

    :param signal: the audio signal from which to compute features. Should be an N*1 array.
    :param samplerate: the sample rate of the signal we are working with, in Hz.
    :param winlen: the length of the analysis window in seconds. Default is 0.025s (25 milliseconds).
    :param winstep: the step between successive windows in seconds. Default is 0.01s (10 milliseconds).
    :returns: A numpy array of size (NUMFRAMES by numcep) containing features. Each row holds 1 feature vector.
    '''
    return mfcc(signal_data, samplerate, winlen, winstep, winfunc=numpy.hamming)

def extract_mfcc_from_wav_file(path, samplerate=16000, winlen=0.025, winstep=0.01):
    '''
    Compute MFCC features from a wav file

    :param path: the wav file path to be open.
    :param samplerate: the wanted sample rate, in Hz. Default is 16000. If you want no resampling fill this argument with None.
    :param winlen: the length of the analysis window in seconds. Default is 0.025s (25 milliseconds).
    :param winstep: the step between successive windows in seconds. Default is 0.01s (10 milliseconds).
    :returns: A numpy array of size (NUMFRAMES by numcep) containing features. Each row holds 1 feature vector.
    '''
    data, sr = librosa.load(path, sr=samplerate, mono=True)
    return extract_mfcc(data, sr, winlen, winstep)

def rms_silence_filter(data, samplerate=16000, segment_length=None, threshold=0.001135):
    '''
    Cut off silence parts from the signal audio data. Doesn't work with signals data affected by environment noise.
    You would consider apply a noise filter before using this silence filter or make sure that environment noise is small enough to be considered as silence.

    :param data: the audio signal data
    :param samplerate: if no segment_length is given, segment_length will be equals samplerate/100 (around 0.01 secs per segment).
    :param segment_length: the number of frames per segment. I.e. for a sample rate SR, a segment length equals SR/100 will represent a chunk containing 0.01 seconds of audio.
    :param threshold: the threshold value. Values less than or equal values will be cut off. The default value was defined at [1] (see the references).
    :returns: the param "data" without silence parts.
    '''
    if segment_length is None:
        segment_length = int(samplerate/100)

    filtered_data = numpy.array([])

    for index in range(0, len(data), segment_length):
        data_slice = data[index : index + segment_length]

        squared_data_slice = numpy.square(data_slice)
        mean = numpy.sqrt(numpy.mean(squared_data_slice))

        if mean > threshold:
            filtered_data = numpy.append(filtered_data, data_slice)

    return filtered_data
    