import numpy as np 
import folium 
import streamlit as st
import pydeck as pdk
import geopandas as gpd
import plotly.express as px 
mapbox_api_key = "pk.eyJ1Ijoid2lsbGlhbmNrIiwiYSI6ImNsNmw0NWxreTA4NHkzbG10NTY1dzIxeHYifQ.syqfYgOWQrngNzdt2yKwfA"
title_ID_str = "cl6l6mrir009215np8uteip1j"
tilesize_pixels = "256"
style1 =f'https://api.mapbox.com/styles/v1/willianck/{title_ID_str}/tiles/{tilesize_pixels}/{{z}}/{{x}}/{{y}}@2x?access_token={mapbox_api_key}'

LATITUDE_COLUMN = 'latitude'

LONGITUDE_COLUMN = 'longitude'

options = st.sidebar.multiselect('What type of chargers do you want to visualise', ['Level 2 Chargers','DC Fast Chargers'])


# CS_COLORS = {
#                 "both" : [255, 255, 0, 0.7],
#                 "dc"   : [0, 125, 0, 1],
#                 "level2" : [255, 0, 0, 0.7],
# }

CS_COLORS = {
                "both": "purple",
                "dc" : "green",
                "level2": "red"
}

COLORS_R = {"purple": 153, "green": 0, "red": 255}

COLORS_G = {"purple": 51, "green": 125, "red": 0}

COLORS_B = {"purple": 255, "green": 0, "red": 0}

 


class ViewStateComponent:
    """Component to let the user set the initial view state to for example Copenhagen or Boston"""

    def __init__(self):
        # 34.0635
        # 118.4455
        self.latitude = 34.0635
        self.longitude = -118.4455
        self.zoom = 6
        self.pitch = 0.0

    # def edit_view(self):
    #     """Lets the user edit the attributes"""
    #     location = st.sidebar.selectbox("Location", options=list(LOCATIONS.keys()), index=0)
    #     self.latitude = LOCATIONS[location]["latitude"]
    #     self.longitude = LOCATIONS[location]["longitude"]

    #     self.zoom = st.sidebar.slider("Zoom", min_value=0, max_value=20, value=self.zoom)
    #     self.pitch = st.sidebar.slider(
    #         "Pitch", min_value=0.0, max_value=100.0, value=self.pitch, step=10.0
    #     )

    @property
    def view_state(self) -> pdk.ViewState:
        """The ViewState according to the attributes

        Returns:
            pdk.ViewState -- [description]
        """
        return pdk.ViewState(
            longitude=self.longitude,
            latitude=self.latitude,
            zoom=self.zoom,
            min_zoom=0,
            max_zoom=15,
            pitch=self.pitch,
            # bearing=-27.36,
        )


class ViewChargingStations:
    """The main app showing the charging stations"""

    def __init__(self,data,selections,attributes):
        self.view_state_component = ViewStateComponent()
        self.show_data = False
        self.selection = selections
        self.map = attributes
        self.data = self.format_data(data)


    # @staticmethod
    def format_data(self,data) -> gpd.GeoDataFrame:
        if not self.selection: 
            return None
        # Transform
        else:
            data["cs_color"] = data['flag_port'].map(CS_COLORS)
            data['ev_connector_types'] = data['ev_connector_types'].fillna('Unknown')
            data['ev_dc_fast_num'] =   data['ev_dc_fast_num'].fillna(0)
            data['ev_level2_evse_num'] = data['ev_level2_evse_num'].fillna(0)
            data["color_r"] = data["cs_color"].map(COLORS_R)
            data["color_g"] = data["cs_color"].map(COLORS_G)
            data["color_b"] = data["cs_color"].map(COLORS_B)
            data["color_a"] = 200

            # using dummy value to set all mask to false values
            mask = data['flag_port'] == 'dummy'
            for s  in self.selection:
                mask |= (data['flag_port']== self.map[s])
                
            data = data[mask]
            return data

         
        

    def _scatter_plotter_layer(self):
        return pdk.Layer(
            "ScatterplotLayer",
            data=self.data,
            get_position=[LONGITUDE_COLUMN, LATITUDE_COLUMN],
            # get_fill_color=[252, 136, 3],
            get_fill_color = "[color_r,color_g,color_b,color_a]",
            pickable=True,
            opacity=0.7,
            stroked=False,
            filled=True,
            wireframe=True,
            radiusScale = 250,
            radiusMinPixels = 5,
        )

    def _deck(self):
        return pdk.Deck(
            map_style="mapbox://styles/mapbox/streets-v11",
            initial_view_state=self.view_state_component.view_state,
            layers=[self._scatter_plotter_layer()],
            tooltip={"html": 
                            "<b>Station Name:</b> {station_name} <br> \
                            <b>street_address:</b> {street_address} <br> \
                            <b>Number of Level 2 chargers:</b> {ev_level2_evse_num} <br> \
                            <b>Number of DC Fast chargers:</b> {ev_dc_fast_num} <br> \
                            <b>EV network:</b> {ev_network} <br> \
                            <b>Connector types:</b> {ev_connector_types}",  "style": {"color": "white"}
                    },
                         )

   # [
            #     "cs_color",'ev_network', 'city', 'County' , 'station_name' ,
            #     'street_address', 'id', LATITUDE_COLUMN, LONGITUDE_COLUMN, 'ev_connector_types', 
            #     'ev_dc_fast_num','ev_level2_evse_num','color_r','color_g','color_b','color_a'

            # ]
    # @st.cache(show_spinner=False)
    # caching the view function stops the map form displayinh
    def view(self):
        """Main view of the app"""

        st.pydeck_chart(self._deck())

        st.json(CS_COLORS)




