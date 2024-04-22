from utils.core import FrequencyType, RateType, RateFactory

r1 = RateFactory.create_rate(value='0.04', rate_type=RateType.FIXED, frequency=FrequencyType.ANNUALLY)

r2 = r1.__copy__()

print(r1 == r2)
print(r1 is r2)
print(id(r1.frequency))