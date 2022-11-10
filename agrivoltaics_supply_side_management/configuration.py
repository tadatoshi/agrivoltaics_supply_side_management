from abc import abstractmethod
import pandas as pd

from agrivoltaics_supply_side_management.agriculture.photosynthetic_rate \
    import PhotosyntheticRate
from agrivoltaics_supply_side_management.supply.strategy_factory \
    import IrradiationShiftingStrategyFactory, DefaultStrategyFactory


class Configuration:

    def __init__(self, net_photosynthetic_rate_parameters, ppfd_data,
                 irradiance_manager, optimization,
                 electricity_generation, cultivation):
        self._net_photosynthetic_rate_parameters \
            = net_photosynthetic_rate_parameters
        self._ppfd_data = ppfd_data
        self._irradiance_manager = irradiance_manager
        self._optimization = optimization
        self._electricity_generation = electricity_generation
        self._cultivation = cultivation

    @abstractmethod
    def supply_strategy_factory(self):
        pass

    @abstractmethod
    def light_saturation_point(self):
        pass

    def supply(self, time_range):
        self._cultivation.light_saturation_point \
            = self.light_saturation_point()

        duration_in_sec = pd.to_timedelta(time_range.freq).total_seconds()

        total_electricity_supply = 0
        total_crop_yield = 0

        for time in time_range:
            supply_strategy = self.supply_strategy_factory(
            ).get_supply_strategy(
                self._irradiance_manager, self._optimization,
                self._electricity_generation, self._cultivation, time)
            electricity_supply, crop_yield = supply_strategy.supply(
                time, duration_in_sec)
            total_electricity_supply += electricity_supply
            total_crop_yield += crop_yield

        cumulative_electric_power_for_morning_peak \
            = self.supply_strategy_factory(
        ).cumulative_electric_power_for_morning_peak()

        cumulative_electric_power_for_afternoon_peak \
            = self.supply_strategy_factory(
        ).cumulative_electric_power_for_afternoon_peak()

        return total_electricity_supply, total_crop_yield, \
               cumulative_electric_power_for_morning_peak, \
               cumulative_electric_power_for_afternoon_peak


class VerticalPvConfiguration(Configuration):

    def supply_strategy_factory(self):
        if ((not hasattr(self, '_supply_strategy_factory')) or
                (self._supply_strategy_factory is None)):
            self._supply_strategy_factory \
                = IrradiationShiftingStrategyFactory()
        return self._supply_strategy_factory

    def light_saturation_point(self):
        light_saturation_point = \
            PhotosyntheticRate.find_light_saturation_point(
                self._net_photosynthetic_rate_parameters['phi'],
                self._net_photosynthetic_rate_parameters['alpha'],
                self._net_photosynthetic_rate_parameters['theta'],
                self._net_photosynthetic_rate_parameters['p_max'],
                self._ppfd_data)
        return light_saturation_point


class OpticalFilmConfiguration(Configuration):

    def supply_strategy_factory(self):
        if ((not hasattr(self, '_supply_strategy_factory')) or
                (self._supply_strategy_factory is None)):
            self._supply_strategy_factory \
                = IrradiationShiftingStrategyFactory()
        return self._supply_strategy_factory

    def light_saturation_point(self):
        pass


class SemitransparentPvConfiguration(Configuration):

    def supply_strategy_factory(self):
        if ((not hasattr(self, '_supply_strategy_factory')) or
                (self._supply_strategy_factory is None)):
            self._supply_strategy_factory \
                = IrradiationShiftingStrategyFactory()
        return self._supply_strategy_factory

    def light_saturation_point(self):
        pass


class DefaultConfiguration(Configuration):

    def supply_strategy_factory(self):
        if ((not hasattr(self, '_supply_strategy_factory')) or
                (self._supply_strategy_factory is None)):
            self._supply_strategy_factory = DefaultStrategyFactory()
        return self._supply_strategy_factory

    def light_saturation_point(self):
        light_saturation_point = \
            PhotosyntheticRate.find_light_saturation_point(
                self._net_photosynthetic_rate_parameters['phi'],
                self._net_photosynthetic_rate_parameters['alpha'],
                self._net_photosynthetic_rate_parameters['theta'],
                self._net_photosynthetic_rate_parameters['p_max'],
                self._ppfd_data)
        return light_saturation_point
