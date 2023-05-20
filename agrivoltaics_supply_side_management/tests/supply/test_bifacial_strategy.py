import pytest
from datetime import datetime
from zoneinfo import ZoneInfo
import pandas as pd

from agrivoltaics_supply_side_management.agriculture.crops import Cultivation
from agrivoltaics_supply_side_management.optimization.convex_optimization\
    import ConvexOptimization
from agrivoltaics_supply_side_management.photovoltaics.pv_modules \
    import BifacialElectricityGeneration
from agrivoltaics_supply_side_management.solar_irradiation.irradiance \
    import BifacialIrradianceManager
from agrivoltaics_supply_side_management.supply.bifacial_strategy import \
    BifacialMiddaySupplyStrategy, BifacialMiddayDepressionSupplyStrategy
from agrivoltaics_supply_side_management.supply.strategy_factory\
    import BifacialIrradiationShiftingStrategyFactory


class TestBifacialSupplyStrategy:

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
    def bifaciality(self):
        return 0.75

    @pytest.fixture()
    def irradiance_manager(self, location_data, timezone, time_range,
                           surface_params, bifaciality):
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

        return BifacialIrradianceManager(
            lattitude, longitude, timezone, time_range,
            surface_azimuth, surface_tilt, axis_azimuth, gcr,
            pvrow_height, pvrow_width, albedo, n_pvrows, index_observed_pvrow,
            bifaciality)

    @pytest.fixture()
    def optimization(self):
        return ConvexOptimization()

    @pytest.fixture()
    def electricity_generation(self, location_data, timezone, time_range,
                               surface_params, irradiance_manager,
                               bifaciality):
        lattitude, longitude = location_data[0], location_data[1]

        surface_azimuth, surface_tilt = surface_params[0], surface_params[1]

        temp_model_parameters_type = 'open_rack_glass_glass'
        module_name = 'Trina_Solar_TSM_300DEG5C_07_II_'
        inverter_name = 'ABB__MICRO_0_25_I_OUTD_US_208__208V_'

        return BifacialElectricityGeneration(lattitude, longitude, timezone,
                                    irradiance_manager.bifacial_irradiances,
                                    temp_model_parameters_type,
                                    module_name, inverter_name,
                                    surface_tilt, surface_azimuth,
                                    bifaciality)

    @pytest.fixture()
    def cultivation(self):
        harvest_index = 0.95
        biomass_energy_ratio = 30
        leaf_area_index = 5
        crop_growth_regulating_factor = 0.95
        return Cultivation(harvest_index, biomass_energy_ratio,
                           leaf_area_index, crop_growth_regulating_factor)

    def test_supply_over_one_day(self, irradiance_manager, optimization,
                                 electricity_generation, cultivation,
                                 time_range):
        supply_strategy_factory = BifacialIrradiationShiftingStrategyFactory()

        duration_in_sec = pd.to_timedelta(time_range.freq).total_seconds()

        total_electricity_supply = 0
        total_crop_yield = 0

        for time in time_range:
            supply_strategy = supply_strategy_factory.get_supply_strategy(
                irradiance_manager, optimization,
                electricity_generation, cultivation, time)
            electricity_supply, crop_yield = supply_strategy.supply(
                                                    time, duration_in_sec)
            total_electricity_supply += electricity_supply
            total_crop_yield += crop_yield

        # total_electricity_supply was 2035.402261259535[Wh], which is
        # much bigger than 1242.6796249192898[Wh/day]
        # by IrradiationShiftingStrategyFactory
        assert total_electricity_supply == pytest.approx(2035, abs=1)
        # total_crop_yield was 0.0019817513464064403, which has reasonable
        # value, since
        # 0.0019817513464064403[(kg/m^2)/day] * 120 * 10000 / 1000
        # = 2.378101615687728[(ton/ha)/year]
        assert total_crop_yield == pytest.approx(0.0019, abs=1e-4)


    class TestBifacialMiddaySupplyStrategy:

        def test_supply(self, irradiance_manager, optimization,
                        electricity_generation, cultivation, timezone):
            supply_strategy = BifacialMiddaySupplyStrategy(
                irradiance_manager, optimization,
                electricity_generation, cultivation)

            date_time = datetime(2022, 7, 6, 12, 0, 0,
                                 tzinfo=ZoneInfo(timezone))
            duration_in_sec = 60  # 1[min]

            electricity_supply, crop_yield = supply_strategy.supply(
                                                date_time, duration_in_sec)

            assert electricity_supply == pytest.approx(268 * duration_in_sec,
                                                       1)
            # crop_yield was 3.903778248443417e-06, which may be a little
            # smaller but OK, since:
            # 3.903778248443417e-06[(kg/m^2)/min] * 60 * 5 * 120 * 10000
            #     / 1000
            # = 1.40536016943963[(ton/ha)/year]
            # Note: Peak solar hours of 5 is used in the calculation above.
            assert crop_yield == pytest.approx(3.9e-6, abs=1e-7)


    class TestBifacialMiddayDepressionSupplyStrategy:

        def test_supply(self, irradiance_manager, optimization,
                        electricity_generation, cultivation, timezone):
            supply_strategy = BifacialMiddayDepressionSupplyStrategy(
                irradiance_manager, optimization,
                electricity_generation, cultivation)

            date_time = datetime(2022, 7, 6, 12, 0, 0,
                                 tzinfo=ZoneInfo(timezone))
            duration_in_sec = 60  # 1[min]

            electricity_supply, crop_yield = supply_strategy.supply(
                                                date_time, duration_in_sec)

            assert electricity_supply == pytest.approx(268 * duration_in_sec,
                                                       1)
            # Should be half of that from MiddaySupplyStrategy:
            assert crop_yield == pytest.approx(1.9e-6, abs=1e-7)
