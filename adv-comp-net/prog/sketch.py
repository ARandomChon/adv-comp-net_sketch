"""
sketch.py

file that performs experiments using sketch and streaming algorithm i proposed

sean bergen
"""

import random

import numpy as np
import matplotlib.pyplot as plt

# note that for these experiments we are using a single group

# function to add a new type of packet to the sketch
def update_sketch(sigma, sketch, m):
    # fields of the sketch per packet are buffer and group number
    if(sigma not in sketch):
        sketch[sigma] = [1, m]
    else:
        sketch[sigma][0] = sketch[sigma][0] + 1
        sketch[sigma][1] = max(1, sketch[sigma][1] - 1)
    # iterate over dictionary and adjust each other packet type
    for k,v in sketch.items():
        if k == sigma:
            continue
        v[0] = v[0] - 1
        if v[0] < 0:
            v[0] = 1
            v[1] = min(m, v[1] + 1)

# update dictionary with count of each item in stream
# it is called `update_counts` because that matches character length of
#              `update_sketch`          :^)
def update_counts(counts, item):
    if(item not in counts):
        counts[item] = 1
    else:
        counts[item] = counts[item] + 1

# format printing to make the sketch easier to read
def print_sketch(sketch):
    print("Packet|Buff|Group")
    for k in sorted(sketch):
        print("  ",k,"  ",sketch[k][0],"  ",sketch[k][1])

# format printing to make the counts easier to read
def print_counts(counts):
    print("Packet|Count")
    for k in sorted(counts):
        print("  ",k,"  ",counts[k])

# updates results dictionary with window_sketch and window_counts
def update_results(w_s, w_c, r):
    keys = sorted(w_s)
    for key in keys:
        # this should only happen the first time
        if key not in r:
            r[key] = [w_s[key] + [w_c[key]]]
        else:
            r[key].append(w_s[key]+[w_c[key]])


if __name__ == '__main__':
    # we can use a dictionary to act as our sketch
    sketch = {}

    # group maximum
    m = 20

    # window size
    n = 40

    seed = 12345678990
    random.seed(seed)
    #stream = random.choices([0,1,2,3,4,5], k=80)

    # attempt at using weights to get the following dist:
    #   0 -> 0.1, 1 -> 0.2, 2 -> 0.4, 3 -> 0.05, 4 -> 0.15, 5 -> 0.1
    stream = random.choices([0,1,2,3,4,5],
                            weights=[0.1,0.2,0.4,0.05,0.15,0.1],
                            k = 8000)
    # build a dictionary showing the number of times each element occurs in
    # the stream
    counts = {}
    
    """
    for packet in stream:
        update_sketch(packet, sketch, m)
        update_counts(counts, packet)
    """

    # create a dictionary for results of count and buff/group per window
    results = {}

    window = 0
    # iterate over the stream, separating by window size
    for i in range(0,len(stream),n):
        window_sketch = {}
        window_counts = {}
        for j in range(n):
            update_sketch(stream[i+j], sketch, m)
            update_sketch(stream[i+j], window_sketch, m)
            update_counts(counts, stream[i+j])
            update_counts(window_counts, stream[i+j])
        
        # print information per window [uncomment to do so]
        #print("Window ", window,":")
        #print_sketch(window_sketch)
        #print_counts(window_counts)
        
        # save window sketch and window count to write out later
        update_results(window_sketch, window_counts, results)
        for x in range(6):
            if len(results[x]) <= window:
                results[x].append([0,m,0])
        window = window + 1
    # for larger stream sizes we just print out the summaries
    """
    print(sketch)
    print(stream)
    print(counts)
    """ 
    """
    # print limited results for the first 15 windows
    keys = sorted(sketch)
    for key in keys:
        print("Packet type",key,":")
        for i in range(15):
            print(results[key][i])
    
    print("Full stream summary:")
    print_sketch(sketch)
    print_counts(counts)
    """

    for x in range(6):
        print(len(results[x]))

    # create plots
    fig, (ax0, ax1, ax2) = plt.subplots(nrows=3, ncols=1, figsize=(12,10))
    
    # same scale, plotting buffer, group number, and count over each window
    x = range(200)

    for key in range(6):
        y0 = []
        y1 = []
        y2 = []
        for i in range(200):
            y0.append(results[key][i][0])
            y1.append(results[key][i][1])
            y2.append(results[key][i][2])
        label0 = "Sig" + str(key) + " Buffer"
        label1 = "Sig" + str(key) + " Group"
        label2 = "Sig" + str(key)
        ax0.plot(x,y0,label=label0)
        ax1.plot(x,y1,label=label1)
        ax2.plot(x,y2,label=label2)
    ax0.set_title("Buffer over Windows")
    ax1.set_title("Group number over Windows")
    ax2.set_title("Count per window")
    
    fig.tight_layout(pad=1.0)
    plt.legend(loc="upper left")

    plt.savefig("plot.svg")
