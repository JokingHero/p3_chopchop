import unittest
import tempfile

from functions.evaluate import gc_content, compare_pam, perm_pam, eval_talens_sequence
from functions.set_default_modes import get_allowed_five_prime

class Test(unittest.TestCase):
    def test_gccontent(self):
        self.assertEqual(0.8260869565217391, gc_content("CCTCCTGCTGCGCGCGCGCTCCC"))
        self.assertEqual(1, gc_content("CCG"))
        self.assertEqual(0.5, gc_content("gCGtiChFYg"))

    def test_comaprePAM(self):
        self.assertTrue(compare_pam("N", "G"))
        self.assertTrue(compare_pam("W", "T"))
        self.assertTrue(compare_pam("W", "A"))
        self.assertTrue(compare_pam("S", "C"))
        self.assertTrue(compare_pam("S", "G"))
        self.assertTrue(compare_pam("M", "A"))
        self.assertTrue(compare_pam("M", "C"))
        self.assertTrue(compare_pam("K", "G"))
        self.assertTrue(compare_pam("K", "T"))
        self.assertTrue(compare_pam("R", "A"))
        self.assertTrue(compare_pam("R", "G"))
        self.assertTrue(compare_pam("Y", "C"))
        self.assertTrue(compare_pam("Y", "T"))
        self.assertTrue(compare_pam("B", "H"))
        self.assertTrue(compare_pam("D", "B"))
        self.assertTrue(compare_pam("H", "S"))
        self.assertTrue(compare_pam("V", "J"))
        self.assertFalse(compare_pam("D", "C"))
        self.assertFalse(compare_pam("H", "G"))
        self.assertFalse(compare_pam("O", "S"))

    def test_permPAM(self):
        self.assertEqual(["AA", "AC", "AT", "AG"], perm_pam("AN"))
        self.assertEqual(["AC", "TC", "AG", "TG"], perm_pam("WS"))
        self.assertNotEqual(["T"], perm_pam("A"))

    def test_getAllowedFivePrime(self):
        self.assertEqual(("AA", "AC", "AG", "AT", "CA", "CC", "CG", "CT", "GA", "GC", "GG", "GT", "TA", "TC", "TG",
                          "TT"), get_allowed_five_prime("NN"))

    def test_evalTalens(self):
        trueTemp = tempfile.TemporaryFile(mode="wt")
        falseTemp = tempfile.TemporaryFile(mode="wt")
        self.assertTrue(eval_talens_sequence("x", 1, "TAT", 4, trueTemp, "A", "T"))
        self.assertFalse(eval_talens_sequence("y", 1, "CGC", 2, falseTemp, "A", "T"))
        trueTemp.close()
        falseTemp.close()

if __name__ == "__main__":
    unittest.main()
