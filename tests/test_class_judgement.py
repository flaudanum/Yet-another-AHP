# coding: UTF-8
"""
Tests for class Criterion
"""

import pytest

import numpy as np
import numpy.testing as npt

from yeahp.judgement import Judgement


@pytest.fixture(scope='module', name='judg_obj')
def judg_obj_fixture():
    # Setup of the instance of class Judgement
    descriptions = ['element #2', 'element #3', 'element #4', 'element #1']

    judg_obj = Judgement(labels=descriptions)

    judg_obj.compare('element #1', 'element #2', 1/3)
    judg_obj.compare('element #1', 'element #3', 3)
    judg_obj.compare('element #1', 'element #4', 1/5)
    judg_obj.compare('element #2', 'element #3', 5)
    judg_obj.compare('element #2', 'element #4', 1/3)
    judg_obj.compare('element #3', 'element #4', 9)

    return judg_obj


@pytest.fixture(scope='module', name='ref_comp_matrix')
def ref_matrix_fixture():
    ref_array = [
        [1, 1 / 3, 3, 1 / 5],
        [3, 1, 5, 1 / 3],
        [1 / 3, 1 / 5, 1, 9],
        [5, 3, 1 / 9, 1]
    ]
    return np.array(ref_array, dtype='float64')


def test_create(judg_obj, ref_comp_matrix):
    """
    **Success testing**
       Instantiation of class Judgement
    """

    # Test the description list of the compared elements
    assert judg_obj.labels == ('element #1', 'element #2', 'element #3', 'element #4')

    # Test the reciprocal comparison matrix
    npt.assert_array_almost_equal_nulp(ref_comp_matrix, judg_obj.matrix, nulp=1)

    # Test the computation of priorities
    eig_val, eig_vect = np.linalg.eig(ref_comp_matrix)
    eig_max_ind = eig_val.argmax()
    priorities = eig_vect[:, eig_max_ind]
    ref_priorities = np.real(priorities / priorities.sum())  # Normalization

    npt.assert_array_almost_equal_nulp(ref_priorities, judg_obj.priorities, nulp=1)


def test_consistency_index(judg_obj, ref_comp_matrix):
    """
    **Success testing**
       Method returning the value of the consistency index of the judgment
    """

    eig_val, eig_vect = np.linalg.eig(ref_comp_matrix)
    n = 4
    # consistency index
    ind_max = eig_val.argmax()
    index = (np.real(eig_val[ind_max]) - n) / (n - 1)

    npt.assert_array_almost_equal_nulp(judg_obj.index(), index)


def test_consistency_deviation(ref_comp_matrix, judg_obj):
    r"""
    **Success testing**

    'w' is the vector of priorities and 'A' is the reciprocal comparison matrix
    D = diag(w_i)
    The error matrix 'E' is:
    E = D^{-1} A D
    with \epsilon_{ij} = a_{ij} w_i/w_j
    """
    eig_val, eig_vect = np.linalg.eig(ref_comp_matrix)
    # consistency index
    ind_max = eig_val.argmax()
    # priority vector
    w = eig_vect[:, ind_max]
    w = np.real(w / w.sum())
    D = np.diag(w)
    E = np.dot(np.linalg.solve(D, ref_comp_matrix), D)
    npt.assert_array_almost_equal_nulp(E-1, judg_obj.deviation_matrix())


def test_create_failure():
    """
    **Failure testing**
       A comparison is missing for computing priorities
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


def test_inconsistency1():
    """
    Test method yeahp.judgement.Judgement#status
    :return: recommended revision (elt_a, elt_b)
    :rtype: tuple(str, str)
    """
    descriptions = ['element #2', 'element #3', 'element #4', 'element #1']

    judg_obj = Judgement(labels=descriptions)

    # Perfectly consistent set of comparison (index == 0)
    judg_obj.compare('element #1', 'element #2', 1 / 3)
    judg_obj.compare('element #1', 'element #3', 1 / 6)
    judg_obj.compare('element #1', 'element #4', 1 / 9)
    judg_obj.compare('element #2', 'element #3', 1 / 2)
    judg_obj.compare('element #2', 'element #4', 1 / 3)
    judg_obj.compare('element #3', 'element #4', 2 / 3)

    assert judg_obj.status() == tuple()


def test_inconsistency2():
    """
    Test method yeahp.judgement.Judgement#status
    :return: recommended revision (elt_a, elt_b)
    :rtype: tuple(str, str)
    """
    descriptions = ['element #2', 'element #3', 'element #4', 'element #1']

    judg_obj = Judgement(labels=descriptions)

    # Perfectly consistent set of comparison (index == 0)
    judg_obj.compare('element #1', 'element #2', 1 / 3)
    judg_obj.compare('element #1', 'element #3', 1 / 5)
    judg_obj.compare('element #1', 'element #4', 1 / 9)
    judg_obj.compare('element #2', 'element #3', 1 / 3)
    judg_obj.compare('element #2', 'element #4', 1 / 3)
    judg_obj.compare('element #3', 'element #4', 9)  # Inconsistency

    assert judg_obj.status() == ('element #3', 'element #4')


if __name__ == "__main__":
    pytest.main()
