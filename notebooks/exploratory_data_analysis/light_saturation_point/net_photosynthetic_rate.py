import numpy as np

def get_net_photosynthetic_rate_function(p_max):
    """
    In order to specify p_max outside net_photosynthetic_rate function, 
    since it is not a part of function 
    variables used by scipy.optimize.curve_fit.
    """

    def net_photosynthetic_rate(l, phi, alpha, theta):
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
        
        inside_sqrt = (phi * l + (1 + alpha) * p_max)**2 - 4 * theta * phi * l * (1 + alpha) * p_max
        
        # Temporary solution to avoid getting nan
        inside_sqrt[inside_sqrt < 0] = 0.0
        
        print(f"l: {l}, phi: {phi}, alpha: {alpha}, theta: {theta}, inside_sqrt: {inside_sqrt}")
        
        net_photosynthetic_rate_result = (phi * l + (1 + alpha) * p_max - np.sqrt(
                inside_sqrt)
                ) / (2 * theta) - alpha * p_max
        
        print(f"net_photosynthetic_rate_result: {net_photosynthetic_rate_result}")
        
        return net_photosynthetic_rate_result

        # return (phi * l + (1 + alpha) * p_max - np.sqrt(
        #         (phi * l + (1 + alpha) * p_max)**2 
        #          - 4 * theta * phi * l * (1 + alpha) * p_max)
        #         ) / (2 * theta) - alpha * p_max
    
    return net_photosynthetic_rate
