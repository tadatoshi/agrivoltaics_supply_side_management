class UnitConversion:

    @staticmethod
    def par_to_irradiance(par):
        assert par >= 0.0

        return par / 4.57
