import tensorflow as tf
import tensorflow_probability as tfp
tfd = tfp.distributions
root = tfd.JointDistributionCoroutine.Root
tfb = tfp.bijectors

def generate_sarima_priors(p, q, seasonal_p, seasonal_q):
    
    @tfd.JointDistributionCoroutine
    def sarima_priors():
        mu0 = yield root(tfd.StudentT(df=6, loc=0, scale=2.5, name='mu0'))
        sigma = yield root(tfd.HalfStudentT(df=7, loc=0, scale=1., 
                                            name='sigma'))
        
        phi = yield root( 
            tfd.Sample(
                tfd.TransformedDistribution(
                    tfd.Beta(concentration1=2., concentration0=2.),
                    tfb.Shift(-1.)(tfb.Scale(2.))),
                p, name='phi')
        )
        theta = yield root(tfd.Sample(tfd.Normal(loc=0, scale=0.5), q, 
                                      name='theta'))
        sphi = yield root(tfd.Sample(tfd.Normal(loc=0, scale=0.5), 
                                     seasonal_p, name='sphi'))
        stheta = yield root(tfd.Sample(tfd.Normal(loc=0, scale=0.5), 
                                       seasonal_q, name='stheta'))
    
    return sarima_priors