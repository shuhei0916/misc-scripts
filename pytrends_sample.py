from pytrends.request import TrendReq

pytrends = TrendReq()

trending_data = pytrends.trending_searches(pn='japan')

top_trendds = trending_data.head(10)
print(top_trendds)
