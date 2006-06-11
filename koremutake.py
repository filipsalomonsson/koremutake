#!/usr/bin/env python

import unittest

__author__ = "Filip Salomonsson (filip@infix.se)"
__date__ = "2006-06-11"

__all__ = ['encode', 'decode']

_vowels = "aeiouy"
_consonants = list("bdfghjklmnprstv") + "br dr fr gr pr st tr".split()
_syllables = [c + v for c in _consonants for v in _vowels][:128]
_revmap = dict([(v, k) for (k, v) in enumerate(_syllables)])

def encode(num, syllables=None):
    """Convert an integer to a koremutake string.
    If the syllables argument is given, the resulting string is at
    least that many syllables."""
    if num < 0:
        raise ValueError("Argument must be a positive number")

    parts = []
    if num == 0:
        parts.insert(0, _syllables[0])
    while num:
        parts.insert(0, _syllables[num & 127])
        num = num >> 7

    # Pad to minimum number of syllables
    if syllables is not None and len(parts) < syllables:
        parts[0:0] = [_syllables[0]] * (syllables - len(parts))
    return ''.join(parts)

def decode(string):
    """Convert a koremutake string to an integer."""
    num = 0
    i = 0
    try:
        for (j, char) in enumerate(string):
            if char in _vowels:
                num <<= 7
                num += _revmap[string[i:j+1]]
                i = j + 1
        if i != j + 1:
            # There was crap at the end of the string
            raise ValueError("Not a valid koreutake string.")
    except KeyError:
        # An invalid vowel was found
        raise ValueError("Not a valid koremutake string.")
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
        self.assertEqual(encode(10610353957), "koremutake")
        self.assertEqual(encode(4398046511103), "tretretretretretre")

        # Negative numbers can't be converted
        self.assertRaises(ValueError, encode, -1)

    def test_encode_padded(self):
        self.assertEqual(encode(0, 2), "baba")
        self.assertEqual(encode(0, 5), "bababababa")
        self.assertEqual(encode(127, 3), "babatre")
        self.assertEqual(encode(128**3, 1), "bebababa")

    def test_decode(self):
        self.assertEqual(decode("ba"), 0)
        self.assertEqual(decode("tre"),127)
        self.assertEqual(decode("beba"), 128)
        self.assertEqual(decode("biba"), 256)
        self.assertEqual(decode("bebaba"), 128**2)
        self.assertEqual(decode("tretre"), 128**2 - 1)
        self.assertEqual(decode("bebababa"), 128**3)
        self.assertEqual(decode("tretretre"), 128**3 - 1)
        self.assertEqual(decode("koremutake"), 10610353957)
        self.assertEqual(decode("tretretretretretre"), 4398046511103)
        self.assertEqual(decode("baba"), 0)
        self.assertEqual(decode("bababababa"), 0)
        self.assertEqual(decode("babatre"), 127)

        # Invalid koremutake strings
        self.assertRaises(ValueError, decode, "foo")
        self.assertRaises(ValueError, decode, "kooremutake")
        self.assertRaises(ValueError, decode, "bab")

if __name__ == "__main__":
    unittest.main()
