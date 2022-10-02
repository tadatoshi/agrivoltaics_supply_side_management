class UnitConversion:

    @staticmethod
    def par_to_irradiance(par):
        assert par >= 0.0

        return par / 4.57

    @staticmethod
    def wh_to_mj(energy_in_wh):
        assert energy_in_wh >= 0.0

        return energy_in_wh * 60 * 60 / 1000000

    @staticmethod
    def j_to_wh(energy_in_j):
        assert energy_in_j >= 0.0

        return energy_in_j / 60 / 60

    @staticmethod
    def ton_per_ha_to_kg_per_m2(value_ton_per_ha):
        assert value_ton_per_ha >= 0.0

        return value_ton_per_ha * 1000 / 100000
