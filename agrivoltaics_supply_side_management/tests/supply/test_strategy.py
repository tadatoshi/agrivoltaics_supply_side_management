import pytest
from datetime import datetime
from zoneinfo import ZoneInfo
import pandas as pd

from agrivoltaics_supply_side_management.agriculture.crops import Cultivation
from agrivoltaics_supply_side_management.optimization.convex_optimization \
    import ConvexOptimization
from agrivoltaics_supply_side_management.photovoltaics.pv_modules \
    import ElectricityGeneration
from agrivoltaics_supply_side_management.solar_irradiation.irradiance \
    import IrradianceManager
from agrivoltaics_supply_side_management.supply.strategy import \
    MiddaySupplyStrategy, MiddayDepressionSupplyStrategy
from agrivoltaics_supply_side_management.supply.strategy_factory\
    import IrradiationShiftingStrategyFactory


class TestSupplyStrategy:

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

    def test_supply_over_one_day(self, irradiance_manager, optimization,
                                 electricity_generation, cultivation,
                                 time_range):
        supply_strategy_factory = IrradiationShiftingStrategyFactory()

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

        # (Note: Result was 159773.09463248006[J] previously when
        #        ElectricityGeneration.produce_electric_power was used.):
        # total_electricity_supply was 1242.6796249192898[Wh], which has
        # reasonable value [Wh/day].
        assert total_electricity_supply == pytest.approx(1242, abs=1)
        # total_crop_yield was 0.0019244353818448326, which has reasonable
        # value, since
        # 0.0019244353818448326[(kg/m^2)/day] * 120 * 10000 / 1000
        # = 2.309322458213799[(ton/ha)/year]
        assert total_crop_yield == pytest.approx(0.002, abs=1e-4)

    class TestMiddaySupplyStrategy:

        def test_supply(self, irradiance_manager, optimization,
                        electricity_generation, cultivation, timezone):
            supply_strategy = MiddaySupplyStrategy(
                irradiance_manager, optimization,
                electricity_generation, cultivation)

            date_time = datetime(2022, 7, 6, 12, 0, 0,
                                 tzinfo=ZoneInfo(timezone))
            duration_in_sec = 60  # 1[min]

            electricity_supply, crop_yield = supply_strategy.supply(
                                                date_time, duration_in_sec)

            assert electricity_supply == pytest.approx(268 * duration_in_sec,
                                                       1)
            # crop_yield was 3.903778248443419e-06, which may be a little big
            # but OK, since it gives the same order of magnitude in
            # [(ton/ha)/year]:
            # 3.903778248443419e-06[(kg/m^2)/min] * 60 * 5 * 120 * 10000
            #     / 1000
            # = 6.745728813310228[(ton/ha)/year]
            # Note: Peak solar hours of 5 is used in the calculation above.
            assert crop_yield == pytest.approx(4e-6, abs=1e-7)

    class TestMiddayDepressionSupplyStrategy:

        def test_supply(self, irradiance_manager, optimization,
                        electricity_generation, cultivation, timezone):
            supply_strategy = MiddayDepressionSupplyStrategy(
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
            assert crop_yield == pytest.approx(2e-6, abs=1e-7)
