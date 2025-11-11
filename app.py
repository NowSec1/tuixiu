from __future__ import annotations

from datetime import date, datetime

from flask import Flask, render_template, request

from policies import (
    RETIREMENT_POLICIES,
    RETIREMENT_SOURCE,
    calculate_retirement,
)

app = Flask(__name__)


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
            today = date.today()
            days_until = (retirement_date - today).days
            total_days = (retirement_date - birth_date).days
            days_elapsed = (today - birth_date).days

            if total_days <= 0:
                percent_remaining = 0.0
            else:
                remaining_days = max(days_until, 0)
                percent_remaining = max(
                    0.0,
                    min(100.0, (remaining_days / total_days) * 100),
                )

            result = {
                "retirement_date": retirement_date,
                "retirement_age": retirement_age,
                "days_until": days_until,
                "is_retired": days_until < 0,
                "total_days": total_days,
                "days_elapsed": days_elapsed,
                "percent_remaining": percent_remaining,
                "percent_elapsed": max(0.0, min(100.0, 100.0 - percent_remaining)),
            }
        except ValueError as exc:
            error_message = str(exc)

    policy_options = {
        gender: [
            {
                "value": role_key,
                "label": f"{policy['label']}（{policy['age']} 岁）",
            }
            for role_key, policy in gender_policies.items()
        ]
        for gender, gender_policies in RETIREMENT_POLICIES.items()
    }

    default_roles = {
        gender: next(iter(gender_policies.keys()))
        for gender, gender_policies in RETIREMENT_POLICIES.items()
    }
    selected_gender = request.form.get("gender", "male")
    if selected_gender not in RETIREMENT_POLICIES:
        selected_gender = next(iter(RETIREMENT_POLICIES.keys()))

    selected_role = request.form.get("role") or default_roles.get(selected_gender, "standard")
    valid_roles = {option["value"] for option in policy_options[selected_gender]}
    if selected_role not in valid_roles:
        selected_role = default_roles[selected_gender]

    return render_template(
        "index.html",
        result=result,
        error_message=error_message,
        policies=RETIREMENT_POLICIES,
        policy_options=policy_options,
        policy_source=RETIREMENT_SOURCE,
        selected_gender=selected_gender,
        selected_role=selected_role,
        default_roles=default_roles,
    )


if __name__ == "__main__":
    app.run(debug=True)