# =========== for page 2 and 3 



class Choroplethmap():
    def __init__(self,data,selection,attributes,style,highlight,fields,aliases,scale) -> None:
        self.data =  data
        self.selection = selection
        self.attributes = attributes
        self.style = style
        self.highlight = highlight
        fields.append(self.attributes[self.selection])
        self.fields = fields
        aliases.append(f"{self.selection}:")
        self.aliases = aliases
        self.scale = scale
        self.zoom = 8.5

    
    def center(self):
        return self.data.centroid.y.mean(),self.data.centroid.x.mean()
        # self.data = self.data.to_crs(epsg=4326)
        # return y,x  
       

    
    def threshold(self):
        threshold_scale = np.linspace(self.data[self.attributes[self.selection]].min(),
                              self.data[self.attributes[self.selection]].max(),
                              self.scale, dtype=float)
        threshold_scale = threshold_scale.tolist() # change the numpy array to a list
        threshold_scale[-1] = threshold_scale[-1]
        return threshold_scale

    #  attribute is the one variable we want to analyse
    #  legend is the title 
    # info fields are the additional meta data that  you can see when hovering over the data
    # alises are the descriptions 
    # OrRd

    def add_choropleth(self):
        maps = folium.Choropleth(
        geo_data= self.data,
        name='Choropleth',
        data= self.data,
        columns=['GEOID',self.attributes[self.selection]],
        key_on="feature.properties.GEOID",
        fill_color='Reds',
        threshold_scale= self.threshold(),
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name= "Intensity",
        smooth_factor=0
        )
        return maps

    # @st.cache()
    # caching the show_map function raises a concerning warning
    def show_map(self,maps):
        # print(self.attributes)
        # st.write(self.attributes)
        x_map, y_map = self.center()
        mainmap =  folium.Map(location=[x_map, y_map], zoom_start=self.zoom,tiles=f'https://api.mapbox.com/styles/v1/willianck/{title_ID_str}/tiles/{tilesize_pixels}/{{z}}/{{x}}/{{y}}@2x?access_token={mapbox_api_key}', attr="Mapbox")
        # maps = self.add_choropleth()
        maps.add_to(mainmap)
    # folium.LayerControl().add_to(mainmap)
        child = folium.features.GeoJson(
                                        self.data,
                                        style_function=self.style, 
                                        control=False,
                                        highlight_function=self.highlight,
                                        tooltip=folium.features.GeoJsonTooltip(
                                        fields= self.fields,
                                        aliases=self.aliases,
                                        style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;")
                                                        )
                                                        )    
        mainmap.add_child(child)
        mainmap.keep_in_front(child)
        folium.LayerControl().add_to(mainmap)
        return mainmap                                                 


def pairwiseplot(data,x,y,xaxes,yaxes,component,size,color):
        fig = px.scatter(data,x=x,y=y,size=size,color=color)
        fig.update_xaxes(title=xaxes)
        fig.update_yaxes(title=yaxes)
        component.plotly_chart(fig,use_container_width=True)
    
def barchartplot(data,x,xaxes,yaxes,component):
        fig = px.bar(data, x = data[x].unique() , y=data[x].value_counts(),color=data[x].unique())
        fig.update_xaxes(title=xaxes)
        fig.update_yaxes(title=yaxes)
        component.plotly_chart(fig,use_container_width=True)


