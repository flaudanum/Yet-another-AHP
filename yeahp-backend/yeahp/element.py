# coding: UTF-8
"""
Definition of class Element
"""


class Element:

    @property
    def description(self):
        """
        :return: Description of the element
        :rtype: :obj:`str`
        """
        return self._description

    def __init__(self, description):
        self._description = description
