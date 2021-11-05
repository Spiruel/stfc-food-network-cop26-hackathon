import pandas as pd
import streamlit as st
import numpy as np
import pickle
import matplotlib.pyplot as plt
import geemap
import datetime
import utils

fertiliser_dic = {
        'NHigh': """The N value of soil is high and might give rise to weeds.
        <br/> Please consider the following suggestions:
        <br/><br/> 1. <i> Manure </i> – adding manure is one of the simplest ways to amend your soil with nitrogen. Be careful as there are various types of manures with varying degrees of nitrogen.
        <br/> 2. <i>Coffee grinds </i> – use your morning addiction to feed your gardening habit! Coffee grinds are considered a green compost material which is rich in nitrogen. Once the grounds break down, your soil will be fed with delicious, delicious nitrogen. An added benefit to including coffee grounds to your soil is while it will compost, it will also help provide increased drainage to your soil.
        <br/>3. <i>Plant nitrogen fixing plants</i> – planting vegetables that are in Fabaceae family like peas, beans and soybeans have the ability to increase nitrogen in your soil
        <br/>4. Plant ‘green manure’ crops like cabbage, corn and brocolli
        <br/>5. <i>Use mulch (wet grass) while growing crops</i> - Mulch can also include sawdust and scrap soft woods""",

        'Nlow': """The N value of your soil is low.
        <br/> Please consider the following suggestions:
        <br/><br/> 1. <i>Add sawdust or fine woodchips to your soil</i> – the carbon in the sawdust/woodchips love nitrogen and will help absorb and soak up and excess nitrogen.
        <br/>2. <i>Plant heavy nitrogen feeding plants</i> – tomatoes, corn, broccoli, cabbage and spinach are examples of plants that thrive off nitrogen and will suck the nitrogen dry.
        <br/>3. <i>Water</i> – soaking your soil with water will help leach the nitrogen deeper into your soil, effectively leaving less for your plants to use.
        <br/>4. <i>Sugar</i> – In limited studies, it was shown that adding sugar to your soil can help potentially reduce the amount of nitrogen is your soil. Sugar is partially composed of carbon, an element which attracts and soaks up the nitrogen in the soil. This is similar concept to adding sawdust/woodchips which are high in carbon content.
        <br/>5. Add composted manure to the soil.
        <br/>6. Plant Nitrogen fixing plants like peas or beans.
        <br/>7. <i>Use NPK fertilizers with high N value.
        <br/>8. <i>Do nothing</i> – It may seem counter-intuitive, but if you already have plants that are producing lots of foliage, it may be best to let them continue to absorb all the nitrogen to amend the soil for your next crops.""",

        'PHigh': """The P value of your soil is high.
        <br/> Please consider the following suggestions:
        <br/><br/>1. <i>Avoid adding manure</i> – manure contains many key nutrients for your soil but typically including high levels of phosphorous. Limiting the addition of manure will help reduce phosphorus being added.
        <br/>2. <i>Use only phosphorus-free fertilizer</i> – if you can limit the amount of phosphorous added to your soil, you can let the plants use the existing phosphorus while still providing other key nutrients such as Nitrogen and Potassium. Find a fertilizer with numbers such as 10-0-10, where the zero represents no phosphorous.
        <br/>3. <i>Water your soil</i> – soaking your soil liberally will aid in driving phosphorous out of the soil. This is recommended as a last ditch effort.
        <br/>4. Plant nitrogen fixing vegetables to increase nitrogen without increasing phosphorous (like beans and peas).
        <br/>5. Use crop rotations to decrease high phosphorous levels""",

        'Plow': """The P value of your soil is low.
        <br/> Please consider the following suggestions:
        <br/><br/>1. <i>Bone meal</i> – a fast acting source that is made from ground animal bones which is rich in phosphorous.
        <br/>2. <i>Rock phosphate</i> – a slower acting source where the soil needs to convert the rock phosphate into phosphorous that the plants can use.
        <br/>3. <i>Phosphorus Fertilizers</i> – applying a fertilizer with a high phosphorous content in the NPK ratio (example: 10-20-10, 20 being phosphorous percentage).
        <br/>4. <i>Organic compost</i> – adding quality organic compost to your soil will help increase phosphorous content.
        <br/>5. <i>Manure</i> – as with compost, manure can be an excellent source of phosphorous for your plants.
        <br/>6. <i>Clay soil</i> – introducing clay particles into your soil can help retain & fix phosphorus deficiencies.
        <br/>7. <i>Ensure proper soil pH</i> – having a pH in the 6.0 to 7.0 range has been scientifically proven to have the optimal phosphorus uptake in plants.
        <br/>8. If soil pH is low, add lime or potassium carbonate to the soil as fertilizers. Pure calcium carbonate is very effective in increasing the pH value of the soil.
        <br/>9. If pH is high, addition of appreciable amount of organic matter will help acidify the soil. Application of acidifying fertilizers, such as ammonium sulfate, can help lower soil pH""",

        'KHigh': """The K value of your soil is high</b>.
        <br/> Please consider the following suggestions:
        <br/><br/>1. <i>Loosen the soil</i> deeply with a shovel, and water thoroughly to dissolve water-soluble potassium. Allow the soil to fully dry, and repeat digging and watering the soil two or three more times.
        <br/>2. <i>Sift through the soil</i>, and remove as many rocks as possible, using a soil sifter. Minerals occurring in rocks such as mica and feldspar slowly release potassium into the soil slowly through weathering.
        <br/>3. Stop applying potassium-rich commercial fertilizer. Apply only commercial fertilizer that has a '0' in the final number field. Commercial fertilizers use a three number system for measuring levels of nitrogen, phosphorous and potassium. The last number stands for potassium. Another option is to stop using commercial fertilizers all together and to begin using only organic matter to enrich the soil.
        <br/>4. Mix crushed eggshells, crushed seashells, wood ash or soft rock phosphate to the soil to add calcium. Mix in up to 10 percent of organic compost to help amend and balance the soil.
        <br/>5. Use NPK fertilizers with low K levels and organic fertilizers since they have low NPK values.
        <br/>6. Grow a cover crop of legumes that will fix nitrogen in the soil. This practice will meet the soil’s needs for nitrogen without increasing phosphorus or potassium.
        """,

        'Klow': """The K value of your soil is low.
        <br/>Please consider the following suggestions:
        <br/><br/>1. Mix in muricate of potash or sulphate of potash
        <br/>2. Try kelp meal or seaweed
        <br/>3. Try Sul-Po-Mag
        <br/>4. Bury banana peels an inch below the soils surface
        <br/>5. Use Potash fertilizers since they contain high values potassium
        """
    }

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
    st.title('Fertiliser Recommendation')

    b1, b2 = st.columns([5,3])

    #b2.header('Enter details')

    with b2:
        st.markdown("**Lookup precipitation forecast in your area**")
        #d = st.date_input("Select a date", datetime.datetime.now(), max_value=datetime.datetime.now())

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
                st.info(f'Location ({lng:.0f}, {lat:.0f}).')

                weather_data = utils.get_weather_forecast_loc(lng, lat)
                st.json(weather_data)

                precip_data = [(datetime.datetime.fromtimestamp(i['dt']),i['rain']['3h']) for i in weather_data['list'] if 'rain' in i.keys()]
                if len(precip_data) == 0:
                    st.success('No upcoming rain is forecast')
                else:
                    precip_df = pd.DataFrame(precip_data, columns=['date', 'precipitation / mm'])
                    precip_df = precip_df.set_index('date')
                    st.bar_chart(precip_df)
        
        st.markdown("**Soil management recommendations**")
        df = pd.read_csv('../data/archive/Fertilizer Prediction.csv')
        crop_name = st.selectbox('Select a crop type', df['Crop Type'].unique())

        n = st.slider('Nitrogen (N) value in soil', min_value=0, max_value=100)
        p = st.slider('Phosphorous (P) value in soil', min_value=0, max_value=100)
        k = st.slider('Potassium (K) value in soil', min_value=0, max_value=100)
        #ph = st.slider('pH value', min_value=6.5, max_value=8.5)
 
        nr = df[df['Crop Type'] == crop_name]['Nitrogen'].iloc[0]
        pr = df[df['Crop Type'] == crop_name]['Phosphorous'].iloc[0]
        kr = df[df['Crop Type'] == crop_name]['Potassium'].iloc[0]

        n = nr - n
        p = pr - p
        k = kr - k
        temp = {abs(n): "N", abs(p): "P", abs(k): "K"}
        max_value = temp[max(temp.keys())]
        if max_value == "N":
            if n < 0:
                key = 'NHigh'
            else:
                key = "Nlow"
        elif max_value == "P":
            if p < 0:
                key = 'PHigh'
            else:
                key = "Plow"
        else:
            if k < 0:
                key = 'KHigh'
            else:
                key = "Klow"

    with b1:
        st.markdown("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.")

        st.info(f'The soil is {key}')

        html_string = fertiliser_dic[key]
        st.info(st.markdown(html_string, unsafe_allow_html=True))

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
