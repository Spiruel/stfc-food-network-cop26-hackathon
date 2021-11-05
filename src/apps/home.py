import streamlit as st
import leafmap.foliumap as leafmap


def app():
    st.title("One Stop Crop Shop")
    st.subheader("A one-stop shop for sustainable farming")

    st.markdown(
        """
        This web app demonstrates various features to provide smallholder farmers with timely 
        and location-specific advice about the crop types and varieties they should grow. 
        Our challenge for the hackathon is to bring together hugely varied datasets - from market price data to soil maps - 
        to design an integrated open access platform for recommending crop type, planting date and management advice 
        for smallholder farmers in India.
        """
    )

    st.info("Click on the left sidebar menu to navigate to the different apps.")

    st.subheader("App features")

    row1_col1, row1_col2, _, _ = st.columns(4)
    with row1_col1:
        st.image(width=256,caption='Find the best type of crop to plant in your field', image="https://cdn3.iconfinder.com/data/icons/farm-outline-5/32/Farm_agriculture_hand_plant_grow_nature-512.png")
        st.image(width=256,caption='Find the best sowing and harvest dates by comparing to previous data', image="https://cdn4.iconfinder.com/data/icons/48-bubbles/48/46.Calendar-512.png")

    with row1_col2:
        st.image(width=256,caption='Find fertiliser recommendations for your soil and crop type',image="https://cdn2.iconfinder.com/data/icons/planting-and-house-plants-fill-natural-green-thumb/512/Fertilizer-512.png")
        st.image(width=256,caption='Explore local market information for your chosen crop',image="https://cdn4.iconfinder.com/data/icons/multimedia-75/512/multimedia-12-512.png")
