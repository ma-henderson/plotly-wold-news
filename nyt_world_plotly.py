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
  countries_dict = {}
  for news_item in res['results']:
    # print(news_item['geo_facet'])
    for geo in news_item['geo_facet']:
      if geo not in countries_dict:
        countries_dict[geo] = {'count': 0, 'titles': [], 'links': []}
      countries_dict[geo]['count'] += 1
      countries_dict[geo]['titles'].append(news_item['title'])
      countries_dict[geo]['links'].append(news_item['url'])
  
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
  
  # print(countries_dict)
  # for c in countries_dict.keys():
  #   print(c)

  # source: https://stackoverflow.com/questions/38095250/sort-a-nested-dictionary-in-python
  countries, news_count, titles, links = [], [], [], []
  for country in sorted(countries_dict, key=lambda x: (countries_dict[x]['count']), reverse=True):
    countries.append(country)
    news_count.append(countries_dict[country]['count'])
    titles.append(countries_dict[country]['titles'])
    links.append(countries_dict[country]['links'])

  # print(countries, news_count, titles, links)

  # For Choropleth API: https://plotly.com/python-api-reference/generated/plotly.graph_objects.Choropleth.html#plotly.graph_objects.Choropleth
  # For hovertemplate details: https://plotly.com/python/hover-text-and-formatting/

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
    # hovertemplate =  ['Custom text {}'.format(i + 1) for i in range(5)]
    customdata = titles,
    hovertemplate =  '<b>%{location}</b><br>'
                  + '<br>%{customdata[0]}'
                  + '<br>%{customdata[1]}'
                  + '<br>%{customdata[2]}'
                  + '<extra></extra>'
    # text = ['{}<br>'.format(i) for i in titles]
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
