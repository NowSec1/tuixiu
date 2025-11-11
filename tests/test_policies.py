import unittest
from datetime import date

from policies import (
    RETIREMENT_POLICIES,
    RETIREMENT_SOURCE,
    FLEXIBLE_RETIREMENT_POLICY,
    calculate_retirement,
    get_flexible_policy_status,
)


class TestRetirementPolicy(unittest.TestCase):
    def test_policy_metadata_contains_expected_ages(self):
        self.assertEqual(RETIREMENT_POLICIES["male"]["standard"]["age"], 63)
        self.assertEqual(RETIREMENT_POLICIES["female"]["cadre"]["age"], 55)
        self.assertEqual(RETIREMENT_POLICIES["female"]["worker"]["age"], 50)

    def test_policy_source_metadata(self):
        self.assertEqual(RETIREMENT_SOURCE["document_no"], "国务院公告（2024年7月）")
        self.assertEqual(RETIREMENT_SOURCE["title"], "国务院关于实施渐进式延迟法定退休年龄的决定")
        self.assertEqual(RETIREMENT_SOURCE["last_verified"], date(2024, 7, 1))

    def test_retirement_date_calculation_respects_age(self):
        birth = date(1990, 5, 20)
        expected = date(2053, 5, 20)
        retirement_date, age = calculate_retirement(birth, "male", "standard")
        self.assertEqual(age, 63)
        self.assertEqual(retirement_date, expected)

    def test_flexible_policy_effectiveness_flag(self):
        policy = get_flexible_policy_status(today=date(2024, 12, 31))
        self.assertFalse(policy["is_effective"])
        self.assertEqual(policy["days_until_effective"], 1)

        policy_effective = get_flexible_policy_status(today=date(2025, 1, 1))
        self.assertTrue(policy_effective["is_effective"])
        self.assertEqual(policy_effective["days_until_effective"], 0)

    def test_flexible_policy_metadata(self):
        self.assertEqual(
            FLEXIBLE_RETIREMENT_POLICY["document_no"],
            "人社部发〔2024〕32号",
        )
        self.assertEqual(
            FLEXIBLE_RETIREMENT_POLICY["effective_date"],
            date(2025, 1, 1),
        )


if __name__ == "__main__":
    unittest.main()
