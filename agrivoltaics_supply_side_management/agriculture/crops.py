



class Cultivation:

    def consume_light_power(self, irradiance):
        self._irradiance = irradiance

    def produce(self):
        pass

    def light_saturation_point(self):
        # Default value. Subclass for a specific crop defines a different
        # value, e.g. soybean
        return 250
