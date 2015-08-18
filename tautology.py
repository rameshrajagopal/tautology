#!/usr/bin/env python
from treeNode import TreeNode

OPERATORS = ('&', '|', '!', '(', ')')

def isCloseBracket(s):
    return s == ')'

def isOperand(s):
    return (s >= 'A' and s <= 'Z') or (s >= 'a' and s <= 'z')

def postfixToExpressionTree(postfix):
    exprTreeStack = []
    for e in postfix: 
        node = TreeNode(e)
        if e in OPERATORS:
            if e == '!':
                node.left = exprTreeStack.pop()
            else:
                node.left  = exprTreeStack.pop()
                node.right = exprTreeStack.pop()
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

def getVariableMap(statement):
    variableMap = {}
    for e in statement:
        if isOperand(e) and not e in variableMap:
            variableMap[e] = 0
    return variableMap


def isTautology(statement):
    '''
       Determines whether a statement given is a tuatology or not
    @statement - proper infix statement with proper paranthesis 
    '''
    variableMap = getVariableMap(statement)
    numVariables = len(variableMap)
    postfix = infixToPostfix(statement)
    for i in range(pow(2, numVariables)):
        for e in enumerate(variableMap):
            offset = e[0]
            key = e[1]
            variableMap[key] = (i & (1 << offset)) >> offset
        if not evaluateExpr(postfix, variableMap): 
            return False
    return True

#main
