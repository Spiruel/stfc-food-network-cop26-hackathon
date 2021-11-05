import streamlit as st
import leafmap.foliumap as leafmap


def app():
    st.title("One Stop Crop Shop")
    st.subheader("A one-stop shop for sustainable farming")

    st.markdown(
        """
        This multi-page web app demonstrates various interactive web apps created using [streamlit](https://streamlit.io) and open-source mapping libraries, 
        such as [leafmap](https://leafmap.org), [geemap](https://geemap.org), [pydeck](https://deckgl.readthedocs.io), and [kepler.gl](https://docs.kepler.gl/docs/keplergl-jupyter).
        This is an open-source project and you are very welcome to contribute your comments, questions, resources, and apps as [issues](https://github.com/giswqs/streamlit-geospatial/issues) or 
        [pull requests](https://github.com/giswqs/streamlit-geospatial/pulls) to the [GitHub repository](https://github.com/giswqs/streamlit-geospatial).

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
