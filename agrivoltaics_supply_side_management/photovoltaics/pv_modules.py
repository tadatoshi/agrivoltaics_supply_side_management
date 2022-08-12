


class ElectricityGeneration:

    def __init__(self):
        # Default value. Changes depending on specific module
        # It's for standard test condition (STD) of irradiance 1000[W/m^2],
        # 25[degree-C], and Air Mass 1.5
        self._module_mpp = 450

    def consume_light_power(self, irradiance):
        assert irradiance >= 0
        self._irradiance = irradiance

    def produce_electric_power(self):

        if self._irradiance <= 1000:
            # Simple way assuming that module power changes linear to
            # irradiance with 0 as intercept.
            # It's true for current but not for voltage, which has
            # a different value as intercept.
            # For accuracy, needs to refer to module's datasheet.
            return 450 * (self._irradiance / 1000)
        else:
            return 450
