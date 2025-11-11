import unittest
from datetime import date

from policies import RETIREMENT_POLICIES, RETIREMENT_SOURCE, calculate_retirement


class TestRetirementPolicy(unittest.TestCase):
    def test_policy_metadata_contains_expected_ages(self):
        self.assertEqual(RETIREMENT_POLICIES["male"]["standard"]["age"], 60)
        self.assertEqual(RETIREMENT_POLICIES["female"]["cadre"]["age"], 55)
        self.assertEqual(RETIREMENT_POLICIES["female"]["worker"]["age"], 50)

    def test_policy_source_metadata(self):
        self.assertEqual(RETIREMENT_SOURCE["document_no"], "国发〔1978〕104号")
        self.assertEqual(RETIREMENT_SOURCE["title"], "国务院关于工人退休、退职的暂行办法")
        self.assertEqual(RETIREMENT_SOURCE["last_verified"], date(2024, 4, 1))

    def test_retirement_date_calculation_respects_age(self):
        birth = date(1990, 5, 20)
        expected = date(2050, 5, 20)
        retirement_date, age = calculate_retirement(birth, "male", "standard")
        self.assertEqual(age, 60)
        self.assertEqual(retirement_date, expected)


if __name__ == "__main__":
    unittest.main()
