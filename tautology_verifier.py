#!/usr/bin/env python

from tautology import PropositionStatement

#main
if __name__ == '__main__':
    while True:
        try:
            expr = input()
            propostionStatement = PropositionStatement(expr)
            if propostionStatement.isTautology():
                print ("True")
            else:
                print ("False")
        except Exception as e:
            break
    
