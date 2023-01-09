import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import pymc3 as pm
import statsmodels.api as sm
import theano
import theano.tensor as tt
from pandas.plotting import register_matplotlib_converters

plt.style.use("seaborn")
register_matplotlib_converters()

from agrivoltaics_supply_side_management.util.statsmodels_to_pymc3_tensor\
    import Loglike


class BayesianSarimaxManager:
    """
    Based on https://www.statsmodels.org/dev/examples/notebooks/generated/
    statespace_sarimax_pymc3.html
    Manages repetitive executions.
    """
    
    def __init__(self, data):
        self._data = data
    
    def perform(self):
        self._perform_sarimax()
        self._perform_pymc3()
        self._apply_pymc3_result()

    def _perform_sarimax(self):
        self._sarimax_model = sm.tsa.statespace.SARIMAX(self._data, 
                                                        order=(1, 0, 1))
        self._sarimax_result = self._sarimax_model.fit(disp=False)
        
    def _perform_pymc3(self):
        ndraws = 3000  # number of draws from the distribution
        nburn = 600  # number of "burn-in points" (which will be discarded)
        
        sarimax_loglike = Loglike(self._sarimax_model)
        
        with pm.Model() as m:
            # Priors
            ar_l1_sarimax = pm.Uniform("ar.l1", -0.99, 0.99)
            ma_l1_sarimax = pm.Uniform("ma.l1", -0.99, 0.99)
            sigma2_sarimax = pm.InverseGamma("sigma2", 2, 4)

            # convert variables to tensor vectors
            theta_sarimax = tt.as_tensor_variable(
                [ar_l1_sarimax, ma_l1_sarimax, sigma2_sarimax])

            # use a DensityDist (use a lamdba function to "call" the Op)
            pm.DensityDist("likelihood", sarimax_loglike, 
                           observed=theta_sarimax)

            # Draw samples
            self._trace_sarimax = pm.sample(
                ndraws,
                tune=nburn,
                return_inferencedata=True,
                cores=1,
                compute_convergence_checks=False,
            )
    
    def plot_pymc3_trace(self):
        plt.tight_layout()

        _ = pm.plot_trace(
            self._trace_sarimax,
            lines=[(k, {}, [v]) for k, v 
                   in dict(self._sarimax_result.params).items()],
            combined=True,
            figsize=(12, 12),
        )
        
    def pymc3_trace_summary(self):
        return pm.summary(self._trace_sarimax)
        
    def _apply_pymc3_result(self):
        bayes_sarimax_params = pm.summary(self._trace_sarimax)["mean"].values
        bayes_sarimax_result = self._sarimax_model.smooth(
            bayes_sarimax_params)
        self._bayes_sarimax_prediction = bayes_sarimax_result.get_prediction()
        self._bayes_sarimax_prediction_ci\
            = self._bayes_sarimax_prediction.conf_int()
        
    def plot_pymc3_application(self):
        # Graph
        fig, ax = plt.subplots(figsize=(9, 4), dpi=300)

        # Plot data points
        self._data.plot(ax=ax, style="-", label="Observed")

        # Plot predictions
        self._bayes_sarimax_prediction.predicted_mean.plot(
            ax=ax, style="r.", label="One-step-ahead forecast")
        ax.fill_between(self._bayes_sarimax_prediction_ci.index, 
                        self._bayes_sarimax_prediction_ci.iloc[:, 0], 
                        self._bayes_sarimax_prediction_ci.iloc[:, 1],
                        color="r", alpha=0.1)
        ax.legend(loc="lower left")
        plt.show()

    @property
    def sarimax_result(self):
        return self._sarimax_result
        
    @property
    def bayes_sarimax_prediction(self):
        return self._bayes_sarimax_prediction
