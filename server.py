import numpy as np
import joblib, json
import streamlit as st
import streamlit_theme as stt
from datetime import date

def strip_date(coe):
    coe = coe.strip()
    years = int(coe.split('/')[0])
    months = int(coe.split('/')[1])
    days = int(coe.split('/')[2])
    return years,months,days

def load_saved_artifacts():
    print("loading saved artifacts...start")
    global mapping
    global cols, v_type

    with open("../models/brand_mapping.json", "r") as f:
        mapping = json.load(f)

    with open('../models/columns.json', 'r') as f:
        cols = json.load(f)
    with open('../models/vehicle_type.json', 'r') as f:
        v_type = json.load(f)

    global model
    if model is None:
        with open('../models/XGB.pkl', 'rb') as f:
            model = joblib.load(f)
    print("loading saved artifacts...done")


def output(brand, mileage, coe_years_left, coe_months_left, coe_days_left, engin, no_own, age, vehicle_type,
           transmission):
    try:
        for i, j in mapping.items():
            if brand in j:
                b_name = i
        if transmission == 'Auto':
            transmission = 0
        elif transmission == 'Manual':
            transmission = 1
        coeleft = coe_years_left * 365 + coe_months_left * 30 + coe_days_left
        user_in = np.zeros((1, 12))
        user_in[0, :7] = [mileage, coeleft, engin, no_own, age, v_type[vehicle_type], transmission]
        brands_col = ['Exotic', 'Ultra_Lux', 'Lux', 'Eco', 'Budget']
        user_in[0, 7 + brands_col.index(b_name)] = 1
        return int(np.exp(model.predict(user_in)[0]))
    except:
        print('Please Enter Valid Input')


def main():
    today = date.today()
    stt.set_theme({'primary': '#5D6D7E'})
    st.title("Singapore Used Car Price Prediction")
    st.subheader("Predict how much your beloved car is roughly worth in the Singapore's car market")
    st.markdown("""<style>
        canvas{
            max-width:100%!important;}
        body {
            background-color:#BDC3C7;}
        </style>""",unsafe_allow_html=True)
    st.image(IMAGE)
    brand = st.selectbox('Choose Your Car Brand',brands)
    brand = brand.strip()
    mileage = st.text_input('Enter Your Mileage in KM',10000)
    try:
        mileage = int(mileage)
    except:
        st.error('Please Enter Valid Input')
    coe_years = st.text_input('COE Years Left if 0, Enter 0',5)
    try:
        coe_years = int(coe_years)
    except:
        st.error('Please Enter Valid Input')
    coe_months = st.text_input('COE Months Left if 0, Enter 0',5)
    try:
        coe_months = int(coe_months)
    except:
        st.error('Please Enter Valid Input')
    coe_days = st.text_input('COE Days Left if 0, Enter 0',0)
    try:
        coe_days = int(coe_days)
    except:
        st.error('Please Enter Valid Input')

    engine = st.text_input('Engine Capicity in CC', 1500)
    try:
        engine = int(engine)
    except:
        st.error('Please Enter Valid Input')
    no_own = st.text_input('Number of Owners', 1)
    try:
        no_own = int(no_own)
    except:
        st.error('Please Enter Valid Input')
    age = st.number_input('Age of the vehicle',1)
    vehicle_type = st.selectbox('Choose Your Vehicle Type', types)
    vehicle_type = vehicle_type.strip()
    trans = st.selectbox('Choose Transmission Type', transmission)
    trans=trans.strip()
    if st.button('Predict Price'):
        ans = output(brand=brand,mileage=mileage,coe_years_left=coe_years,coe_months_left=coe_months,
                     coe_days_left=coe_days,engin=engine,no_own=no_own,age=age,vehicle_type=vehicle_type,
                     transmission=trans)
        st.success('The Price of Your car is : '+str(ans) + ' SGD')

if __name__=='__main__':
    mapping = None
    cols = None
    model = None
    v_type = None

    load_saved_artifacts()
    brands = []
    for i in mapping.values():
        for j in i:
            brands.append(j)
    brands = sorted(brands, key=len)

    types = []
    for j in v_type.keys():
        types.append(j)

    transmission = ['Auto', 'Manual']

    IMAGE = 'car.jpg'
    main()