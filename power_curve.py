import pandas as pd
import numpy as np
import plotly.io as pio
import plotly.express as px

pio.renderers.default = "browser"


def load_data(path="data/activities/activity.csv"):

    df = pd.read_csv(path)

    t_end = len(df)
    time = np.arange(0, t_end)
    df["Time/s"] = time

    return df

def find_best_effort(series, windows=[30, 60, 180, 300, 600, 1800, 2000]):
    
    best_efforts = {}
    
    for window in windows:
        max_average = series.rolling(window).mean()
        list_max_avg = max_average.max()
        best_efforts[window] = list_max_avg
    
    df2 = pd.DataFrame.from_dict(best_efforts, orient='index', columns=['Best Effort'])
    df2 = df2.reset_index().rename(columns={'index': 'Time/s'})

    return df2

def plot_power_curve(df2):
    figure = px.line(
        df2,
        x="Time/s",
        y="Best Effort",
        title="Powercurve",
        markers=True
    )




    
    figure.update_layout(
        xaxis_title="Zeit (s)",
        yaxis_title="Leistung (W)",
        legend_title_text="Best Effort",
        template="plotly_white"
    )
    figure.update_traces(mode='lines+markers')
    figure.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
    figure.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
    figure.update_layout(
        margin=dict(l=20, r=20, t=40, b=20),
        height=600,
        width=800
    )
    figure.update_layout(
        title_font=dict(size=24, color='black'),
        xaxis_title_font=dict(size=18, color='black'),
        yaxis_title_font=dict(size=18, color='black'),
        legend_font=dict(size=14, color='black')
    )
    figure.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    figure.update_layout(
        font=dict(family="Arial, sans-serif", size=14, color="black")
    )
    figure.update_layout(
        hovermode="x unified",
        hoverlabel=dict(bgcolor="white", font_size=14, font_family="Arial")
    )
    figure.update_traces(
        hovertemplate="<b>Time/s:</b> %{x}<br><b>Best Effort:</b> %{y:.2f} W"
    )
    figure.update_layout(
        shapes=[
            dict(
                type="line",
                x0=0, x1=df2["Time/s"].max(),
                y0=0, y1=0,
                line=dict(color="black", width=1, dash="dash")
            )
        ]
    )
    figure.update_layout(
        annotations=[
            dict(
                x=df2["Time/s"].max() * 0.95,
                y=0.05,
                xref="x",
                yref="paper",
                text="Best Effort",
                showarrow=False,
                font=dict(size=14, color="black")
            )
        ]
    )
    figure.update_layout(
        title={
            'text': "Powercurve",
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        }
    )
    figure.update_layout(
        xaxis=dict(
            showline=True,
            linewidth=1,
            linecolor='black',
            ticks='outside',
            tickwidth=1,
            tickcolor='black'
        ),
        yaxis=dict(
            showline=True,
            linewidth=1,
            linecolor='black',
            ticks='outside',
            tickwidth=1,
            tickcolor='black'
        )
    )
    figure.update_layout(
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    figure.update_layout(
        hovermode="closest",
        dragmode="zoom"
    )
    figure.update_layout(
        coloraxis_colorbar=dict(
            title="Best Effort",
            tickvals=df2["Best Effort"].unique(),
            ticktext=[f"{val:.2f} W" for val in df2["Best Effort"].unique()],
            lenmode="fraction",
            len=0.5,
            yanchor="top",
            y=1,
            xanchor="left",
            x=0.01
        )
    )

    return figure












if __name__ == "__main__":
    
    df = load_data()

    best_efforts = find_best_effort(df["PowerOriginal"])

    print(best_efforts)

    fig = plot_power_curve(best_efforts)
    pio.show(fig)