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
    def criteria_hash(self):
        return dict(self._criteriaHash)

    @property
    def criteria_descriptions(self):
        """
        :return: Sorted list of criteria descriptions
        :rtype: list(str)
        """
        return sorted([crit.description for crit in self._criteria])

    @property
    def alternatives(self):
        return tuple(self._alternatives)

    @property
    def convering_criteria(self):
        return tuple([crit for crit in self._criteria if crit.is_covering()])

    @property
    def alternatives_hash(self):
        return dict(self._alternativesHash)

    @property
    def goal_properties(self):
        return dict(self._goalPriorities)

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

        priorities = judg.priorities_dict

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
        self._goalPriorities = dict()

        self._descriptionTree = tree
        self._goal = Criterion(description=goal)  # type: Criterion
        self._goal.priority = 1.
        self._criteria = [self._goal, ]

        self._bfs(position=[], parent=self._goal)

        self._criteriaHash = dict([(crit.description, crit) for crit in self._criteria])

        self._alternatives = [Alternative(description=descr, covering=self.convering_criteria)
                              for descr in sorted(alternatives)]
        self._alternativesHash = dict([(alt.description, alt) for alt in self._alternatives])

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

    def alternatives_compare(self, comparisons):
        """

        :param comparisons:
        :type comparisons: dict
        :return:
        """
        descriptions = [alt.description for alt in self._alternatives]

        # Check the validity of criteria description in the argument 'comparisons'
        comparisons_set = set(comparisons.keys())  # set of criteria descriptions in the argument 'comparisons'
        criteria_desc_set = set(self.criteria_descriptions)  # set of all criteria descriptions
        desc_diff = comparisons_set - criteria_desc_set
        if desc_diff:
            unmatched = ['\'{}\''.format(s) for s in list(desc_diff)]
            message = 'The description(s): {}\ndo(es) not match any criterion in the AHP tree'.\
                format(", ".join(unmatched))
            raise NameError(message)

        # Iter over the description of criteria in argument 'comparisons'
        for cov_crit_descr in comparisons:

            # Check that alternatives are compared against covering criteria
            if not self._criteriaHash[cov_crit_descr].is_covering():
                message = "'{}' is not a covering criterion".format(cov_crit_descr)
                raise ValueError(message)

            # Initialize judgment of alternatives against the covering criterion
            judg = Judgement(labels=descriptions)
            for comp in comparisons[cov_crit_descr]:
                judg.compare(comp[0], comp[1], comp[2])

            # Update the priority values of alternatives against each covering criterion
            for descr in judg.priorities_dict:
                priority = judg.priorities_dict[descr]
                self._alternativesHash[descr].update_covering(cov_descr=cov_crit_descr, priority=priority)

        # Weighted sum of priorities of alternatives against each covering criterion
        for alt in self._alternatives:
            alt_descr = alt.description
            self._goalPriorities[alt_descr] = 0
            for crit, prio in alt.covering_priorities.items():
                crit_prio = self._criteriaHash[crit].priority
                self._goalPriorities[alt_descr] += prio * crit_prio
