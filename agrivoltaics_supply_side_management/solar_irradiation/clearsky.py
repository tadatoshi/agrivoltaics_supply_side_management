from pvlib import location


def get_clearsky(lattitude, longitude, timezone, time_range,
                 location_name='Vancouver, BC, Canada'):
    site_location = location.Location(lattitude, longitude, tz=timezone,
                                      name=location_name)
    solar_position = site_location.get_solarposition(time_range)
    return site_location.get_clearsky(time_range)