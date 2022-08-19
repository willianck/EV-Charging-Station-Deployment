import streamlit as st
st.set_page_config(layout='wide')
import pandas as pd
import geopandas as gpd
from shapely import wkt
import warnings
from shapely.errors import ShapelyDeprecationWarning
warnings.filterwarnings("ignore", category=ShapelyDeprecationWarning) 
from helper import  ViewChargingStations, barchartplot
import ast 
import plotly.express as px 
import json 

# clear map monochrome

st.session_state.update(st.session_state)



mapbox_api_key = "pk.eyJ1Ijoid2lsbGlhbmNrIiwiYSI6ImNsNmw0NWxreTA4NHkzbG10NTY1dzIxeHYifQ.syqfYgOWQrngNzdt2yKwfA"
title_ID_str = "cl6l6mrir009215np8uteip1j"
tilesize_pixels = "256"

def string_to_list(x):
  if x!= "":
    x = ast.literal_eval(x)
    x = [n.strip() for n in x]
  return x

def fill_connectors(conn,connectors):
    if conn!="":
      for x in conn:
        connectors[x] = 1 + connectors.get(x,0)




st.title('Charging Stations')
st.sidebar.image('/Users/william/Desktop/capstone/icon.png',width=100)
st.sidebar.markdown("<div><h1 style='display:inline-block'>EV Analytics</h1><div>",unsafe_allow_html=True)
# st.sidebar.markdown("<div><img src ='https://www.kindpng.com/imgv/ixwowhm_labor-analytics-icon-analytics-icon-png-transparent-png/' width=100 /><h1 style='display:inline-block'>EV Analytics</h1><div>",unsafe_allow_html=True)
st.sidebar.markdown("This dashboard is used to analyse EV and EV stations data")
st.sidebar.markdown("To get started simply select an option from selection box")

df =  pd.read_csv('/Users/william/Desktop/captsone/CS_merge.csv')
@st.cache(show_spinner=False,allow_output_mutation=True)
def load_data():
#  loading the different data set we need 
    ct_data = pd.read_csv('/Users/william/Desktop/capstone/census_tract_merge.csv')
    cis_data = pd.read_csv('/Users/william/Desktop/capstone/counties_data_merge.csv')
    cs_data = pd.read_csv('/Users/william/Desktop/capstone/CS_merge.csv')
    ct_data = ct_data[ct_data['County'] == 'Los Angeles County']

    ct_data['geometry'] = ct_data['geometry'].apply(wkt.loads)
    cis_data['geometry'] = cis_data['geometry'].apply(wkt.loads)
    cs_data['geometry'] = cs_data['geometry'].apply(wkt.loads)
    
    ct_data  = gpd.GeoDataFrame(ct_data, crs='epsg:4326')
    cis_data =  gpd.GeoDataFrame(cis_data, crs='epsg:4326')
    cs_data  =  gpd.GeoDataFrame(cs_data, crs='epsg:4326')
    ct_data.set_geometry(col='geometry', inplace=True)
    cis_data.set_geometry(col='geometry', inplace=True)
    cs_data.set_geometry(col='geometry', inplace=True)

    f = open('/Users/william/Desktop/captsone/connectors.json')
    connectors = json.load(f)
    # ct_data = ct_data.to_crs(epsg=3035)
    # cis_data = cis_data.to_crs(epsg=3035)
    # cs_data = cs_data.to_crs(epsg=3035)
    return ct_data,cis_data,cs_data,connectors


# street map v-11
# mapbox_api_key = "pk.eyJ1Ijoid2lsbGlhbmNrIiwiYSI6ImNsNmw1enhnMDA4cmwzZW8wczN0NDV2MG4ifQ.yId4w-pxZ-Jvo41CDh6PEw"
# tileset_ID_str = "streets-v11"



tract_data , counties_data , cs_data, connectors = load_data()

option_map = {'Level 2 Chargers only': 'LEVEL 2',
                 'DC Fast Chargers only': 'DC FAST',
                  'Level 2 and DC Fast': 'BOTH'}


data_dicts = {'Level 2 Chargers only': 'level2',
                 'DC Fast Chargers only': 'dc',
                  'Level 2 and DC Fast': 'both'}





with st.container():
    options = st.multiselect('For the EV stations, what type of chargers do you want to visualise',
     ['Level 2 Chargers only','DC Fast Chargers only','Level 2 and DC Fast'],
     format_func=lambda x: option_map[x],key ='multiselect')

    charging_stations = ViewChargingStations(cs_data,options,data_dicts)
    charging_stations.view()

with st.container():
    st.markdown('# Chargers Port distribution #')
    left_col , right_col = st.columns(2,gap='large')
    all_counties =  cs_data['County'].unique()
    county_options = right_col.selectbox('Which County do you want to look at ',all_counties,key='county_port')
    data_subset = cs_data[cs_data['County']== county_options]
    barchartplot(cs_data,'flag_port','Type of EV Port','Number of Ports',left_col)
    barchartplot(data_subset,'flag_port','Type of EV Port','Number of Ports',right_col)



with st.container():
    st.markdown(' # EV Connector Types distribution')
    fig = px.bar(x = connectors.keys(), y=connectors.values(),color=connectors.keys())
    fig.update_xaxes(title='EV Connector Types')
    fig.update_yaxes(title='Number of Connectors')
    st.plotly_chart(fig,use_container_width=True)


with st.container():
    st.markdown('# EV Network distribution')
    barchartplot(cs_data,'ev_network','EV Network','Number of stations',st)







    
   



    



