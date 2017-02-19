"""
Michael Harrington

Main Python File for Puzzle Project 1

This puzzle is using search algorithms (and a later phase, heuristics)
in order to navigate a traffic jam like game with the
addition of a gradient cost field dubbed a radiation field.
"""

from cmd import Cmd

from clilib.helpers import isInputPiped
from game.heuristic import createGreedyHeuristic
from game.gameSolver import GameSolver
from game.util.pathFinders import BFTS, DLGS, IDDFGS, GrBFGS

class GameCLI(Cmd):
    def __init__(self):
        Cmd.__init__(self)
        self.prompt = 'Isotope Boat>'
        self.solver = GameSolver(lambda i, n, c, g: GrBFGS(i, n, c, g, createGreedyHeuristic(i)))

    """
    These functions control the behavior of our cli
    """

    def precmd(self, line):
        # If we pipe in input from file, make it look pretty
        if isInputPiped():
            print(line)
        return Cmd.precmd(self, line)

    def preloop(self):
        print 'Welcome to Isotope Boat Solver. Use help to explore commands.'
        print

    def postloop(self):
        print

    def emptyline(self):
        pass

    """
    These functions provide actual commands for the cli
    """

    def help_solve(self):
        print 'solve <inputFile> <outputFile>'
        print 'Solves the input puzzle file writing output to output file'

    def do_solve(self, line):
        inFile, outFile = line.split()
        if self.solver.runInputFile('puzzles/' + inFile):
            output = self.solver.strOutput()
            with open('solutions/' + outFile, 'w') as fileObj:
                fileObj.write(output)
        else:
            print '(Error) No solution found'

    def do_EOF(self, line):
        return True

if __name__ == '__main__':
    cli = GameCLI()
    cli.cmdloop()

