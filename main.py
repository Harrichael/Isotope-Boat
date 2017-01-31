"""
Michael Harrington

Main Python File for Puzzle Project 1

This puzzle is using search algorithms and heuristics
in order to navigate a traffic jam like game with the
addition of a gradient cost field.

TODO:
    Code Comments/Headers
"""

from gameSolver import GameSolver

if __name__ == '__main__':
    solver = GameSolver()
    if solver.runInputFile('puzzles/puzzle1.txt'):
        output = solver.strOutput()
        with open('solutions/solution1.txt', 'w') as fileObj:
            fileObj.write(output)
    else:
        print '(Error) No solution found'

