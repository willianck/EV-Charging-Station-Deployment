import streamlit as st
from Home import counties_data
from helper import Choroplethmap , pairwiseplot
from streamlit_folium import folium_static 
# st.session_state.update(st.session_state)

# if 'viewmap' not in st.session_state:
#     st.session_state.viewmap = None

# if 'viz' not in st.session_state:
#     st.session_state.viz =  None


#  colours = { 'Neutral': 'rgb(128,128,128)',
#                     'Positive' : 'rgb(0,255,0)',
#                     'Negative': 'rgb(255,0,0)'
#                 }

mapbox_api_key = "pk.eyJ1Ijoid2lsbGlhbmNrIiwiYSI6ImNsNmw0NWxreTA4NHkzbG10NTY1dzIxeHYifQ.syqfYgOWQrngNzdt2yKwfA"
title_ID_str = "cl6l6mrir009215np8uteip1j"
tilesize_pixels = "256"
st.title('Counties')
st.sidebar.markdown('# Counties #')


# relevant data for map constructor 

attributes = {" EV Charging Station density ": "County_CS_count",
                "Electric Vehicle density" : "num EVs"
                }

selection = st.sidebar.radio("Which metric do you want to visualise ?", 
            [" EV Charging Station density ", "Electric Vehicle density"],key='selection_map')


data = counties_data


style_function = lambda x: {'fillColor': '#ffffff', 
                            'color':'#000000', 
                            'fillOpacity': 0.1, 
                            'weight': 0.1}


highlight_function = lambda x: {'fillColor': '#000000', 
                                'color':'#000000', 
                                'fillOpacity': 0.50, 
                                'weight': 0.1}

fields = ['County','County population']
aliases = ['Name:','County population']
scale = 10
 # def __init__(self,data,data_dicts,select_data,style,highlight) -> None:
map = Choroplethmap(data,selection,attributes,style_function,highlight_function,fields,aliases,scale)

with st.container():
    viewmaps = map.add_choropleth()
    resultmap = map.show_map(viewmaps)
    # if not st.session_state.viz:
    #     st.session_state.viz = map.add_choropleth()
    # if not st.session_state.viewmap:
    #     st.session_state.viewmap = map.show_map(st.session_state.viz)

    # folium_static(st.session_state.viewmap)
    folium_static(resultmap)


with st.container():
    pairwiseplot(counties_data,'num EVs','County_CS_count','Number of EVs','Number of charging stations',st,'num EVs','num EVs')
    

with st.container():
    pairwiseplot(counties_data,'County population','County_CS_count','Population','Number of charging stations',st,'County_CS_count','County_CS_count')

