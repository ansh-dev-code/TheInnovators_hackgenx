import streamlit as st
import pandas as pd
import joblib

# Load your trained model and transformation objects (encoder and scaler)
model = joblib.load("trained_model.pkl")
encoder = joblib.load('onehot_encoder.pkl')  # Load the encoder
scaler = joblib.load('scaler.pkl')  # Load the scaler

# ---- Page Config ----
st.set_page_config(page_title="Smart Budget Predictor", page_icon="💼", layout="centered")

# ---- Custom CSS ----
st.markdown("""
    <style>
        .main {
            background-color: #f8f9fa;
            padding: 2rem;
            border-radius: 16px;
            box-shadow: 0px 0px 12px rgba(0,0,0,0.08);
        }
        h1 {
            color: #4B0082;
            text-align: center;
        }
        .stButton > button {
            background-color: #4B0082;
            color: white;
            border-radius: 8px;
            font-weight: bold;
            padding: 0.5em 1em;
        }
    </style>
""", unsafe_allow_html=True)

# ---- UI ----
st.markdown('<div class="main">', unsafe_allow_html=True)
st.markdown("## 💼 Smart Budget Allocation Predictor")

# ---- Input Fields ----
company = st.text_input("🏢 Company Name")
year = st.number_input("📅 Year", min_value=2000, max_value=2100, step=1, value=2025)
department = st.selectbox("🏬 Department", [
    "R&D", "HR", "Marketing", "IT Support", "Product Development", "Sale", "Finance", "Security", "Customer Success",
    "Business Intelligence", "Operations", "Legal"
])

# ---- Prediction ----
if st.button("🔍 Predict Budget"):
    if company:
        # Step 1: Create DataFrame from user input
        input_df = pd.DataFrame({
            'Company': [company],
            'Year': [year],
            'Department': [department]
        })
        
        # Step 2: Apply OneHotEncoder transformation to the categorical columns
        encoded_input = encoder.transform(input_df[['Company', 'Department']])
        encoded_input_df = pd.DataFrame(encoded_input, columns=encoder.get_feature_names_out(['Company', 'Department']))
        
        # Step 3: Apply StandardScaler to 'Year' (and any other numerical columns if required)
        input_df['Year'] = scaler.transform(input_df[['Year']])
        
        # Step 4: Concatenate the scaled 'Year' and the encoded categorical features
        final_input = pd.concat([input_df.drop(['Company', 'Department'], axis=1), encoded_input_df], axis=1)
        
        # Step 5: Predict using the trained model
        try:
            prediction = model.predict(final_input)[0]
            st.success(f"📊 Predicted Budget for **{department}** in **{company}**, {year}:")
            st.markdown(f"<h2 style='color:#4B0082;'>${prediction:,.2f}</h2>", unsafe_allow_html=True)
        except Exception as e:
            st.error("🚫 Error during prediction. Please ensure your model accepts inputs as: Company, Year, Department.")
            st.error(f"Details: {e}")
    else:
        st.warning("⚠️ Please enter a company name before predicting.")

st.markdown("</div>", unsafe_allow_html=True)
