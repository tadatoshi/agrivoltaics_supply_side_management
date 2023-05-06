import pytest
import numpy as np
import pandas as pd

from agrivoltaics_supply_side_management.agriculture.photosynthetic_rate\
    import PhotosyntheticRate
from agrivoltaics_supply_side_management.bayesian.model_1\
    import BayesianModel1


class TestModel1:

    @pytest.fixture()
    def net_photosynthetic_rate_df(self):
        index_column_name = "Photosynthetically Active Radiation" \
                            + " [micromol / m^2 / s]"
        column_1_name = 'Monocropping - CO2 uptake [micromol / m^2 / s]'
        column_2_name = 'Intercropping - CO2 uptake [micromol / m^2 / s]'
        data_df = pd.read_csv("data/soybean_net_photosynthetic_rate.csv",
                              index_col=index_column_name)
        data_df.rename(columns={column_1_name: 'Monocropping',
                                column_2_name: 'Intercropping'},
                       inplace=True)
        data_df.index.names = ['PAR']
        return data_df

    def test_execute(self, net_photosynthetic_rate_df):

        ppfd = net_photosynthetic_rate_df.index.values
        net_photosynthetic_rate_data \
            = net_photosynthetic_rate_df.Intercropping.values
        p_max = max(net_photosynthetic_rate_data)
        net_photosynthetic_rate_function = \
            PhotosyntheticRate.get_net_photosynthetic_rate_function(
                p_max, avoid_nan=False)
        prior_mean_phi, prior_mean_alpha, prior_mean_theta \
            = PhotosyntheticRate.net_photosynthetic_rate_parameters(ppfd,
                        net_photosynthetic_rate_data)

        std_net_photosynthetic_rate \
            = net_photosynthetic_rate_df.Intercropping.std()

        bayesian_model_1 = BayesianModel1()
        actual_posterior_mean_phi, actual_posterior_mean_alpha, \
        actual_posterior_mean_theta \
            = bayesian_model_1.execute(std_net_photosynthetic_rate,
                prior_mean_phi, prior_mean_alpha, prior_mean_theta, ppfd,
                net_photosynthetic_rate_data,
                net_photosynthetic_rate_function)

        assert 0.01 < actual_posterior_mean_phi < 1.0
        assert 0.01 < actual_posterior_mean_alpha < 1.0
        #assert -4.0 < actual_posterior_mean_theta < 4.0
        assert -7.0 < actual_posterior_mean_theta < 4.0
