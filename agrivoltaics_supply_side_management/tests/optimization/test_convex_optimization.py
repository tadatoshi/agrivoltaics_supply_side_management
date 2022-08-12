import pytest
import pyomo.environ as pyo

from agrivoltaics_supply_side_management.optimization.convex_optimization\
    import ConvexOptimization


class TestConvexOptimization:

    @pytest.mark.parametrize(
        "irradiance, light_saturation_point",
        [
            (1000, 250)
        ]
    )
    def test_optimize(self, irradiance, light_saturation_point):
        """
        Arguments
        ---------
        light_saturation_point : float [W/m^2]
            Solar irradiance at which plant photosynthesis saturates.
            The value 250 is based on Figure 2 of [2] in README.


        """
        convex_optimization = ConvexOptimization()
        pv_result, crop_result = convex_optimization.optimize(irradiance,
                                            light_saturation_point)

        assert pv_result == 750
        assert crop_result == 250

    def test_temp(self):
        convex_optimization = ConvexOptimization()
        instance = convex_optimization.temp()
        instance.display()

        # print("objective value: ", instance.OBJ())
        # print("result value x1: ", pyo.value(instance.x[1]))
        # print("result value x2: ", pyo.value(instance.x[2]))

        assert pyo.value(instance.x[1]) == 0.333333333333333
        assert pyo.value(instance.x[2]) == 0.0
