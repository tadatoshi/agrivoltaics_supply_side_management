import numpy as np


class PhotosyntheticModel:

    def crop_yield(self, harvest_index, biomass_energy_ratio, photosynthetically_active_radiation,
                   leaf_area_index, crop_growth_regulating_factor, number_of_days):

        coefficient_1 = 0.001
        coefficient_2 = -0.65

        crop_yield = (harvest_index * (coefficient_1 * number_of_days) * biomass_energy_ratio
                      * photosynthetically_active_radiation
                      * (1 - np.exp(coefficient_2 * leaf_area_index))
                      * crop_growth_regulating_factor)

        return crop_yield
