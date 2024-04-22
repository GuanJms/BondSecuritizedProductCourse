from utils.core import Value, Rate, Time


class Loan:
    def __init__(self, principal: Value | None, rate: Rate | None, maturity: Time | None):
        self._principal = principal
        self._rate = rate
        self._maturity = maturity

    @property
    def principal(self) -> Value:
        return self._principal

    @property
    def rate(self) -> Rate:
        return self._rate

    @property
    def maturity(self) -> Time:
        return self._maturity
