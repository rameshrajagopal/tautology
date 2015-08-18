#!/usr/bin/env python

import tautology

#main
if __name__ == '__main__':
    while True:
        try:
            expr = input()
            if tautology.isTautology(expr): 
                print ("True")
            else:
                print ("False")
        except Exception as e:
            break
    
