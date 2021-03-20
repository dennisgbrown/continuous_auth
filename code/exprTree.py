# -*- coding: utf-8 -*-
import sys


class ExprTree():
    """
    Defines an Expression Tree -- this is the encoding of an individual.
    """
    def __init__(self, root):
        self.root = root
        self.fitness = -1  # fitness may be modified by parsimony pressure
        self.score = -1
        self.world_data = []  # the world data that produced the fitness


class Node():
    """
    Defines a node in an ExprTree.

    We're building a (form of) Decision Tree. Will it work? Definitely maybe!

    Each interior node will have
    two values from the controller function set (func1 and func2)
    that are compared.

    Each leaf node will have a single value from the controller terminal set.

    Some abuses:
        - There are either 2 children or 0 children.
        - 0 children indicates this is a terminal node. It's often checked
          by left_child is None?
        - func1 is the node value if this is a terminal node.
    """
    def __init__(self, func1 = None, func2 = None,
                 left_child = None, right_child = None,
                 constant = 0):
        self.func1 = func1
        self.func2 = func2
        self.left_child = left_child
        self.right_child = right_child
        self.constant = constant
        self.parent = None
        self.depth = 0
        self.height = 0
        self.size = 1


    def calc(self, precalcs):
        """
        Return the value represented by this node.
        """
        # If this is a terminal, return its value (stored as "func1")
        if (self.left_child is None):
            return self.func1

        # Set left and right values for comparison
        val1 = 0
        val2 = 0
        if (self.func1 == 'constant'):
            val1 = self.constant
        else:
            val1 = precalcs[self.func1]

        if (self.func2 == 'constant'):
            val2 = self.constant
        else:
            val2 = precalcs[self.func2]

        # Return either left or right child based on comparison
        if (val1 < val2):
            return self.left_child.calc(precalcs)
        else:
            return self.right_child.calc(precalcs)


    def reset_metrics(self, parent = None, depth = 0):
        """
        Recursive method to reset depth, height, and size of all nodes.
        """
        self.parent = parent
        self.depth = depth
        self.height = 0
        self.size = 1

        # If not terminal node, recurse.
        if (not (self.left_child is None)):
            self.left_child.reset_metrics(parent = self, depth = self.depth + 1)
            self.right_child.reset_metrics(parent = self, depth = self.depth + 1)
            self.size += (self.left_child.size + self.right_child.size)
            self.height = 1 + max(self.left_child.height, self.right_child.height)


    def find_nth_node(self, n, counter = 1):
        """
        Use breadth-first-search to identify and return the "nth"
        node of the tree.
        """
        # Sanity check
        if (n > self.size):
            print("find_nth_node error: n > size:", n)
            sys.exit(1)

        # Visit nodes with BFS, incrementing counter until we find a match
        to_visit = [self]
        counter = 0
        while (len(to_visit) > 0):
            curr = to_visit.pop(0)
            counter += 1
            if (counter == n):
                return curr
            # If not terminal node, add children to visit queue.
            if (not (curr.left_child is None)):
                to_visit.append(curr.left_child)
                to_visit.append(curr.right_child)


    def copy(self, node):
        """
        Copy values from given node to this node
        """
        self.func1 = node.func1
        self.func2 = node.func2
        self.left_child = node.left_child
        self.right_child = node.right_child
        self.constant = node.constant
        self.parent = node.parent
        self.depth = node.depth
        self.height = node.height
        self.size = node.size


    def repr_helper(self, level):
        """
        Return a string representing this node.

        level = depth of this node, for printing the pipe indents
        """
        # If terminal node, return string representing it
        if (self.left_child is None):
            return ('|' * level) + self.func1 + '\n'

        # If function node, return a recursively-generated string.
        else:
            return_string = ('|' * level) + 'if ';
            if (self.func1 == 'constant'):
                return_string += str(self.constant)
            else:
                return_string += self.func1
            return_string += ' < '
            if (self.func2 == 'constant'):
                return_string += str(self.constant)
            else:
                return_string += self.func2
            return_string += '\n'

            return return_string \
                + self.left_child.repr_helper(level + 1) \
                + self.right_child.repr_helper(level + 1)


    def __repr__(self):
        """
        Return a string representing this node.
        """
        return self.repr_helper(0)
