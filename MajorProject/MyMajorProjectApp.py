import os
import streamlit as st  # type: ignore
import pickle
import numpy as npp

# ---------------------------
# Title and Header
# ---------------------------
st.title("🚗 Welcome to the Car Price App")
st.header("Please fill in the car details below")


# Load model and encoders safely

script_dir = os.getcwd()
model_path = os.path.join(script_dir, "MajorProject", "ModelDeployment", "model.pkl")

if not os.path.exists(model_path):
    st.error(f"❌ Model file not found. Please place 'model.pkl' in the 'MajorProject/ModelDeployment' folder.")
    st.stop()

try:
    with open(model_path, "rb") as f:
        combined = pickle.load(f)
except Exception as e:
    st.error(f"❌ Failed to load model: {e}")
    st.stop()

model = combined.get("model")
encoders = combined.get("encoders")

if model is None or encoders is None:
    st.error("❌ Model or encoders not found in the pickle file.")
    st.stop()

# ---------------------------
# Brand-Model Mapping
# ---------------------------
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

# User Inputs

brand = st.selectbox("Select Brand:", sorted(brand_model_mapping.keys()))
model_name = st.selectbox("Select Model:", sorted(brand_model_mapping[brand]))

vehicle_age = st.slider("Vehicle Age (years):", 0, 50, 5)
km_driven = st.slider("Kilometers Driven:", 0, 500000, 50000)
mileage = st.slider("Mileage (km/l):", 0.0, 50.0, 18.0)
engine = st.slider("Engine (CC):", 0.0, 5000.0, 1200.0)
max_power = st.slider("Max Power (bhp):", 0.0, 500.0, 80.0)
seats = st.number_input("Number of Seats:", 1, 10, 5)
fuel_type = st.selectbox("Fuel Type:", ["Petrol", "Diesel"])
transmission_type = st.selectbox("Transmission Type:", ["Manual", "Automatic"])


# Encode categorical features

def safe_encode(encoder, value, label):
    try:
        return encoder.transform([value])[0]
    except Exception:
        st.warning(f"⚠️ Unrecognized {label}: '{value}'. Using 0 instead.")
        return 0

brand_encoded = safe_encode(encoders["brand"], brand, "brand")
model_encoded = safe_encode(encoders["model"], model_name, "model")
fuel_encoded = safe_encode(encoders["fuel_type"], fuel_type, "fuel type")
trans_encoded = safe_encode(encoders["transmission_type"], transmission_type, "transmission type")


# Input data

input_data = np.array([[brand_encoded, model_encoded, vehicle_age, km_driven,
                        fuel_encoded, trans_encoded, mileage, engine, max_power, seats]])


# Predict price

if st.button("Predict Price"):
    try:
        predicted_price = model.predict(input_data)[0]
        st.success(f"💰 Estimated Car Price: ₹{predicted_price:,.2f}")
    except Exception as e:
        st.error(f"❌ Error during prediction: {e}")
