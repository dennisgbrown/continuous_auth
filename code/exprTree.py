# -*- coding: utf-8 -*-
import sys
import random


class ExprTree():
    """
    Defines an Expression Tree -- this is the encoding of an individual.
    """
    def __init__(self, root):
        self.root = root
        self.fitness = -1  # fitness may be modified by parsimony pressure
        self.score = -1
        self.world_data = []  # the world data that produced the fitness


    def build_tree(self, pop, node, depth, dmax, grow_or_full):
        """
        Recursively build an expression tree to the given depth using either
        the 'grow' or 'full' method.
        """
        expr_parms = None
        # Randomly choose a new expression. If not at depth limit,
        # choose an inner node from a set that depends on method 'grow' or 'full'
        if (depth < dmax):
            # Grow selects from all functions and terminals at this depth
            if (grow_or_full == 'grow'):
                # Choose the left value
                expr_parms = random.choice(pop.functions + pop.terminals)
            # Full selects only from non-terminals at this depth
            else:
                expr_parms = random.choice(pop.functions)
        # If depth is at Dmax, randomly choose a terminal.
        else:
            expr_parms = random.choice(pop.terminals)

        # Make a new tree node with this info
        node.expr = DTExpr(expr_parms)
        node.depth = depth

        # If this node is not a terminal, make its children and update
        # height and count of this node.
        if (not (node.expr.datatype == 'terminal')):
            node.left_child = Node()
            self.build_tree(pop, node.left_child, depth + 1, dmax, grow_or_full)
            node.right_child = Node()
            self.build_tree(pop, node.right_child, depth + 1, dmax, grow_or_full)

        return node


class Node():
    """
    Defines a node in an ExprTree.

    We're building a (form of) Decision Tree. Will it work? Definitely maybe!

    Each node contains an expression. Interior nodes produce a boolean value
    while leaf nodes produce terminal values.

    Some abuses:
        - There are either 2 children or 0 children.
        - 0 children indicates this is a terminal node. It's often checked
          by left_child is None?
    """
    def __init__(self, expr = None,
                 left_child = None, right_child = None):
        self.expr = expr
        self.left_child = left_child
        self.right_child = right_child
        self.parent = None
        self.depth = 0
        self.height = 0
        self.size = 1


    def calc(self, precalcs):
        """
        Recursive method to determine the value represented by this node.
        """
        curr_val = self.expr.calc_expr(precalcs)

        # If this is a terminal, return its value
        if (self.left_child is None):
            return curr_val

        # Return either left or right child based on boolean result of calc
        if (curr_val == True):
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
        self.expr = node.expr
        self.left_child = node.left_child
        self.right_child = node.right_child
        self.parent = node.parent
        self.depth = node.depth
        self.height = node.height
        self.size = node.size


    def repr_helper(self, level):
        """
        Return a string representing this node.

        level = depth of this node, for printing the pipe indents
        """
        return_string = ('|' * level) + self.expr.__repr__() + '\n'

        # If terminal node, return string representing it
        if (self.left_child is None):
            return return_string

        # If function node, return a recursively-generated string.
        else:
            return return_string \
                + self.left_child.repr_helper(level + 1) \
                + self.right_child.repr_helper(level + 1)


    def __repr__(self):
        """
        Return a string representing this node.
        """
        return self.repr_helper(0)


class DTExpr():
    """
    Decision Tree expressions that live in Nodes of the expression tree
    """
    def __init__(self, expr_parms):
        self.name = expr_parms[0]
        self.datatype = expr_parms[1]
        self.invert = False
        self.opts_list = expr_parms[2] if (len(expr_parms) > 2) else None
        self.comp_name = None
        self.constant = 0

        # If this is a real comparison, choose against what we compare it.
        if (self.datatype == 'real'):
            self.comp_name = random.choice(self.opts_list[0])
            if (self.comp_name == 'constant'):
                self.constant = random.uniform(self.opts_list[1][0],
                                               self.opts_list[1][1])

        # Randomly choose if this comparison is inverted
        # ("greater than" instead of "less than")
        self.invert = (random.random() < 0.5)

        # Generate random parameters for attack
        if (self.name == 'attack'):
            self.opts_list = []
            for _ in range(6): self.opts_list.append(random.random())


    def calc_expr(self, precalcs):
        """
        Return the current value of this expression (name if terminal,
        boolean if internal node)
        """
        if (self.datatype == 'terminal'):
            return self.name

        retval = True
        val1 = precalcs[self.name]

        # Check for boolean (one argument) case
        if (self.datatype == 'boolean'):
            retval = bool(val1)

        # Check for comparison of real values
        if (self.datatype == 'real'):
            val2 = self.constant if (self.comp_name == 'constant') \
                else precalcs[self.comp_name]
            retval = (val1 < val2)

        return retval if (not(self.invert)) else (not(retval))


    def __repr__(self):
        if (self.datatype == 'terminal'):
            if (self.name == 'attack'):
                return self.name + ' ' + str(self.opts_list)
            else:
                return self.name
        if (self.datatype == 'boolean'):
            return 'if ' + ('not ' if (self.invert) else '') + self.name
        if (self.datatype == 'real'):
            return_string = 'if ' + self.name
            return_string += ' < ' if (not(self.invert)) else ' > '
            return_string += str(self.constant) if (self.comp_name == 'constant') else self.comp_name
            return return_string
        return 'unknown datatype: ' + self.datatype
