from agrivoltaics_supply_side_management.util.unit_conversion \
    import UnitConversion


class ElectricityGeneration:

    def __init__(self):
        # Default value. [W/m^2] Changes depending on specific module
        # It's for standard test condition (STD) of irradiance 1000[W/m^2],
        # 25[degree-C], and Air Mass 1.5
        self._module_mpp = 210

    def consume_light_power(self, irradiance):
        assert irradiance >= 0
        self._irradiance = irradiance

    def produce_electric_power(self):

        if self._irradiance <= 1000:
            # Simple way assuming that module power changes linear to
            # irradiance with 0 as intercept.
            # For accuracy, needs to refer to module's datasheet.
            return self._module_mpp * (self._irradiance / 1000)
        else:
            return self._module_mpp

    def produce_electric_energy(self, duration_in_sec):

        return UnitConversion.j_to_wh(
                            self.produce_electric_power() * duration_in_sec)
