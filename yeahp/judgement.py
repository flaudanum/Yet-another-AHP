# coding: UTF-8
"""
Definition of class Judgement
"""

import numpy as np


class Judgement:

    @property
    def labels(self):
        """
        :return: Sorted list of descriptive labels of compared elements
        :rtype: tuple(str)
        """
        return tuple(self._labels)

    @property
    def matrix(self):
        """
        :return: comparison matrix (reciprocal matrix)
        :rtype: np.ndarray
        """
        return np.array(self._comparisonMatrix)

    @property
    def priorities(self):
        """
        :return: calculated priorities
        :rtype: np.ndarray
        """
        if self._priorities is None:
            self._compute_priorities()
        return self._priorities

    @property
    def priorities_dict(self):
        """
        :return: hash of priority values with priority labels
        :rtype: dict
        """
        if self._priorities is None:
            self._compute_priorities()
        return dict([(descr, prio) for descr, prio in zip(self._labels, self._priorities)])

    def __init__(self, labels):
        # Sorted list of descriptive labels of compared elements
        self._labels = sorted(labels)
        # Position of compared elements in the label list
        self._labels_dict_pos = dict([(lab, n) for n, lab in enumerate(self._labels)])
        # Number of elements compared
        self._size = len(labels)
        # Reciprocal comparison matrix
        self._comparisonMatrix = np.eye(self._size, self._size)
        # Priority values (initially no values)
        self._priorities = None

    def compare(self, elt1, elt2, score):
        """
        Comparison of 2 elements. If the score equals 1, the elements have equal importance. If the score is greater
        with a maximal value of 9 then element 1 is favored with the a strenght measured by *score*. If the score is
        less than 1 (must be positive) then element 2 is favored with a strength equal to 1/*score*.

        This routine updates the comparison matrix.

        :param elt1: description of the element 1
        :type elt1: str
        :param elt2: description of the element 2
        :type elt2: str
        :param score: strength of the comparison
        :type score: float
        """
        assert elt1 in self._labels
        assert elt2 in self._labels
        if score > 9.:
            message = 'score = {} is greater than 9'.format(score)
            raise ValueError(message)
        if score <= 0.:
            message = 'score = {} is less or equal to 0'.format(score)
            raise ValueError(message)
        pos1 = self._labels_dict_pos[elt1]
        pos2 = self._labels_dict_pos[elt2]

        self._comparisonMatrix[pos1, pos2] = score
        self._comparisonMatrix[pos2, pos1] = 1./score

    def _compute_priorities(self):
        """
        Compute priorities of elements with the eigen-value method and update the priority vector.
        """
        if not (self._comparisonMatrix > 0).all():
            message = 'Some comparisons are missing'
            raise ValueError(message)

        eig_val, eig_vect = np.linalg.eig(self._comparisonMatrix)
        eig_max_ind = eig_val.argmax()
        priorities = eig_vect[:, eig_max_ind]
        self._priorities = np.real(priorities / priorities.sum())  # Normalization

    def index(self):
        """
        Consistency index
        :rtype: float
        """
        if not (self._comparisonMatrix > 0).all():
            message = 'Some comparisons are missing'
            raise ValueError(message)

        eig_val, eig_vect = np.linalg.eig(self._comparisonMatrix)
        n = self._comparisonMatrix.shape[0]
        # consistency index
        ind_max = eig_val.argmax()
        return (np.real(eig_val[ind_max]) - n) / (n - 1)

    def deviation_matrix(self):
        """
        'w' is the vector of priorities and 'A' is the reciprocal comparison matrix
        D = diag(w_i)
        The error matrix 'E' is:
        E = D^{-1} A D
        with \epsilon_{ij} = a_{ij} w_i / w_j
        The deviation matrix is E - 1
        """
        if not (self._comparisonMatrix > 0).all():
            message = 'Some comparisons are missing'
            raise ValueError(message)

        mat_A = self._comparisonMatrix
        eig_val, eig_vect = np.linalg.eig(mat_A)
        n = mat_A.shape[0]
        # consistency index
        ind_max = eig_val.argmax()
        # priority vector
        w = eig_vect[:, ind_max]
        w = np.real(w / w.sum())
        D = np.diag(w)
        E = np.dot(np.linalg.solve(D, mat_A), D)
        return E - 1.
