## Submission Rules

This is your submission repository for CS5400, puzzle assignment 4. Within this repository, you need to write a program that will solve four puzzle instances of Isotope Boat using A-Star Graph Search (A*GS). As part of implementing A*GS, you will be implementing a custom, high-quality heuristic of your own design, which takes the radiation of the puzzle into account. The puzzle instances are located in puzzles/puzzle1.txt, puzzles/puzzle2.txt, puzzles/puzzle3.txt, and puzzles/puzzle4.txt. Your program should place the solutions in solutions/solution1.txt, solutions/solution2.txt, solutions/solution3.txt and solutions/solution4.txt, respectively. See http://web.mst.edu/~tauritzd/courses/cs5400/sp2017/puzzle.html for information on the puzzle and solution formats. Once your submission is ready, you should commit and push your submission to the master branch on git-classes by the submission deadline.

Note that there is also an examplePuzzle.txt in the puzzles directory. You are not required to provide a solution for this one, but your program should still be able to solve it.

Just like with puzzle assignments 2 and 3, your repository contains a file named "readyToSubmit.txt". The first line of this file just contains the word "no". When you are ready to submit, change the "no" to a "yes", and submit your files as normal (including that file). This is how you will let us know whether your repository is ready to be graded on the due date. If you do need to turn in the assignment late, then this will also let us know when you are ready to submit. 

You may copy over and re-use code from previous puzzle assignments, but your final submission for puzzle assignment 4 should be an A*GS algorithm, with a heuristic that takes radiation into account.

In order for your submission to count, you **MUST** change the *run.sh* script to **compile and run** your submission. 
    * Note: This script, and your program, must run on the standard MST campus linux machines, without any additional command line arguments.


Feel free to:
1. Add any files or folders you require.
2. Commit, branch, and clone this repo. (We'll only look at *master* for grading)

## Bonus

You can earn a 15% bonus on this assignment by implementing two different heuristics, where the user can specify at runtime which is to be used (with a default choice if the user does not specify a choice). One of the heuristics must be consistent, and the other must be admissible, but non-consistent. For each heuristic, submit solution files for each puzzle it is able to solve. Follow the solution naming format above, and append "_1" after the solution number for solutions produced by the first heuristic, and "_2" for solutions produced by the second heuristic (so, the solution for puzzle 3 produced by the second heuristic would be named "solution3_2.txt"). Additionally, a fifth puzzle will be posted to the puzzle website, http://web.mst.edu/~tauritzd/courses/cs5400/sp2017/puzzle.html, sometime this week. Your A*GS employing the consistent heuristic must solve puzzle 5 at least 10% faster than A*GS employing the admissible, non-consistent heuristic. 

You can earn a further 10% bonus by submitting a proof that your admissible and non-consistent heuristic is admissible and non-consistent. You may earn another further 20% by submitting a proof that your consistent heuristic is consistent. In total, completing all bonus tasks for puzzle assignment 4 will award a potential 45% bonus.


## Compiling and Running
As mentioned above, we will be using the *run.sh* bash script to compile and run your submissions. This script must work on campus linux machines, without any additional command line arguments. Therefore, when testing and running your submission, I suggest always using the command:
```
./run.sh
```

I've also provided you with an example of what this script might look like for a simple C++ compilation and execution, example.cpp. Feel free to reuse parts of this for your own 
project, though I suggest instead using a makefile for compilation.

## Coding Standards
Code formatting and style for C, C++, C# and Java should roughly follow [MST's C++ coding guidelines.](http://web.mst.edu/~cpp/cpp_coding_standard_v1_1.pdf)
For python, [PEP8](https://www.python.org/dev/peps/pep-0008/) is ideal.

Because this course is more about the algorithms, we won't strictly hold you to these standards as long as your code is readable.
Having said that, we want you to comment and document the core algorithms very well so that it's clear you understand them.
