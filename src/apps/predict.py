import pandas as pd
import streamlit as st
import numpy as np
import pickle
import matplotlib.pyplot as plt
import geemap
import datetime
import utils
import config

model = pickle.load(open('clf.pkl','rb'))

b = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21]

a = ['Apple','Banana','blackgram','chickpea','coconut','coffee',
     'cotton','grapes','jute','kidney beans','lentil','maize','mango',
     'moth beans','mung bean','muskmelon','orange','papaya','pigeonpeas',
     'pomegranate','Rice','Watermelon']

a = pd.DataFrame(a,columns=['label'])
b = pd.DataFrame(b,columns=['encoded'])
classes = pd.concat([a,b],axis=1).sort_values('encoded').set_index('label')

@st.cache
def predict(X):
    pred = model.predict(X)
    return pred

@st.cache
def predict_proba(X):
    probas = model.predict_proba(X)
    return probas

def app():
    st.title('Crop Recommendation')

    b1, b2 = st.columns([5,3])

    #b2.header('Enter details')

    with b2:
        #d = st.date_input("Select a date", datetime.datetime.now(), max_value=datetime.datetime.now())
        yr = st.selectbox('Select a year:', [2020,2019,2018,2017,2016])
        area = st.number_input('Field size (Ha):', min_value=0., max_value=45., step=0.001)
        #input_choice = st.radio("",('Lookup parameters by location', 'Enter parameters manually'))

        keyword = st.text_input("Search location:", "")
        if keyword:
            locations = geemap.geocode(keyword)
            if locations is not None and len(locations) > 0:
                str_locations = [str(g)[1:-1] for g in locations]
                location = st.selectbox("Select a location:", str_locations)
                loc_index = str_locations.index(location)
                selected_loc = locations[loc_index]
                lat, lng = selected_loc.lat, selected_loc.lng
                st.info(f'Obtained parameters for ({lng:.0f}, {lat:.0f}).')
        
        predict_btn = st.button('Predict')

        '''st.markdown("**Soil Parameters**")
        n = st.number_input('Soil Organic Carbon')
        n,p,k,temp,humi,ph,rain = 0,0,0,0,0,0,0
        st.markdown("**Weather Parameters**")
        temp = st.slider('Temperature in °C', min_value=0, max_value=40, value=24)
        humi = st.slider('Humidity in %', min_value=0, max_value=100)
        rain = st.number_input('Rain Fall in mm')'''

    with b1:
        st.markdown("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.")

        recom_crop = st.empty()

        if predict_btn:
            with st.spinner(text='Predicting...'):
                X_df = utils.gee_dl_features(lat, lng, area, yr)
 
                if type(X_df) is int:
                    if X_df == 0:
                        st.error('Could not obtain soil data from GEE for this location.')
                    if X_df == 1:
                        st.error('Could not obtain ERA5 soil data from GEE for this location.')
                else:
                    try:
                        X = X_df.values

                        b2.markdown("**Downloaded parameters**")
                        b2.table(X_df.drop('Area (HA)',1).T)

                        pred = predict(X)
                        probas = predict_proba(X)

                        crop_pred = config.crops[pred[0]]
                        recom_crop.info(f"Recommended Crop: {crop_pred}")
                        #st.text(probas)

                        st.markdown('**Recommended crops**')

                        df = pd.DataFrame()
                        df['Crop'] = config.crops
                        df['Recommendation %'] = probas[0]*100
                        df = df.set_index('Crop')
                        df = df.sort_values('Recommendation %', ascending=False)

                        st.bar_chart(df)
                        st.table(df.style.highlight_max(axis=0))

                    except Exception as e:
                        st.error('There was an error running predictions.')
                        with st.expander("Error message"):
                            st.error(e)

   
    #fig, axes = plt.subplots()
    #print(a[:5].values)
    #mask = np.argsort(preds)
    #axes.bar(x=np.array(['Apple','Banana','blackgram','chickpea','coconut'])[mask],height=preds[mask])
    #st.pyplot(fig)