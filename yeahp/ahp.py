# coding: UTF-8
"""
Definition of class Ahp
"""

from yeahp.criterion import Criterion
from yeahp.alternative import Alternative
from yeahp.judgement import Judgement


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

    @property
    def criteria_hash(self):
        return dict(self._criteriaHash)

    @staticmethod
    def _compare_criteria(parent, comparisons):
        """
        :param parent:
        :type parent: Criterion
        :param comparisons:
        :return:
        """

        descriptions = [child.description for child in parent.children]
        judg = Judgement(labels=descriptions)

        for comp in comparisons:
            judg.compare(comp[0], comp[1], comp[2])

        priorities = dict([(descr, prio) for descr, prio in zip(judg.labels, judg.priorities)])

        for child in parent.children:  # type: Criterion
            child.priority = priorities[child.description]

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
        self._goal = Criterion(description=goal)  # type: Criterion
        self._goal.priority = 1.
        self._criteria = [self._goal, ]

        self._bfs(position=[], parent=self._goal)

        self._criteriaHash = dict([(crit.description, crit) for crit in self._criteria])

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

    def hierarchical_compare(self, comparisons):
        """

        :param comparisons:
        :type comparisons: dict
        :return:
        """

        for descr in comparisons:
            crit = self.criteria_hash[descr]
            # Cannot make comparisons against 'covering criteria'
            if crit.is_covering():
                message = 'Cannot make comparisons against a covering criterion'
                raise NameError(message)

            Ahp._compare_criteria(crit, comparisons[descr])

        # hierarchical weighting
        for crit in self._criteria:
            if crit.parent is None:
                continue
            crit.priority *= crit.parent.priority

