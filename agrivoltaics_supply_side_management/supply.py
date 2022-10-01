"""
Temporarily created to express supply pattern in order to figure out the
model to describe what is needed.
"""
from abc import abstractmethod
from datetime import datetime, time


class SupplyStrategy:

    def __init__(self, irradiance_manager, optimization):
        self._irradiance_manager = irradiance_manager
        self._optimization = optimization

    @classmethod
    def get_supply_strategy(cls, irradiance_manager, optimization,
                            electricity_generation, cultivation,
                            date_time: datetime):
        """
        Factory method to create SupplyStrategy instance.

        Since the crop cultivation happens only during Daylight Saving Time,
        we only look at the time during Daylight Saving Time.
        """
        if time(8, 0, 0) <= date_time.time() < time(10, 0, 0):
            if ((not hasattr(cls, '_morning_supply_strategy')) or
                    (cls._morning_supply_strategy is None)):
                cls._morning_supply_strategy = MorningSupplyStrategy(
                    irradiance_manager, optimization,
                    electricity_generation)
            return cls._morning_supply_strategy
        elif time(10, 0, 0) <= date_time.time() < time(15, 0, 0):
            if ((not hasattr(cls, '_midday_supply_strategy')) or
                    (cls._midday_supply_strategy is None)):
                cls._midday_supply_strategy = MiddaySupplyStrategy(
                    irradiance_manager, optimization,
                    electricity_generation, cultivation)
            return cls._midday_supply_strategy
        elif time(15, 0, 0) <= date_time.time() < time(18, 0, 0):
            if ((not hasattr(cls, '_afternoon_supply_strategy')) or
                    (cls._afternoon_supply_strategy == None)):
                cls._afternoon_supply_strategy = AfternoonSupplyStrategy(
                    irradiance_manager, optimization, electricity_generation)
            return cls._afternoon_supply_strategy
        else:
            if ((not hasattr(cls, '_default_supply_strategy')) or
                    (cls._default_supply_strategy == None)):
                cls._default_supply_strategy = DefaultSupplyStrategy(
                    irradiance_manager, optimization,
                    electricity_generation, cultivation)
            return cls._default_supply_strategy

    @abstractmethod
    def supply(self):
        pass


class MorningSupplyStrategy(SupplyStrategy):

    def __init__(self, irradiance_manager, optimization,
                 electricity_generation):
        super().__init__(irradiance_manager, optimization)
        self._electricity_generation = electricity_generation

    def supply(self, date_time: datetime):
        irradiance = self._irradiance_manager.get_irradiance(date_time)
        self._electricity_generation.consume_light_power(irradiance)

        return self._electricity_generation.produce_electric_power(), 0


class MiddaySupplyStrategy(SupplyStrategy):

    def __init__(self, irradiance_manager, optimization,
                 electricity_generation, cultivation):
        super().__init__(irradiance_manager, optimization)
        self._electricity_generation = electricity_generation
        self._cultivation = cultivation

    def supply(self, date_time: datetime):
        irradiance = self._irradiance_manager.get_irradiance(date_time)
        light_saturation_point = self._cultivation.light_saturation_point()

        pv_irradiance, crop_irradiance = self._optimization.optimize(
            irradiance, light_saturation_point)

        # allcate irradiance to electricity_generation and cultivation
        self._electricity_generation.consume_light_power(pv_irradiance)
        self._cultivation.consume_light_power(crop_irradiance)

        return (self._electricity_generation.produce_electric_power(),
                self._cultivation.produce())


class AfternoonSupplyStrategy(SupplyStrategy):

    def __init__(self, irradiance_manager, optimization,
                 electricity_generation):
        super().__init__(irradiance_manager, optimization)
        self._electricity_generation = electricity_generation

    def supply(self, date_time: datetime):
        irradiance = self._irradiance_manager.get_irradiance(date_time)

        self._electricity_generation.consume_light_power(irradiance)

        return self._electricity_generation.produce_electric_power(), 0


class DefaultSupplyStrategy(SupplyStrategy):

    def __init__(self, irradiance_manager, optimization,
                 electricity_generation, cultivation):
        super().__init__(irradiance_manager, optimization)
        self._electricity_generation = electricity_generation
        self._cultivation = cultivation

    def supply(self, date_time: datetime):
        irradiance = self._irradiance_manager.get_irradiance(date_time)
        light_saturation_point = self._cultivation.light_saturation_point()

        pv_irradiance, crop_irradiance = self._optimization.optimize(
            irradiance, light_saturation_point)

        # allcate irradiance to electricity_generation and cultivation
        self._electricity_generation.consume_light_power(pv_irradiance)
        self._cultivation.consume_light_power(crop_irradiance)

        return (self._electricity_generation.produce_electric_power(),
                self._cultivation.produce())
