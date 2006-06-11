#!/usr/bin/env python

import unittest

__author__ = "Filip Salomonsson (filip@infix.se)"
__date__ = "2006-06-11"

_vowels = "aeiouy"
_consonants = list("bdfghjklmnprstv") + "br dr fr gr pr st tr".split()
_syllables = [c + v for c in consonants for v in vowels][:128]

def encode(num, syllables=None):
    """Converts a number to a koremutake string.
    If the syllables argument is given, the resulting string is at
    least that many syllables."""
    if num < 0:
        raise TypeError("Argument must be a positive number")
    if num == 0: return syllables[0]
    parts = []
    while num:
        num, remainder = divmod(num, 128)
        parts.append(_syllables[remainder])

    if syllables is not None and len(parts) < syllables:
        parts.extend([_syllables[0]] * (syllables - len(parts)))
    return ''.join(reversed(parts))

class TestKoremutake(unittest.TestCase):
    def test_encode(self):
        self.assertEqual(encode(0), "ba")
        self.assertEqual(encode(127), "tre")
                         
if __name__ == "__main__":
    unittest.main()
