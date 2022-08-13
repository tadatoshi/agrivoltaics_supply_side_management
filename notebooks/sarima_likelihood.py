import numpy as np
import tensorflow as tf
import tensorflow_probability as tfp
tfd = tfp.distributions
root = tfd.JointDistributionCoroutine.Root

def generate_sarima_likelihood(observed, r, t):

    def sarima_likelihood(mu0, sigma, phi, theta, sphi, stheta):
        batch_shape = tf.shape(mu0)
        y_extended = tf.concat(
            [tf.zeros(tf.concat([[r], batch_shape], axis=0), dtype=mu0.dtype),
             tf.einsum('...,j->j...',
                      tf.ones_like(mu0, dtype=observed.dtype),
                      observed)],
            axis=0)
        eps_t = tf.zeros_like(y_extended, dtype=observed.dtype)

        def arma_onestep(t, eps_t):
            t_shift = t + r
            # AR
            y_past = tf.gather(y_extended, t_shift - (np.arange(p) + 1))
            ar = tf.einsum("...p,p...->...", phi, y_past)
            # MA
            eps_past = tf.gather(eps_t, t_shift - (np.arange(q) + 1))
            ma = tf.einsum("...q,q...->...", theta, eps_past)
            # Seasonal AR
            sy_past = tf.gather(y_extended, t_shift - (np.arange(seasonal_p) + 1) * period)
            sar = tf.einsum("...p,p...->...", sphi, sy_past)
            # Seasonal MA
            seps_past = tf.gather(eps_t, t_shift - (np.arange(seasonal_q) + 1) * period)
            sma = tf.einsum("...q,q...->...", stheta, seps_past)

            mu_at_t = ar + ma + sar + sma + mu0
            eps_update = tf.gather(y_extended, t_shift) - mu_at_t
            epsilon_t_next = tf.tensor_scatter_nd_update(
                    eps_t, [[t_shift]], eps_update[None, ...])
            return t+1, epsilon_t_next

        t, eps_output_ = tf.while_loop(
            lambda t, *_: t < observed.shape[-1], 
            arma_onestep,
            loop_vars=(0, eps_t), 
            maximum_iterations=observed.shape[-1])
        eps_output = eps_output_[r:]
        return tf.reduce_sum(
            tfd.Normal(0, sigma[None, ...]).log_prob(eps_output), axis=0)
    
    return sarima_likelihood