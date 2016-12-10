# The converter of the dialog data

This is the converter of the dialog data, that is used in order to prepare the 
[https://www.cs.cornell.edu/~cristian/Cornell_Movie-Dialogs_Corpus.html](the Cornell Movie Dialogs Corpus) in the way that it could be used as the training input for the [https://www.tensorflow.org/versions/r0.12/tutorials/recurrent/index.html](Recurrent Neural Networks). In order to simplify the process, the code in the repository is self-contained and, in order to prepare the training data, you can just execute the following command:

       python converter.py

This will produce 2 files that are needed for the learning process:

* train.a;
* train.b;

If you would like to know more, following sections of the page will give you all the required details. Though, I would strongly advise you to go through the rest of the page just to have some basic understanding what is going on here.
