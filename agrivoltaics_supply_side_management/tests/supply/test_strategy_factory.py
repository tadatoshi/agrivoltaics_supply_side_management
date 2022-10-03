import pytest
from datetime import datetime
from zoneinfo import ZoneInfo
import pandas as pd

from agrivoltaics_supply_side_management.agriculture.crops import Cultivation
from agrivoltaics_supply_side_management.optimization.convex_optimization\
    import ConvexOptimization
from agrivoltaics_supply_side_management.photovoltaics.pv_modules\
    import ElectricityGeneration
from agrivoltaics_supply_side_management.solar_irradiation.irradiance\
    import IrradianceManager
from agrivoltaics_supply_side_management.supply.strategy \
    import DefaultSupplyStrategy, MorningSupplyStrategy, \
    MiddaySupplyStrategy, AfternoonSupplyStrategy,\
    MiddayDepressionSupplyStrategy
from agrivoltaics_supply_side_management.supply.strategy_factory \
    import IrradiationShiftingStrategyFactory, DefaultStrategyFactory


class TestStrategyFactory:

    @pytest.fixture()
    def location_data(self):
        lattitude, longitude = 49.26757152616243, -123.25266177347093
        return lattitude, longitude

    @pytest.fixture()
    def timezone(self):
        return 'Canada/Pacific'

    @pytest.fixture()
    def time_range(self, timezone):
        return pd.date_range('2022-07-06', '2022-07-07', freq='1T',
                             tz=timezone)

    @pytest.fixture()
    def irradiance_manager(self, location_data, timezone, time_range):
        lattitude, longitude = location_data[0], location_data[1]
        return IrradianceManager(lattitude, longitude, timezone, time_range)

    @pytest.fixture()
    def optimization(self):
        return ConvexOptimization()

    @pytest.fixture()
    def electricity_generation(self):
        return ElectricityGeneration()

    @pytest.fixture()
    def cultivation(self):
        harvest_index = 0.95
        biomass_energy_ratio = 30
        leaf_area_index = 5
        crop_growth_regulating_factor = 0.95
        return Cultivation(harvest_index, biomass_energy_ratio,
                           leaf_area_index, crop_growth_regulating_factor)

    class TestIrradiationShiftingStrategyFactory:

        def test_get_supply_strategy(irradiance_manager, optimization,
                                     electricity_generation, cultivation,
                                     timezone):

            supply_strategy_factory = IrradiationShiftingStrategyFactory()

            early_morning = datetime(2022, 8, 8, 6, 0, 0,
                                     tzinfo=ZoneInfo(timezone))
            supply_strategy_1 = supply_strategy_factory.get_supply_strategy(
                irradiance_manager, optimization, electricity_generation,
                cultivation, early_morning)
            assert type(supply_strategy_1) is DefaultSupplyStrategy

            morning = datetime(2022, 8, 8, 9, 30, 0,
                               tzinfo=ZoneInfo(timezone))
            supply_strategy_2 = supply_strategy_factory.get_supply_strategy(
                irradiance_manager, optimization, electricity_generation,
                cultivation, morning)
            assert type(supply_strategy_2) is MorningSupplyStrategy

            midday = datetime(2022, 8, 8, 12, 0, 0,
                              tzinfo=ZoneInfo(timezone))
            supply_strategy_3 = supply_strategy_factory.get_supply_strategy(
                irradiance_manager, optimization, electricity_generation,
                cultivation, midday)
            assert type(supply_strategy_3) is MiddaySupplyStrategy

            afternoon = datetime(2022, 8, 8, 17, 0, 0,
                                 tzinfo=ZoneInfo(timezone))
            supply_strategy_4 = supply_strategy_factory.get_supply_strategy(
                irradiance_manager, optimization, electricity_generation,
                cultivation, afternoon)
            assert type(supply_strategy_4) is AfternoonSupplyStrategy

            evening = datetime(2022, 8, 8, 19, 0, 0,
                               tzinfo=ZoneInfo(timezone))
            supply_strategy_5 = supply_strategy_factory.get_supply_strategy(
                irradiance_manager, optimization, electricity_generation,
                cultivation, evening)
            assert type(supply_strategy_5) is DefaultSupplyStrategy

    class TestDefaultStrategyFactory:

        def test_get_supply_strategy(irradiance_manager, optimization,
                                     electricity_generation, cultivation,
                                     timezone):

            supply_strategy_factory = DefaultStrategyFactory()

            early_morning = datetime(2022, 8, 8, 6, 0, 0,
                                     tzinfo=ZoneInfo(timezone))
            supply_strategy_1 = supply_strategy_factory.get_supply_strategy(
                irradiance_manager, optimization, electricity_generation,
                cultivation, early_morning)
            assert type(supply_strategy_1) is DefaultSupplyStrategy

            morning = datetime(2022, 8, 8, 9, 30, 0,
                               tzinfo=ZoneInfo(timezone))
            supply_strategy_2 = supply_strategy_factory.get_supply_strategy(
                irradiance_manager, optimization, electricity_generation,
                cultivation, morning)
            assert type(supply_strategy_2) is DefaultSupplyStrategy

            midday = datetime(2022, 8, 8, 12, 0, 0,
                              tzinfo=ZoneInfo(timezone))
            supply_strategy_3 = supply_strategy_factory.get_supply_strategy(
                irradiance_manager, optimization, electricity_generation,
                cultivation, midday)
            assert type(supply_strategy_3) is MiddayDepressionSupplyStrategy

            afternoon = datetime(2022, 8, 8, 17, 0, 0,
                                 tzinfo=ZoneInfo(timezone))
            supply_strategy_4 = supply_strategy_factory.get_supply_strategy(
                irradiance_manager, optimization, electricity_generation,
                cultivation, afternoon)
            assert type(supply_strategy_4) is DefaultSupplyStrategy

            evening = datetime(2022, 8, 8, 19, 0, 0,
                               tzinfo=ZoneInfo(timezone))
            supply_strategy_5 = supply_strategy_factory.get_supply_strategy(
                irradiance_manager, optimization, electricity_generation,
                cultivation, evening)
            assert type(supply_strategy_5) is DefaultSupplyStrategy
