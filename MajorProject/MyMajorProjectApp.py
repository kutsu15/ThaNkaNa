import streamlit as st
import pickle
import numpy as np
with open("decision_tree_model.pkl", "wb") as file
st.title (" Car Price App")
st.write ("Please fill in car details below")
brand_list = ['Maruti', 'Hyundai', 'Toyota', 'Honda', 'Ford', 'BMW', 'Audi', 'Tata', 'Mahindra', 'Mercedes-Benz']
brand = st.selectbox("Select Brand:", brand_list)
model_list= ['Swift', 'Baleno', 'i20', 'Creta', 'City', 'Civic', 'Fortuner', 'XUV500', '3 Series', 'A4', 'C-Class']
model_name = st.selectbox("Select Model:", model_list)
vehicle_age = st.number_input("Vehicle age:", min_value=1, max_value=50, value=5)
km_driven = st.number_input("Kilometers Driven:", min_value=100, max_value=380000, value=50000)
mileage = st.number_input("Mileage (km/l):", min_value=4, max_value=50, value=18)
engine = st.number_input("Engine:", min_value=500.0, max_value=5000.0, value=1200.0)
max_power = st.number_input("Max Power:", min_value=20.0, max_value=500.0, value=80.0)
seats = st.number_input("Number of Seats:", min_value=1.0, max_value=10.0, value=5.0)
if st.button("Predict Selling Price"):
    input_data = np.array([[vehicle_age, km_driven, mileage, engine, max_power, seats]])
predicted_price = model.predict(input_data) [0]
st.success(f" The estimated car purchase price is: R {predicted_price:,.2f}")