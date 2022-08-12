import pyomo.environ as pyo
from pyomo.core import maximize


class ConvexOptimization:

    def optimize(self, irradiance, light_saturation_point):
        """
        Performs convex optimization for agrivoltaic system.

        Arguments
        ---------
        light_saturation_point : float [W/m^2]
            Solar irradiance at which plant photosynthesis saturates.


        """

        model = pyo.ConcreteModel()
        model.x = pyo.Var([1, 2], domain=pyo.NonNegativeReals)
        model.OBJ = pyo.Objective(expr=model.x[1] + model.x[2], sense=maximize)
        model.total = pyo.Constraint(expr=model.x[1] + model.x[2] <= irradiance)
        model.crop = pyo.Constraint(expr=model.x[1] <=
                                         light_saturation_point)
        result = pyo.SolverFactory('glpk').solve(model, tee=True)

        # model.display()
        # print(result)

        pv_result, crop_result = pyo.value(model.x[2]), pyo.value(model.x[1])

        return pv_result, crop_result

    def temp(self):
        model = pyo.ConcreteModel()

        model.x = pyo.Var([1, 2], domain=pyo.NonNegativeReals)

        model.OBJ = pyo.Objective(expr=2 * model.x[1] + 3 * model.x[2])

        model.Constraint1 = pyo.Constraint(expr=3 * model.x[1] + 4 * model.x[2] >= 1)

        instance = model.create_instance()

        result = pyo.SolverFactory('glpk').solve(instance, tee=True)

        return instance



