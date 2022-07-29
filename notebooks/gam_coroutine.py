import tensorflow as tf
import tensorflow_probability as tfp

def gen_gam_jd(training=True):
    @tfp.distributions.JointDistributionCoroutine
    def gam():
        beta = yield tfp.distributions.JointDistributionCoroutine.Root(
            tfp.distributions.Sample( 
                tfp.distributions.Normal(0., 1.), 
                sample_shape=n_pred, 
                name='beta'))
        seasonality = tf.einsum('ij,...j->...i', x_pred, beta)

        k = yield tfp.distributions.JointDistributionCoroutine.Root(
                tfp.distributions.HalfNormal(10., name='k'))
        m = yield tfp.distributions.JointDistributionCoroutine.Root(
                tfp.distributions.Normal(
                    co2_by_month_training_data['CO2'].mean(), 
                    scale=5., name='m'))
        tau = yield tfp.distributions.JointDistributionCoroutine.Root(
                tfp.distributions.HalfNormal(10., name='tau'))
        delta = yield tfp.distributions.Sample(
                tfp.distributions.Laplace(0., tau),
                    sample_shape=n_changepoints,
                    name='delta')

        growth_rate = k[..., None] + tf.einsum('ij,...j->...i', matrix_a, delta)
        offset = m[..., None] + tf.einsum('ij,...j->...i', matrix_a, -s * delta)
        trend = growth_rate * t + offset

        y_hat = seasonality + trend
        if training:
            y_hat = y_hat[..., :co2_by_month_training_data.shape[0]]

        noise_sigma = yield tfp.distributions.JointDistributionCoroutine.Root(
            tfp.distributions.HalfNormal(scale=5., name='noise_sigma'))
        observed = yield tfp.distributions.Independent(
            tfp.distributions.Normal(y_hat, noise_sigma[..., None]), 
            reinterpreted_batch_ndims=1, name='observed')
        
    return gam