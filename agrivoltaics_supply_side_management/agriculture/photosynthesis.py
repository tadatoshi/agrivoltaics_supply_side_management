import numpy as np


class Photosynthesis:
    """
    Comprise various photosynthesis related models and calculations.
    """

    def crop_yield(self, harvest_index, biomass_energy_ratio,
                   photosynthetically_active_radiation, leaf_area_index,
                   crop_growth_regulating_factor, number_of_days):
        """
        Using data from 'Table 3 Default parameters for potato' of
        P. E. Campana, B. Stridh, S. Amaducci, and M. Colauzzi,
        “Optimisation of vertically mounted agrivoltaic systems,”
        Journal of Cleaner Production, vol. 325, p. 129091, Nov. 2021,
        doi: 10.1016/j.jclepro.2021.129091.
        TODO: biomass_energy_ratio has kg in unit and crop_yield has ton
        in unit. Thus, the units don't match. Investigate.

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
        number_of_days: integer
            4 momths between planting and harvesting
            with average 30 days / month
        expected_crop_yield: float [ton/ha]

        Returns
        -------
        crop yield: float [ton/ha]
            Reference [1] (See README)
            biomass_energy_ratio has kg in unit. Thus, according to the
            equation, it's [kg/ha]. But we keep it as [ton/ha]
        """

        coefficient_1 = 0.001
        coefficient_2 = -0.65

        # TODO: Modified to make the sum over list of
        #       photosynthetically_active_radiation
        #       except for harvest_index, which is outside of summation
        crop_yield = (harvest_index * coefficient_1 * biomass_energy_ratio
                      * photosynthetically_active_radiation
                      * (1 - np.exp(coefficient_2 * leaf_area_index))
                      * crop_growth_regulating_factor
                      * number_of_days)

        return crop_yield
