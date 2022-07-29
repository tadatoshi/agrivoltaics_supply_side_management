import tensorflow as tf
import tensorflow_probability as tfp
tfd = tfp.distributions
root = tfd.JointDistributionCoroutine.Root
from gam_alternative import gam_trend_seasonality

def generate_gam_ar_latent(n_changepoints, matrix_a, x_pred, n_pred, 
                 co2_by_month_training_data, s, t, 
                 training=True):
    
    @tfd.JointDistributionCoroutine
    def gam_with_latent_ar():
        seasonality, trend, noise_sigma = yield from gam_trend_seasonality(
            n_changepoints, matrix_a, x_pred, n_pred, 
            co2_by_month_training_data, s, t)
        
        # Latent AR(1)
        ar_sigma = yield root(tfd.HalfNormal(.1, name="ar_sigma")) 
        rho = yield root(tfd.Uniform(-1., 1., name="rho"))
        def ar_fun(y):
            loc = tf.concat([tf.zeros_like(y[..., :1]), y[..., :-1]], 
                            axis=-1) * rho[..., None]
            return tfd.Independent(
                tfd.Normal(loc=loc, scale=ar_sigma[..., None]), 
                reinterpreted_batch_ndims=1)
        temporal_error = yield tfd.Autoregressive( 
            distribution_fn=ar_fun, 
            sample0=tf.zeros_like(trend), 
            num_steps=trend.shape[-1], 
            name="temporal_error")
        
        # Linear prediction
        y_hat = seasonality + trend + temporal_error
        if training:
             y_hat = y_hat[..., :co2_by_month_training_data.shape[0]]
        
        # Likelihood
        observed = yield tfd.Independent( 
            tfd.Normal(y_hat, noise_sigma[..., None]), 
            reinterpreted_batch_ndims=1, 
            name="observed"
        )
        
    return gam_with_latent_ar