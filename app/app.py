import plotly.graph_objects as go
import pandas as pd
import datetime as dt
import json

VAX_DATA_URL = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv'

# source: https://github.com/johan/world.geo.json/blob/master/countries.geo.json
GEOJSON = 'app/assets/countries.geo.json'
countries_borders_geojson = json.load(open(GEOJSON))

df = pd.read_csv(VAX_DATA_URL)

with open(GEOJSON) as geojson_file:
    geojson_countries = json.load(geojson_file)

def filter_data(df):
    df[['iso_code', 'date', 'location', 'people_vaccinated', 'population']].dropna(inplace=True)
    df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d")
    df_max_dates = df[df.groupby('iso_code').date.transform('max') == df['date']].reset_index()
    df_max_dates.drop(columns='index', inplace=True)
    df_max_dates['perc_pop_vaccinated'] = df_max_dates['people_vaccinated'] / df_max_dates['population']
    return df_max_dates

dff = filter_data(df)

def render_globe():
    choropleth = go.Choropleth(
        geojson=countries_borders_geojson,
        showscale=True,
        colorscale='Burgyl',
        zmin=0, zmax=1,
        z=dff['perc_pop_vaccinated'],
        locationmode="ISO-3",
        locations=dff.iso_code,
        featureidkey="properties.name"
    )

    scattergeo = go.Scattergeo(geojson=countries_borders_geojson)

    fig = go.Figure(data=[choropleth, scattergeo])
    fig.update_layout(
        margin={"r":0,"t":0,"l":0,"b":0},
        geo = dict(
            showland = True,
            showcountries = True,
            showocean = True,
            countrywidth = 0.5,
            landcolor = 'rgb(155, 155, 155)',
            lakecolor = 'rgb(115, 155, 355)',
            oceancolor = 'rgb(115, 155, 355)',
            projection = dict(
                type = 'orthographic',
                rotation = dict(
                    lon = 40,
                    lat = 30,
                    roll = 0
                )
            ),
            lonaxis = dict(
                showgrid = True,
                gridcolor = 'rgb(102, 102, 102)',
                gridwidth = 0.5
            ),
            lataxis = dict(
                showgrid = True,
                gridcolor = 'rgb(102, 102, 102)',
                gridwidth = 0.5
            )
        )
    )
    return fig
