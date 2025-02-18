# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 08:21:55 2019

@author: Man Vinayaka
"""


def timeProp(df, year, pollutant):
    """ Plot a stacked bar graph of all data in the df
        based on frequency of wind direction in compass
        directions. Takes the average of every 3 days
        in each bar. The hight of the bar is value of 
        the pollutant that 3 day period. The bars are 
        binned proportionaly based on the overall value of the 
        pollutant 
		
		Parameters
		----------
		df: data frame
			data frame which has the fields of date and the pollutant
			to be graphed
		year: type string
			The year of which the data will be cut
		pollutant: type string
			The pollutant of which to plot
    """
    import datetime as dt
    import matplotlib.pyplot as plt
    import matplotlib as mpl
    import numpy as np
    import pandas as pd
    from numpy import array
    import matplotlib.patches as mpatches

    # =============================================================================
    #     Cuts data into the year specified and averages the
    #     values of each day
    # =============================================================================
    df.index = pd.to_datetime(df.date)
    df = df.drop("date", axis=1)
    df_2003 = df[year]
    df_2003 = df_2003.fillna(method="ffill")
    df_2003["month"] = df_2003.index.month

    # New df containing only the values of the pollutant specified
    polArray = df[year].resample("1D").mean()
    polArray = df_2003[pollutant]

    nA = []
    neA = []
    eA = []
    seA = []
    sA = []
    swA = []
    wA = []
    nwA = []
    polMeanS = 0
    polMeanE = 3
    dfStart = 0
    dfEnd = 72  # 24*3 for 3 day average

    x = 0

    while x < 121:  # 365 days / 3 = 121 floored. Represents number of bars total
        n = 0
        ne = 0
        e = 0
        se = 0
        s = 0
        sw = 0
        w = 0
        nw = 0
        a = df_2003[dfStart:dfEnd]
        b = a["wd"]

        i = 0
        while i < 72:  # Bins the wd data into categories for stacked bar graph
            if b[i] > 348.75 or b[i] < 33.75:
                n = n + 1
            elif b[i] > 33.75 and b[i] < 78.75:
                ne = ne + 1
            elif b[i] > 78.75 and b[i] < 123.75:
                e = e + 1
            elif b[i] > 123.75 and b[i] < 168.75:
                se = se + 1
            elif b[i] > 168.75 and b[i] < 213.75:
                s = s + 1
            elif b[i] > 213.75 and b[i] < 258.75:
                sw = sw + 1
            elif b[i] > 258.75 and b[i] < 303.75:
                w = w + 1
            elif b[i] > 303.75 and b[i] < 348.75:
                nw = nw + 1

            i = i + 1
        # calculates the 3 day proportion mean of each polutant and stores
        # it in a new list
        n = (n / 72) * (polArray[polMeanS:polMeanE].mean())
        ne = (ne / 72) * (polArray[polMeanS:polMeanE].mean())
        e = (e / 72) * (polArray[polMeanS:polMeanE].mean())
        se = (se / 72) * (polArray[polMeanS:polMeanE].mean())
        s = (s / 72) * (polArray[polMeanS:polMeanE].mean())
        sw = (sw / 72) * (polArray[polMeanS:polMeanE].mean())
        w = (w / 72) * (polArray[polMeanS:polMeanE].mean())
        nw = (nw / 72) * (polArray[polMeanS:polMeanE].mean())

        nA.append(n)
        neA.append(ne)
        eA.append(e)
        seA.append(se)
        sA.append(s)
        swA.append(sw)
        wA.append(s)
        nwA.append(nw)
        x = x + 1
        # Adds to start and end values to get through end of df
        polMeanS = polMeanS + 3
        polMeanE = polMeanE + 3
        dfStart = dfStart + 72
        dfEnd = dfEnd + 72

    #########################################

    # Plots the stacked bar graph with specific color represtations.
    # A legend is also plotted
    X = np.arange(121)

    data = np.array([nA, neA, eA, seA, sA, swA, wA, nwA])

    color_list = ["red", "blue", "green", "purple", "orange", "yellow", "brown", "pink"]
    X = np.arange(data.shape[1])
    for i in range(data.shape[0]):
        plt.bar(
            X,
            data[i],
            bottom=np.sum(data[:i], axis=0),
            color=color_list[i % len(color_list)],
        )
    red_patch = mpatches.Patch(color="red", label="north")
    blue_patch = mpatches.Patch(color="blue", label="north east")
    green_patch = mpatches.Patch(color="green", label="east")
    purple_patch = mpatches.Patch(color="purple", label="south east")
    orange_patch = mpatches.Patch(color="orange", label="south")
    yellow_patch = mpatches.Patch(color="yellow", label="south west")
    brown_patch = mpatches.Patch(color="brown", label="west")
    pink_patch = mpatches.Patch(color="pink", label="north west")
    plt.legend(
        bbox_to_anchor=(1.05, 1),
        loc=2,
        borderaxespad=0.0,
        handles=[
            red_patch,
            blue_patch,
            green_patch,
            purple_patch,
            orange_patch,
            yellow_patch,
            brown_patch,
            pink_patch,
        ],
    )

    plt.xticks(
        np.arange(0, 121, 10),
        (
            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "May",
            "Jun",
            "Jul",
            "Aug",
            "Sep",
            "Oct",
            "Nov",
            "Dec",
        ),
    )
    plt.title("wind direction")
    plt.xlabel("Contribution weighted by Mean")
    plt.ylabel("pollutant")
    plt.show()


# =============================================================================
# mydata = pd.read_csv('mydata.csv')
# timeProp(mydata,'2003','so2')
# =============================================================================
