# Quiz Parser

This is a simple Python command-line utility that takes in the html file of a MCC quiz and outputs
a json file with the quiz questions and your selected answers. This is primarily to be used
in combination with my flashcard generator program, which takes in the json file and lets you 
study with flashcards (WIP).

## Usage
Simply navigate to your gradebook, go to the quiz you want to practice, and right click the page.
Press "Save as..." and select a location. Now go into the new folder at that location and copy the path
to the html file that is named something like 50001.html. Then, run the `main.py` file from the terminal,
passing in the path to that file. The JSON will then be generated on the `output` directory by default.

Good luck studying :)
