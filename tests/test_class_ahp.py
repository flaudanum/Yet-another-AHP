# coding: UTF-8
"""
Tests for class Ahp
"""

import pytest

from yeahp.ahp import Ahp


def test_create():
    """
    **Success testing**
    """

    goal = "goal"

    tree = {
        "Criterion #1": None,
        "Criterion #2": {
            "Sub-criterion #21": None,
            "Sub-criterion #22": None,
            "Sub-criterion #23": None
        },
        "Criterion #3": None
    }

    alternatives = ["alternative #2", "alternative #3", "alternative #1"]

    ahp_obj = Ahp(goal=goal, tree=tree, alternatives=alternatives)

    assert ahp_obj.goal.description == "goal"

    assert ahp_obj.criteria_table[0].description == "goal"
    assert ahp_obj.criteria_table[1].description == "Criterion #1"
    assert ahp_obj.criteria_table[2].description == "Criterion #2"
    assert ahp_obj.criteria_table[3].description == "Criterion #3"
    assert ahp_obj.criteria_table[4].description == "Sub-criterion #21"
    assert ahp_obj.criteria_table[5].description == "Sub-criterion #22"
    assert ahp_obj.criteria_table[6].description == "Sub-criterion #23"

    assert [crit.is_covering() for crit in ahp_obj.criteria_table] == [False, True, False, True, True, True, True]

    assert [alt.description for alt in ahp_obj.alternatives] == ["alternative #1", "alternative #2", "alternative #3"]


if __name__ == "__main__":
    pytest.main()
