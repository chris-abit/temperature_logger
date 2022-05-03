#!/usr/bin/env python
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import click


def plot_dataframe(df):
    """ Plot temperature readings over time. """
    plt.plot(
        df["time"], df[["temp_chip", "temp_rod"]],
        label=["chip", "rod"]
    )
    plt.title("Temperature readings degrees Celsius")
    plt.legend()
    plt.show()


def read_data(fname):
    """
    Read temperature readings from file.
    Assumes no header is present and data is in the format:
    temp_C_chip, temp_C_rod, timestamp.
    """
    df = pd.read_csv(fname, header=None)
    df.rename({0: "temp_chip", 1: "temp_rod", 2: "time"}, inplace=True, axis=1)
    df["time"] = pd.to_datetime(df["time"])
    return df


@click.command()
@click.option("-f", "--file", "fname", default=None, help="Filename")
@click.option(
    "-a", "--all", "all_", is_flag=True, default=False,
    help="Plot all data collected."
)
def plot_readings(fname, all_):
    """
    Plot temperature readings over time.
    Will either use a spesific file given by fname or all files
    located in the csv/ folder.
    """
    path = Path(".")
    csvs = path.glob("csv/*.csv")
    df = pd.DataFrame(
        columns=["temp_chip", "temp_rod", "time"]
    )
    if all_:
        for csv in csvs:
            df = df.append(read_data(csv))
    elif fname:
        df = read_data(fname)
    else:
        raise ValueError("Invalid arguments.")
    plot_dataframe(df)


if __name__ == "__main__":
    plot_readings()
