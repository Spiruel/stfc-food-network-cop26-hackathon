import streamlit as st
from multiapp import MultiApp
from apps import (
	home,
	predict,
	fertiliser,
	market,
	sowing
)

st.set_page_config(layout="wide")


apps = MultiApp()

# Add all your application here

apps.add_app("Home", home.app)
apps.add_app("Crop recommendation", predict.app)
apps.add_app("Fertiliser recommendation", fertiliser.app)
apps.add_app("Crop market data", market.app)
apps.add_app("Crop sowing and harvest", sowing.app)

# The main app
apps.run()
