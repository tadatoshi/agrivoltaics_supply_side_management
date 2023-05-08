import pytest
import numpy as np
import pandas as pd
from agrivoltaics_supply_side_management.photovoltaics.pv_modules\
    import ElectricityGeneration, BifacialElectricityGeneration


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


class TestBifacialElectricityGeneration:

    @pytest.fixture()
    def time_index(self):
        times = pd.date_range('2022-07-06', '2022-07-07', freq='1T',
                              tz='Canada/Pacific')
        return times[700:704]

    @pytest.fixture()
    def bifacial_irradiances(self, time_index):
        data = {'total_inc_front': [903.2, 904.8, 906.4, 907.9],
                'total_inc_back': [34.3, 34.4, 34.4, 34.4],
                'total_abs_front': [876.1, 877.7, 879.2, 880.7],
                'total_abs_back': [32.6, 32.6, 32.7, 32.7],
                'effective_irradiance': [900.7, 902.2, 903.7, 905.2]}
        bifacial_irradiances = pd.DataFrame(data, index=time_index)
        return bifacial_irradiances

    @pytest.mark.parametrize(
        "temp_model_parameters_type, module_name, inverter_name",
        [
            ('open_rack_glass_glass', 'Trina_Solar_TSM_300DEG5C_07_II_',
             'ABB__MICRO_0_25_I_OUTD_US_208__208V_')
        ]
    )
    def test_produce_electric_power(self, time_index, bifacial_irradiances,
                                    temp_model_parameters_type,
                                    module_name, inverter_name):
        lattitude, longitude = 49.26757152616243, -123.25266177347093
        timezone = 'Canada/Pacific'
        surface_tilt = 20
        surface_azimuth = 180

        bifacial_electricity_generation = BifacialElectricityGeneration(
                                    lattitude, longitude, timezone,
                                    bifacial_irradiances,
                                    temp_model_parameters_type,
                                    module_name, inverter_name,
                                    surface_tilt, surface_azimuth)

        bifacial_electricity_generation.consume_light_power(
            date_time=time_index[0])
        actual_power =\
            bifacial_electricity_generation.produce_electric_power()

        assert np.isclose(actual_power, 235, rtol=1)

    @pytest.mark.parametrize(
        "temp_model_parameters_type, module_name, inverter_name",
        [
            ('open_rack_glass_glass', 'Trina_Solar_TSM_300DEG5C_07_II_',
             'ABB__MICRO_0_25_I_OUTD_US_208__208V_')
        ]
    )
    def test_produce_electric_energy(self, time_index, bifacial_irradiances,
                                     temp_model_parameters_type,
                                     module_name, inverter_name):
        lattitude, longitude = 49.26757152616243, -123.25266177347093
        timezone = 'Canada/Pacific'
        surface_tilt = 20
        surface_azimuth = 180

        duration_in_sec = 60

        bifacial_electricity_generation = BifacialElectricityGeneration(
                                    lattitude, longitude, timezone,
                                    bifacial_irradiances,
                                    temp_model_parameters_type,
                                    module_name, inverter_name,
                                    surface_tilt, surface_azimuth)

        bifacial_electricity_generation.consume_light_power(
            date_time=time_index[0])
        actual_energy =\
            bifacial_electricity_generation.produce_electric_energy(
                duration_in_sec)

        assert np.isclose(actual_energy, 235 * duration_in_sec / (60 * 60),
                          rtol=1)
