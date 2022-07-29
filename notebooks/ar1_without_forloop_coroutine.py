import tensorflow as tf
import tensorflow_probability as tfp

@tfp.distributions.JointDistributionCoroutine
def ar1_without_forloop():
    sigma = yield tfp.distributions.JointDistributionCoroutine.Root(
                    tfp.distributions.HalfNormal(1.))
    rho = yield tfp.distributions.JointDistributionCoroutine.Root(
                    tfp.distributions.Uniform(-1., 1.))
    
    def ar1_fun(x):
        x_tm1 = tf.concat([tf.zeros_like(x[..., :1]), x[..., :-1]], axis=-1)
        loc = x_tm1 * rho[..., None]
        return tfp.distributions.Independent(tfp.distributions.Normal(
            loc=loc, scale=sigma[..., None]),
            reinterpreted_batch_ndims=1)
    
    dist = yield tfp.distributions.Autoregressive(
        distribution_fn=ar1_fun, 
        sample0=tf.zeros([n_t], dtype=rho.dtype), 
        num_steps=n_t)