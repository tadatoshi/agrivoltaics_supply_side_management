import pytest
import numpy as np
import pandas as pd

from agrivoltaics_supply_side_management.solar_irradiation.irradiance\
    import BifacialIrradianceManager


class TestBifacialIrradianceManager:

    def test_get_bifacial_irradiances(self):

        lattitude, longitude = 49.26757152616243, -123.25266177347093
        timezone = 'Canada/Pacific'
        time_range = pd.date_range('2022-07-06', '2022-07-07', freq='1T',
                              tz=timezone)

        surface_azimuth = 180
        surface_tilt = 20
        axis_azimuth = 180
        pvrow_height = 1
        pvrow_width = 4
        pitch = 10
        gcr = pvrow_width / pitch
        albedo = 0.2
        n_pvrows = 3
        index_observed_pvrow = 1
        bifaciality = 0.75

        bifacial_irradiance_manager = BifacialIrradianceManager(
            lattitude, longitude, timezone, time_range,
            surface_azimuth, surface_tilt, axis_azimuth, gcr,
            pvrow_height, pvrow_width, albedo, n_pvrows, index_observed_pvrow,
            bifaciality)

        bifacial_irradiance_df =\
            bifacial_irradiance_manager._get_bifacial_irradiances(
                surface_azimuth, surface_tilt, axis_azimuth,
                albedo, gcr, pvrow_height, pvrow_width, n_pvrows,
                index_observed_pvrow, bifaciality)

        assert all(column in bifacial_irradiance_df.columns for column in
                                                  ['total_inc_front',
                                                   'total_inc_back',
                                                   'total_abs_front',
                                                   'total_abs_back',
                                                   'effective_irradiance'])

    def test_calculate_ground_absorbed_irrardiance(self):
        times = pd.date_range('2022-07-06', '2022-07-07', freq='1T',
                              tz='Canada/Pacific')
        index = times[700:704]
        data = {'total_inc_front': [903.2, 904.8, 906.4, 907.9],
                'total_inc_back': [34.3, 34.4, 34.4, 34.4],
                'total_abs_front': [876.1, 877.7, 879.2, 880.7],
                'total_abs_back': [32.6, 32.6, 32.7, 32.7],
                'effective_irradiance': [900.7, 902.2, 903.7, 905.2]}
        bifacial_irradiances = pd.DataFrame(data, index=index)

        lattitude, longitude = 49.26757152616243, -123.25266177347093
        timezone = 'Canada/Pacific'
        time_range = pd.date_range('2022-07-06', '2022-07-07', freq='1T',
                              tz=timezone)

        surface_azimuth = 180
        surface_tilt = 20
        axis_azimuth = 180
        pvrow_height = 1
        pvrow_width = 4
        pitch = 10
        gcr = pvrow_width / pitch
        albedo = 0.2
        n_pvrows = 3
        index_observed_pvrow = 1
        bifaciality = 0.75

        bifacial_irradiance_manager = BifacialIrradianceManager(
            lattitude, longitude, timezone, time_range,
            surface_azimuth, surface_tilt, axis_azimuth, gcr,
            pvrow_height, pvrow_width, albedo, n_pvrows, index_observed_pvrow,
            bifaciality)

        actual_ground_absorbed_irradiance =\
            bifacial_irradiance_manager._calculate_ground_absorbed_irrardiance(
                bifacial_irradiances, surface_tilt, albedo)

        assert all(column in actual_ground_absorbed_irradiance.columns for column in
                                                  ['ground_absorbed_irradiance'])
        assert actual_ground_absorbed_irradiance.iloc[0][
            'ground_absorbed_irradiance'] == bifacial_irradiances.iloc[0][
                'total_inc_back'] * np.cos(np.radians(surface_tilt)
                                                     ) / albedo * (1 - albedo)
        #assert actual_ground_absorbed_irradiance.iloc[0][
        #    'ground_absorbed_irradiance'] == bifacial_irradiances.iloc[0][
        #        'total_inc_back'] / albedo * (1 - albedo)

    def test_inc_front_horizontal_irrardiance(self):
        times = pd.date_range('2022-07-06', '2022-07-07', freq='1T',
                              tz='Canada/Pacific')
        index = times[700:704]
        data = {'total_inc_front': [903.2, 904.8, 906.4, 907.9],
                'total_inc_back': [34.3, 34.4, 34.4, 34.4],
                'total_abs_front': [876.1, 877.7, 879.2, 880.7],
                'total_abs_back': [32.6, 32.6, 32.7, 32.7],
                'effective_irradiance': [900.7, 902.2, 903.7, 905.2]}
        bifacial_irradiances = pd.DataFrame(data, index=index)

        lattitude, longitude = 49.26757152616243, -123.25266177347093
        timezone = 'Canada/Pacific'
        time_range = pd.date_range('2022-07-06', '2022-07-07', freq='1T',
                              tz=timezone)

        surface_azimuth = 180
        surface_tilt = 20
        axis_azimuth = 180
        pvrow_height = 1
        pvrow_width = 4
        pitch = 10
        gcr = pvrow_width / pitch
        albedo = 0.2
        n_pvrows = 3
        index_observed_pvrow = 1
        bifaciality = 0.75

        bifacial_irradiance_manager = BifacialIrradianceManager(
            lattitude, longitude, timezone, time_range,
            surface_azimuth, surface_tilt, axis_azimuth, gcr,
            pvrow_height, pvrow_width, albedo, n_pvrows, index_observed_pvrow,
            bifaciality)
        # Set fixture for testing
        bifacial_irradiance_manager._bifacial_irradiance_df =\
            bifacial_irradiances

        actual_inc_front_horizontal_irradiance =\
            bifacial_irradiance_manager.inc_front_horizontal_irradiance

        assert actual_inc_front_horizontal_irradiance.iloc[0][
            'inc_front_horizontal_irradiance'
               ] == bifacial_irradiances.iloc[0][
                'total_inc_front'] * np.cos(np.radians(surface_tilt))

