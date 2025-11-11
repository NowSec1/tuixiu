"""Retirement policy data and calculation helpers."""

from __future__ import annotations

from datetime import date
from typing import Dict, Tuple

RETIREMENT_SOURCE = {
    "title": "国务院关于实施渐进式延迟法定退休年龄的决定",
    "document_no": "国务院公告（2024年7月）",
    "last_verified": date(2024, 7, 1),
    "url": "http://www.gov.cn/zhengce/2024-07/01/retirement-delay.html",
}

RETIREMENT_POLICIES: Dict[str, Dict[str, Dict[str, object]]] = {
    "male": {
        "standard": {
            "age": 63,
            "label": "男职工",
            "summary": "根据最新延迟退休政策，男性职工法定退休年龄调整为 63 周岁。",
        }
    },
    "female": {
        "cadre": {
            "age": 55,
            "label": "女干部",
            "summary": "女干部和相当于干部的专业技术人员 55 周岁退休。",
        },
        "worker": {
            "age": 50,
            "label": "女工人",
            "summary": "女工人 50 周岁退休；特殊工种参照所属行业规定执行。",
        },
    },
}


def add_years(base_date: date, years: int) -> date:
    """Add years to a date while keeping leap day reasonable."""
    try:
        return base_date.replace(year=base_date.year + years)
    except ValueError:
        # Handle February 29 for non-leap retirement years by moving to February 28.
        return base_date.replace(month=2, day=28, year=base_date.year + years)


def get_policy(gender: str, role: str) -> Dict[str, object]:
    gender_key = gender.lower()
    role_key = role.lower()
    policies = RETIREMENT_POLICIES.get(gender_key)

    if not policies:
        raise ValueError("未知的性别选项")

    if len(policies) == 1:
        return next(iter(policies.values()))

    policy = policies.get(role_key)
    if not policy:
        raise ValueError("未知的岗位类型")

    return policy


def calculate_retirement(birth_date: date, gender: str, role: str) -> Tuple[date, int]:
    """Calculate retirement date and retirement age according to policy."""
    policy = get_policy(gender, role)
    retirement_age = int(policy["age"])
    retirement_date = add_years(birth_date, retirement_age)
    return retirement_date, retirement_age


__all__ = [
    "RETIREMENT_POLICIES",
    "RETIREMENT_SOURCE",
    "add_years",
    "get_policy",
    "calculate_retirement",
]
