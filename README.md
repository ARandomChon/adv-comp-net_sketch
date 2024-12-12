# adv-comp-net_sketch
Final Project for CSE 534: Advanced Computer Networks taught by Dr. Violet Syrotiuk

Sketching method that separates network traffic depending on traffic rates.  Writeup, presentation, short code in python, and (coming soon) P4 implementation

To run the simulations, use `sketch.py` in the `prog` folder.  Dependencies are random, numpy, and matplotlib.  Currently it is run with no command line arguments, though I plan
to add arguments for setting a custom seed, stream length, window size, max group number, number of symbols (packet types) and a probability distribution for them, and a custom filename for the figure.

With the current default settings, the plot in the presentation and report should be reproduced by running this file and will be output as `plot.svg` in the same directory as the file.
