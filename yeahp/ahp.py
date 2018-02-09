# coding: UTF-8
"""
Definition of class Ahp
"""

from yeahp.criterion import Criterion
from yeahp.alternative import Alternative


class Ahp:

    @property
    def goal(self):
        return self._goal

    @property
    def criteria_table(self):
        return tuple(self._criteria)

    @property
    def alternatives(self):
        return tuple(self._alternatives)

    def __init__(self, goal, tree, alternatives):
        """

        :param goal:
        :type goal: str
        :param tree:
        :type tree: dict
        :param alternatives:
        :type alternatives: list(str)
        """

        self._alternatives = [Alternative(description=descr) for descr in sorted(alternatives)]

        self._descriptionTree = tree
        self._goal = Criterion(description=goal)   # type: Criterion
        self._criteria = [self._goal, ]

        self._bfs(position=[], parent=self._goal)

    def _bfs(self, position, parent):
        """
        Breadth First Search:

        :param position: position in the description tree
        :type position: list
        :param parent: parent criterion
        :type parent: Criterion
        """

        subtree = self._descriptionTree
        position_queue = list(position)
        while position_queue:
            subtree = subtree[position_queue.pop(0)]

        if subtree is not None:
            queue = sorted(subtree.keys())
        else:
            queue = list()

        children = [Criterion(description=descr, parent=parent) for descr in queue]
        self._criteria += children

        for child in children:
            new_position = position + [child.description, ]
            self._bfs(position=new_position, parent=child)




