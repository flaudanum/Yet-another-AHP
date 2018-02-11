# coding: UTF-8
"""
Definition of class Criterion
"""

from yeahp.element import Element


class Criterion(Element):
    """
    This class instantiates representations of the criteria used for weighting the influence of
    alternatives against the main purpose (top element of the hierarchical tree).

    :param description: Description of the criterion
    :type description: :obj:`str`
    :param parent: Parent criterion. If ``None`` is provided this is the top element of the tree,
                  that is the **main purpose**.
    :type parent: :py:class:`~yeahp.criterion.Criterion` or ``None``
    """

    @property
    def parent(self):
        """
        :return: Parent criterion
        :rtype: :py:class:`~yeahp.criterion.Criterion` or ``None``
        """
        return self._parent

    @property
    def children(self):
        """
        :return: :obj:`tuple` with references to child criteria
        :rtype: tuple(Criterion)
        """
        return tuple(self._children)

    @property
    def priority(self):
        return self._priority

    @priority.setter
    def priority(self, new_val):
        assert new_val >= 0.
        assert new_val <= 1.
        self._priority = new_val

    def __init__(self, description, parent=None):
        super(Criterion, self).__init__(description)

        # Check that parent is a Criterion element or None (top element of the hierarchical tree)
        assert isinstance(parent, Criterion) or (parent is None)
        self._parent = parent
        self._children = list()
        self._priority = None

        # Add self as new child to parent
        if self._parent is not None:
            self._parent.add_child(self)

    def is_top(self):
        """
        :return: is this criterion a top element in a hierarchical tree?
        :rtype: :obj:`bool`
        """
        return self._parent is None

    def is_covering(self):
        """
        :return: is this criterion a *covering criterion*?
        :rtype: :obj:`bool`
        """
        return self._children == []

    def add_child(self, new_child):
        # Check that new_child is a Criterion instance
        assert isinstance(new_child, Criterion)

        self._children.append(new_child)
