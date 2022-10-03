
from agrivoltaics_supply_side_management.agriculture.photosynthesis\
    import Photosynthesis
from agrivoltaics_supply_side_management.util.unit_conversion \
    import UnitConversion


class Cultivation:

    def __init__(self, harvest_index, biomass_energy_ratio, leaf_area_index,
                 crop_growth_regulating_factor):
        self._harvest_index = harvest_index
        self._biomass_energy_ratio = biomass_energy_ratio
        self._leaf_area_index = leaf_area_index
        self._crop_growth_regulating_factor = crop_growth_regulating_factor

    def consume_light_power(self, irradiance):
        self._irradiance = irradiance

    def produce(self, duration_in_sec):

        irradiation = UnitConversion.j_to_wh(
            self._irradiance * duration_in_sec)
        photosynthetically_active_radiation = UnitConversion.wh_to_mj(
                                                    irradiation)

        photosynthesis = Photosynthesis()

        crop_yield_in_kg_per_ha = photosynthesis.crop_yield(
                self._harvest_index, self._biomass_energy_ratio,
                photosynthetically_active_radiation, self._leaf_area_index,
                self._crop_growth_regulating_factor)

        crop_yield = UnitConversion.ton_per_ha_to_kg_per_m2(
            crop_yield_in_kg_per_ha)

        return crop_yield

    @property
    def light_saturation_point(self):

        if ((hasattr(self, '_light_saturation_point')) and
                (self._light_saturation_point is not None)):
            return self._light_saturation_point
        else:
            # Default value based on [2] (See README).
            # Subclass for a specific crop defines a different
            # value, e.g. soybean
            return 250

    @light_saturation_point.setter
    def light_saturation_point(self, value):
        self._light_saturation_point = value

    def reduce_biomass_energy_ratio(self, reduction_ratio):
        self._biomass_energy_ratio *= reduction_ratio
