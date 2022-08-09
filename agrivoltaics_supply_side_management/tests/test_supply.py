import pytest
from datetime import datetime
from zoneinfo import ZoneInfo

from agrivoltaics_supply_side_management.supply import SupplyStrategy, \
    MorningSupplyStrategy, MiddaySupplyStrategy, AfternoonSupplyStrategy, \
    DefaultSupplyStrategy


class TestSupply:

    def test_create(self):
        timezone = 'Canada/Pacific'

        early_morning = datetime(2022, 8, 8, 6, 0, 0,
                                 tzinfo=ZoneInfo(timezone))
        supply_strategy_1 = SupplyStrategy.create(early_morning)
        assert type(supply_strategy_1) is DefaultSupplyStrategy

        morning = datetime(2022, 8, 8, 9, 30, 0,
                           tzinfo=ZoneInfo(timezone))
        supply_strategy_2 = SupplyStrategy.create(morning)
        assert type(supply_strategy_2) is MorningSupplyStrategy

        midday = datetime(2022, 8, 8, 12, 0, 0,
                          tzinfo=ZoneInfo(timezone))
        supply_strategy_3 = SupplyStrategy.create(midday)
        assert type(supply_strategy_3) is MiddaySupplyStrategy

        afternoon = datetime(2022, 8, 8, 17, 0, 0,
                             tzinfo=ZoneInfo(timezone))
        supply_strategy_4 = SupplyStrategy.create(afternoon)
        assert type(supply_strategy_4) is AfternoonSupplyStrategy

        evening = datetime(2022, 8, 8, 19, 0, 0,
                           tzinfo=ZoneInfo(timezone))
        supply_strategy_5 = SupplyStrategy.create(evening)
        assert type(supply_strategy_5) is DefaultSupplyStrategy
