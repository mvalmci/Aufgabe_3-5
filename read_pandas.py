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

 
def filter_data(df):
    df["zone1"] = df["HeartRate"] < 100
    df["zone2"] = (df["HeartRate"] >= 100) & (df["HeartRate"] < 150)
    df["zone3"] = (df["HeartRate"] >= 150) & (df["HeartRate"] < 200)
    df["zone4"] = df["HeartRate"] >= 200


def assign_zones(df):
    # Zone-Spalte (1-4) erstellen
    df["zone"] = np.select(
        [
            df["HeartRate"] < 100,
            (df["HeartRate"] >= 100) & (df["HeartRate"] < 150),
            (df["HeartRate"] >= 150) & (df["HeartRate"] < 200),
            df["HeartRate"] >= 200
        ],
        [1, 2, 3, 4],
        default=0
    )
    return df

def make_plot(df):
    # HeartRate farblich nach Zonen
    fig1 = px.scatter(
        df, x="Time", y="HeartRate", color="zone",
        color_discrete_map={1:'blue', 2:'green', 3:'orange', 4:'red'},
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

def how_much_time_is_spent_in_the_zones(df):
    # Falls filter_data das DataFrame verändert, das Ergebnis zuweisen!
    # df = filter_data(df)
    
    total = len(df)
    time_in_zone_1 = df["zone1"].sum() / total
    time_in_zone_2 = df["zone2"].sum() / total
    time_in_zone_3 = df["zone3"].sum() / total
    time_in_zone_4 = df["zone4"].sum() / total

    print(f"Time in zone 1: {time_in_zone_1:.2%}")
    print(f"Time in zone 2: {time_in_zone_2:.2%}")
    print(f"Time in zone 3: {time_in_zone_3:.2%}")
    print(f"Time in zone 4: {time_in_zone_4:.2%}")

def print_average_power_per_zone(df):
    df["zone1_power"] = df["PowerOriginal"][df["zone1"]].mean()
    df["zone2_power"] = df["PowerOriginal"][df["zone2"]].mean()
    df["zone3_power"] = df["PowerOriginal"][df["zone3"]].mean()
    df["zone4_power"] = df["PowerOriginal"][df["zone4"]].mean()

    print(f"Average power in zone 1: {df['zone1_power'].iloc[0]:.2f} W")
    print(f"Average power in zone 2: {df['zone2_power'].iloc[0]:.2f} W")
    print(f"Average power in zone 3: {df['zone3_power'].iloc[0]:.2f} W")
    print(f"Average power in zone 4: {df['zone4_power'].iloc[0]:.2f} W")





if __name__ == "__main__":

    df = read_my_csv()
    df = assign_zones(df)
    fig = make_plot(df)
    fig.show()

    filter_data(df)
    how_much_time_is_spent_in_the_zones(df)
    print_average_power_per_zone(df)