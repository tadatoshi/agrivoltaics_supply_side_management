import pytest
from datetime import datetime
from zoneinfo import ZoneInfo
import pandas as pd

from agrivoltaics_supply_side_management.optimization.convex_optimization import ConvexOptimization
from agrivoltaics_supply_side_management.solar_irradiation.irradiance import IrradianceManager
from agrivoltaics_supply_side_management.supply import SupplyStrategy, \
    MorningSupplyStrategy, MiddaySupplyStrategy, AfternoonSupplyStrategy, \
    DefaultSupplyStrategy


class TestSupply:

    def test_get_supply_strategy(self):
        timezone = 'Canada/Pacific'

        early_morning = datetime(2022, 8, 8, 6, 0, 0,
                                 tzinfo=ZoneInfo(timezone))
        supply_strategy_1 = SupplyStrategy.get_supply_strategy(early_morning)
        assert type(supply_strategy_1) is DefaultSupplyStrategy

        morning = datetime(2022, 8, 8, 9, 30, 0,
                           tzinfo=ZoneInfo(timezone))
        supply_strategy_2 = SupplyStrategy.get_supply_strategy(morning)
        assert type(supply_strategy_2) is MorningSupplyStrategy

        midday = datetime(2022, 8, 8, 12, 0, 0,
                          tzinfo=ZoneInfo(timezone))
        supply_strategy_3 = SupplyStrategy.get_supply_strategy(midday)
        assert type(supply_strategy_3) is MiddaySupplyStrategy

        afternoon = datetime(2022, 8, 8, 17, 0, 0,
                             tzinfo=ZoneInfo(timezone))
        supply_strategy_4 = SupplyStrategy.get_supply_strategy(afternoon)
        assert type(supply_strategy_4) is AfternoonSupplyStrategy

        evening = datetime(2022, 8, 8, 19, 0, 0,
                           tzinfo=ZoneInfo(timezone))
        supply_strategy_5 = SupplyStrategy.get_supply_strategy(evening)
        assert type(supply_strategy_5) is DefaultSupplyStrategy

    class TestMiddaySupplyStrategy:

        def test_supply(self):
            lattitude, longitude = 49.26757152616243, -123.25266177347093
            timezone = 'Canada/Pacific'
            times = pd.date_range('2022-07-06', '2022-07-07', freq='1T',
                                  tz=timezone)

            irradiance_manager = IrradianceManager(lattitude, longitude,
                                                   timezone, times)
            optimization = ConvexOptimization()

            supply_strategy = MiddaySupplyStrategy()
            supply_strategy.irradiance_manager = irradiance_manager
            supply_strategy.optimization = optimization

            date_time = datetime(2022, 8, 11, 12, 0, 0)

            electricity_supply = supply_strategy.supply(date_time)

            assert electricity_supply == 337.5
