import pytest
import numpy as np
import pandas as pd

from agrivoltaics_supply_side_management.agriculture.crops import Cultivation
from agrivoltaics_supply_side_management.configuration import VerticalPvConfiguration
from agrivoltaics_supply_side_management.optimization.convex_optimization import ConvexOptimization
from agrivoltaics_supply_side_management.photovoltaics.pv_modules import ElectricityGeneration
from agrivoltaics_supply_side_management.solar_irradiation.irradiance import IrradianceManager


class TestVerticalPvConfiguration:

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
        duration_in_sec = 60 # 1[min]
        return Cultivation(harvest_index, biomass_energy_ratio, leaf_area_index, crop_growth_regulating_factor)

    @pytest.mark.parametrize(
        "phi, alpha, theta, p_max",
        [
            (0.055, 0.2, 0.96, 15)
        ]
    )
    def test_supply(self, phi, alpha, theta, p_max,
                    irradiance_manager, optimization, electricity_generation,
                    cultivation, time_range):

        net_photosynthetic_rate_parameters = {
            "phi": phi,
            "alpha": alpha,
            "theta": theta,
            "p_max": p_max
        }

        ppfd_data = np.linspace(0, 1200)

        configuration = VerticalPvConfiguration(
            net_photosynthetic_rate_parameters, ppfd_data,
            irradiance_manager, optimization, electricity_generation,
            cultivation)

        electricity_supply, crop_yield = configuration.supply(time_range)

        # TODO: Assert with actual value
        #       (Note: Result was 65816.26368455126):
        assert electricity_supply > 0
        # crop_yield was 0.0025746571495983022, which has reasonable
        # value, since
        # 0.0025746571495983022[(kg/m^2)/day] * 120 * 10000 / 1000
        # = 3.089588579517963[(ton/ha)/year]
        assert crop_yield == pytest.approx(0.002, abs=1e-3)
