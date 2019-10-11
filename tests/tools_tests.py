import unittest
import librosa
from python_speech_features import mfcc
from fastdtw import fastdtw
import numpy

from speaker_verification_toolkit.tools import compute_distance
from speaker_verification_toolkit.tools import extract_mfcc
from speaker_verification_toolkit.tools import extract_mfcc_from_wav_file
from speaker_verification_toolkit.tools import find_nearest_voice_data
from speaker_verification_toolkit.tools import rms_silence_filter

class Tests(unittest.TestCase):

    def setUp(self):
        self.arr1 = [x for x in range(100)]
        self.arr2 = [x + 1 for x in range(100)]
        self.file1, self.sr1 = librosa.load('example.wav', 16000)
        self.mfcc1 = mfcc(self.file1, self.sr1, winfunc=numpy.hamming)

    def test_compute_distance(self):
        self.assertEqual(compute_distance(self.arr1, self.arr2), 2.0)

    def test_extract_mfcc(self):
        mfcc_test = extract_mfcc(self.file1, self.sr1)
        self.assertEqual(mfcc_test.all(), self.mfcc1.all())
    
    def test_extract_mfcc_from_wav_file(self):
        self.assertEqual(
            self.mfcc1.all(),
            extract_mfcc_from_wav_file('example.wav', samplerate=16000).all()
        )

    def test_find_nearest_voice_data(self):
        arr1 = [x for x in range(32000)]
        arr2 = [2 * x for x in range(32000)]
        arr3 = [x**2  - 50 * x + 20 for x in range(32000)]
        arr4 = [x * 0.5 for x in range(32000)]

        self.assertEqual(
            find_nearest_voice_data(
                [arr1, arr2, arr3, arr4],
                [2.4 * x for x in range(32000)]
            ),
            1
        )
    
    def test_find_nearest_voice_data_empty_list_exception(self):
        with self.assertRaises(Exception):
            find_nearest_voice_data([], self.mfcc1)

    def test_rms_silence_filter(self):
        data = [0.001135 for x in range(16000)] + [0.001140 for x in range(16000)]
        self.assertListEqual(
            rms_silence_filter(data).tolist(),
            [0.001140 for x in range(16000)]
        )
        self.assertListEqual(
            rms_silence_filter(data, segment_length=160).tolist(),
            [0.001140 for x in range(16000)]
        )

if __name__ == '__main__':
    unittest.main()