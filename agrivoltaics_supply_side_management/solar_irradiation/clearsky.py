from pvlib import location


def get_clearsky(lattitude, longitude, timezone, times):
    site_location = location.Location(lattitude, longitude, tz=timezone, name='Vancouver, BC, Canada')
    solar_position = site_location.get_solarposition(times)
    return site_location.get_clearsky(times)