import numpy as np
from scipy import optimize


class PhotosyntheticRate:

    @staticmethod
    def net_photosynthetic_rate_parameters(ppfd_data, net_photosynthetic_rate_data):
        """
        Obtain parameters for theoretic Net Photosynthetis Rate equation, i.e.
        Equation (1) from [7] (see README).

        Arguments
        ---------
        ppfd_data: numpy array of floats
            Empirical data of PPFD incident on a leaf.
        net_photosynthetic_rate_data: numpy array of floats
            Empirical data of Net Photosynthetic Rate.

        Returns
        -------
        phi: float
            maximum quantum yield
        alpha: float
            fraction of maximum photosynthetic capacity used
            for dark respiration
        theta: float
            curvature of light-response curve
        """

        p_max = max(net_photosynthetic_rate_data)
        net_photosynthetic_rate_function \
            = PhotosyntheticRate.get_net_photosynthetic_rate_function(p_max)
        popt, pcov = optimize.curve_fit(
            net_photosynthetic_rate_function, ppfd_data,
            net_photosynthetic_rate_data)

        phi, alpha, theta = popt[0], popt[1], popt[2]
        return phi, alpha, theta

    @staticmethod
    def get_net_photosynthetic_rate_function(p_max):
        """
        In order to specify p_max outside net_photosynthetic_rate function,
        since it is not a part of function
        variables used by scipy.optimize.curve_fit.
        """

        def net_photosynthetic_rate_function(l, phi, alpha, theta):
            """
            function to pass to scipy.optimize.curve_fit.

            Arguments
            ---------
            l: float
                L - PPFD incident on a leaf
            phi: float
                maximum quantum yield
            alpha: float
                fraction of maximum photosynthetic capacity used
                for dark respiration
            theta: float
                curvature of light-response curve

            Returns
            -------
            Net Photosynthetic Rate: float
            """

            inside_sqrt = ((phi * l + (1 + alpha) * p_max) ** 2
                           - 4 * theta * phi * l * (1 + alpha) * p_max)

            # Temporary solution to avoid getting nan
            inside_sqrt[inside_sqrt < 0] = 0.0

            net_photosynthetic_rate_result = (phi * l + (1 + alpha) * p_max
                                              - np.sqrt(inside_sqrt)
                                              ) / (2 * theta) - alpha * p_max

            return net_photosynthetic_rate_result

        return net_photosynthetic_rate_function
