import requests
from collections import defaultdict
import plotly.graph_objs as go

API_KEY = 'w515iNqDwRxeWkDLkH7NJ9SPLkKRzQgA'
def execute():
  requestUrl = "https://api.nytimes.com/svc/topstories/v2/world.json?api-key=" + API_KEY
  requestHeaders = {
    "Accept": "application/json"
  }

  r = requests.get(requestUrl, headers=requestHeaders)
  res = r.json()
  # print(res['section'])

  # grouping raw data from response
  countries_dict = defaultdict(int)
  # info_dict = {'country': '', 'titles': [], 'links': []}
  for news_item in res['results']:
    # print(news_item['geo_facet'])
    for geo in news_item['geo_facet']:
      countries_dict[geo] += 1
      # info_dict[

  
  # Clean up country lists, does not remove more than 1 country per article
  # 'flatten' by countries ie 'Pozzallo (Italy)' -> 'Italy'
  # note: here we assume defaultdict properly removed exact duplicates
  deletion_list = []
  for country in countries_dict.keys():
    for c in countries_dict.keys():
      if c.lower().find(country.lower()) > 0 and c not in deletion_list:
        deletion_list.append(c)
  for c in deletion_list:
    del countries_dict[c]
  
  countries, news_count = [], []
  # plain english: temporarily sorted the countries_dict by its values (accessed thru .get)
  # ... then enabled reverse=True for Descending order
  for country in sorted(countries_dict, key=countries_dict.get, reverse=True):
    # print(country, countries_dict[country])
    countries.append(country)
    news_count.append(countries_dict[country])

  # For Choropleth API:
  # https://plotly.com/python-api-reference/generated/plotly.graph_objects.Choropleth.html#plotly.graph_objects.Choropleth

  # plotly - data
  fig = go.Figure(data = go.Choropleth( 
    locations = countries,
    z = news_count, 
    colorscale = 'Viridis',
    autocolorscale = False,
    reversescale = False,
    marker_line_color='darkgray',
    marker_line_width=0.5,
    colorbar_tickprefix="#",
    locationmode = 'country names',
    colorbar_title = 'News Articles per Country',
    text = news_count
  ))
  
  # plotly - layout
  fig.update_layout(
    title_text = "NYT world news by Country",
    geo = dict(
      showframe=False,
      showcoastlines=False,
      projection_type = 'equirectangular'
    ),
    annotations = [dict(
      x=0.55,
      y=0.01,
      xref='paper',
      yref='paper',
      text="source: NYT API",
      showarrow=False
    )]
  )

  fig.show()
        


  
  


execute()
