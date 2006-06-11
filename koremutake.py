#!/usr/bin/env python

import unittest
import re

__author__ = "Filip Salomonsson (filip@infix.se)"
__date__ = "2006-06-11"

_vowels = "aeiouy"
_consonants = list("bdfghjklmnprstv") + "br dr fr gr pr st tr".split()
_syllables = [c + v for c in _consonants for v in _vowels][:128]

def encode(num, syllables=None):
    """Converts a number to a koremutake string.
    If the syllables argument is given, the resulting string is at
    least that many syllables."""
    if num < 0:
        raise TypeError("Argument must be a positive number")
    parts = []
    if num == 0:
        parts.append(_syllables[0])
    while num:
        num, remainder = divmod(num, 128)
        parts.append(_syllables[remainder])

    if syllables is not None and len(parts) < syllables:
        parts.extend([_syllables[0]] * (syllables - len(parts)))
    return ''.join(reversed(parts))

_koremutake_re = re.compile(r"^(%s)+$" % "|".join(_syllables))
_syllable_re = re.compile(r"(%s)" % "|".join(_syllables))
def decode(s):
    if not _syllable_re.match(s):
        raise ValueError("Argument is not a valid koremutake string.")
    num = 0
    for syllable in _syllable_re.findall(s):
        num <<= 7
        num += _syllables.index(syllable)
    return num

class TestKoremutake(unittest.TestCase):
    def test_encode(self):
        self.assertEqual(encode(0), "ba")
        self.assertEqual(encode(127), "tre")
        self.assertEqual(encode(128), "beba")
        self.assertEqual(encode(256), "biba")
        self.assertEqual(encode(128**2), "bebaba")
        self.assertEqual(encode(128**2 - 1), "tretre")
        self.assertEqual(encode(128**3), "bebababa")
        self.assertEqual(encode(128**3 - 1), "tretretre")

    def test_encode_padded(self):
        self.assertEqual(encode(0, 2), "baba")
        self.assertEqual(encode(0, 5), "bababababa")
        self.assertEqual(encode(127, 3), "babatre")
        self.assertEqual(encode(128**3, 1), "bebababa")


    def test_decode(self):
        self.assertEqual(decode("ba"), 0)
        self.assertEqual(decode("tre"),127 )
        self.assertEqual(decode("beba"), 128)
        self.assertEqual(decode("biba"), 256)
        self.assertEqual(decode("bebaba"), 128**2)
        self.assertEqual(decode("tretre"), 128**2 - 1)
        self.assertEqual(decode("bebababa"), 128**3)
        self.assertEqual(decode("tretretre"), 128**3 - 1)
        self.assertEqual(decode("baba"), 0)
        self.assertEqual(decode("bababababa"), 0)
        self.assertEqual(decode("babatre"), 127)

if __name__ == "__main__":
    unittest.main()
