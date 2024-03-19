import pymc as pm


class BayesianModel1:

    def execute(self, std_net_photosynthetic_rate,
                prior_mean_phi, prior_mean_alpha, prior_mean_theta, ppfd,
                net_photosynthetic_rate_data,
                net_photosynthetic_rate_function):

        with pm.Model() as model_1:
            std = pm.HalfStudentT('sigma', std_net_photosynthetic_rate, 100)
            phi = pm.Normal('phi', prior_mean_phi, 1.0)
            alpha = pm.Normal('alpha', prior_mean_alpha, 1.0)
            theta = pm.Normal('theta', prior_mean_theta, 10.0)
            mu = pm.Deterministic('mu',
                    net_photosynthetic_rate_function(ppfd, phi, alpha, theta))

            net_photosynthetic_rate = pm.Normal('net_photosynthetic_rate',
                    mu=mu, sigma=std, observed=net_photosynthetic_rate_data)

            idata = pm.sample(3000, tune=2000, return_inferencedata=True)

        posterior_mean_phi = idata['posterior']['phi'].to_numpy().mean()
        posterior_mean_alpha = idata['posterior']['alpha'].to_numpy().mean()
        posterior_mean_theta = idata['posterior']['theta'].to_numpy().mean()

        return posterior_mean_phi, posterior_mean_alpha, posterior_mean_theta
