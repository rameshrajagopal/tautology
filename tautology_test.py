#!/usr/bin/env python
import unittest
from tautology import infixToPostfix, evaluateExpr, isTautology, postfixToExpressionTree
from tautology import evaluateExprFromTree
from treeNode import TreeNode

class TestInfixToPostfix(unittest.TestCase):
    def test_simple_expr(self):
        expr = 'a'
        self.assertEqual(infixToPostfix(expr), 'a')

    def test_simple_expr_braces(self):
        expr = 'a&b'
        self.assertEqual(infixToPostfix(expr), 'ab&')

    def test_complex_expr_braces(self):
        expr = 'a & (b | c)'
        self.assertEqual(infixToPostfix(expr), 'abc|&')

    def test_expr_with_not(self):
        expr = '!a & !b'
        self.assertEqual(infixToPostfix(expr), 'a!b!&')

    def test_expr_with_not_same(self):
        expr = 'a & !a'
        self.assertEqual(infixToPostfix(expr), 'aa!&')

    def test_expr_with_not_complex(self):
        expr = '(a & (!b | b)) | (!a & (!b | b))'
        self.assertEqual(infixToPostfix(expr), 'ab!b|&a!b!b|&|')

class TestEvaluateExpr(unittest.TestCase):
    def test_evaluate_expr_simple(self):
        expr = 'a'
        variableMap = {'a' : 0}
        postfix = infixToPostfix(expr)
        self.assertEqual(evaluateExpr(postfix, variableMap), 0)

    def test_evaluate_expr_true(self):
        expr = 'a | !a'
        variableMap = {'a' : 0}
        postfix = infixToPostfix(expr)
        root = postfixToExpressionTree(postfix)
        root.in_traversal()
        print('')
        self.assertEqual(evaluateExpr(postfix, variableMap), 1)

    def test_evaluate_complex_expr(self):
        expr = '(a & (!b | b)) | (!a & (!b | b))'
        variableMap = {'a' : 0, 'b' : 1}
        postfix = infixToPostfix(expr)
        root = postfixToExpressionTree(postfix)
        root.in_traversal()
        print('')
        self.assertEqual(evaluateExpr(postfix, variableMap), 1)

    def test_evaluate_3var_expr(self):
        expr = 'a & b | c'
        variableMap = {'a' : 0, 'b' : 1 , 'c' : 0 }
        postfix = infixToPostfix(expr)
        root = postfixToExpressionTree(postfix)
        root.in_traversal()
        print('')
        self.assertEqual(evaluateExpr(postfix, variableMap), 0)

class TestTautology(unittest.TestCase):
    def test_tautology_expr_simple(self):
        expr = 'a'
        self.assertEqual(isTautology(expr), False)

    def test_tautology_expr_true(self):
        expr = 'a | !a'
        self.assertEqual(isTautology(expr), True)

    def test_tautology_complex_expr(self):
        expr = '(a & (!b | b)) | (!a & (!b | b))'
        self.assertEqual(isTautology(expr), True)

    def test_tautology_3var_expr(self):
        expr = 'a & b | c'
        self.assertEqual(isTautology(expr), False)

    def test_tautology_1var_expr(self):
        expr = '(!a | (a & a))'
        self.assertEqual(isTautology(expr), True)

    def test_tautology_2var_expr(self):
        expr = '(!a | (b & !a))'
        self.assertEqual(isTautology(expr), False)

    def test_tautology_4var_expr(self):
        expr = '(a & b) | (!a & b) | (c & d) | (!c & d)'
        self.assertEqual(isTautology(expr), False)

    def test_tautology_4var_expr_with_negations(self):
        expr = '(a & b) | (!a & b) | (c & d) | (!c & d) | (!b & !d)'
        self.assertEqual(isTautology(expr), True)

    def test_tautology_4var_expr_all_negations_but_one(self):
        expr = '((a & b) | (!a & b) | (c & d)) | ((!c & d) | (!b & d))'
        self.assertEqual(isTautology(expr), False)

    def test_tautology_4var_expr_all_negations_but_one_with_or(self):
        expr = '(a & b) | (!a & b) | (c & d) | (!c & d) | (!b | d)'
        self.assertEqual(isTautology(expr), True)

    def test_tautology_4var_expr_all_negations_but_one_with_or_divided(self):
        expr = '((a & b) | (!a & b) | (c & d)) | ((!c & d) | (!b | d))'
        self.assertEqual(isTautology(expr), True)
    
    def test_tautology_divided_by_true_with_expression(self):
        expr = '((!a | a) | ((a & b) | (c | d) | (d & e) & (f & g)))'
        self.assertEqual(isTautology(expr), True)

    def test_tautology_divided_by_true_with_expression_and(self):
        expr = '((!a | a) & ((a & b) | (c | d) | (d & e) & (f & g)))'
        self.assertEqual(isTautology(expr), False)

    def test_tautology_divided_by_true_with_expression_and(self):
        expr = '((!a & a) | ((a & b) | (c | d) | (d & e) & (f & g)))'
        self.assertEqual(isTautology(expr), False)

class TestEvaluateExprFromTree(unittest.TestCase):
    def test_tree_evalute_expr_simple(self):
        expr = 'a'
        variableMap = {'a' : 0}
        postfix = infixToPostfix(expr)
        root = postfixToExpressionTree(postfix) 
        self.assertEqual(evaluateExprFromTree(root, variableMap), 0)

    def test_tree_evaluate_expr_true(self):
        expr = 'a | !a'
        variableMap = {'a' : 0}
        postfix = infixToPostfix(expr)
        root = postfixToExpressionTree(postfix)
        self.assertEqual(evaluateExprFromTree(root, variableMap), 1)

    def test_tree_evaluate_complex_expr(self):
        expr = '(a & (!b | b)) | (!a & (!b | b))'
        variableMap = {'a' : 0, 'b' : 1}
        postfix = infixToPostfix(expr)
        root = postfixToExpressionTree(postfix)
        self.assertEqual(evaluateExprFromTree(root, variableMap), 1)

    def test_tree_evaluate_3var_expr(self):
        expr = 'a & b | c'
        variableMap = {'a' : 0, 'b' : 1 , 'c' : 0 }
        postfix = infixToPostfix(expr)
        root = postfixToExpressionTree(postfix)
        self.assertEqual(evaluateExprFromTree(root, variableMap), 0)

#main
if __name__ == '__main__':
    unittest.main()
