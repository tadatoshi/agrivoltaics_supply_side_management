from datetime import datetime, time

from agrivoltaics_supply_side_management.supply.strategy\
    import MorningSupplyStrategy, MiddaySupplyStrategy, \
    AfternoonSupplyStrategy, DefaultSupplyStrategy


class SupplyStrategyFactory:

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
