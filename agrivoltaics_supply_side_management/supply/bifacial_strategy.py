from agrivoltaics_supply_side_management.supply.strategy\
    import MorningSupplyStrategy, MiddaySupplyStrategy,\
        AfternoonSupplyStrategy, MiddayDepressionSupplyStrategy,\
        DefaultSupplyStrategy


class BifacialMorningSupplyStrategy(MorningSupplyStrategy):

    def _irradiance_comsumption(self, date_time):
        self._electricity_generation.consume_light_power(
            date_time=date_time)


class BifacialMiddaySupplyStrategy(MiddaySupplyStrategy):

    def _irradiance_comsumption(self, date_time):
        crop_irradiance =\
            self._irradiance_manager.ground_absorbed_irrardiance.loc[
            date_time].values[0]
        light_saturation_point = self._cultivation.light_saturation_point

        # TODO: Extract method.
        #       Create an optimization to get angle of module, not to make
        #       crop_irradiance exceed light_saturation_point
        if crop_irradiance > light_saturation_point:
            crop_irradiance = light_saturation_point

        # allocate irradiance to electricity_generation and cultivation
        self._electricity_generation.consume_light_power(
            date_time=date_time)
        self._cultivation.consume_light_power(crop_irradiance)


class BifacialAfternoonSupplyStrategy(AfternoonSupplyStrategy):

    def _irradiance_comsumption(self, date_time):
        self._electricity_generation.consume_light_power(
            date_time=date_time)


class BifacialMiddayDepressionSupplyStrategy(MiddayDepressionSupplyStrategy):

    def _irradiance_comsumption(self, date_time):
        crop_irradiance =\
            self._irradiance_manager.ground_absorbed_irrardiance.loc[
            date_time].values[0]
        light_saturation_point = self._cultivation.light_saturation_point

        # TODO: Extract method.
        #       Create an optimization to get angle of module, not to make
        #       crop_irradiance exceed light_saturation_point
        if crop_irradiance > light_saturation_point:
            crop_irradiance = light_saturation_point

        # allocate irradiance to electricity_generation and cultivation
        self._electricity_generation.consume_light_power(
            date_time=date_time)
        self._cultivation.consume_light_power(crop_irradiance)


class DefaultBifacialSupplyStrategy(DefaultSupplyStrategy):

    def _irradiance_comsumption(self, date_time):
        crop_irradiance =\
            self._irradiance_manager.ground_absorbed_irrardiance.loc[
            date_time].values[0]
        light_saturation_point = self._cultivation.light_saturation_point

        # TODO: Extract method.
        #       Create an optimization to get angle of module, not to make
        #       crop_irradiance exceed light_saturation_point
        if crop_irradiance > light_saturation_point:
            crop_irradiance = light_saturation_point

        # allocate irradiance to electricity_generation and cultivation
        self._electricity_generation.consume_light_power(
            date_time=date_time)
        self._cultivation.consume_light_power(crop_irradiance)
