from agrivoltaics_supply_side_management.photovoltaics.pv_modules\
    import ElectricityGeneration


class TestElectricityGeneration:

    def test_produce_electric_power(self):

        irradiance = 1000

        electricity_generation = ElectricityGeneration()
        electricity_generation.consume_light_power(irradiance)
        actual_power = electricity_generation.produce_electric_power()

        # TODO: Modify ElectricityGeneration not to use default value:
        expected_power = 210

        assert actual_power == expected_power

    def test_produce_electric_energy(self):

        irradiance = 1000
        duration_in_sec = 60

        electricity_generation = ElectricityGeneration()
        electricity_generation.consume_light_power(irradiance)
        actual_energy = electricity_generation.produce_electric_energy(
                                                            duration_in_sec)

        # TODO: Modify ElectricityGeneration not to use default value:
        # Dividing by (60 * 60) to get value in Wh:
        expected_energy = 210 * duration_in_sec / (60 * 60)

        assert actual_energy == expected_energy
