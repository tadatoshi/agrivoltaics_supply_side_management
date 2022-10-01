from datetime import datetime

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
