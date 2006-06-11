#!/usr/bin/env python

import unittest

__author__ = "Filip Salomonsson (filip@infix.se)"
__date__ = "2006-06-11"

vowels = "aeiouy"
consonants = list("bdfghjklmnprstv") + "br dr fr gr pr st tr".split()
syllables = [c + v for c in consonants for v in vowels][:128]

def encode(num):
    """Converts a number to a koremutake string."""
    if num < 0:
        raise TypeError("Argument must be a positive number")
    if num == 0: return syllables[0]
    parts = []
    while num:
        num, remainder = divmod(num, 128)
        parts.append(syllables[remainder])
    return ''.join(reversed(parts))

class TestKoremutake(unittest.TestCase):
    def test_encode(self):
        self.assertEqual(encode(0), "ba")
        self.assertEqual(encode(127), "tre")
                         
if __name__ == "__main__":
    unittest.main()
