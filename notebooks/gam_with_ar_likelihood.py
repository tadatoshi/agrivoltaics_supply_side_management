import tensorflow as tf
import tensorflow_probability as tfp
tfd = tfp.distributions
root = tfd.JointDistributionCoroutine.Root
from gam_alternative import gam_trend_seasonality

def generate_gam_ar_likelihood(n_changepoints, matrix_a, x_pred, n_pred, 
                 co2_by_month_training_data, s, t, 
                 training=True):
    
    @tfd.JointDistributionCoroutine
    def gam_with_ar_likelihood():
        seasonality, trend, noise_sigma = yield from gam_trend_seasonality(
            n_changepoints, matrix_a, x_pred, n_pred, 
            co2_by_month_training_data, s, t)
        y_hat = seasonality + trend
        if training:
            y_hat = y_hat[..., :co2_by_month_training_data.shape[0]]
        
        # likelihood
        rho = yield root(tfd.Uniform(-1., 1., name="rho"))
        def ar_fun(y):
            loc = tf.concat([tf.zeros_like(y[..., :1]), y[..., :-1]], 
                            axis=-1) * rho[..., None] + y_hat
            return tfd.Independent(
                tfd.Normal(loc=loc, scale=noise_sigma[..., None]), 
                reinterpreted_batch_ndims=1)
        observed = yield tfd.Autoregressive( 
            distribution_fn=ar_fun, 
            sample0=tf.zeros_like(y_hat), 
            num_steps=1,
            name="observed")
        
    return gam_with_ar_likelihood