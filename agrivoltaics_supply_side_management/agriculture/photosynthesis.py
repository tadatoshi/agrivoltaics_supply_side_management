import numpy as np


class Photosynthesis:
    """
    Comprise various photosynthesis related models and calculations.
    """

    def crop_yield(self, harvest_index, biomass_energy_ratio,
                   photosynthetically_active_radiation, leaf_area_index,
                   crop_growth_regulating_factor):
        """
        Equation (6) o [1] (See README)
        biomass_energy_ratio has kg in unit and crop_yield has ton
        in unit. Thus, the units don't match. Investigate.
        -> Update: Based on the calculated result value, the unit of
        expected_crop_yield seems to be correct despite the units don't
        match in the equation.

        Arguments
        ---------
        harvest_index: float
            0.25 − 0.35 for soybean and 0.40 − 0.55 for maize.
        biomass_energy_ratio: float [(kg/ha)/(MJ/m2)]
        photosynthetically_active_radiation : float (will be changed to list)
            [MJ/m^2]
            Based on 5 peak sun hours
            with solar irradiance 1000[W/m^2] per day on a sunny summer day
            and [MJ] = [Wh] * 60[min/h] * 60[sec/min] / 1000000
            1000[W/m^2] -> 5000[Wh/m^2] -> 18[MJ/m^2]

        Returns
        -------
        crop yield: float [ton/ha]
            Reference [1] (See README)
            biomass_energy_ratio has kg in unit. Thus, according to the
            equation, it's [kg/ha]. But we keep it as [ton/ha]
        """

        coefficient_1 = 0.001
        coefficient_2 = -0.65

        # As opposed to discrete as given in the literature [1] (See README),
        # which is a sum by number of days, this calculation is continuous.
        # Hence, multiplication by number_of_days is removed.
        # photosynthetically_active_radiation contains the accumulated value
        # for the given duration, duration of cultivation, one day, or one
        # minute:
        crop_yield = harvest_index * (coefficient_1 * biomass_energy_ratio
                      * photosynthetically_active_radiation
                      * (1 - np.exp(coefficient_2 * leaf_area_index))
                      * crop_growth_regulating_factor)

        return crop_yield
