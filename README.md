# The Converter of The Dialog Data

This is the converter of the dialog data, that is used in order to prepare the 
[the Cornell Movie Dialogs Corpus](https://www.cs.cornell.edu/~cristian/Cornell_Movie-Dialogs_Corpus.html) in the way that it could be used as the training input for the [Recurrent Neural Networks](https://www.tensorflow.org/versions/r0.12/tutorials/recurrent/index.html).

## Requirements

The script only requires the ```scikit-learn``` in order to work. If you do not have it, you can easily install it with the following command:

    sudo pip install scikit-learn

## Usage

In order to simplify the process, the code in the repository is self-contained and, in order to prepare the training data, you can just execute the following command:

    python converter.py

This will produce 4 files that are needed for the learning process:

* train.a;
* train.b;
* test.a;
* test.b;

Even though, you have already all the required files, I would strongly advise you to go through the rest of the page just to have some basic understanding what is going on here.

# The Cornell Movie Dialogs Corpus And The Part That is Used By The script

In order to understand what type of data is in the corpus here is the quote for the official page: 

    This corpus contains a large metadata-rich collection of fictional conversations extracted from raw movie scripts:
    
    - 220,579 conversational exchanges between 10,292 pairs of movie characters
    - involves 9,035 characters from 617 movies
    - in total 304,713 utterances

The corpus itself contains different files. The one, that we are interested in, is the following one: ```movie_lines.txt```. The file contains actual conversations. Each line in the file is a phrase from a dialog, that was observed in a movie(with a meta data). All phrases have been sorted with respect to how they appear in a script, so no need to sort anything.

## Lines From The "movie_lines" File

Here are examples of lines from the file:

    L1045 +++$+++ u0 +++$+++ m0 +++$+++ BIANCA +++$+++ They do not!
    L1044 +++$+++ u2 +++$+++ m0 +++$+++ CAMERON +++$+++ They do to!
    
As can be seen, the string ```+++$+++```is used as a fields separator. Each line includes following fields:

* lineID (e.g. L1045). As can be seen from the example: yes lines are sorted, however they are sorted in desend order ¯\\\_(ツ)\_/¯;
* characterID (who uttered this phrase, e.g.: u0);
* movieID (e.g.: m0);
* character name (e.g.: BIANCA);
* text of the utterance (e.g.: They do to!);

# What Exactly The Script Extracts From The "movie_lines" File?

For the simple RNN network only special cases of the dialogs are useful for the training. Technically you can train RNN with any type of dialogs, however for the sake of simplicity we are limiting ourselves to cases with simple dialogs. A dialog is considered simple if:

1. Only 2 persons are participating in a dialog;
2. There should not be 2 consequent lines that belong to a same character;

## A Bad Dialog Examples

In order to understand a "simple dialog" requirements let me show the example of the dialogue that is not satisfying above requirements:

    L280 +++$+++ u2 +++$+++ m0 +++$+++ CAMERON +++$+++ There.
    L277 +++$+++ u2 +++$+++ m0 +++$+++ CAMERON +++$+++ Well, there's someone I think might be --
    L276 +++$+++ u0 +++$+++ m0 +++$+++ BIANCA +++$+++ How is our little Find the Wench A Date plan progressing?
    L275 +++$+++ u0 +++$+++ m0 +++$+++ BIANCA +++$+++ Forget French.
 
The dialog violates the second requirement. First, there are 2 consequent lines from the same character (u2/CAMERON), then, there are 2 consequent lines from the other character (u0/BIANCA).

# Pre-processing Of Dialogs

There is only one operation that is executed as pre-processing of dialogue - all words are made lowercase. This is needed in order to prevent our chatbot of thinking that words "The" and "the" are completely different words.

# How The Script's Output Is Structured

The script produces 4 files as the output:

* train.a;
* train.b;
* test.a;
* test.b;

As can be seen, dialogs have been split into 2 groups: train and test. As well as each group has been splitted into 2 sub-groups: a and b.

# A "train"/"test" Separation

Dialogs are split randomly into 2 groups: "train" and "test" with respect to the next proportions: 80% of all dialogs goes to the "train" group and 20% goes to the "test" group.

Actual separation is implemented with the [train_test_split](http://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html) method.

# A "a"/"b" Separation

All dialogs within the same group ("train" or "test") are split into 2 parts ("a" and "b"). For the sake of the example, we will demonstrate the split process for the group "train". In order to split dialogs into "a"/"b" groups, in each simple dialog, lines are split into 2 parts, one part with lines that have even numbers, another part contains lines with non-even numbers. Let me show an example:

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
