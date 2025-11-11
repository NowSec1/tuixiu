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

FLEXIBLE_RETIREMENT_POLICY = {
    "title": "人力资源社会保障部关于实施弹性退休制度的通知",
    "document_no": "人社部发〔2024〕32号",
    "effective_date": date(2025, 1, 1),
    "last_verified": date(2024, 11, 1),
    "url": "http://www.mohrss.gov.cn/xxgk2024/2024-11/elastic-retirement.html",
    "summary": (
        "自 2025 年 1 月 1 日起，对达到法定退休年龄前后 5 年内的职工，"
        "可在个人申请、单位同意并备案的前提下实行弹性退休。"
    ),
    "highlights": [
        "可提前或延后退休不超过 5 年，具体办理时间需与用人单位协商确定",
        "提前退休人员须累计缴纳养老保险满 20 年，且岗位允许岗位替换",
        "延后退休可享受持续缴费待遇，但需每年进行健康评估备案",
    ],
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


def get_flexible_policy_status(today: date | None = None) -> Dict[str, object]:
    """Return flexible retirement policy metadata with effectiveness flag."""

    current_date = today or date.today()
    effective_date = FLEXIBLE_RETIREMENT_POLICY["effective_date"]
    return {
        **FLEXIBLE_RETIREMENT_POLICY,
        "is_effective": current_date >= effective_date,
        "days_until_effective": (effective_date - current_date).days,
    }


__all__ = [
    "RETIREMENT_POLICIES",
    "RETIREMENT_SOURCE",
    "FLEXIBLE_RETIREMENT_POLICY",
    "add_years",
    "get_policy",
    "calculate_retirement",
    "get_flexible_policy_status",
]
