from pvlib import location
from pvlib import pvsystem
from pvlib import modelchain
from pvlib.temperature import TEMPERATURE_MODEL_PARAMETERS as PARAMS
from agrivoltaics_supply_side_management.util.unit_conversion \
    import UnitConversion


class ElectricityGeneration:

    def __init__(self):
        # Default value. [W/m^2] Changes depending on specific module
        # It's for standard test condition (STD) of irradiance 1000[W/m^2],
        # 25[degree-C], and Air Mass 1.5
        self._module_mpp = 210

    def consume_light_power(self, irradiance):
        assert irradiance >= 0
        self._irradiance = irradiance

    def produce_electric_power(self):

        if self._irradiance <= 1000:
            # Simple way assuming that module power changes linear to
            # irradiance with 0 as intercept.
            # For accuracy, needs to refer to module's datasheet.
            return self._module_mpp * (self._irradiance / 1000)
        else:
            return self._module_mpp

    def produce_electric_energy(self, duration_in_sec):

        return UnitConversion.j_to_wh(
                            self.produce_electric_power() * duration_in_sec)


class BifacialElectricityGeneration:

    def __init__(self, lattitude, longitude, timezone, bifacial_irradiances,
                 temp_model_parameters_type,
                 module_name, inverter_name, surface_tilt, surface_azimuth):
        """
        Arguments:
        ----------
        bifacial_irradiances: DataFrame
        """
        self._site_location = location.Location(latitude=lattitude,
                                longitude=longitude,
                                tz=timezone)

        self._bifacial_irradiances = bifacial_irradiances

        self._temp_model_parameters = PARAMS['sapm'][temp_model_parameters_type]
        cec_modules = pvsystem.retrieve_sam('CECMod')
        self._cec_module = cec_modules[module_name]
        cec_inverters = pvsystem.retrieve_sam('cecinverter')
        self._cec_inverter = cec_inverters[inverter_name]
        self._fixed_mount = pvsystem.FixedMount(surface_tilt, surface_azimuth)

    def consume_light_power(self, irradiance):
        pass

    def produce_electric_power(self, date_time=None):
        if ((not hasattr(self, '_ac_power')) or
                (self._ac_power is None)):
            pv_array = pvsystem.Array(mount=self._fixed_mount,
                module_parameters=self._cec_module,
                temperature_model_parameters=self._temp_model_parameters)
            pv_system = pvsystem.PVSystem(arrays=[pv_array],
                                    inverter_parameters=self._cec_inverter)
            model_chain = modelchain.ModelChain(pv_system,
                                                self._site_location,
                                                aoi_model='no_loss')
            model_chain.run_model_from_effective_irradiance(
                self._bifacial_irradiances)
            self._ac_power = model_chain.results.ac

        return self._ac_power.loc[date_time]
