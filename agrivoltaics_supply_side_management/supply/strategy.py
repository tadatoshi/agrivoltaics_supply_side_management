"""
Temporarily created to express supply pattern in order to figure out the
model to describe what is needed.
"""
from abc import abstractmethod
from datetime import datetime
import copy


class SupplyStrategy:

    def __init__(self, irradiance_manager, optimization):
        self._irradiance_manager = irradiance_manager
        self._optimization = optimization
        self._cumulative_electric_energy = 0.0

    @abstractmethod
    def supply(self, date_time: datetime, duration_in_sec):
        """
        Obtains how much electricity and crop yield are supplied
        during the given period specified by date_time timestamp
        and duration.

        Arguments
        ---------
        date_time: datetime
            Time stamp of the period of supply.
        duration_in_sec: float
            Duration in second for the period of supply.

        Returns
        -------
        electric_energy, crop_yield: tuple of (float, float)
        """
        pass

    def cumulative_electric_energy(self):
        return self._cumulative_electric_energy


class MorningSupplyStrategy(SupplyStrategy):

    def __init__(self, irradiance_manager, optimization,
                 electricity_generation):
        super().__init__(irradiance_manager, optimization)
        self._electricity_generation = electricity_generation

    def supply(self, date_time: datetime, duration_in_sec):
        irradiance = self._irradiance_manager.get_irradiance(date_time)
        self._electricity_generation.consume_light_power(irradiance)

        electric_energy\
            = self._electricity_generation.produce_electric_energy(
                                                        duration_in_sec)
        self._cumulative_electric_energy += electric_energy

        return electric_energy, 0


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

        electric_energy\
            = self._electricity_generation.produce_electric_energy(
                                                            duration_in_sec)
        self._cumulative_electric_energy += electric_energy
        crop_yield = self._cultivation.produce(duration_in_sec)

        return electric_energy, crop_yield


class AfternoonSupplyStrategy(SupplyStrategy):

    def __init__(self, irradiance_manager, optimization,
                 electricity_generation):
        super().__init__(irradiance_manager, optimization)
        self._electricity_generation = electricity_generation

    def supply(self, date_time: datetime, duration_in_sec):
        irradiance = self._irradiance_manager.get_irradiance(date_time)

        self._electricity_generation.consume_light_power(irradiance)

        electric_energy\
            = self._electricity_generation.produce_electric_energy(
                                                        duration_in_sec)
        self._cumulative_electric_energy += electric_energy

        return electric_energy, 0


class MiddayDepressionSupplyStrategy(SupplyStrategy):

    def __init__(self, irradiance_manager, optimization,
                 electricity_generation, cultivation):
        super().__init__(irradiance_manager, optimization)
        self._electricity_generation = electricity_generation
        # TODO: Find a better way to specify reduced biomass_energy_ratio
        #       due to midday depression:
        self._cultivation = self._reduce_biomass_energy_ratio(cultivation)

    def supply(self, date_time: datetime, duration_in_sec):
        irradiance = self._irradiance_manager.get_irradiance(date_time)
        light_saturation_point = self._cultivation.light_saturation_point

        pv_irradiance, crop_irradiance = self._optimization.optimize(
            irradiance, light_saturation_point)

        # allcate irradiance to electricity_generation and cultivation
        self._electricity_generation.consume_light_power(pv_irradiance)
        self._cultivation.consume_light_power(crop_irradiance)

        electric_energy\
            = self._electricity_generation.produce_electric_energy(
                                                            duration_in_sec)
        self._cumulative_electric_energy += electric_energy
        crop_yield = self._cultivation.produce(duration_in_sec)

        return electric_energy, crop_yield

    def _reduce_biomass_energy_ratio(self, cultivation):
        # TODO: Find a better way to specify reduced biomass_energy_ratio
        #       due to midday depression:
        copied_cultivation = copy.deepcopy(cultivation)
        # Rough reduction ratio. TODO: If better data are found, modify it:
        reduction_ratio = 1/2
        copied_cultivation.reduce_biomass_energy_ratio(reduction_ratio)
        return copied_cultivation


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

        electric_energy\
            = self._electricity_generation.produce_electric_energy(
                                                            duration_in_sec)
        self._cumulative_electric_energy += electric_energy
        crop_yield = self._cultivation.produce(duration_in_sec)

        return electric_energy, crop_yield
