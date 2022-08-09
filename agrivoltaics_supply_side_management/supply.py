"""
Temporarily created to express supply pattern in order to figure out the
model to describe what is needed.
"""
from datetime import datetime, time


class SupplyStrategy:

    @staticmethod
    def create(date_time: datetime):
        """
        Factory method to create SupplyStrategy instance.

        Since the crop cultivation happens only during Daylight Saving Time,
        we only look at the time during Daylight Saving Time.
        """
        if time(8, 0, 0) <= date_time.time() < time(10, 0, 0):
            return MorningSupplyStrategy()
        elif time(10, 0, 0) <= date_time.time() < time(15, 0, 0):
            return MiddaySupplyStrategy()
        elif time(15, 0, 0) <= date_time.time() < time(18, 0, 0):
            return AfternoonSupplyStrategy()
        else:
            return DefaultSupplyStrategy()

    def supply(self):
        pass


class MorningSupplyStrategy(SupplyStrategy):
    def supply(self):
        pass


class MiddaySupplyStrategy(SupplyStrategy):
    def supply(self):
        pass


class AfternoonSupplyStrategy(SupplyStrategy):
    def supply(self):
        pass


class DefaultSupplyStrategy:
    def supply(self):
        pass
