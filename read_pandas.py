import pandas as pd
import plotly.express as px
import numpy as np
import plotly.io as pio

pio.renderers.default = "browser"

def read_my_csv():
    
    df = pd.read_csv("data/activities/activity.csv")

    t_end = len(df)
    time = np.arange(0, t_end)
    df["Time"] = time

    return df

'''
def filter_data(df):
    df["zone1"] = df["HeartRate"] < 100
    df["zone2"] = (df["HeartRate"] >= 100) & (df["HeartRate"] < 150)
    df["zone3"] = (df["HeartRate"] >= 150) & (df["HeartRate"] < 200)
    df["zone4"] = df["HeartRate"] >= 200
'''

def assign_zones(df, max_hr=190):

    df["zone"] = np.select(
        [
            df["HeartRate"] < 0.6 * max_hr,
            (df["HeartRate"] >= 0.6 * max_hr) & (df["HeartRate"] < 0.7 * max_hr),
            (df["HeartRate"] >= 0.7 * max_hr) & (df["HeartRate"] < 0.8 * max_hr),
            (df["HeartRate"] >= 0.8 * max_hr) & (df["HeartRate"] < 0.9 * max_hr),
            df["HeartRate"] >= 0.9 * max_hr
        ],
        [1, 2, 3, 4, 5],
        default=0
    )
    return df


def make_plot(df):
    # HeartRate farblich nach Zonen
    fig1 = px.scatter(
        df, x="Time", y="HeartRate", color="zone",
        color_discrete_map={1:'blue', 2:'green', 3:'orange', 4:'red', 5:'purple'},
        labels={"zone":"Herzfrequenz-Zone"},
        title="HeartRate farblich nach Zonen"
    )
    
    return fig1

def make_plot_power(df):
    # Power farblich nach Zonen
    fig2 = px.line(
        df, x="Time", y="PowerOriginal",
        labels={"PowerOriginal":"Leistung (W)"},
        title="Leistung über die Zeit"
    )
    
    return fig2

def how_much_time_is_spent_in_the_zones(df, sampling_rate=1):
    
    sek_pro_wert = 1 / sampling_rate
    return {
        f"zone{i}": ((df["zone"] == i).sum() * sek_pro_wert) / 60
        for i in range(1, 6)
    }



def average_power_per_zone(df):
    
    return {
        f"zone{i}": df[df["zone"] == i]["PowerOriginal"].mean()
        for i in range(1, 6)
    }


if __name__ == "__main__":

    df = read_my_csv()
    df = assign_zones(df)
    fig = make_plot(df)
    fig.show()

    #filter_data(df)
    how_much_time_is_spent_in_the_zones(df)
    #average_power_per_zone(df)