import pytest
from hypothesis import given, strategies as st

from agrivoltaics_supply_side_management.agriculture.unit_conversion import UnitConversion


class TestUnitConversion:

    @given(par=st.floats(max_value=2000.0, min_value=0.0))
    def test_par_to_irradiance(self, par):

        irradiance = UnitConversion.par_to_irradiance(par)

        assert irradiance >= 0.0
        assert irradiance <= 500
