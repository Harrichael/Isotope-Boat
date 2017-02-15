// This is an example source code file that will be compiled and 
// executed by run.sh. This code will read a puzzle file from the 
// 'puzzles' directory and create an example solution in the 'solutions'
// directory. You should create your own source files, then edit 
// 'run.sh' to compile and run your own program

#include <iostream>
#include <fstream>

int main(int argc, char* argv[])
{
  std::ifstream puzzleFile;
  std::ofstream solutionFile;
  std::string line;
  
  // read every line in the puzzle file
  std::cout << "Reading the puzzle file: \n";
  puzzleFile.open("puzzles/examplePuzzle.txt");
  while(std::getline(puzzleFile, line))
  {
	 std::cout << line << '\n'; 
  }
  puzzleFile.close();
  
  // output an example solution file
  solutionFile.open("solutions/exampleSolution.txt");
  solutionFile << "9848\n";
  solutionFile << "73\n";
  solutionFile << "6\n";
  solutionFile << "T 1 L,A 0 D,B 0 R,B 0 R,B 0 R,B 0 C\n";
  solutionFile << "5 4\n";
  solutionFile << "0 1\n";
  solutionFile << "10 1\n";
  solutionFile << "1 2 1\n";
  solutionFile << "2 3 U\n";
  solutionFile << "0 2 R\n";
  solutionFile << "1 3 L\n";
  solutionFile << "3 3\n";
  solutionFile << "3 0 D\n";
  solutionFile << "3 1\n";
  solutionFile.close();

  return 0;
}
