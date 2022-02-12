import numpy as np
from matplotlib.pyplot import figure, show
import pandas as pd
import re

# TODO: add info about what the file format should be
filename = str(input("Please enter filename:"))
stop = 0

filedata = pd.read_csv(filename, encoding="utf8")

# Converting date column to datetime object
filedata['Date'] = pd.to_datetime(filedata['Date'], format='%d-%m-%y')

# Adding delta day column necessary for plotting
filedata['Delta_day'] = filedata['Date'] - filedata['Date'][0]

# Getting all users in the chat
names = filedata['Author'].unique()

# Options menu
choice = 0
while not ((choice == 1) or (choice == 2) or (choice == 3) or (choice == 4)):
    choice = int(input('Type 1 for total messages, type 2 for total words, type 3 for filtered words, '
                       'type 4 for average words per message:'))

# Retrieving filter words
if choice == 3:
    filterwords = np.array([])
    stop = 0
    while stop != 1:
        name = input("Enter a filtered word, enter nothing to stop adding more filtered words:")
        if name != '':
            filterwords = np.append(filterwords,str(name))
        if name == '':
            if len(filterwords)==0:
                print("Please fill in at least 1 word.")
            else:
                stop = 1
    # We have to make the filterwords into a query for pandas count to undertand using '|'s
    if len(filterwords)==1:
        filterword_query = filterwords[0]
    else:
        filterword_query = filterwords[0]
        for word in filterwords[1::]:
            filterword_query += f"|{word}"

fig = figure()
frame = fig.add_subplot(1,1,1)


# Data analysis and plotting
if choice == 1:
    # Getting number of messages in chat
    data = filedata.groupby(['Author','Delta_day']).size()

    # Unstacking data and filling in the NaNs, this is done so we can do the cumsum later
    data = data.unstack(0)
    data = data.fillna(0)

    # Cumulative summing
    data = data.cumsum()

    for name in names:
        number = str(int(data[name][-1]))
        frame.plot(range(data.index.size),data[name],label=(name + f': {number} messages'))
    frame.set_ylim(bottom=0)
    frame.set_xlim(left=0)
    frame.grid()
    frame.set_ylabel("Messages")
    frame.set_xlabel("Days since " + filedata['Date'][0].strftime("%d/%m/%Y"))

    fig.legend(loc=2)
    fig.suptitle('Data for sum of messages ' + filename)
    show()

if choice == 2:
    filedata['word_number'] = filedata['Content'].str.split().str.len()

    data = filedata[["Author", "word_number", "Delta_day"]]

    # Getting number of messages in chat
    data = data.groupby(['Author','Delta_day']).sum()

    # Unstacking data and filling in the NaNs, this is done so we can do the cumsum later
    data = data.unstack(0)
    data = data.fillna(0)

    # Cumulative summing
    data = data.cumsum()

    for column in data.columns:
        number = str(int(data[column][-1]))
        frame.plot(range(data.index.size),data[column],label=(column[1] + f': {number} words'))
    frame.set_ylim(bottom=0)
    frame.set_xlim(left=0)
    frame.grid()
    frame.set_ylabel("Words")
    frame.set_xlabel("Days since " + filedata['Date'][0].strftime("%d/%m/%Y"))

    fig.legend(loc=2)
    fig.suptitle('Data for sum of words ' + filename)
    show()

if choice == 3:
    filedata['filter_count'] = filedata['Content'].str.count(filterword_query, flags=re.IGNORECASE)

    data = filedata[["Author", "filter_count", "Delta_day"]]

    print(data)

    # Getting number of messages in chat
    data = data.groupby(['Author','Delta_day']).sum()

    # Unstacking data and filling in the NaNs, this is done so we can do the cumsum later
    data = data.unstack(0)
    data = data.fillna(0)

    # Cumulative summing
    data = data.cumsum()

    for column in data.columns:
        number = str(int(data[column][-1]))
        frame.plot(range(data.index.size),data[column],label=(column[1] + f': {number} times said'))
    frame.set_ylim(bottom=0)
    frame.set_xlim(left=0)
    frame.grid()
    frame.set_ylabel("Words")
    frame.set_xlabel("Days since " + filedata['Date'][0].strftime("%d/%m/%Y"))

    fig.legend(loc=2)
    fig.suptitle('Data for filtered words:' + str(filterwords))
    show()


