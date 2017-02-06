"""
Michael Harrington

Main Python File for Puzzle Project 1

This puzzle is using search algorithms (and a later phase, heuristics)
in order to navigate a traffic jam like game with the
addition of a gradient cost field dubbed a radiation field.
"""

from game.gameSolver import GameSolver

inputPuzzles = [ 'puzzle1.txt',
                 'examplePuzzle.txt',
               ]

outputFiles = [ 'solution1.txt',
                'solution2.txt',
              ]

if __name__ == '__main__':
    solver = GameSolver()
    for inFile, outFile in zip(inputPuzzles, outputFiles):
        if solver.runInputFile('puzzles/' + inFile):
            output = solver.strOutput()
            with open('solutions/' + outFile, 'w') as fileObj:
                fileObj.write(output)
        else:
            print '(Error) No solution found'

