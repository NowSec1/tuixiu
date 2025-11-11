from __future__ import annotations

from datetime import date, datetime
from typing import Dict, Tuple

from flask import Flask, render_template, request

app = Flask(__name__)


RETIREMENT_POLICIES: Dict[str, Dict[str, int]] = {
    "male": {"standard": 60},
    "female": {"cadre": 55, "worker": 50},
}


def add_years(base_date: date, years: int) -> date:
    """Add years to a date while keeping leap day reasonable."""
    try:
        return base_date.replace(year=base_date.year + years)
    except ValueError:
        # Handle February 29 for non-leap retirement years by moving to February 28.
        return base_date.replace(month=2, day=28, year=base_date.year + years)


def calculate_retirement(birth_date: date, gender: str, role: str) -> Tuple[date, int]:
    """Calculate retirement date and retirement age according to policy."""
    gender_key = gender.lower()
    role_key = role.lower()
    policies = RETIREMENT_POLICIES.get(gender_key)

    if not policies:
        raise ValueError("未知的性别选项")

    if len(policies) == 1:
        retirement_age = next(iter(policies.values()))
    else:
        retirement_age = policies.get(role_key)
        if retirement_age is None:
            raise ValueError("未知的岗位类型")

    retirement_date = add_years(birth_date, retirement_age)
    return retirement_date, retirement_age


@app.route("/", methods=["GET", "POST"])
def index():
    error_message = None
    result = None

    if request.method == "POST":
        birth_input = request.form.get("birthdate", "").strip()
        gender = request.form.get("gender", "male")
        role = request.form.get("role", "standard")

        try:
            birth_date = datetime.strptime(birth_input, "%Y-%m-%d").date()
            if birth_date > date.today():
                raise ValueError("出生日期不能晚于今天")
            retirement_date, retirement_age = calculate_retirement(birth_date, gender, role)
            days_until = (retirement_date - date.today()).days
            result = {
                "retirement_date": retirement_date,
                "retirement_age": retirement_age,
                "days_until": days_until,
                "is_retired": days_until < 0,
            }
        except ValueError as exc:
            error_message = str(exc)

    return render_template(
        "index.html",
        result=result,
        error_message=error_message,
        policies=RETIREMENT_POLICIES,
    )


if __name__ == "__main__":
    app.run(debug=True)
