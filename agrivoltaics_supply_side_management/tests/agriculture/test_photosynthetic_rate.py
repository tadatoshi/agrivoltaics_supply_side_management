import pytest
import numpy as np
import pandas as pd

from agrivoltaics_supply_side_management.agriculture.photosynthetic_rate\
    import PhotosyntheticRate


class TestPhotosyntheticRate:

    @pytest.fixture()
    def net_photosynthetic_rate_data(self):
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

    def test_net_photosynthetic_rate_function(self,
                                              net_photosynthetic_rate_data):
        xdata = net_photosynthetic_rate_data.index.values
        ydata_1 = net_photosynthetic_rate_data.Monocropping.values
        ydata_2 = net_photosynthetic_rate_data.Intercropping.values

        phi_1, alpha_1, theta_1 \
            = PhotosyntheticRate.net_photosynthetic_rate_parameters(
                xdata, ydata_1)

        # TODO: Replace with Hypothesis assert since the expected values
        #       below are the ones calculated in Jupyter notebook,
        #       in order to construct this test case:
        assert phi_1 == pytest.approx(0.03442842, abs=1e-8)
        assert alpha_1 == pytest.approx(0.0951081, abs=1e-8)
        assert theta_1 == pytest.approx(1.32757914, abs=1e-8)

        phi_2, alpha_2, theta_2 \
            = PhotosyntheticRate.net_photosynthetic_rate_parameters(
                xdata, ydata_2)

        # TODO: Replace with Hypothesis assert since the expected values
        #       below are the ones calculated in Jupyter notebook,
        #       in order to construct this test case:
        assert phi_2 == pytest.approx(0.05498626, abs=1e-8)
        assert alpha_2 == pytest.approx(0.12013631, abs=1e-8)
        assert theta_2 == pytest.approx(0.74425981, abs=1e-8)

    @pytest.mark.parametrize(
        "phi, alpha, theta, p_max",
        [
            (0.055, 0.2, 0.96, 15)
        ]
    )
    def test_find_light_saturation_point(self, phi, alpha, theta, p_max):

        ppfd_data = np.linspace(0, 1200)

        actual_light_saturation_point = \
            PhotosyntheticRate.find_light_saturation_point(
                phi, alpha, theta, p_max, ppfd_data)

        # From graph A of Fig. 1 of [7] (see README):
        expected_light_saturation_point = 350

        # actual_light_saturation_point was 367.3469387755102
        assert actual_light_saturation_point == pytest.approx(
            expected_light_saturation_point, abs=1e+2)
