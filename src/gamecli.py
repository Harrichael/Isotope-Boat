"""
Michael Harrington

Main Python File for Puzzle Project 1

This puzzle is using search algorithms (and a later phase, heuristics)
in order to navigate a traffic jam like game with the
addition of a gradient cost field dubbed a radiation field.
"""

from cmd import Cmd

from clilib.helpers import isInputPiped
from game.heuristic import ( createGreedyHeuristic,
                             createSmartHeuristic,
                             createAdmissableHeuristic,
                             createConsistentHeuristic
                           )
from game.gameSolver import GameSolver
from game.util.pathFinders import BFTS, IDDFGS, GrBFGS, AStarGS

class GameCLI(Cmd):
    heuristicDict = {
            'smart': createSmartHeuristic,
            'admissable': createAdmissableHeuristic,
            'consistent': createConsistentHeuristic,
        }
    algorithmDict = {
            'asgs': (AStarGS, True),
            'grbfgs':  (GrBFGS,  True),
            'id-dfgs': (IDDFGS,  False),
            'bfts':    (BFTS,    False),
        }
    def __init__(self):
        Cmd.__init__(self)
        self.prompt = 'Isotope Boat>'
        # defaults
        self.heuristic = createSmartHeuristic
        self.useHeuristic = True
        self.algorithm = AStarGS

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
        # Set up solving inst
        if self.useHeuristic:
            algConstructor = lambda i, n, c, g: self.algorithm(i, n, c, g, self.heuristic(i))
        else:
            algConstructor = lambda i, n, c, g: self.algorithm(i, n, c, g)
        solver = GameSolver(algConstructor)
        # Solve
        inFile, outFile = line.split()
        if solver.runInputFile('puzzles/' + inFile):
            output = solver.strOutput()
            with open('solutions/' + outFile, 'w') as fileObj:
                fileObj.write(output)
        else:
            print '(Error) No solution found'

    def help_heuristic(self):
        print 'heuristic <heuristic>'
        print 'Selects the heuristic to use for solving'

    def do_heuristic(self, line):
        line = line.lower()
        if line in self.heuristicDict:
            self.heuristic = self.heuristicDict[line]

    def help_algorithm(self):
        print 'algorithm <algorithm>'
        print 'Selects the algorithm used to solve puzzles'

    def do_algorithm(self, line):
        line = line.lower()
        if line in self.algorithmDict:
            self.algorithm, self.useHeuristic = self.algorithmDict[line]

    """
    These functions exit the cli command loop
    """

    def do_exit(self, line):
        """Exits Isotope Boat CLI"""
        return True

    def do_EOF(self, line):
        return True

if __name__ == '__main__':
    cli = GameCLI()
    cli.cmdloop()

