import streamlit as st
import leafmap.foliumap as leafmap
#import geemap.foliumap as geemap
import geemap
import config
import utils
import pandas as pd

def app():

    st.title("Crop market data")

    def _update_slider(width_value, height_value, zoom_value, lat_value, lon_value):
        st.session_state["width_slider"] = width_value
        st.session_state["height_slider"] = height_value
        st.session_state["zoom_slider"] = zoom_value
        st.session_state["lat_slider"] = lat_value
        st.session_state["lon_slider"] = lon_value

    if "width_slider" not in st.session_state:
        st.session_state["width_slider"] = 700
    if "height_slider" not in st.session_state:
        st.session_state["height_slider"] = 500
    if "zoom_slider" not in st.session_state:
        st.session_state["zoom_slider"] = 4
    if "lat_slider" not in st.session_state:
        st.session_state["lat_slider"] = 40
    if "lon_slider" not in st.session_state:
        st.session_state["lon_slider"] = -100

    district = 'unknown'

    col1, col2, = st.columns(2)
    with col1:
        lat, lon = 55,0
        crop_choice = st.selectbox("Select a crop", sorted(config.crops), index=0)

        keyword = st.text_input("Search location:", "")
        if keyword:
            locations = geemap.geocode(keyword)
            if locations is not None and len(locations) > 0:
                str_locations = [str(g)[1:-1] for g in locations]
                location = st.selectbox("Select a location:", str_locations)
                loc_index = str_locations.index(location)
                selected_loc = locations[loc_index]
                lat, lon = selected_loc.lat, selected_loc.lng
                st.text("")
                st.info(f"Longitude: {lon:.2f}, Latitude: {lat:.2f}")
                district = utils.get_district(lat, lon)

        st.button(
            "Reset",
            on_click=_update_slider,
            kwargs={
                "width_value": 700,
                "height_value": 500,
                "zoom_value": 4,
                "lat_value": 40,
                "lon_value": -100,
            },
        )

        m = leafmap.Map(center=[lat, lon], zoom=6)
        m.to_streamlit(width=700, height=500)

    with col2:
        st.subheader(f"{crop_choice.title()} in the {district} district")
        market_list = utils.get_markets(district)
        if len(market_list) > 0:
            st.write(f'Nearby markets include: {", ".join(market_list)}')

        if st.button(f'Search market data for {crop_choice}'):
            if district != 'unknown':
                with st.spinner(text=f'Getting market data...'):
                    year = 2021
                    df_2021 = utils.data_gov_in_req("2fd1940c-f831-42ae-8b3c-b87fc2c44183")
                    print(df_2021.columns)
                    df_2020 = utils.data_gov_in_req("25c977b6-8e8c-4452-87fb-52d626ec5374")
                    print(df_2020.columns)
                    #df_2019 = utils.data_gov_in_req("8d779906-fe3b-4b1c-a081-6b0af25a8ab7")
                    df = pd.DataFrame([df_2021, df_2020])
                    print(df, df.columns)
                    df = df.loc[df['district'] == district]
                
                st.metric("Mean price in district", f"{df.modal_price.mean():.2f} INR", f"+99% compared to {year-1}")
                #st.table(df.head())

                def plot_market_data():
                    plot_df = df.set_index('arrival_date')
                    plot_df = plot_df.loc[plot_df.market == market_choice]
                    plot_df.index = pd.to_datetime(plot_df.index)
                    plot_df = plot_df[['min_price', 'max_price', 'modal_price']]
                    plot_container.bar_chart(plot_df)

                market_choice = st.selectbox('Select a market to view:', market_list, on_change=plot_market_data)
                plot_container = st.container()

                st.metric("Wind", "9 mph", "-8%")
                st.metric("Humidity", "86%", "-6 Compared to 1 year ago")
            else:
                st.error('Unknown district')