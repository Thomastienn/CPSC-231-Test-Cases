import wexpect
import unittest
import re

from pexpect import TIMEOUT


class Assignment1Test(unittest.TestCase):
    def setUp(self):
        self.file_path = "../eligibilty_checker.py"
        self.valid_ans = ["Yes", "yes", "No", "no"]

    def init_child(self):
        return wexpect.spawn(f'python {self.file_path}')

    def get_out_from_in(self, inp: list):
        child = self.init_child()
        for i in inp:
            child.sendline(str(i))
            child.readline()

        try:
            child.expect(wexpect.EOF, timeout=0.1)
            return child.before.strip()
        except wexpect.TIMEOUT:
            return "pass"

    def test_citizen(self):
        self.assertEqual(self.get_out_from_in(["Nah"]), "Invalid response.")
        self.assertEqual(self.get_out_from_in(["Ye"]), "Invalid response.")
        for ans in self.valid_ans:
            self.assertEqual(self.get_out_from_in([ans]), "pass")

    def test_albertan(self):
        self.assertEqual(self.get_out_from_in(["Yes", "Nah"]), "Invalid response.")
        self.assertEqual(self.get_out_from_in(["Yes","Ye"]), "Invalid response.")
        for ans in self.valid_ans:
            self.assertEqual(self.get_out_from_in(["Yes", ans]), "pass")

    def test_month(self):
        pass_ans = ["Yes", "Yes"]
        self.assertEqual(self.get_out_from_in(pass_ans + ["january"]), "Invalid response.")
        self.assertEqual(self.get_out_from_in(pass_ans + ["Augst"]), "Invalid response.")
        self.assertEqual(self.get_out_from_in(pass_ans + ["May"]), "pass")
        self.assertEqual(self.get_out_from_in(pass_ans + ["December"]), "pass")

    def test_year(self):
        pass_ans = ["Yes", "Yes", "January", 10]
        self.assertEqual(self.get_out_from_in(pass_ans + [1890]), "Invalid response.")
        self.assertEqual(self.get_out_from_in(pass_ans + [2026]), "Invalid response.")
        self.assertEqual(self.get_out_from_in(pass_ans + [1900]), "You are eligible to vote.")
        self.assertEqual(self.get_out_from_in(pass_ans + [2024]), "You are not eligible to vote.")
        self.assertEqual(self.get_out_from_in(pass_ans + [2000]), "You are eligible to vote.")

    # month, day, year
    def test_valid_bday(self):
        pass_ans = ["Yes", "Yes"]
        self.assertEqual(self.get_out_from_in(pass_ans + ["January", 32,2000]), "Invalid birth date.")
        self.assertEqual(self.get_out_from_in(pass_ans + ["February", 29, 2011]), "Invalid birth date.")
        self.assertEqual(self.get_out_from_in(pass_ans + ["October", 15, 2024]), "Invalid birth date.")
        self.assertEqual(self.get_out_from_in(pass_ans + ["September", 28, 2024]), "Invalid birth date.")
        self.assertEqual(self.get_out_from_in(pass_ans + ["August", 15, 2024]), "You are not eligible to vote.")
        self.assertEqual(self.get_out_from_in(pass_ans + ["September", 10, 2024]), "You are not eligible to vote.")
        self.assertEqual(self.get_out_from_in(pass_ans + ["August", 31, 2000]), "You are eligible to vote.")

        # Test leap year
        self.assertEqual(self.get_out_from_in(pass_ans + ["February", 29, 2000]), "You are eligible to vote.")
        self.assertEqual(self.get_out_from_in(pass_ans + ["February", 29, 1900]), "Invalid birth date.")
        self.assertEqual(self.get_out_from_in(pass_ans + ["February", 29, 2004]), "You are eligible to vote.")

    def test_eligibility(self):
        self.assertEqual(self.get_out_from_in(["Yes", "Yes", "January", 20, 2000]), "You are eligible to vote.")
        self.assertEqual(self.get_out_from_in(["Yes", "Yes", "January", 20, 2006]), "You are eligible to vote.")
        self.assertEqual(self.get_out_from_in(["Yes", "Yes", "September", 25, 2006]), "You are eligible to vote.")
        self.assertEqual(self.get_out_from_in(["Yes", "Yes", "September", 28, 2006]), "You are not eligible to vote.")
        self.assertEqual(self.get_out_from_in(["Yes", "Yes", "October", 2, 2006]), "You are not eligible to vote.")
        self.assertEqual(self.get_out_from_in(["Yes", "Yes", "January", 20, 2007]), "You are not eligible to vote.")


if __name__ == "__main__":
    unittest.main()
    pass