# coding: UTF-8
"""
Definition of class Judgement
"""

import numpy as np


class Judgement:

    @property
    def labels(self):
        return tuple(self._labels)

    @property
    def matrix(self):
        return np.array(self._comparisonMatrix)

    @property
    def priorities(self):
        if self._priorities is None:
            self._compute_priorities()
        return self._priorities

    @property
    def priorities_dict(self):
        if self._priorities is None:
            self._compute_priorities()
        return dict([(descr, prio) for descr, prio in zip(self._labels, self._priorities)])

    def __init__(self, labels):
        self._labels = sorted(labels)
        self._labels_dict_pos = dict([(lab,n) for n,lab in enumerate(self._labels)])
        self._size = len(labels)
        self._comparisonMatrix = np.eye(self._size, self._size)
        self._priorities = None

    def compare(self, elt1, elt2, score):
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
        if not (self._comparisonMatrix > 0).all():
            message = 'Some comparisons are missing'
            raise ValueError(message)

        eig_val, eig_vect = np.linalg.eig(self._comparisonMatrix)
        eig_max_ind = eig_val.argmax()
        priorities = eig_vect[:, eig_max_ind]
        self._priorities = np.real(priorities / priorities.sum())  # Normalization
