
from agrivoltaics_supply_side_management.agriculture.photosynthesis\
    import Photosynthesis
from agrivoltaics_supply_side_management.agriculture.unit_conversion\
    import UnitConversion


class Cultivation:

    def __init__(self, harvest_index, biomass_energy_ratio, leaf_area_index,
                 crop_growth_regulating_factor, duration_in_sec):
        self._harvest_index = harvest_index
        self._biomass_energy_ratio = biomass_energy_ratio
        self._leaf_area_index = leaf_area_index
        self._crop_growth_regulating_factor = crop_growth_regulating_factor
        self._duration_in_sec = duration_in_sec

    def consume_light_power(self, irradiance):
        self._irradiance = irradiance

    def produce(self):

        irradiation = UnitConversion.j_to_wh(
            self._irradiance * self._duration_in_sec)
        photosynthetically_active_radiation = UnitConversion.wh_to_mj(
                                                    irradiation)

        # TODO: Modify Photosynthesis.crop_yield to interprete the equation
        #       from
        #           sum of discrete values per day with
        #           daily photosynthetically_active_radiation
        #       to
        #           continuous value of photosynthetically_active_radiation
        if self._duration_in_sec <= 24 * 60 * 60:
            number_of_days = 1
        else:
            number_of_days = self._duration_in_sec / (24 * 60 * 60)

        photosynthesis = Photosynthesis()

        crop_yield_in_kg_per_ha = photosynthesis.crop_yield(
            self._harvest_index, self._biomass_energy_ratio,
            photosynthetically_active_radiation,
            self._leaf_area_index, self._crop_growth_regulating_factor,
            number_of_days)

        crop_yield = UnitConversion.ton_per_ha_to_kg_per_m2(
            crop_yield_in_kg_per_ha)

        return crop_yield

    def light_saturation_point(self):
        # Default value. Subclass for a specific crop defines a different
        # value, e.g. soybean
        return 250
