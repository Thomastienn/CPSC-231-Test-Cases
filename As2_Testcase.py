import wexpect
import unittest

class Assignment2Test(unittest.TestCase):
    def setUp(self):
        self.file_path = "../analyse_fert_rate.py"

    def init_child(self):
        return wexpect.spawn(f'python {self.file_path}')

    def get_out_from_in(self, inp: list):
        child = self.init_child()
        for i in inp:
            child.sendline(str(i))
            child.readline()

        try:
            child.expect(wexpect.EOF, timeout=0.1)
            return child.before.strip().replace("\r", "").replace("\n", "")
        except wexpect.TIMEOUT:
            try:
                child.expect("Must enter at least two data points.", timeout=0.1)
                return child.after.strip().replace("\r", "").replace("\n", "")
            except wexpect.TIMEOUT:
                return "pass"

    def test_n_entries(self):
        self.assertEqual(self.get_out_from_in([-1]), "Must enter at least two data points.")
        self.assertEqual(self.get_out_from_in([1]), "Must enter at least two data points.")
        self.assertEqual(self.get_out_from_in([2]), "pass")
        self.assertEqual(self.get_out_from_in([3]), "pass")

    def test_s_year(self):
        self.assertEqual(self.get_out_from_in([2, 2000, 1, 2001, 1, 1900]), "The start year does not exist.")
        self.assertEqual(self.get_out_from_in([2, 2000, 1, 2001, 1, 2000]), "pass")

    def test_e_year(self):
        self.assertEqual(self.get_out_from_in([2, 2000, 1, 2001, 1, 2000, 1900]), "The end year does not exist.")
        self.assertEqual(self.get_out_from_in([2, 2000, 1, 2001, 1, 2000, 2000]), "End year must be after start year.")
        self.assertEqual(self.get_out_from_in([2, 2000, 1, 2001, 1, 2001, 2000]), "End year must be after start year.")

    def test_avg_func(self):
        self.assertEqual(".".join(self.get_out_from_in([2, 2000, 2, 2001, 3, 2000, 2001]).split(".")[0:2]) + ".",
                         "The average fertility rate of these two years is 2.50.")
        self.assertEqual(".".join(self.get_out_from_in([2, 2000, 5, 2001, 5, 2000, 2001]).split(".")[0:2]) + ".",
                         "The average fertility rate of these two years is 5.00.")
        self.assertEqual(".".join(self.get_out_from_in([2, 2000, 30, 2001, 25, 2000, 2001]).split(".")[0:2]) + ".",
                         "The average fertility rate of these two years is 27.50.")
        self.assertEqual(".".join(self.get_out_from_in([2, 2000, 2.24, 2001, 1.53, 2000, 2001]).split(".")[0:2]) + ".",
                         "The average fertility rate of these two years is 1.89.")
        self.assertEqual(".".join(self.get_out_from_in([2, 2000, 3.26, 2001, 2.25, 2000, 2001]).split(".")[0:2]) + ".",
                         "The average fertility rate of these two years is 2.76.")

    def test_trend(self):
        self.assertEqual(self.get_out_from_in([2, 2000, 1, 2001, 1, 2000, 2001]).split(".")[2] + ".",
                         "There is a sideways trend.")
        self.assertEqual(self.get_out_from_in([2, 2000, 1, 2001, 1.5, 2000, 2001]).split(".")[2] + ".",
                         "There is an upward trend.")
        self.assertEqual(self.get_out_from_in([2, 2000, 3, 2001, 2.5, 2000, 2001]).split(".")[2] + ".",
                         "There is a downward trend.")

if __name__ == "__main__":
    unittest.main()
