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
