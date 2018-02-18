# coding: UTF-8
"""
Definition of class Alternative
"""

import numpy as np
from yeahp.element import Element


class Alternative(Element):

    @property
    def covering_priorities(self):
        """
        :rtype: dict
        """
        return dict(self._coveringPriorities)

    def __init__(self, description, covering):
        super(Alternative, self).__init__(description)
        self._coveringCriteria = covering
        self._coveringPriorities = dict([(crit.description, 0.) for crit in self._coveringCriteria])

    def update_covering(self, cov_descr, priority):
        """

        :param cov_descr:
        :type cov_descr: str
        :param priority:
        :type priority: float
        :return:
        """
        assert priority >= 0.
        assert priority <= 1.
        self._coveringPriorities[cov_descr] = priority

