import numpy as np


class Photosynthesis:

    def crop_yield(self, harvest_index, biomass_energy_ratio, photosynthetically_active_radiation,
                   leaf_area_index, crop_growth_regulating_factor, number_of_days):

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
