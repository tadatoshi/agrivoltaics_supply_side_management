"""
Temporarily created to express supply pattern in order to figure out the
model to describe what is needed.
"""
from abc import abstractmethod
from datetime import datetime


class SupplyStrategy:

    def __init__(self, irradiance_manager, optimization):
        self._irradiance_manager = irradiance_manager
        self._optimization = optimization

    @abstractmethod
    def supply(self, date_time: datetime, duration_in_sec):
        pass


class MorningSupplyStrategy(SupplyStrategy):

    def __init__(self, irradiance_manager, optimization,
                 electricity_generation):
        super().__init__(irradiance_manager, optimization)
        self._electricity_generation = electricity_generation

    def supply(self, date_time: datetime, duration_in_sec):
        irradiance = self._irradiance_manager.get_irradiance(date_time)
        self._electricity_generation.consume_light_power(irradiance)

        return self._electricity_generation.produce_electric_energy(
                                                        duration_in_sec), 0


class MiddaySupplyStrategy(SupplyStrategy):

    def __init__(self, irradiance_manager, optimization,
                 electricity_generation, cultivation):
        super().__init__(irradiance_manager, optimization)
        self._electricity_generation = electricity_generation
        self._cultivation = cultivation

    def supply(self, date_time: datetime, duration_in_sec):
        irradiance = self._irradiance_manager.get_irradiance(date_time)
        light_saturation_point = self._cultivation.light_saturation_point

        pv_irradiance, crop_irradiance = self._optimization.optimize(
            irradiance, light_saturation_point)

        # allcate irradiance to electricity_generation and cultivation
        self._electricity_generation.consume_light_power(pv_irradiance)
        self._cultivation.consume_light_power(crop_irradiance)

        return (self._electricity_generation.produce_electric_energy(
                                                            duration_in_sec),
                self._cultivation.produce(duration_in_sec))


class AfternoonSupplyStrategy(SupplyStrategy):

    def __init__(self, irradiance_manager, optimization,
                 electricity_generation):
        super().__init__(irradiance_manager, optimization)
        self._electricity_generation = electricity_generation

    def supply(self, date_time: datetime, duration_in_sec):
        irradiance = self._irradiance_manager.get_irradiance(date_time)

        self._electricity_generation.consume_light_power(irradiance)

        return self._electricity_generation.produce_electric_energy(
                                                        duration_in_sec), 0


class DefaultSupplyStrategy(SupplyStrategy):

    def __init__(self, irradiance_manager, optimization,
                 electricity_generation, cultivation):
        super().__init__(irradiance_manager, optimization)
        self._electricity_generation = electricity_generation
        self._cultivation = cultivation

    def supply(self, date_time: datetime, duration_in_sec):
        irradiance = self._irradiance_manager.get_irradiance(date_time)
        light_saturation_point = self._cultivation.light_saturation_point

        pv_irradiance, crop_irradiance = self._optimization.optimize(
            irradiance, light_saturation_point)

        # allcate irradiance to electricity_generation and cultivation
        self._electricity_generation.consume_light_power(pv_irradiance)
        self._cultivation.consume_light_power(crop_irradiance)

        return (self._electricity_generation.produce_electric_energy(
                                                            duration_in_sec),
                self._cultivation.produce(duration_in_sec))
