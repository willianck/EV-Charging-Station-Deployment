import streamlit as st
from Home import tract_data
from helper import Choroplethmap,pairwiseplot
from streamlit_folium import folium_static 
mapbox_api_key = "pk.eyJ1Ijoid2lsbGlhbmNrIiwiYSI6ImNsNmw0NWxreTA4NHkzbG10NTY1dzIxeHYifQ.syqfYgOWQrngNzdt2yKwfA"
title_ID_str = "cl6l6mrir009215np8uteip1j"
tilesize_pixels = "256"

# st.session_state.update(st.session_state)

# if 'viewmap2' not in st.session_state:
#     st.session_state.viewmap2 = None

# if 'viz2' not in st.session_state:
#     st.session_state.viz2 =  None

st.title('Census Tract Los Angeles County')
st.sidebar.markdown('# Census Tract #')


attributes = {"EV Charging Station density ": "CS_count",
                "Electric Vehicle density" : "num EVs Tract"
                }

selection = st.sidebar.radio("Which metric do you want to visualise ?", 
            ["EV Charging Station density ", "Electric Vehicle density"])

data = tract_data


style_function = lambda x: {'fillColor': '#ffffff', 
                            'color':'#000000', 
                            'fillOpacity': 0.1, 
                            'weight': 0.1}


highlight_function = lambda x: {'fillColor': '#000000', 
                                'color':'#000000', 
                                'fillOpacity': 0.50, 
                                'weight': 0.1}


fields = ['CENSUS TRACT','Tract pop']
aliases = ['Name:','Census Tract population:']
scale = 10
 # def __init__(self,data,data_dicts,select_data,style,highlight) -> None:
map = Choroplethmap(data,selection,attributes,style_function,highlight_function,fields,aliases,scale)

with st.container():
    viewmaps = map.add_choropleth()
    resultmap = map.show_map(viewmaps)
    # if not st.session_state.viz2:
    #     st.session_state.viz2 = map.add_choropleth()
    # if not st.session_state.viewmap2:
    #     st.session_state.viewmap2 = map.show_map(st.session_state.viz2)

    # folium_static(st.session_state.viewmap2)
    folium_static(resultmap)


with st.container():
    pairwiseplot(tract_data,'CS_count','num EVs Tract','Number of charging stations','Number of EVs',st,'CS_count','CS_count')
    
