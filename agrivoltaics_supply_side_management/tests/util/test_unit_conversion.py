from hypothesis import given, strategies as st

from agrivoltaics_supply_side_management.util.unit_conversion\
    import UnitConversion


class TestUnitConversion:

    @given(par=st.floats(max_value=2000.0, min_value=0.0))
    def test_par_to_irradiance(self, par):

        irradiance = UnitConversion.par_to_irradiance(par)

        assert irradiance >= 0.0
        assert irradiance <= 500

    def test_wh_to_mj(self):
        energy_in_wh = 5000

        expected_energy_in_mj = 18

        actual_energy_in_mj = UnitConversion.wh_to_mj(energy_in_wh)

        assert actual_energy_in_mj == expected_energy_in_mj

    def test_j_to_wh(self):
        # 1000[W] * 60[sec]
        # i.e. energy for duration of 1 min for average power = 1000[W]
        energy_in_j = 1000 * 60

        expected_energy_in_wh = 1000 / 60

        actual_energy_in_wh = UnitConversion.j_to_wh(energy_in_j)

        assert actual_energy_in_wh == expected_energy_in_wh
