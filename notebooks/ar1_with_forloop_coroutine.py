import tensorflow as tf
import tensorflow_probability as tfp

@tfp.distributions.JointDistributionCoroutine
def ar1_with_forloop():
    sigma = yield tfp.distributions.JointDistributionCoroutine.Root(
                    tfp.distributions.HalfNormal(1.))
    rho = yield tfp.distributions.JointDistributionCoroutine.Root(
                    tfp.distributions.Uniform(-1., 1.))
    x0 = yield tfp.distributions.Normal(0., sigma)
    x = [x0]
    for i in range(1, n_t):
        x_i = yield tfp.distributions.Normal(x[i-1] * rho, sigma)
        x.append(x_i)