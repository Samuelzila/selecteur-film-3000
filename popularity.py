from pytrends.request import TrendReq
import bdd


def get_popularity(id1, id2, id3):
    """
    Retourne un dataframe qui contient la popularité des films selon Google Trends
    Il est de la structure: dates, popularité relative 1, 2, 3
    """

    pytrends = TrendReq(hl='en-US', tz=300)

    titles = (bdd.get_title(id1), bdd.get_title(id2), bdd.get_title(id3))
    kw_list = [titles[0], titles[1], titles[2]]
    pytrends.build_payload(kw_list, cat=34, timeframe='all')

    interests = pytrends.interest_over_time()

    return interests.loc[:, kw_list]
