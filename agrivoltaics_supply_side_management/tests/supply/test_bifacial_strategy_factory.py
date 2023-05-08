import pytest
from datetime import datetime
from zoneinfo import ZoneInfo
import pandas as pd

from agrivoltaics_supply_side_management.agriculture.crops import Cultivation
from agrivoltaics_supply_side_management.photovoltaics.pv_modules\
    import BifacialElectricityGeneration
from agrivoltaics_supply_side_management.solar_irradiation.irradiance\
    import BifacialIrradianceManager
from agrivoltaics_supply_side_management.supply.bifacial_strategy \
    import DefaultBifacialSupplyStrategy, BifacialMorningSupplyStrategy, \
    BifacialMiddaySupplyStrategy, BifacialAfternoonSupplyStrategy,\
    BifacialMiddayDepressionSupplyStrategy
from agrivoltaics_supply_side_management.supply.strategy_factory \
    import BifacialIrradiationShiftingStrategyFactory, DefaultBifacialStrategyFactory


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
    def surface_params(self):
        surface_azimuth = 180
        surface_tilt = 20
        return surface_azimuth, surface_tilt

    @pytest.fixture()
    def irradiance_manager(self, location_data, timezone, time_range,
                           surface_params):
        lattitude, longitude = location_data[0], location_data[1]

        surface_azimuth, surface_tilt = surface_params[0], surface_params[1]
        axis_azimuth = 180
        pvrow_height = 1
        pvrow_width = 4
        pitch = 10
        gcr = pvrow_width / pitch
        albedo = 0.2
        n_pvrows = 3
        index_observed_pvrow = 1
        bifaciality = 0.75

        return BifacialIrradianceManager(
            lattitude, longitude, timezone, time_range,
            surface_azimuth, surface_tilt, axis_azimuth, gcr,
            pvrow_height, pvrow_width, albedo, n_pvrows, index_observed_pvrow,
            bifaciality)

    @pytest.fixture()
    def optimization(self):
        return None

    @pytest.fixture()
    def electricity_generation(self, location_data, timezone, time_range,
                               surface_params, irradiance_manager):
        lattitude, longitude = location_data[0], location_data[1]

        surface_azimuth, surface_tilt = surface_params[0], surface_params[1]

        temp_model_parameters_type = 'open_rack_glass_glass'
        module_name = 'Trina_Solar_TSM_300DEG5C_07_II_'
        inverter_name = 'ABB__MICRO_0_25_I_OUTD_US_208__208V_'

        return BifacialElectricityGeneration(lattitude, longitude, timezone,
                                    irradiance_manager.bifacial_irradiances,
                                    temp_model_parameters_type,
                                    module_name, inverter_name,
                                    surface_tilt, surface_azimuth)

    @pytest.fixture()
    def cultivation(self):
        harvest_index = 0.95
        biomass_energy_ratio = 30
        leaf_area_index = 5
        crop_growth_regulating_factor = 0.95
        return Cultivation(harvest_index, biomass_energy_ratio,
                           leaf_area_index, crop_growth_regulating_factor)

    class TestBifacialIrradiationShiftingStrategyFactory:

        def test_get_supply_strategy(irradiance_manager, optimization,
                                     electricity_generation, cultivation,
                                     timezone):

            supply_strategy_factory =\
                BifacialIrradiationShiftingStrategyFactory()

            early_morning = datetime(2022, 8, 8, 6, 0, 0,
                                     tzinfo=ZoneInfo(timezone))
            supply_strategy_1 = supply_strategy_factory.get_supply_strategy(
                irradiance_manager, optimization, electricity_generation,
                cultivation, early_morning)
            assert type(supply_strategy_1) is DefaultBifacialSupplyStrategy

            morning = datetime(2022, 8, 8, 9, 30, 0,
                               tzinfo=ZoneInfo(timezone))
            supply_strategy_2 = supply_strategy_factory.get_supply_strategy(
                irradiance_manager, optimization, electricity_generation,
                cultivation, morning)
            assert type(supply_strategy_2) is BifacialMorningSupplyStrategy

            midday = datetime(2022, 8, 8, 12, 0, 0,
                              tzinfo=ZoneInfo(timezone))
            supply_strategy_3 = supply_strategy_factory.get_supply_strategy(
                irradiance_manager, optimization, electricity_generation,
                cultivation, midday)
            assert type(supply_strategy_3) is BifacialMiddaySupplyStrategy

            afternoon = datetime(2022, 8, 8, 17, 0, 0,
                                 tzinfo=ZoneInfo(timezone))
            supply_strategy_4 = supply_strategy_factory.get_supply_strategy(
                irradiance_manager, optimization, electricity_generation,
                cultivation, afternoon)
            assert type(supply_strategy_4) is BifacialAfternoonSupplyStrategy

            evening = datetime(2022, 8, 8, 19, 0, 0,
                               tzinfo=ZoneInfo(timezone))
            supply_strategy_5 = supply_strategy_factory.get_supply_strategy(
                irradiance_manager, optimization, electricity_generation,
                cultivation, evening)
            assert type(supply_strategy_5) is DefaultBifacialSupplyStrategy

    class TestDefaultBifacialStrategyFactory:

        def test_get_supply_strategy(irradiance_manager, optimization,
                                     electricity_generation, cultivation,
                                     timezone):

            supply_strategy_factory = DefaultBifacialStrategyFactory()

            early_morning = datetime(2022, 8, 8, 6, 0, 0,
                                     tzinfo=ZoneInfo(timezone))
            supply_strategy_1 = supply_strategy_factory.get_supply_strategy(
                irradiance_manager, optimization, electricity_generation,
                cultivation, early_morning)
            assert type(supply_strategy_1) is DefaultBifacialSupplyStrategy

            morning = datetime(2022, 8, 8, 9, 30, 0,
                               tzinfo=ZoneInfo(timezone))
            supply_strategy_2 = supply_strategy_factory.get_supply_strategy(
                irradiance_manager, optimization, electricity_generation,
                cultivation, morning)
            assert type(supply_strategy_2) is DefaultBifacialSupplyStrategy

            midday = datetime(2022, 8, 8, 12, 0, 0,
                              tzinfo=ZoneInfo(timezone))
            supply_strategy_3 = supply_strategy_factory.get_supply_strategy(
                irradiance_manager, optimization, electricity_generation,
                cultivation, midday)
            assert type(supply_strategy_3
                        ) is BifacialMiddayDepressionSupplyStrategy

            afternoon = datetime(2022, 8, 8, 17, 0, 0,
                                 tzinfo=ZoneInfo(timezone))
            supply_strategy_4 = supply_strategy_factory.get_supply_strategy(
                irradiance_manager, optimization, electricity_generation,
                cultivation, afternoon)
            assert type(supply_strategy_4) is DefaultBifacialSupplyStrategy

            evening = datetime(2022, 8, 8, 19, 0, 0,
                               tzinfo=ZoneInfo(timezone))
            supply_strategy_5 = supply_strategy_factory.get_supply_strategy(
                irradiance_manager, optimization, electricity_generation,
                cultivation, evening)
            assert type(supply_strategy_5) is DefaultBifacialSupplyStrategy
