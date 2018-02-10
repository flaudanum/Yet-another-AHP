# coding: UTF-8
"""
Tests for class Criterion
"""

import pytest

import numpy as np
import numpy.testing as npt

from yeahp.judgement import Judgement


def test_create():
    """
    **Success testing**
    """

    # Setup of the instance of class Judgement
    descriptions = ['element #2', 'element #3', 'element #4', 'element #1']

    judg_obj = Judgement(labels=descriptions)

    judg_obj.compare('element #1', 'element #2', 1/3)
    judg_obj.compare('element #1', 'element #3', 3)
    judg_obj.compare('element #1', 'element #4', 1/5)
    judg_obj.compare('element #2', 'element #3', 5)
    judg_obj.compare('element #2', 'element #4', 1/3)
    judg_obj.compare('element #3', 'element #4', 9)

    # Test the description list of the compared elements
    assert judg_obj.labels == ('element #1', 'element #2', 'element #3', 'element #4')

    # Test the reciprocal comparison matrix
    ref_array = [
        [1, 1 / 3, 3, 1 / 5],
        [3, 1, 5, 1 / 3],
        [1 / 3, 1 / 5, 1, 9],
        [5, 3, 1 / 9, 1]
    ]
    ref_matrix = np.array(ref_array, dtype='float64')

    npt.assert_array_almost_equal_nulp(ref_matrix, judg_obj.matrix, nulp=1)

    # Test the computation of priorities
    eig_val, eig_vect = np.linalg.eig(ref_matrix)
    eig_max_ind = eig_val.argmax()
    priorities = eig_vect[:, eig_max_ind]
    ref_priorities = np.real(priorities / priorities.sum())  # Normalization

    npt.assert_array_almost_equal_nulp(ref_priorities, judg_obj.priorities, nulp=1)


def test_create_failure():
    """
    **Failure testing**
    """

    # Setup of the instance of class Judgement
    descriptions = ['element #2', 'element #3', 'element #4', 'element #1']

    judg_obj = Judgement(labels=descriptions)

    judg_obj.compare('element #1', 'element #2', 1/3)
    judg_obj.compare('element #1', 'element #3', 3)
    judg_obj.compare('element #1', 'element #4', 1/5)
    judg_obj.compare('element #2', 'element #3', 5)
    judg_obj.compare('element #2', 'element #4', 1/3)
    # judg_obj.compare('element #3', 'element #4', 9) This comparison is missing

    with pytest.raises(ValueError) as excinfo:
        # noinspection PyStatementEffect
        judg_obj.priorities

    assert 'Some comparisons are missing' in str(excinfo.value)


if __name__ == "__main__":
    pytest.main()
