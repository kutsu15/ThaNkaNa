import streamlit as st  # type: ignore
import pickle
import numpy as np  # type: ignore
import os

st.title("🚗 Welcome to the Car Price App")
st.header("Please fill in the car details below")


# Script diretory
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct model path 
model_path = os.path.join(script_dir, "..", "ModelDeployment", "model_combined.pkl")

# Check if the file exists
if not os.path.exists(model_path):
    st.error("❌ Model file not found. Please ensure 'model_combined.pkl' is located in the ModelDeployment folder.")
    st.stop()

# Load the model
with open(model_path, "rb") as file:
    combined = pickle.load(file)

model = combined["model"]
encoders = combined["encoders"]


# Map labels the model was trained on

brand_model_mapping = {
    "Audi": ["A4"],
    "Datsun": ["GO", "RediGO", "redi-GO"],
    "Ford": ["Aspire", "Ecosport", "Freestyle"],
    "Honda": ["City", "Civic", "Jazz", "WR-V", "Amaze"],
    "Hyundai": ["Verna", "Creta", "Venue", "i10", "i20", "Aura", "Santro"],
    "Kia": ["Seltos", "S-Presso"],
    "Mahindra": ["KUV", "KUV100", "XUV300"],
    "Maruti": ["Alto", "Swift", "Dzire LXI", "Dzire VXI", "Dzire ZXI",
               "Baleno", "Celerio", "Wagon R", "Ignis", "Swift Dzire", "Ciaz", "Glanza"],
    "Nissan": ["Kicks", "X-Trail"],
    "Renault": ["Duster", "KWID"],
    "Skoda": ["Rapid", "Octavia", "Superb"],
    "Tata": ["Tiago", "Tigor", "Nexon"],
    "Toyota": ["Yaris", "Vitara", "CR-V"],
    "Volkswagen": ["Polo", "Vento"]
}

# Brand and Model selection

brands = sorted(brand_model_mapping.keys())
brand = st.selectbox("Select Brand:", brands)
models = sorted(brand_model_mapping[brand])
model_name = st.selectbox("Select Model:", models)


# Other input features

vehicle_age = st.slider("Vehicle Age (years):", 1, 50, 5)
km_driven = st.slider("Kilometers Driven:", 100, 380000, 50000)
mileage = st.slider("Mileage (km/l):", 4.0, 50.0, 18.0)
engine = st.slider("Engine (CC):", 500.0, 5000.0, 1200.0)
max_power = st.slider("Max Power (bhp):", 20.0, 500.0, 80.0)
seats = st.number_input("Number of Seats:", 1, 10, 5)
fuel_type = st.selectbox("Fuel Type:", ["Petrol", "Diesel"])
transmission_type = st.selectbox("Transmission Type:", ["Manual", "Automatic"])


# Safely encode categorical features safely

def safe_encode(encoder, value):
    if value in encoder.classes_:
        return encoder.transform([value])[0]
    else:
        st.error(f"Unrecognized value: {value}")
        st.stop()

brand_encoded = safe_encode(encoders["brand"], brand)
model_encoded = safe_encode(encoders["model"], model_name)
fuel_encoded = safe_encode(encoders["fuel_type"], fuel_type)
trans_encoded = safe_encode(encoders["transmission_type"], transmission_type)


# Prepare input data for prediction

input_data = np.array([[brand_encoded, model_encoded, vehicle_age, km_driven,
                        fuel_encoded, trans_encoded, mileage, engine, max_power, seats]])


# Predict price

if st.button("Get the prediction"):
    predicted_price = model.predict(input_data)[0]
    st.success(f"💰 The estimated car price is: R {predicted_price:,.2f}")
