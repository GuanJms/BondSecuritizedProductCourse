from abc import ABC, abstractmethod

from utils.assets import Mortgage


class MortgageCalculator(ABC):

    @staticmethod
    @abstractmethod
    def calculate_payment(mortgage: Mortgage):
        pass

    @staticmethod
    @abstractmethod
    def calculate_interest_payment(mortgage: Mortgage, period: int):
        pass

    @staticmethod
    @abstractmethod
    def calculate_principal_payment(mortgage: Mortgage, period: int):
        pass

    @staticmethod
    @abstractmethod
    def calculate_remaining_principal(mortgage: Mortgage, period: int):
        pass

    @staticmethod
    @abstractmethod
    def calculate_lifecycle_payment_schedule(mortgage: Mortgage):
        pass

    @staticmethod
    @abstractmethod
    def calculate_weighted_average_life(mortgage: Mortgage, current_period: int):
        pass
