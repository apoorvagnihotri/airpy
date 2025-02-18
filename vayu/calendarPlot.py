# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 15:52:41 2019

@author: Man Vinayaka
"""

#!/usr/bin/env python
# coding: utf-8


def calendarPlot(df, pollutant, year, **kwargs):
    """ Plots a heatmap on a calendar layout based 
        on the intensity of the pollutant per day.
        Each day contains an arrow indicating both 
        wind direction as well as wind speed
		
		Parameters
		----------
		df: data frame
			minimally containing date and at least one other
			numeric variable 
		pollutant: type string
			A pollutant name correspoinding to 
			a variable in a data frame, ex: 'pm25'
		year: type string
			Year to plot, ex '2003'
    """
    import datetime as dt
    import matplotlib.pyplot as plt
    import matplotlib as mpl
    import numpy as np
    import pandas as pd
    from numpy import array

    def calendar_array(dates, data):
        """ creates the calendar array returning i,j giving
            positional values in the array
        """
        i, j = zip(*[d.isocalendar()[1:] for d in dates])
        i = np.array(i) - min(i)
        j = np.array(j) - 1
        ni = max(i) + 1

        calendar = np.nan * np.zeros((ni, 7))
        calendar[i, j] = data
        return i, j, calendar

    def calendar_heatmap(ax, dates, data):
        """ Sets heatmap information
        """
        i, j, calendar = calendar_array(dates, data)
        im = ax.imshow(calendar, interpolation="none", cmap="YlOrRd", vmin=0, vmax=40)
        label_days(ax, dates, i, j, calendar)

    def label_days(ax, dates, i, j, calendar):
        """ Based on the day of the week, it will print that 
            text on each box of the day. The arrow is also ploted on
            each box for every day converting the given wind direction
            to a xy coordinate
        """
        ni, nj = calendar.shape
        day_of_month = np.nan * np.zeros((ni, 7))
        day_of_month[i, j] = [d.day for d in dates]

        for (i, j), day in np.ndenumerate(day_of_month):
            if np.isfinite(day):
                ax.arrow(
                    j,
                    i,
                    avg_ws[int(day) - 1 + a]
                    * np.cos(avg_wd[int(day) - 1 + a] * np.pi / 180.0)
                    / 15.0,
                    -avg_ws[int(day) - 1 + a]
                    * np.sin(avg_wd[int(day) - 1 + a] * np.pi / 180.0)
                    / 15.0,
                    head_width=0.15,
                    head_length=0.1,
                    fc="k",
                    ec="k",
                )

        ax.set_yticklabels([])
        ax.set_xticklabels([])

    # =============================================================================
    #     Cuts given data to show average of each day.
    #     Adds a month coloumn to the df as well
    # =============================================================================

    df.index = pd.to_datetime(df.date)
    df = df.drop("date", axis=1)
    df_2003 = df[year].resample("1D").mean()
    df_2003 = df_2003.fillna(method="ffill")
    df_2003["month"] = df_2003.index.month
    df_2003.index.dayofweek

    t = 1

    fig, ax = plt.subplots(figsize=(10, 10), nrows=4, ncols=4)

    # =============================================================================
    #     """ Plots 12 seperate plots that are then put togeather in a
    #         4x4 arrangement with the last column being used to plot
    #         the colorbar
    #     """
    # =============================================================================
    while t <= 12:

        avg_ws = []
        avg_wd = []
        avg_pm25 = []
        df_2003_1 = df_2003[df_2003.month == t]
        avg_wd = df_2003_1["wd"]
        avg_ws = df_2003_1["ws"]
        avg_pm25 = df_2003_1[pollutant]

        i = 1
        a = 0
        b = len(avg_pm25)
        while i <= 1:
            data = avg_pm25[a:b]
            num = len(data)
            if t == 12:
                start = dt.datetime(2003, 1, 1)
            else:
                start = dt.datetime(2003, t, 1)
            dates = [start + dt.timedelta(days=i) for i in range(num)]

            month_labels = [
                "               Jan               ",
                "               Feb               ",
                "               Mar               ",
                "               Apr               ",
                "               May               ",
                "               Jun               ",
                "               Jul               ",
                "               Aug               ",
                "               Sep               ",
                "               Oct               ",
                "               Nov               ",
                "               Dec               ",
            ]
            ax[(t - 1) // 3][(t - 1) % 3].set_title(
                month_labels[t - 1], bbox=dict(facecolor="whitesmoke")
            )
            calendar_heatmap(ax[(t - 1) // 3][(t - 1) % 3], dates, data)
            i = i + 1
        t = t + 1

    plt.tight_layout()

    # =============================================================================
    #    Colorbar plotting
    # =============================================================================
    grid = plt.GridSpec(4, 4, wspace=2, hspace=0.3)

    cbar_ax = plt.subplot(grid[:, 3])
    cmap = plt.cm.get_cmap("YlOrRd")
    norm = mpl.colors.Normalize(vmin=0, vmax=50)

    cb1 = mpl.colorbar.ColorbarBase(
        cbar_ax, cmap=cmap, norm=norm, orientation="vertical"
    )
    cb1.ax.tick_params(labelsize=15)

    plt.show()
    plt.close("all")


# calendarPlot(mydata,'pm25','2003')
