import pandas as pd
import streamlit as st
import numpy as np
import pickle
import matplotlib.pyplot as plt
import geemap
import datetime
import utils

#model = pickle.load(open('model.pkl','rb'))

b = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21]

a = ['Apple','Banana','blackgram','chickpea','coconut','coffee',
     'cotton','grapes','jute','kidney beans','lentil','maize','mango',
     'moth beans','mung bean','muskmelon','orange','papaya','pigeonpeas',
     'pomegranate','Rice','Watermelon']

a = pd.DataFrame(a,columns=['label'])
b = pd.DataFrame(b,columns=['encoded'])
classes = pd.concat([a,b],axis=1).sort_values('encoded').set_index('label')

@st.cache
def predict(n,p,k,temp,humi,ph,rain):
    pred = np.random.choice(['papaya','pigeonpeas', 'pomegranate','Rice','Watermelon'])
    return pred

@st.cache
def predict_proba(n,p,k,temp,humi,ph,rain):
    #pred = model.predict_proba([[n,p,k,temp,humi,ph,rain]])
    preds = np.random.random(size=5)
    preds /= np.sum(preds)
    return preds

def app():
    st.title('Crop Recommendation')

    b1, b2 = st.columns([5,3])

    #b2.header('Enter details')

    with b2:
        d = st.date_input("Select a date", datetime.datetime.now(), max_value=datetime.datetime.now())

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
                st.info(f'Obtained parameters for the {d.year} calendar year at ({lng:.0f}, {lat:.0f}).')

                weather_data = utils.get_weather_forecast_loc(lng, lat)
                st.json(weather_data)
        
        st.markdown("**Soil Parameters**")
        n = st.number_input('Soil Organic Carbon')
        n,p,k,temp,humi,ph,rain = 0,0,0,0,0,0,0
        st.markdown("**Weather Parameters**")
        temp = st.slider('Temperature in °C', min_value=0, max_value=40, value=24)
        humi = st.slider('Humidity in %', min_value=0, max_value=100)
        rain = st.number_input('Rain Fall in mm')

        predict_btn = st.button('Predict')

    with b1:
        st.markdown("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.")

        recom_crop = st.empty()
        recom_crop.info("Recommended Crop: pomegranate")

        if predict_btn:
            prediction = predict(n,p,k,temp,humi,ph,rain)
            recom_crop.info(f'Recommended Crop: {prediction}')

        st.markdown('**Top 5 recommended crops**')
        with st.spinner(text='predicting...'):
            n,p,k,temp,humi,ph,rain = 0,0,0,0,0,0,0
            preds = predict_proba(n,p,k,temp,humi,ph,rain)
        df = pd.DataFrame()
        df['Crop'] = ['Apple','Banana','blackgram','chickpea','coconut']
        df['Recommendation %'] = preds*100
        df = df.set_index('Crop')
        df = df.sort_values('Recommendation %')
        st.table(df.style.highlight_max(axis=0))
        st.bar_chart(df)
        #st.success('Done')

    b3, res, b4 = st.columns([1,5,1])
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Temperature", "70 °F", "1.2 °F")
    col2.metric("Wind", "9 mph", "-8%")
    col3.metric("Humidity", "86%", "4%")
    
    #fig, axes = plt.subplots()
    #print(a[:5].values)
    #mask = np.argsort(preds)
    #axes.bar(x=np.array(['Apple','Banana','blackgram','chickpea','coconut'])[mask],height=preds[mask])
    #st.pyplot(fig)

    with st.expander("Tell Me More (LP Model)"):
        st.title('Building the LP Model')

        st.markdown("""
        Factors to consider in the Linear Programming (LP) Model:
        - Which factors which will influence the optimal solution. These included the **network tariffs**, the **building consumption
        profile** and the **PV generation profile**.
        - How to obtain a global optimal solution quickly as an entire year worth of 15 minute interval data is being considered.
        - In order to properly assess the financial impact of different batteries, we need to decide on how the battery will
        be controlled. The controller could be a simple reactive one or we could do more sophisticated model predictive control.
        To keep things simple, it is assumed that the battery controller has access to perfect knowledge about what will 
        happen in the building.
        - We must initially define the variables that we are going to optimise. In this model they are the **battery state (kWh)**, 
        **battery charge (kW)** and **battery discharge (kW)**, the **total house power (kW)** and **power cost (pence)**.
        """)

        st.latex(
            """
            levelofcharge_i, \:charge_i, \:discharge_i, \:totalpower_i, \:costpower_i
            """
        )
        st.markdown(
            r"""
            The following equality and inequality constraints have to be met for each **timestep $i$**:
            """)

        st.latex(
            r"""\begin{aligned}
            totalpower[i] &= charge[i] - discharge[i] + load[i] - solarpv[i] \\
            costpower[i] &\geq timestep \cdot costbuy \cdot totalpower[i] \\
            costpower[i] &\geq timestep \cdot pricesell \cdot totalpower[i] \\
            levelofcharge[i] &\leq max\:battery\:capacity \\
            charge[i] &\leq max\:battery\:power \\
            discharge[i] &\leq max\:battery\:power \\
            \end{aligned}
            """)

        st.markdown(
            r"""
            The following expression shows the objective function which aims to minimise 
            the total cost of power over the year.
            """)

        st.latex(r"""
        min\:\sum_{i}^{Nsteps} costpower_i
        """)

        st.markdown(r"""
        where **$Nsteps$** is the total number of time steps over the year of data.
        Battery charge state constraints are as follows:
        """)

        st.latex(
            r"""\begin{aligned}
                levelofcharge[i] &= levelofcharge[i - 1] + timestep \cdot (eff \cdot charge[i] - discharge[i]) \\
                levelofcharge[0] &= initialcharge \\
                levelofcharge[Nsteps - 1] &= initialcharge
                \end{aligned}
            """
        )
        st.markdown(r"""
        where **$eff$** is the combined efficiency of the inverter and battery. The first expression states
        that the level of the battery at time $i$ has to equal the level of charge from the previous timestep
        plus the change in $charge$ and $discharge$ at the current timestep. The level of charge at the start of the 
        period is equal to $initialcharge$ and this is equal to the state of the battery at the end of the time period.
        """)
                
        st.markdown(r"""
        We can go further and change the battery size ($max\:battery\:capacity$) to a variable. Then add to the 
        objective function a term which considers the capital cost of the battery based on its $kWh$ output,
        shown below.
            """)

        st.latex(r"""
        min\:\sum_{i}^{Nsteps} (costpower_i + batt\:cost\:per\:kWh \cdot max\:battery\:capacity)
        """)
