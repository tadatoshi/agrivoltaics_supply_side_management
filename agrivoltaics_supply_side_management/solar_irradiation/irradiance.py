from datetime import datetime
import numpy as np
import pandas as pd
from pvlib import location
from pvlib.bifacial.pvfactors import pvfactors_timeseries

from agrivoltaics_supply_side_management.solar_irradiation.clearsky import get_clearsky


class IrradianceManager:
    """
    Class to take care of selecting appropriate irradiance model,
    e.g. clearsky and use it to get irradiance for the timespan.
    And gives the irradiance based on the specified time.
    """

    def __init__(self, lattitude, longitude, timezone, time_range):
        self._lattitude = lattitude
        self._longitude = longitude
        self._timezone = timezone
        self._time_range = time_range

        # Step 1: Logic to select appropriate irradiance model.
        # Step 2: Use the model to get irradiance data for the given
        #         time_range
        # Step 3: Hold the irradiance data as member field

        # Temporarily use clearsky model.
        # TODO: Implement the logic to select various irradiance model
        clearsky_irradiaces = get_clearsky(lattitude, longitude,
                                           timezone, time_range)
        self._irradiace_data = clearsky_irradiaces['ghi']

    def get_irradiance(self, date_time: datetime):

        return self._irradiace_data.loc[date_time]


class BifacialIrradianceManager:

    def __init__(self, lattitude, longitude, timezone, time_range,
                 surface_azimuth, surface_tilt, axis_azimuth, gcr,
                 pvrow_height, pvrow_width, albedo, n_pvrows,
                 index_observed_pvrow, bifaciality):
        self._lattitude = lattitude
        self._longitude = longitude
        self._timezone = timezone
        self._time_range = time_range

        self._bifacial_irradiance_df = self._get_bifacial_irradiances(
            surface_azimuth, surface_tilt, axis_azimuth,
            albedo, gcr, pvrow_height, pvrow_width, n_pvrows,
            index_observed_pvrow, bifaciality)

        self._ground_absorbed_irrardiance =\
            self._calculate_ground_absorbed_irrardiance(self._bifacial_irradiance_df,
                                           surface_tilt, albedo)

    def get_irradiance(self, date_time: datetime):
        pass

    def _get_bifacial_irradiances(self, surface_azimuth, surface_tilt,
                                  axis_azimuth,
                                  albedo, gcr, pvrow_height,
                                  pvrow_width, n_pvrows, index_observed_pvrow,
                                  bifaciality):
        """
        Get irradiance over bifacial moudle plane of array (POA) by
        bifacial module of pvlib-python
        """
        loc = location.Location(latitude=self._lattitude,
                                longitude=self._longitude,
                                tz=self._timezone)
        solar_position = loc.get_solarposition(self._time_range)
        clearsky = loc.get_clearsky(self._time_range)
        irradiances = pvfactors_timeseries(
            solar_azimuth=solar_position['azimuth'],
            solar_zenith=solar_position['apparent_zenith'],
            surface_azimuth=surface_azimuth,
            surface_tilt=surface_tilt,
            axis_azimuth=axis_azimuth,
            timestamps=self._time_range,
            dni=clearsky['dni'],
            dhi=clearsky['dhi'],
            gcr=gcr,
            pvrow_height=pvrow_height,
            pvrow_width=pvrow_width,
            albedo=albedo,
            n_pvrows=n_pvrows,
            index_observed_pvrow=index_observed_pvrow
        )
        bifacial_irradiances = pd.concat(irradiances, axis=1)
        bifacial_irradiances['effective_irradiance'] = (
                bifacial_irradiances['total_abs_front']
                + (bifacial_irradiances['total_abs_back'] * bifaciality)
        )

        return bifacial_irradiances

    def _calculate_ground_absorbed_irrardiance(self, bifacial_irradiances,
                                               surface_tilt, albedo):
        """
        Reverse engineer irradiance over ground based on the incident
        irradiance on the back of bifacial module
        """

        # Get reflected irradiance from the ground over the surface covered
        # by PV module
        # Note: Since the value is per m^2, we don't perform mulciplication by
        #       cos, which reduces surface area to be less than 1[m^2].
        #       We assume that crops are entirely covered by module, which is
        #       bigger than 1[m^2].
        # TODO: Come back and adjust to the case where ground covered by module
        #       is less than 1[m^2].
        #reflected_irradiance_on_ground = bifacial_irradiances['total_inc_back'
        #                                 ] * np.cos(np.radians(surface_tilt))
        reflected_irradiance_on_ground = bifacial_irradiances['total_inc_back'
                                                ].copy()
        # Portion indicated albedo is considered to be the reflected
        # irradiance on ground
        result_series = reflected_irradiance_on_ground / albedo * (1 - albedo)

        return result_series.to_frame(name='ground_absorbed_irradiance')

    @property
    def bifacial_irradiances(self):
        return self._bifacial_irradiance_df

    @property
    def ground_absorbed_irrardiance(self):
        return self._ground_absorbed_irrardiance
