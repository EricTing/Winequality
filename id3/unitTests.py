"""
Coding for data mining class at LSU, Oct. 2014

@author: Chenguang Zhang
"""

import unittest

from heuristics import entropy

class TddPython(unittest.TestCase):
    def test_func_entropy(self):
        self.assertEqual(entropy([1,1,1,1]),0)
        self.assertEqual(entropy([1,1,0,0]),1)

    def test_func_majorityValue(self):
        self.assertEqual(majorityValue([1,1,1,2,2,3]),1)
        self.assertEqual(majorityValue(['cat','cat','dog']),'cat')
