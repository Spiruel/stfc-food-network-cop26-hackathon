# STFC FN+ COP26 Hackathon
<table>
<tr>
<th><img src="handbook/img/fn_logo.png" alt="alt text" height="50"/></th>
<th><img src="handbook/img/csa_orig.png" alt="alt text" height="50"/></th>
<th><img src="handbook/img/ibm_res.jpeg" alt="alt text" height="50"/></th>
<th><img src="handbook/img/stfc_logo.png" alt="alt text" height="50"/></th>
</tr>
</table>

## Event Handbook
This handbook contains all the necessary information for participants of the event. If you have any queries about the materials provided or find a problem, please email [helpdesk@joefennell.org](helpdesk@joefennell.org)

## 1. The Challenge
Through our partnerships with UKRI STFC, STFC Hartree Centre, IBM Research, and the [Centre for Sustainable Agriculture](https://csa-india.org/) we have identified a need to provide smallholder farmers with timely and location-specific advice about the crop types and varieties they should grow. Our challenge for the hackathon is to bring together hugely varied datasets - from market price data to soil maps - to design an integrated **open access** platform for recommending crop type, planting date and management advice for smallholder farmers in India.

More information about the e-Krishi project can be found in the pdf: `SFN Hackathon-CSA-eKrishi-TRANSSITioN-SC.pdf`

## 2. Pre-event activities
### 2.1. Register with Open Government Data Platform India

This data service is part of the Indian Open Government Data initiative and provides a large number of datasets across multiple sectors. It is important to register for an account as you will need an API Key to access the database.

[Click Here To Register](https://auth.mygov.in/user/register?destination=oauth2/register/datagovindia)

### 2.2. Check you can access your API key
<img src="handbook/img/data.gov.in.png" alt="alt text" height="150"/>

### 2.3. Get a Google Account and register for Google Earth Engine [optional]
Google Earth Engine allows you to access and process different geospatial datasets. The service is free with a limit on the amount of processing you can request.

[Click Here To Register](https://earthengine.google.com/)

## 3. Participation and Agenda
Firstly, please read the [code of conduct](CODE_OF_CONDUCT.md) and the terms and conditions of entry. By participating in this event, you agree to adhere to the behaviour code and the terms and conditions.

Secondly, please make a note of the times of the two mandatory sessions: 10:00 - 11:00 GMT on Tuesday 2nd November and 14:15 - 16:15 GMT on Friday 5th November.

| **Tuesday 2nd November**| | |
|:--- |:--- |:--- |
10:00-10:30 GMT | Welcome and Introduction | Professor Sonal Choudhury
10:30-11:00 GMT | Q&A: Technical/Practical Advice | Dr Joe Fennell
**Friday 5th November**
14:00 GMT | Deadline for slide submission | send to [helpdesk@joefennell.org](helpdesk@joefennell.org)
14:15-15:30 GMT | Team pitch |
15:30-16:00 GMT | Judging (offline) |
16:00 - 16:15 GMT| Award

## 4. Your pitch
Your team will produce a 10 minute pitch that showcases your idea and present this in the session on Friday. The format is up to you, but remember this is a pitch for funding, so you need to present a coherent argument for why and how your app will support the objectives of the project.

It could include :
- [**User Stories**](https://www.atlassian.com/agile/project-management/user-stories) Descriptions of why and how your users will interact with the platform
- **Results**  from the data experiments you carry out during the hackathon
- **How the app will work** This could include a description of analysis strategies
- **Visualisations** This could be example interfaces shown as mock-ups, wireframes or prototype demonstrations
- **Management** How your team will use the investment to produce the platform. How will you keep it running?

You must submit your slides by 14:00 GMT on Friday 5th of November (email slides or a link to [helpdesk@joefennell.org](helpdesk@joefennell.org)). Slides
submitted later than this will not be accepted, but you will still be able to
pitch (without slides).

Alternatively, you are welcome to submit a video presentation of no more than 10
minutes by the slide deadline. This should be hosted on Youtube or Vimeo and cannot be edited after the deadline. Note that these services take time to process a video, so you should aim to upload an hour before the deadline. Please email the link as above.

## 5. Recommended Datasets
We have included data gathered by project partners as well as relevant 3rd party geospatial data providers.

### 5.1. Accessing the Tutorial Notebooks

The following assumes you have a working Python Anaconda 3 installation and some experience of Jupyter Lab/Jupyter Notebook. If you do not have this, you can download and install [Anaconda here](https://www.anaconda.com/products/individual) and find learning resources on their webpages.

If you would like to run the tutorials, you will need to clone the repository and install the dependencies into a conda environment:

```bash
git clone git@github.com:joe-fennell/stfc-food-network-cop26-hackathon.git
cd stfc-food-network-cop26-hackathon
conda env create --file=environment.yaml
conda activate cop26
```

You can now launch a Jupyter Labs server session:

```bash
jupyter lab
```

This will start the server and open a web browser pointing to the correct url (normally `http://localhost:8888/lab`).

You will then be able to access the three notebooks (.ipynb file extension) included with this handbook.

### 5.2. Farm survey data
This is a 4 year farm survey with the yield and crop type along with incomplete spatial information. The dataset is included in this repository at `data/sample_data_gov_in.csv`

| Field | Description | dtype |
| --- | --- | --- |
Year | Year of survey | int
Farmer Tracenet code | unique farmer code | str
Village | Village of farm | str
District | District of farm | str
State | State of farm | str
Latitude | Latitude of farm. Although may not be exact | float
Longitude | Longitude of farm (May not be exact) | float
Crops | Crop type | str
Area (HA) | Area of that crop type | float
Estimated yield | Weight of crop in metric tonnes | float

You can find a quick introduction and example analysis in the notebook [1_Farm_survey_data.ipynb](1_Farm_survey_data.ipynb).

### 5.3. Market data from Indian Government
The [data.gov.in](https://data.gov.in) website has over 300,000 datasets. Part of this hackathon is about exploring the breadth and quality of these data. The most relevant section is probably the [agricultural markets section](https://data.gov.in/sector/agricultural-marketing).

An example dataset is the Daily Market Prices of Garlic across India. The holding
page is here: [https://data.gov.in/resources/variety-wise-daily-market-prices-garlic-2021/api](https://data.gov.in/resources/variety-wise-daily-market-prices-garlic-2021/api) displaying the resource ID.

You can then make an API request over https to download a CSV. e.g.

https://api.data.gov.in/resource/af4ed290-ed4f-40e1-a8b8-a4440e57a9ed?api-key=579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b&format=csv&offset=0

> Note that the `api-key` has been set to a test key that limits the number of
records to 10. You can replace this with the key in your user space (see section 2.2).

The response from this request is located in `data/sample_data_gov_in.csv`

There is a pip-installable package called `datagovindia` that offers a Python interface
to the data service: [visit project pages](https://pypi.org/project/datagovindia/).
We have not tested this.

Another option would be using the [Requests](https://pypi.org/project/requests/) library in Python to help you parse requests to the web service. You can find a short demonstration of retrieving data from the data.gov.in in the notebook [2_data_gov_india.ipynb](2_data_gov_india.ipynb)

### 5.4. Soil Data
Your project may require soils data. One source is [Soil Grids](https://data.isric.org/geonetwork/srv/eng/catalog.search#/home) who provide a [Web Mapping Service](https://maps.isric.org/) for various soil parameters. This is gridded at different spatial resolutions, but typically 250m.

You can access this in many different ways. One option would be the [OWSLib](https://geopython.github.io/OWSLib/introduction.html) Python interface. You can find a short demonstration of making a WMS request to the Soil Grids server in the notebook [3_SoilMap_WMS.ipynb](3_SoilMap_WMS.ipynb).

### 5.5. Google Earth Engine
Earth Engine is a tool giving access to many freely-available Remote Sensing datasets and allowing on-the-fly processing for various analyses. It can be accessed via the Code Editor GUI
<img src="handbook/img/ee.png" alt="alt text"/>
**Google Earth Engine Code Editor**

Alternatively it can be accessed via the Python API. An introduction Jupyter Notebook to this can be found [here](https://developers.google.com/earth-engine/guides/python_install-colab) that demonstrates how to authenticate and access Google Earth Engine resources.

### 5.6. Fertiliser, Pesticides and Disease Data
A set of 7 CSV files have been previously generated by project partners for combining different agronomic datasets. These are located in `data/agronomic/`.

A PDF document has also been supplied containing yield-fertiliser relationships for a number of different crops. This is located at `data/agronomic/eKrishi-Ferilizer Recommendation - yield equations.pdf`

### 5.7. Indian Districts
District polygons retrieved originally from [here](https://www.kaggle.com/imdevskp/india-district-wise-shape-files). The ESRI shapefile is located in `data/geospatial/india_districts.shp`

### 5.8. Other Information Sources

| Link | Type |
|:--- | :--- |
[Seednet](https://seednet.gov.in) | Crop groups and crops based on seednet
[Crop Nutrition](https://www.cropnutrition.com/efu-soil-ph) | Soil pH information
[Natural Resource Conservation Service](https://www.nrcs.usda.gov/Internet/FSE_DOCUMENTS/nrcs142p2_053260.pdf) | Soil bulk density Information
[FAO](http://www.fao.org/tempref/FI/CDrom/FAO_Training/FAO_Training/General/x6706e/x6706e06.htm) | Soil Classifications
[AgroMonitoring](https://agromonitoring.com/api) | Alternative service for remotely-sensed imagery and weather data (polygon API)
[Weather Stack](https://weatherstack.com/product) | weather data
[AccuWeather](http://apidev.accuweather.com/developers/) | weather data
[Indian Weather Service](http://nwp.imd.gov.in/dist_fcst.htm) | weather forecast data
[Krishi](https://krishi.icar.gov.in/ObservationData/) | Agricultural study/monitoring data
[Moqups](https://moqups.com/) | Wireframe and prototyping tools
