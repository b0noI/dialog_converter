# The converter of the dialog data

This is the converter of the dialog data, that is used in order to prepare the 
[the Cornell Movie Dialogs Corpus](https://www.cs.cornell.edu/~cristian/Cornell_Movie-Dialogs_Corpus.html) in the way that it could be used as the training input for the [Recurrent Neural Networks](https://www.tensorflow.org/versions/r0.12/tutorials/recurrent/index.html). In order to simplify the process, the code in the repository is self-contained and, in order to prepare the training data, you can just execute the following command:

    python converter.py

This will produce 2 files that are needed for the learning process:

* train.a;
* train.b;

If you would like to know more, following sections of the page will give you all the required details. Though, I would strongly advise you to go through the rest of the page just to have some basic understanding what is going on here.

# The Cornell Movie Dialogs Corpus and the part that is used by the script

In order to understand what type of data is in the corpus here is the quote for the official page: 

    This corpus contains a large metadata-rich collection of fictional conversations extracted from raw movie scripts:
    
    - 220,579 conversational exchanges between 10,292 pairs of movie characters
    - involves 9,035 characters from 617 movies
    - in total 304,713 utterances

The corpus itself contains different files. The one, that we are interested in, is the following one: ```movie_lines.txt```. The file contains actual conversations. Each line in the file is a phrase from a dialog, that was observed in a movie(with a meta data). All phrases have been sorted with respect to how they appear in a script, so no need to sort anything.

## Lines from the movie_lines file

Here are examples of lines from the file:

    L1045 +++$+++ u0 +++$+++ m0 +++$+++ BIANCA +++$+++ They do not!
    L1044 +++$+++ u2 +++$+++ m0 +++$+++ CAMERON +++$+++ They do to!
    
As can be seen, the string ```+++$+++```is used as a fields separator. Each line includes following fields:

* lineID (e.g. L1045). As can be seen from the example: yes lines are sorted, however they are sorted in desend order ¯\\\_(ツ)\_/¯;
* characterID (who uttered this phrase, e.g.: u0);
* movieID (e.g.: m0);
* character name (e.g.: BIANCA);
* text of the utterance (e.g.: They do to!);

# What exactly the script extracts from the movie_lines file?

For the simple RNN network only special cases of the dialogs are useful for the training. Technically you can train RNN with any type of dialogs, however for the sake of simplicity we are limiting ourselves to cases with simple dialogs. A dialog is considered simple if:

1. Only 2 persons are participating in a dialog;
2. There should not be 2 consequent lines that belong to a same character;

## Bad dialog examples

In order to understand a "simple dialog" requirements let me show the example of the dialogue that is not satisfying above requirements:

    L280 +++$+++ u2 +++$+++ m0 +++$+++ CAMERON +++$+++ There.
    L277 +++$+++ u2 +++$+++ m0 +++$+++ CAMERON +++$+++ Well, there's someone I think might be --
    L276 +++$+++ u0 +++$+++ m0 +++$+++ BIANCA +++$+++ How is our little Find the Wench A Date plan progressing?
    L275 +++$+++ u0 +++$+++ m0 +++$+++ BIANCA +++$+++ Forget French.
 
The dialog violates the second requirement. First, there are 2 consequent lines from the same character (u2/CAMERON), then, there are 2 consequent lines from the other character (u0/BIANCA).

# How the script's output is structured

The script produces 2 files as the output:

* train.a;
* train.b;

Files contain simple dialogs that are split into 2 parts. In an each simple dialog, lines are split into 2 parts, one part with lines that have even numbers, another part contains lines with non-even numbers. Let me show an example:

    L19693 +++$+++ u198 +++$+++ m13 +++$+++ ELAINE +++$+++ It's a damn good thing you don't know how much he hates your guts.
    L19692 +++$+++ u214 +++$+++ m13 +++$+++ STRIKER +++$+++ It's a damn good thing he doesn't know how much I hate his guts.
    L19691 +++$+++ u198 +++$+++ m13 +++$+++ ELAINE +++$+++ Sluggish. Like a wet sponge.
    L19690 +++$+++ u214 +++$+++ m13 +++$+++ STRIKER +++$+++ Sluggish. Like a wet sponge.

Lines number 0 and 2 (even) will go to the one file (```train.a```):

    L19693 +++$+++ u198 +++$+++ m13 +++$+++ ELAINE +++$+++ It's a damn good thing you don't know how much he hates your guts.
    L19691 +++$+++ u198 +++$+++ m13 +++$+++ ELAINE +++$+++ Sluggish. Like a wet sponge.

Lines number 1 and 3 (non-even) will go to the another file (```train.b```):

    L19692 +++$+++ u214 +++$+++ m13 +++$+++ STRIKER +++$+++ It's a damn good thing he doesn't know how much I hate his guts.
    L19690 +++$+++ u214 +++$+++ m13 +++$+++ STRIKER +++$+++ Sluggish. Like a wet sponge.

As the result, there will be 2 files, each line of the file ```train.a``` will contain a replica from a simple dialog, while a line with the same number from the file ```train.b``` contains answer to the phrase from the same dialog. For example line number 0 form the ```train.a``` might contain:

    It's a damn good thing he doesn't know how much I hate his guts.

while the line number 0 from the ```train.b``` will contain:

    It's a damn good thing you don't know how much he hates your guts.
