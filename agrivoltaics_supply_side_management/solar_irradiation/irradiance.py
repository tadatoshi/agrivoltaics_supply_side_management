from datetime import datetime


class IrradianceManager:
    """
    Class to take care of selecting appropriate irradiance model,
    e.g. clearsky and use it to get irradiance for the timespan.
    And gives the irradiance based on the specified time.
    """

    def __init__(self, lattitude, longitude, timezone, times):
        self._lattitude = lattitude
        self._longitude = longitude
        self._timezone = timezone
        self._times = times

        # Step 1: Logic to select appropriate irradiance model.
        # Step 2: Use the model to get irradiance data for the givee
        #         times
        # Step 3: Hold the irradiance data as member field

    def get_irradiance(self, date_time: datetime):

        # TODO: Get irradiance from irradiance data:
        # For now, return hardcoded value in order to make the rest of
        # codiing going:
        return 1000
