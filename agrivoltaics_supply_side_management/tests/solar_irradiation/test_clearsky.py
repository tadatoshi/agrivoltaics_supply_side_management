import pytest
import pandas as pd
import matplotlib.pyplot as plt
from agrivoltaics_supply_side_management.solar_irradiation.clearsky\
    import get_clearsky


class TestClearsky:

    def test_get_clearsky(self):

        lattitude, longitude = 49.26757152616243, -123.25266177347093
        timezone = 'Canada/Pacific'
        time_range = pd.date_range('2022-07-06', '2022-07-07', freq='1T',
                              tz=timezone)

        clearsky = get_clearsky(lattitude, longitude, timezone, time_range)

        assert type(clearsky) is pd.DataFrame

        # print("type(clearsky)", type(clearsky))
        # print("clearsky", clearsky)
        # clearsky.plot()
