import unittest
from traitement import frameData
from traitement import DataManager

class TestDatamanager(unittest.TestCase):


    def test_strToData(self):
        self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")

    def test_rectOverlap(self):
        dm = DataManager("../obj.names")
        r1 = [10, 10, 10, 10]
        r2 = [15, 15, 10, 10]
        r3 = [5, 5, 5, 5]

        # Rect overlaping
        self.assertTrue(dm.isRectOverlap(r1,r2), "Should be True")

        # Rect not overlaping
        self.assertFalse(dm.isRectOverlap(r2, r3), "Should be False")

        # One side touching (one side in common)
        self.assertFalse(dm.isRectOverlap(r1, r3), "Should be False")

    def test_findObjOverlap(self):
        self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")


if __name__ == '__main__':
    unittest.main()