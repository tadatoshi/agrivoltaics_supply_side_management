from agrivoltaics_supply_side_management.supply.strategy\
    import MorningSupplyStrategy, MiddaySupplyStrategy,\
        AfternoonSupplyStrategy, MiddayDepressionSupplyStrategy,\
        DefaultSupplyStrategy


class IrradianceAllocationMixin:

    def _allocate_irradiance(self, crop_irradiance, light_saturation_point,
                             date_time):

        single_inc_front_horizontal_irradiance =\
            self._irradiance_manager.inc_front_horizontal_irradiance.loc[
                date_time].values[0]
        remaining_max_usable_crop_irradiance = \
            light_saturation_point - crop_irradiance
        horizontal_pv_irradiance, remaining_usable_crop_irradiance = \
            self._optimization.optimize(
                single_inc_front_horizontal_irradiance,
                remaining_max_usable_crop_irradiance)
        crop_irradiance += remaining_usable_crop_irradiance
        pv_irradiance = \
            self._irradiance_manager.get_inc_irradiance_from_horizontal(
                horizontal_pv_irradiance)
        return crop_irradiance, pv_irradiance


class BifacialMorningSupplyStrategy(MorningSupplyStrategy):

    def _irradiance_comsumption(self, date_time):
        self._electricity_generation.consume_light_power(
            date_time=date_time)


class BifacialMiddaySupplyStrategy(MiddaySupplyStrategy,
                                   IrradianceAllocationMixin):

    def _irradiance_comsumption(self, date_time):
        crop_irradiance =\
            self._irradiance_manager.ground_absorbed_irrardiance.loc[
            date_time].values[0]
        light_saturation_point = self._cultivation.light_saturation_point

        if crop_irradiance < light_saturation_point:
            crop_irradiance, allocated_pv_irradiance =\
                self._allocate_irradiance(
                    crop_irradiance, light_saturation_point, date_time)
            self._electricity_generation.consume_light_power(
                irradiance=allocated_pv_irradiance, date_time=date_time)
        else:
            if crop_irradiance > light_saturation_point:
                crop_irradiance = light_saturation_point
            self._electricity_generation.consume_light_power(
                date_time=date_time)

        self._cultivation.consume_light_power(crop_irradiance)


class BifacialAfternoonSupplyStrategy(AfternoonSupplyStrategy):

    def _irradiance_comsumption(self, date_time):
        self._electricity_generation.consume_light_power(
            date_time=date_time)


class BifacialMiddayDepressionSupplyStrategy(MiddayDepressionSupplyStrategy,
                                             IrradianceAllocationMixin):

    def _irradiance_comsumption(self, date_time):
        crop_irradiance =\
            self._irradiance_manager.ground_absorbed_irrardiance.loc[
            date_time].values[0]
        light_saturation_point = self._cultivation.light_saturation_point

        if crop_irradiance < light_saturation_point:
            crop_irradiance, allocated_pv_irradiance =\
                self._allocate_irradiance(
                    crop_irradiance, light_saturation_point, date_time)
            self._electricity_generation.consume_light_power(
                irradiance=allocated_pv_irradiance, date_time=date_time)
        else:
            if crop_irradiance > light_saturation_point:
                crop_irradiance = light_saturation_point
            self._electricity_generation.consume_light_power(
                date_time=date_time)

        self._cultivation.consume_light_power(crop_irradiance)


class DefaultBifacialSupplyStrategy(DefaultSupplyStrategy,
                                    IrradianceAllocationMixin):

    def _irradiance_comsumption(self, date_time):
        crop_irradiance =\
            self._irradiance_manager.ground_absorbed_irrardiance.loc[
            date_time].values[0]
        light_saturation_point = self._cultivation.light_saturation_point

        if crop_irradiance < light_saturation_point:
            crop_irradiance, allocated_pv_irradiance =\
                self._allocate_irradiance(
                    crop_irradiance, light_saturation_point, date_time)
            self._electricity_generation.consume_light_power(
                irradiance=allocated_pv_irradiance, date_time=date_time)
        else:
            if crop_irradiance > light_saturation_point:
                crop_irradiance = light_saturation_point
            self._electricity_generation.consume_light_power(
                date_time=date_time)

        self._cultivation.consume_light_power(crop_irradiance)
