from pytrends.request import TrendReq


def get_popularity(id1, id2, id3):
    """
    Retourne un dataframe qui contient la popularité des films selon Google Trends
    Il est de la structure: dates, popularité relative 1, 2, 3
    """

    pytrends = TrendReq(hl='en-US', tz=300)

    kw_list = ["The rooms", "Inception"]
    pytrends.build_payload(kw_list, cat=34, timeframe='all')

    interests = pytrends.interest_over_time()

    return interests.iloc[:, 0:3]
