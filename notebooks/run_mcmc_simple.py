# a NUTS sampling routine with simple tuning
import tensorflow as tf
import tensorflow_probability as tfp
from tensorflow_probability.python.internal import unnest 
from tensorflow_probability.python.internal import samplers
tfd = tfp.distributions

def run_mcmc_simple(
    n_draws,
    joint_dist,
    n_chains=4,
    num_adaptation_steps=1000,
    return_compiled_function=False,
    target_log_prob_fn=None,
    bijector=None,
    init_state=None,
    seed=None,
    **pins):
    
    joint_dist_pinned = joint_dist.experimental_pin(**pins) if pins\
                        else joint_dist
    
    if bijector is None:
        bijector = \
            joint_dist_pinned.experimental_default_event_space_bijector() 
    if target_log_prob_fn is None:
        target_log_prob_fn = joint_dist_pinned.unnormalized_log_prob
        
    if seed is None: 
        seed = 26401
    run_mcmc_seed = samplers.sanitize_seed(seed, salt='run_mcmc_seed')
    
    if init_state is None:
        if pins:
            init_state_ = joint_dist_pinned.sample_unpinned(n_chains)
        else:
            init_state_ = joint_dist_pinned.sample(n_chains)
        ini_state_unbound = bijector.inverse(init_state_)
        run_mcmc_seed, *init_seed = samplers.split_seed(
            run_mcmc_seed, n=len(ini_state_unbound)+1)
        init_state = bijector.forward(
            tf.nest.map_structure(
                lambda x, seed: tfd.Uniform(-1., tf.constant(1., x.dtype)
                    ).sample(x.shape, seed=seed),
                ini_state_unbound,
                tf.nest.pack_sequence_as(ini_state_unbound, init_seed)))
        
        @tf.function(autograph=False, jit_compile=True)
        def run_inference_nuts(init_state, draws, tune, seed):
            seed, tuning_seed, sample_seed = samplers.split_seed(seed, n=3)
            
            def gen_kernel(step_size):
                hmc = tfp.mcmc.NoUTurnSampler(
                    target_log_prob_fn=target_log_prob_fn, 
                    step_size=step_size)
                hmc = tfp.mcmc.TransformedTransitionKernel(
                    hmc, bijector=bijector)
                tuning_hmc = tfp.mcmc.DualAveragingStepSizeAdaptation(
                    hmc, tune // 2, target_accept_prob=0.85)
                return tuning_hmc
            
            def tuning_trace_fn(_, pkr):
                return pkr.inner_results.transformed_state, pkr.new_step_size
            
            def get_tuned_stepsize(samples, step_size):
                return tf.math.reduce_std(samples, axis=0) * step_size[-1]
            
            step_size = tf.nest.map_structure(
                tf.ones_like, bijector.inverse(init_state))
            tuning_hmc = gen_kernel(step_size)
            init_samples, (sample_unbounded, tuning_step_size) = \
                tfp.mcmc.sample_chain(
                    num_results=200,
                    num_burnin_steps=tune // 2 - 200,
                    current_state=init_state,
                    kernel=tuning_hmc,
                    trace_fn=tuning_trace_fn,
                    seed=tuning_seed)
            
            tuning_step_size = tf.nest.pack_sequence_as(
                sample_unbounded, tuning_step_size)
            step_size_new = tf.nest.map_structure(get_tuned_stepsize,
                                                  sample_unbounded,
                                                  tuning_step_size)
            sample_hmc = gen_kernel(step_size_new)
            
            def sample_trace_fn(_, pkr):
                energy_diff = unnest.get_innermost(pkr, 'log_accept_ratio')
                return {
                    'target_log_prob': unnest.get_innermost(pkr, 'target_log_prob'),
                    'n_steps': unnest.get_innermost(pkr, 'leapfrogs_taken'),
                    'diverging': unnest.get_innermost(pkr, 'has_divergence'),
                    'energy': unnest.get_innermost(pkr, 'energy'),
                    'accept_ratio': tf.minimum(1., tf.exp(energy_diff)),
                    'reach_max_depth': unnest.get_innermost(pkr, 'reach_max_depth'),
                }
            current_state = tf.nest.map_structure(lambda x: x[-1], init_samples)
            return tfp.mcmc.sample_chain(
                num_results=draws,
                num_burnin_steps=tune // 2,
                current_state=current_state,
                kernel=sample_hmc,
                trace_fn=sample_trace_fn,
                seed=sample_seed)
        
        mcmc_samples, mcmc_diagnostic = run_inference_nuts(
            init_state, n_draws, num_adaptation_steps, run_mcmc_seed)
        
        if return_compiled_function:
            return mcmc_samples, mcmc_diagnostic, run_inference_nuts
        else:
            return mcmc_samples, mcmc_diagnostic