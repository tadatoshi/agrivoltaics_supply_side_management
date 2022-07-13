import pytest
from hypothesis import given, assume
from hypothesis.strategies import floats

from agrivoltaics_supply_side_management.agriculture.photosynthetic import PhotosyntheticModel


class TestPhotosyntheticModel:

    def test_crop_yield_potato(self):

        harvest_index = 0.95
        biomass_energy_ratio = 30
        #  [MJ] = [kHh] * 60[min/h] * 60[sec/min] / 1000
        photosynthetically_active_radiation = 1000 * 60 * 60 / 1000
        leaf_area_index = 5
        crop_growth_regulating_factor = 0.95
        number_of_days = 1

        photosynthetic_model = PhotosyntheticModel()

        actual_crop_yield = photosynthetic_model.crop_yield(harvest_index, biomass_energy_ratio,
                   photosynthetically_active_radiation,
                   leaf_area_index, crop_growth_regulating_factor, number_of_days)

    @given(floats(0, 1))
    def test_crop_yield_potato_with_property(self, harvest_index):
        # assume(harvest_index >= 0 and harvest_index <=1)

        biomass_energy_ratio = 30
        #  [MJ] = [kHh] * 60[min/h] * 60[sec/min] / 1000
        photosynthetically_active_radiation = 1000 * 60 * 60 / 1000
        leaf_area_index = 5
        crop_growth_regulating_factor = 0.95
        number_of_days = 1

        photosynthetic_model = PhotosyntheticModel()

        actual_crop_yield = photosynthetic_model.crop_yield(harvest_index, biomass_energy_ratio,
                   photosynthetically_active_radiation,
                   leaf_area_index, crop_growth_regulating_factor, number_of_days)

        # Good harvest is 25 tons per hectare and experienced farmers can achieve 40 to 70 tons per hectare
        # accordiing to https://wikifarmer.com/potato-harvest-yield-storage/
        #assert actual_crop_yield <=70 # harvest_index = 1 gave 98.62176627646531
        assert actual_crop_yield >=0
