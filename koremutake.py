#!/usr/bin/env python

import unittest

__author__ = "Filip Salomonsson (filip@infix.se)"
__date__ = "2006-06-11"

vowels = "aeiouy"
consonants = list("bdfghjklmnprstv") + "br dr fr gr pr st tr".split()
syllables = [c + v for c in consonants for v in vowels][:128]

def encode(n):
    """Converts a number to a koremutake string."""
    return syllables[n]

class TestKoremutake(unittest.TestCase):
    def test_encode(self):
        self.assertEqual(encode(0), "ba")
        self.assertEqual(encode(127), "tre")
                         
if __name__ == "__main__":
    unittest.main()
