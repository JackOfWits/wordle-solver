import unittest
import wordle

class TestWordle(unittest.TestCase):

    def test_compare(self):
        self.assertEqual(
            wordle.compare('relic', 'lyric'),
            '*_*##',
        )
        self.assertEqual(
            wordle.compare('cocoa', 'coach'),
            '##*_*',
        )

    def test_filter(self):
        self.assertEqual(
            wordle.filter('tares', '_**#_'),
            ['alder', 'abler', 'arced', 'anger', 'armed', 'auger', 'amber', 'ameer', 'adder'],
        )
        self.assertEqual(
            wordle.filter('sleep', '__*__', ['sight', 'eight', 'light', 'night', 'might', 'bight']),
            ['eight'],
        )

    def test_score(self):
        self.assertEqual(wordle.score('tares'), 106.26398114420398)
        words = ['sight', 'eight', 'light', 'night', 'might', 'bight', 'wight', 'fight', 'tight']
        self.assertEqual(
            min(wordle.WORDS, key=lambda word: wordle.score(word, words)),
            'mewls',
        )
