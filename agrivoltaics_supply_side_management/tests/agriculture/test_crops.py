from hypothesis import given
from hypothesis.strategies import floats, just, sampled_from

from agrivoltaics_supply_side_management.agriculture.crops import Cultivation
from agrivoltaics_supply_side_management.util.unit_conversion\
    import UnitConversion


class TestCultivation:

    @given(floats(0.25, 0.35), just(35), just(5), just(0.5),
           sampled_from((60, 60 * 15)))
    def test_produce(self, harvest_index,
        biomass_energy_ratio, leaf_area_index, crop_growth_regulating_factor,
        duration_in_sec):

        cultivation = Cultivation(harvest_index, biomass_energy_ratio,
                            leaf_area_index, crop_growth_regulating_factor)

        irradiance = 250 # Light saturation point from Figure 2 of [2]
        cultivation.consume_light_power(irradiance)

        actual_crop_yield = cultivation.produce(duration_in_sec)
        #print("actual_crop_yield: ", actual_crop_yield)

        # Anual crop yield 5[ton/ha] (Fig.10 of [1]),
        # 4 months of cultivation (30 days * 4)
        # 5 peak sun hour
        # (4 * (15 min))/hour
        assert actual_crop_yield <= (
                UnitConversion.ton_per_ha_to_kg_per_m2(5) / (30 * 4) / 5 / 4)
        assert actual_crop_yield >= 0
