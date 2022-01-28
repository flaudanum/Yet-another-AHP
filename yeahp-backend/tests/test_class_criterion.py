# coding: UTF-8
"""
Tests for class Criterion
"""

import pytest

from yeahp.criterion import Criterion


def test_create():
    """
    **Success testing**
    """

    parent_obj = Criterion(description="Parent criterion", parent=None)
    criterion_obj = Criterion("The criterion", parent=parent_obj)
    children_obj = [Criterion("Children #{}".format(n), parent=criterion_obj) for n in range(3)]

    assert parent_obj.is_top()
    assert parent_obj.children == (criterion_obj,)
    assert criterion_obj.parent == parent_obj
    assert criterion_obj.children == tuple(children_obj)
    for child in criterion_obj.children:
        assert child.is_covering()

# TODO: check that the description are blank-stripped


if __name__ == "__main__":
    pytest.main()
