import pytest
import pandas as pd
import serial
from temp_log import parse_data, write_data


@pytest.fixture
def serial_dev():
    ser = serial.serial_for_url("loop://", timeout=0)
    def _serial_dev(timeout=None):
        ser.timeout = timeout
        return ser
    yield _serial_dev
    ser.close()


def test_write_data_clears_df():
    df = pd.DataFrame(
        columns=["deg_c_chip", "deg_c_rod", "time"]
    )
    data = parse_data(b"23.0,52.1")
    df = df.append(data, ignore_index=True)
    print(df)
    write_data("mu", df)
    print(df)
    assert False


class TestLogData:
    def test_demo(self, serial_dev):
        ser = serial_dev()
        print(f"{ser=}")
        print(f"{ser.port=}")
        ser.write(b"23.0,22.9\n")
        print(f"{ser.is_open=}")
        log = LogData()
        log.device = ser
        log.run()
        assert False
