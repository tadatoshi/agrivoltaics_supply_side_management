import tensorflow as tf
import tensorflow_probability as tfp
tfd = tfp.distributions
root = tfd.JointDistributionCoroutine.Root

def gam_trend_seasonality(n_changepoints, matrix_a, x_pred, n_pred, 
                          co2_by_month_training_data, s, t):
    beta = yield root(tfd.Sample(
         tfd.Normal(0., 1.), sample_shape=n_pred, name="beta"))
    seasonality = tf.einsum("ij,...j->...i", x_pred, beta)
    
    k = yield root(tfd.HalfNormal(10., name="k"))
    m = yield root(tfd.Normal(
            co2_by_month_training_data["CO2"].mean(), scale=5., name="m"))
    tau = yield root(tfd.HalfNormal(10., name="tau"))
    delta = yield tfd.Sample(
         tfd.Laplace(0., tau), sample_shape=n_changepoints, name="delta")
    
    growth_rate = k[..., None] + tf.einsum("ij,...j->...i", matrix_a, delta)
    offset = m[..., None] + tf.einsum("ij,...j->...i", matrix_a, -s * delta)
    trend = growth_rate * t + offset
    noise_sigma = yield root(tfd.HalfNormal(scale=5., name="noise_sigma"))
    
    return seasonality, trend, noise_sigma

def generate_gam(n_changepoints, matrix_a, x_pred, n_pred, 
                 co2_by_month_training_data, s, t, 
                 training=True):
    
    @tfd.JointDistributionCoroutine
    def gam():
        seasonality, trend, noise_sigma = yield from gam_trend_seasonality(
            n_changepoints, matrix_a, x_pred, n_pred, 
            co2_by_month_training_data, s, t)
        y_hat = seasonality + trend
        if training:
            y_hat = y_hat[..., :co2_by_month_training_data.shape[0]]
        
        # likelihood
        observed = yield tfd.Independent( 
            tfd.Normal(y_hat, noise_sigma[..., None]), 
            reinterpreted_batch_ndims=1, 
            name="observed"
        )
        
    return gam