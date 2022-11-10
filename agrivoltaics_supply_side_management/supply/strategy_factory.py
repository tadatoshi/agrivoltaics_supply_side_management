from abc import abstractmethod
from datetime import datetime, time

from agrivoltaics_supply_side_management.supply.strategy \
    import MorningSupplyStrategy, MiddaySupplyStrategy, \
    AfternoonSupplyStrategy, DefaultSupplyStrategy, MiddayDepressionSupplyStrategy


class SupplyStrategyFactory:

    @abstractmethod
    def get_supply_strategy(self, irradiance_manager, optimization,
                            electricity_generation, cultivation,
                            date_time: datetime):
        pass

    def cumulative_electric_power_for_morning_peak(self):
        return self._morning_peak_supply_strategy.cumulative_electric_energy()

    def cumulative_electric_power_for_afternoon_peak(self):
        return \
            self._afternoon_peak_supply_strategy.cumulative_electric_energy()


class IrradiationShiftingStrategyFactory(SupplyStrategyFactory):

    def get_supply_strategy(self, irradiance_manager, optimization,
                            electricity_generation, cultivation,
                            date_time: datetime):
        """
        Factory method to create SupplyStrategy instance.

        Since the crop cultivation happens only during Daylight Saving Time,
        we only look at the time during Daylight Saving Time.
        """
        if time(8, 0, 0) <= date_time.time() < time(10, 0, 0):
            if ((not hasattr(self, '_morning_peak_supply_strategy')) or
                    (self._morning_peak_supply_strategy is None)):
                self._morning_peak_supply_strategy = MorningSupplyStrategy(
                    irradiance_manager, optimization,
                    electricity_generation)
            return self._morning_peak_supply_strategy
        elif time(10, 0, 0) <= date_time.time() < time(15, 0, 0):
            if ((not hasattr(self, '_midday_supply_strategy')) or
                    (self._midday_supply_strategy is None)):
                self._midday_supply_strategy = MiddaySupplyStrategy(
                    irradiance_manager, optimization,
                    electricity_generation, cultivation)
            return self._midday_supply_strategy
        elif time(15, 0, 0) <= date_time.time() < time(18, 0, 0):
            if ((not hasattr(self, '_afternoon_peak_supply_strategy')) or
                    (self._afternoon_peak_supply_strategy == None)):
                self._afternoon_peak_supply_strategy \
                    = AfternoonSupplyStrategy(
                    irradiance_manager, optimization, electricity_generation)
            return self._afternoon_peak_supply_strategy
        else:
            if ((not hasattr(self, '_default_supply_strategy')) or
                    (self._default_supply_strategy == None)):
                self._default_supply_strategy = DefaultSupplyStrategy(
                    irradiance_manager, optimization,
                    electricity_generation, cultivation)
            return self._default_supply_strategy


class DefaultStrategyFactory(SupplyStrategyFactory):

    def get_supply_strategy(self, irradiance_manager, optimization,
                            electricity_generation, cultivation,
                            date_time: datetime):
        """
        Factory method to create SupplyStrategy instance.

        Since the crop cultivation happens only during Daylight Saving Time,
        we only look at the time during Daylight Saving Time.
        """
        if time(8, 0, 0) <= date_time.time() < time(10, 0, 0):
            if ((not hasattr(self, '_morning_peak_supply_strategy')) or
                    (self._morning_peak_supply_strategy is None)):
                self._morning_peak_supply_strategy = DefaultSupplyStrategy(
                    irradiance_manager, optimization,
                    electricity_generation, cultivation)
            return self._morning_peak_supply_strategy
        elif time(10, 0, 0) <= date_time.time() < time(15, 0, 0):
            if ((not hasattr(self, '_midday_depression_supply_strategy')) or
                    (self._midday_depression_supply_strategy is None)):
                self._midday_depression_supply_strategy\
                    = MiddayDepressionSupplyStrategy(
                            irradiance_manager, optimization,
                            electricity_generation, cultivation)
            return self._midday_depression_supply_strategy
        elif time(15, 0, 0) <= date_time.time() < time(18, 0, 0):
            if ((not hasattr(self, '_afternoon_peak_supply_strategy')) or
                    (self._afternoon_peak_supply_strategy == None)):
                self._afternoon_peak_supply_strategy = DefaultSupplyStrategy(
                    irradiance_manager, optimization,
                    electricity_generation, cultivation)
            return self._afternoon_peak_supply_strategy
        else:
            if ((not hasattr(self, '_default_supply_strategy')) or
                    (self._default_supply_strategy == None)):
                self._default_supply_strategy = DefaultSupplyStrategy(
                    irradiance_manager, optimization,
                    electricity_generation, cultivation)
            return self._default_supply_strategy
