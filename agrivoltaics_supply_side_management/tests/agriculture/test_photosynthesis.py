import pytest
import pandas as pd
from hypothesis import given, assume
from hypothesis.strategies import floats

from agrivoltaics_supply_side_management.agriculture.photosynthesis\
    import Photosynthesis


class TestPhotosynthesis:

    @pytest.mark.parametrize(
        "harvest_index, biomass_energy_ratio, " + \
        "photosynthetically_active_radiation, " + \
        "leaf_area_index, crop_growth_regulating_factor, number_of_days, " + \
        "expected_crop_yield",
        [
            (0.95, 30, 5000 * 60 * 60 / 1000000, 5, 0.95, 4 * 30, 56)
        ]
    )
    def test_crop_yield_potato_with_default_parameters(self, harvest_index,
            biomass_energy_ratio, photosynthetically_active_radiation,
            leaf_area_index, crop_growth_regulating_factor, number_of_days,
            expected_crop_yield):
        """
        Using data from 'Table 3 Default parameters for potato' of
        [1] in README.
        TODO: biomass_energy_ratio has kg in unit and crop_yield has ton
        in unit. Thus, the units don't match. Investigate.

        Arguments
        ---------
        photosynthetically_active_radiation : float (will be changed to list)
            [MJ/m^2]
            Based on 5 peak sun hours
            with solar irradiance 1000[W/m^2] per day on a sunnay summer day
            and [MJ] = [Wh] * 60[min/h] * 60[sec/min] / 1000000
            1000[W/m^2] -> 5000[Wh/m^2] -> 18[MJ/m^2]
        number_of_days: integer
            4 momths between planting and harvesting
            with average 30 days / month
        expected_crop_yield: float [ton/ha]

        """

        # TODO: biomass_energy_ratio has kg in unit and crop_yield has ton
        #       in unit. Thus, the units don't match. Investigate.

        # harvest_index = 0.95
        # biomass_energy_ratio = 30
        # photosynthetically_active_radiation = 5000 * 60 * 60 / 1000000
        # leaf_area_index = 5
        # crop_growth_regulating_factor = 0.95
        # number_of_days = 4 * 30

        photosynthesis = Photosynthesis()

        actual_crop_yield = photosynthesis.crop_yield(
            harvest_index, biomass_energy_ratio,
            photosynthetically_active_radiation,
            leaf_area_index, crop_growth_regulating_factor, number_of_days)

        assert actual_crop_yield == pytest.approx(expected_crop_yield, 1)

    @given(floats(0.1, 1), floats(20, 40), floats(1, 10), floats(0.1, 1),
           floats(2.5 * 30, 6 * 30))
    def test_crop_yield_with_property(self, harvest_index,
                biomass_energy_ratio, leaf_area_index,
                crop_growth_regulating_factor, number_of_days):
        # assume(harvest_index >= 0 and harvest_index <=1)

        #  [MJ] = [Wh] * 60[min/h] * 60[sec/min] / 1000000
        photosynthetically_active_radiation = 5000 * 60 * 60 / 1000000

        photosynthesis = Photosynthesis()

        actual_crop_yield = photosynthesis.crop_yield(
            harvest_index, biomass_energy_ratio,
            photosynthetically_active_radiation,
            leaf_area_index, crop_growth_regulating_factor, number_of_days)

        # print("actual_crop_yield:", actual_crop_yield)

        # For pootatos, Good harvest is 25 tons per hectare and experienced
        # farmers can achieve 40 to 70 tons per hectare
        # per year with 2.5 to 4 momths between planting and harvesting
        # accordiing to https://wikifarmer.com/potato-harvest-yield-storage/
        assert actual_crop_yield <= 130
        assert actual_crop_yield >= 0
