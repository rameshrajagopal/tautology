#!/usr/bin/env python

from treeNode import TreeNode
OPERATORS = ('&', '|', '!', '(', ')')

def isCloseBracket(s):
    return s == ')'

def isOperand(s):
    return (s >= 'A' and s <= 'Z') or (s >= 'a' and s <= 'z')

def notOp(a):
    return "!{}".format(a)

def orOp(a, b):
    if a == b:
        return a
    if isinstance(a, type('str')) and isinstance(b, type('str')):
        if len(a) > len(b) and len(b) == 1 and a == '!{}'.format(b):
             return True
        if len(a) < len(b) and len(a) == 1 and b == '!{}'.format(a):
             return True
        return '{}|{}'.format(a, b)
    if a is True  or b is True:
        return True
    if not a:
        return b
    if not b:
        return a

def andOp(a, b):
    if a == b:
        return a
    if isinstance(a, type('str')) and isinstance(b, type('str')):
        if len(a) > len(b) and len(b) == 1 and a == '!{}'.format(b):
             return False
        if len(a) < len(b) and len(a) == 1 and b == '!{}'.format(a):
             return False
        return '{}&{}'.format(a, b)
    if a is False or b is False:
        return False
    if a:
        return b
    if b:
        return a

def postfixToExpressionTree(postfix):
    exprTreeStack = []
    for e in postfix: 
        node = TreeNode(e)
        if e in OPERATORS:
            if e == '!':
                node.left = exprTreeStack.pop()
            else:
                node.right = exprTreeStack.pop()
                node.left  = exprTreeStack.pop()
        exprTreeStack.append(node)
    root = exprTreeStack.pop()
    return root

def infixToPostfix(infix):
    '''
        convert infix expression to postfix expression 
    '''
    top = -1
    precedence = {'!': 3, '&' : 2, '|' : 2, '(' : 1}
    operatorstack = []
    postfix = ''
    for s in infix:
        if s in OPERATORS:
            if isCloseBracket(s):
                while operatorstack:
                    op = operatorstack.pop()
                    top -= 1
                    if op == '(':
                        break
                    postfix += op
            else:
                temp_top = top
                if s == '(':
                    operatorstack.append(s)
                else:
                    while temp_top > -1:
                        if operatorstack[temp_top] == '(':
                            break
                        if precedence[operatorstack[top]] >= precedence[s]:
                            postfix += str(operatorstack.pop())
                            top -= 1
                        temp_top -= 1
                    operatorstack.append(s)
                top += 1
        elif isOperand(s):
            postfix += s
    while operatorstack:
        postfix += str(operatorstack.pop())
        top -= 1
    return postfix

def preEvaluateExprFromTree(root):
    '''
       This function evaulates the expression using expression 
       tree
       Some optimization over postfix evaluation using expression 
       tree
    '''
    if root:
        value = root.data
        if isOperand(value):
            return value
        left = preEvaluateExprFromTree(root.left)
        if value == '!': 
            return notOp(left)
        elif value == '&' and isinstance(left, type(True)) and not left:
            return False
        elif value == '|' and isinstance(left, type(True)) and left:
            return True
        right = preEvaluateExprFromTree(root.right)
        if value == '&':
            return andOp(left, right)
        elif value == '|':
            return orOp(left, right)
        return True
    return True

def evaluateExpr(postfix, variableMap):
    '''
        This function expects statement to be postfix expression with 
        values of variables map to variableMap dictionary and it calculates
        the given expression is true or false based on the values of
        variableMap

    @postfix - the input statement has to be postfix expression
    @variableMap - the variables mapped values
    '''
    resultStack = []
    for e in postfix:    
        if isOperand(e):
            resultStack.append(e)
        elif e in OPERATORS:
            if e == '!':
                val = resultStack.pop()
                if isinstance(val, type('str')):
                    val = variableMap[val]
                resultStack.append(not val)
            elif e == '&':
                valA = resultStack.pop()
                valB = resultStack.pop()
                if isinstance(valA, type('str')): 
                    valA = variableMap[valA]
                if isinstance(valB, type('str')): 
                    valB = variableMap[valB]
                resultStack.append(valA and valB)
            elif e == '|':
                valA = resultStack.pop()
                valB = resultStack.pop()
                if isinstance(valA, type('str')): 
                    valA = variableMap[valA]
                if isinstance(valB, type('str')): 
                    valB = variableMap[valB]
                resultStack.append(valA or valB)
    result = resultStack.pop()
    if isinstance(result, type('str')):
        result = variableMap[result]
    return result 

def evaluateExprTree(root, variableMap):
    '''
        This function evaulates the expression using expression 
        tree
        Some optimization over postfix evaluation using expression 
        tree
     '''
    if root:
         value = root.data
         if isOperand(value):
            return variableMap[value]
         left = evaluateExprTree(root.left, variableMap)
         if value == '!': 
            return not left
         elif value == '&' and not left:
            return False
         elif value == '|' and left:
            return True
         right = evaluateExprTree(root.right, variableMap)
         if value == '&':
            return left and right
         elif value == '|':
            return left or right
         return True
    return True

if __name__ == '__main__':
    #statement = '((!a | a) & ((a & b) | (c | d) | (d & e) & (f & g)))'
    statement = '(a & b) | (!a & b) | (c & d) | (!c & d)'
    print (statement)
    postfix = infixToPostfix(statement)
    print (postfix)
    root = postfixToExpressionTree(postfix)
    print (preEvaluateExprFromTree(root))
    statement = '((!a & a) | ((a & b) | (c | d) | (d & e) & (f & g)))'
    postfix = infixToPostfix(statement)
    print (postfix)
    root = postfixToExpressionTree(postfix)
    print (preEvaluateExprFromTree(root))

