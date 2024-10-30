import matplotlib.pyplot as plt
from pytrends.request import TrendReq
import pandas as pd

pytrends = TrendReq(hl='en-US', tz=300)

kw_list = ["The rooms", "Inception"]
pytrends.build_payload(kw_list, cat=34, timeframe='all')

interests = pytrends.interest_over_time()

plt.plot(interests.iloc[:, 0:2])
plt.show()
