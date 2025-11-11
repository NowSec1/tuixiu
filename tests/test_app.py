import os
import sys
import unittest
from datetime import date

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app import app  # noqa: E402


class TestAppFormValidation(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_requires_start_work_month(self):
        response = self.client.post(
            "/",
            data={
                "birthdate": "1990-01-01",
                "gender": "male",
                "role": "standard",
            },
            follow_redirects=True,
        )
        self.assertIn("请填写开始工作时间", response.get_data(as_text=True))

    def test_start_work_cannot_precede_birth(self):
        response = self.client.post(
            "/",
            data={
                "birthdate": "1990-01-01",
                "start_work": "1989-01",
                "gender": "male",
                "role": "standard",
            },
            follow_redirects=True,
        )
        self.assertIn("开始工作时间不能早于出生日期", response.get_data(as_text=True))

    def test_valid_submission_renders_start_work_hint(self):
        today = date.today()
        start_year = today.year - 10
        response = self.client.post(
            "/",
            data={
                "birthdate": f"{start_year - 20}-01-01",
                "start_work": f"{start_year}-01",
                "gender": "male",
                "role": "standard",
            },
            follow_redirects=True,
        )
        content = response.get_data(as_text=True)
        self.assertIn(f"倒计时起算：{start_year}年01月", content)


if __name__ == "__main__":
    unittest.main()
