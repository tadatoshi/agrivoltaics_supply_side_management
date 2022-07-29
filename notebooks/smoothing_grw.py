import tensorflow as tf
import tensorflow_probability as tfp
tfd = tfp.distributions
root = tfd.JointDistributionCoroutine.Root

def generate_smoothing_grw(num_steps):

    @tfd.JointDistributionCoroutine
    def smoothing_grw():
        alpha = yield root(tfd.Beta(5, 1.))
        variance = yield root(tfd.HalfNormal(10.))
        sigma0 = tf.sqrt(variance * alpha)
        sigma1 = tf.sqrt(variance * (1. - alpha))
        z = yield tfd.Sample(tfd.Normal(0., sigma0), num_steps)
        observed = yield tfd.Independent(
            tfd.Normal(tf.math.cumsum(z, axis=-1), sigma1[..., None]),
            name='observed'
        )
        
    return smoothing_grw