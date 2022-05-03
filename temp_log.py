#!/usr/bin/env python
from datetime import datetime
import pandas as pd
import serial


def parse_data(data):
    """
    Parse and timestamp data.
    Designed to be a helper function for log_data. It
    strips input and splits it into the separate
    temperature readings. Returning a dictionary with
    the data.
    """
    data = data.strip().split(b",")
    temp_chip, temp_rod = [float(x) for x in data]
    tmp = {
        "deg_c_chip": temp_chip,
        "deg_c_rod": temp_rod,
        "time": datetime.now(),
    }
    return tmp


def write_data(f_name, df):
    """
    Write data from log_data to file.
    Clears dataframe df to avoid duplicates.
    """
    df.to_csv(f_name, mode="w", header=False, index=False)
    return df.iloc[0:0]


def log_data(port="/dev/ttyACM0", baud=9600, w_threshold=100):
    """
    Log temperature readings from arduino board.
    Writes readings to disk after w_threshold readings.
    port: Which port the arduino is connected to.
    baud:
    w_threshold: Number of readings before a write to disk.
    """
    f_name = f"csv/{datetime.now()}.csv"
    df = pd.DataFrame(
        columns=["deg_c_chip", "deg_c_rod", "time"]
    )
    with serial.Serial(port, baud, timeout=11) as ser:
        ser.reset_input_buffer()
        try:
            while True:
                data = parse_data(ser.readline())
                df = df.append(data, ignore_index=True)
                if df.index.size == w_threshold:
                    df = write_data(f_name, df)
        except KeyboardInterrupt:
            write_data(f_name, df)
            print("Logging done, exiting.")


if __name__ == "__main__":
    log_data()
