# coding: UTF-8
"""
Tests for class Ahp
"""

import pytest
import numpy as np
import numpy.testing as npt

from yeahp.ahp import Ahp
from yeahp.criterion import Criterion

pytestmark = [pytest.mark.yeahp_compute]


@pytest.fixture(scope="module", name="ahp_obj")
def ahp_obj_fixture():
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

    return Ahp(goal=goal, tree=tree, alternatives=alternatives)


def test_create(ahp_obj):
    """
    **Success testing**
    """

    assert ahp_obj.goal.description == "goal"
    assert ahp_obj.goal.priority == 1.

    assert ahp_obj.criteria_table[0].description == "goal"
    assert ahp_obj.criteria_table[1].description == "Criterion #1"
    assert ahp_obj.criteria_table[2].description == "Criterion #2"
    assert ahp_obj.criteria_table[3].description == "Criterion #3"
    assert ahp_obj.criteria_table[4].description == "Sub-criterion #21"
    assert ahp_obj.criteria_table[5].description == "Sub-criterion #22"
    assert ahp_obj.criteria_table[6].description == "Sub-criterion #23"

    assert set(ahp_obj.criteria_hash) == {"goal", "Criterion #1", "Criterion #2", "Criterion #3", "Sub-criterion #21",
                                          "Sub-criterion #22", "Sub-criterion #23"}

    assert [crit.is_covering() for crit in ahp_obj.criteria_table] == [False, True, False, True, True, True, True]

    assert [alt.description for alt in ahp_obj.alternatives] == ["alternative #1", "alternative #2", "alternative #3"]


# TODO: Check that criteria have distinct names


def test_compare_criteria(ahp_obj):
    """
    **Success testing**
       Cross-comparison of a set of child criteria against their parent

    :param ahp_obj:
    :type ahp_obj: Ahp
    """
    parent = ahp_obj.criteria_table[0]

    comp = [
        ["Criterion #1", "Criterion #2", 3],
        ["Criterion #1", "Criterion #3", 7],
        ["Criterion #2", "Criterion #3", 3]
    ]

    ahp_obj._compare_criteria(parent=parent, comparisons=comp)

    # Test the computation of priorities assigned to criteria
    ref_matrix = np.array(
        [
            [1, 3, 7],
            [1 / 3, 1, 3],
            [1 / 7, 1 / 3, 1]
        ]
    )
    eig_val, eig_vect = np.linalg.eig(ref_matrix)
    eig_max_ind = eig_val.argmax()
    priorities = eig_vect[:, eig_max_ind]
    ref_priorities = np.real(priorities / priorities.sum())  # Normalization
    crit1 = ahp_obj.criteria_table[1]  # type: Criterion
    crit2 = ahp_obj.criteria_table[2]  # type: Criterion
    crit3 = ahp_obj.criteria_table[3]  # type: Criterion
    npt.assert_array_almost_equal_nulp(ref_priorities[0], crit1.priority)
    npt.assert_array_almost_equal_nulp(ref_priorities[1], crit2.priority)
    npt.assert_array_almost_equal_nulp(ref_priorities[2], crit3.priority)


def test_hierarchical_comparison(ahp_obj):
    """
    **Success testing**
       Complete hierarchical cross-comparison of criteria against their parent and hierarchical weighting of priorities.

    :param ahp_obj:
    :type ahp_obj: Ahp
    """

    comparisons = {
        "goal": [
            ["Criterion #1", "Criterion #2", 3],
            ["Criterion #1", "Criterion #3", 7],
            ["Criterion #2", "Criterion #3", 3]
        ],
        "Criterion #2": [
            ["Sub-criterion #21", "Sub-criterion #22", 1 / 3],
            ["Sub-criterion #21", "Sub-criterion #23", 1],
            ["Sub-criterion #22", "Sub-criterion #23", 3]
        ]
    }

    ahp_obj.hierarchical_compare(comparisons=comparisons)

    crit1 = ahp_obj.criteria_table[1]  # type: Criterion
    crit2 = ahp_obj.criteria_table[2]  # type: Criterion
    crit3 = ahp_obj.criteria_table[3]  # type: Criterion
    crit21 = ahp_obj.criteria_table[4]  # type: Criterion
    crit22 = ahp_obj.criteria_table[5]  # type: Criterion
    crit23 = ahp_obj.criteria_table[6]  # type: Criterion

    # Comparisons against 'goal'
    ref_matrix = np.array(
        [
            [1, 3, 7],
            [1 / 3, 1, 3],
            [1 / 7, 1 / 3, 1]
        ]
    )
    eig_val, eig_vect = np.linalg.eig(ref_matrix)
    eig_max_ind = eig_val.argmax()
    priorities = eig_vect[:, eig_max_ind]
    ref_priorities = np.real(priorities / priorities.sum())  # Normalization
    npt.assert_array_almost_equal_nulp(ref_priorities[0], crit1.priority)
    npt.assert_array_almost_equal_nulp(ref_priorities[1], crit2.priority)
    npt.assert_array_almost_equal_nulp(ref_priorities[2], crit3.priority)

    # Comparisons against 'Criterion #2'
    ref_matrix = np.array(
        [
            [1, 1 / 3, 1],
            [3, 1, 3],
            [1, 1 / 3, 1]
        ]
    )
    eig_val, eig_vect = np.linalg.eig(ref_matrix)
    eig_max_ind = eig_val.argmax()
    priorities = eig_vect[:, eig_max_ind]
    ref_priorities = np.real(priorities / priorities.sum())  # Normalization
    ref_priorities *= crit2.priority  # Hierarchical weighting
    npt.assert_array_almost_equal_nulp(ref_priorities[0], crit21.priority)
    npt.assert_array_almost_equal_nulp(ref_priorities[1], crit22.priority)
    npt.assert_array_almost_equal_nulp(ref_priorities[2], crit23.priority)

    # Priorities of all covering criteria must sum to one
    priorities = np.array([crit.priority for crit in ahp_obj.criteria_table if crit.is_covering()], dtype="float64")
    npt.assert_array_almost_equal_nulp(1., priorities.sum(), nulp=1)


def test_hierarchical_comparison_failure1(ahp_obj):
    """
    **Failure testing**
       Raise exception when a key-label refer to a covering criterion
    """
    comparisons = {
        "goal": [
            ["Criterion #1", "Criterion #2", 3],
            ["Criterion #1", "Criterion #3", 7],
            ["Criterion #2", "Criterion #3", 3]
        ],
        "Criterion #1": [
            ["Sub-criterion #21", "Sub-criterion #22", 1 / 3],
            ["Sub-criterion #21", "Sub-criterion #23", 1],
            ["Sub-criterion #22", "Sub-criterion #23", 3]
        ]
    }

    with pytest.raises(NameError) as excinfo:
        ahp_obj.hierarchical_compare(comparisons=comparisons)
    assert 'Cannot make comparisons against a covering criterion' in str(excinfo.value)


def test_hierarchical_comparison_failure2(ahp_obj):
    """
    **Failure testing**
       Raise exception when a key-label refer to a covering criterion
    """
    comparisons = {
        "goal": [
            ["Criterion #1", "Criterion #2", 3],
            ["Criterion #1", "Criterion #3", 7],
            ["Criterion #2", "Criterion #3", 3]
        ],
        "Criterion #2": [
            ["Sub-criterion #21", "Sub-criterion #22", 1 / 3],
            ["Sub-criterion #21", "Sub-criterion #23", 1],
            ["Sub-criterion #22", "wrong label", 3]
        ]
    }

    with pytest.raises(AssertionError):
        ahp_obj.hierarchical_compare(comparisons=comparisons)


def test_alternatives_comparison(ahp_obj):
    """
    **Success testing**
       Comparison of alternatives against covering criteria

    :param ahp_obj:
    :type ahp_obj: Ahp
    """

    crit_priorities = {
        'Criterion #1': 0.66941686944898771,
        'Criterion #3': 0.087946208819056057,
        'Sub-criterion #22': 0.14558215303917371,
        'Sub-criterion #21': 0.048527384346391249,
        'Sub-criterion #23': 0.048527384346391249
    }

    for descr in crit_priorities:
        ahp_obj.criteria_hash[descr].priority = crit_priorities[descr]

    comparisons = {
        'Criterion #1': [
            ['alternative #1', 'alternative #2', 3],
            ['alternative #1', 'alternative #3', 1 / 2],
            ['alternative #2', 'alternative #3', 1 / 9],
        ],
        'Sub-criterion #21': [
            ['alternative #1', 'alternative #2', 3],
            ['alternative #1', 'alternative #3', 1],
            ['alternative #2', 'alternative #3', 1 / 3],
        ],
        'Sub-criterion #22': [
            ['alternative #1', 'alternative #2', 1 / 2],
            ['alternative #1', 'alternative #3', 1 / 2],
            ['alternative #2', 'alternative #3', 1],
        ],
        'Sub-criterion #23': [
            ['alternative #1', 'alternative #2', 1 / 9],
            ['alternative #1', 'alternative #3', 1 / 9],
            ['alternative #2', 'alternative #3', 1],
        ],
        'Criterion #3': [
            ['alternative #1', 'alternative #2', 1],
            ['alternative #1', 'alternative #3', 3],
            ['alternative #2', 'alternative #3', 3],
        ],
    }

    ahp_obj.alternatives_compare(comparisons=comparisons)

    np.testing.assert_array_almost_equal_nulp(np.array(list(ahp_obj.goal_properties.values())).sum(), 1.)


def test_alternatives_comparison_failure(ahp_obj):
    """
    **Failure testing**
       Fails if the argument *comparison* does not refer to a proper criterion description

    :param ahp_obj:
    :type ahp_obj: Ahp
    """

    comparisons = {
        'Criterion @$': None,
        'Sub-criterion #21': None,
        'Sub-criterion #22': None,
        'WRONG CRITERION DESCRIPTION': None,
        'Criterion #3': None
    }

    with pytest.raises(NameError) as excinfo:
        ahp_obj.alternatives_compare(comparisons=comparisons)
    assert 'The description(s): \'Criterion @$\', \'WRONG CRITERION DESCRIPTION\'\ndo(es)' + \
           ' not match any criterion in the AHP tree' in str(excinfo.value)


if __name__ == "__main__":
    pytest.main()
