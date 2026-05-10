import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests
import json

# Page configuration
st.set_page_config(
    page_title="Salary Prediction MLOps",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title and description
st.title("💼 Salary Prediction MLOps Dashboard")
st.markdown("""
Welcome to the **Salary Prediction MLOps Dashboard**! This application uses machine learning
to predict employee salaries based on years of experience.
""")

# Sidebar with information
st.sidebar.header("📊 Model Information")
st.sidebar.markdown("""
**Algorithm:** Linear Regression
**Training Data:** 30 employee records
**Features:** Years of Experience
**Target:** Annual Salary
**Model Performance:** R² = 0.90
""")

st.sidebar.header("🔧 API Configuration")
api_url = st.sidebar.text_input("API URL", "http://127.0.0.1:8001")
test_connection = st.sidebar.button("Test API Connection")

if test_connection:
    try:
        response = requests.get(f"{api_url}/")
        if response.status_code == 200:
            st.sidebar.success("✅ API Connected Successfully!")
        else:
            st.sidebar.error(f"❌ API Error: {response.status_code}")
    except Exception as e:
        st.sidebar.error(f"❌ Connection Failed: {str(e)}")

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.header("🎯 Salary Prediction")

    # Input form
    with st.form("prediction_form"):
        years_exp = st.slider(
            "Years of Experience",
            min_value=0.0,
            max_value=50.0,
            value=5.0,
            step=0.5,
            help="Select the number of years of professional experience"
        )

        submitted = st.form_submit_button("🔮 Predict Salary")

        if submitted:
            with st.spinner("Making prediction..."):
                try:
                    # Make API call
                    payload = {"years_experience": years_exp}
                    response = requests.post(f"{api_url}/predict", json=payload)

                    if response.status_code == 200:
                        result = response.json()

                        # Display results
                        st.success("✅ Prediction Complete!")

                        col_a, col_b, col_c = st.columns(3)
                        with col_a:
                            st.metric("Predicted Salary", f"${result['predicted_salary']:,.2f}")
                        with col_b:
                            st.metric("Years Experience", f"{result['years_experience']} years")
                        with col_c:
                            st.metric("Confidence", result['confidence'])

                        # Additional insights
                        st.info(f"💡 For {years_exp} years of experience, the predicted annual salary is **${result['predicted_salary']:,.2f}**")

                    else:
                        st.error(f"❌ API Error: {response.status_code}")
                        st.text(response.text)

                except requests.exceptions.RequestException as e:
                    st.error(f"❌ Connection Error: {str(e)}")
                    st.info("💡 Make sure the FastAPI server is running on the specified URL")

with col2:
    st.header("📈 Data Visualization")

    # Load and display sample data
    try:
        # Try to load data from the data directory
        data_path = "data/salary_data.csv"
        df = pd.read_csv(data_path)

        st.subheader("Sample Data")
        st.dataframe(df.head(), use_container_width=True)

        # Create scatter plot
        st.subheader("Experience vs Salary")
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.scatter(df['YearsExperience'], df['Salary'], alpha=0.6, color='blue')
        ax.set_xlabel('Years of Experience')
        ax.set_ylabel('Salary ($)')
        ax.set_title('Salary vs Experience Relationship')
        ax.grid(True, alpha=0.3)

        # Add trend line if prediction was made
        if 'result' in locals() and submitted:
            # Simple linear trend for visualization
            x_trend = [df['YearsExperience'].min(), df['YearsExperience'].max()]
            # Using approximate slope from our model (you could get exact from API)
            slope = 9000  # Approximate slope
            intercept = 25000  # Approximate intercept
            y_trend = [slope * x + intercept for x in x_trend]
            ax.plot(x_trend, y_trend, 'r--', alpha=0.8, label='Trend Line')
            ax.legend()

        st.pyplot(fig)

        # Statistics
        st.subheader("📊 Quick Statistics")
        col_stats1, col_stats2 = st.columns(2)
        with col_stats1:
            st.metric("Average Salary", f"${df['Salary'].mean():,.0f}")
            st.metric("Min Experience", f"{df['YearsExperience'].min()} years")
        with col_stats2:
            st.metric("Average Experience", f"{df['YearsExperience'].mean():.1f} years")
            st.metric("Max Salary", f"${df['Salary'].max():,.0f}")

    except FileNotFoundError:
        st.warning("⚠️ Sample data file not found. Make sure the data directory exists.")
    except Exception as e:
        st.error(f"❌ Error loading data: {str(e)}")

# Footer
st.markdown("---")
st.markdown("""
**🚀 MLOps Pipeline Features:**
- Automated model training and deployment
- REST API for predictions
- Monitoring with Prometheus/Grafana
- Containerized with Docker
- CI/CD with Jenkins
""")

# Instructions
with st.expander("📖 How to Use"):
    st.markdown("""
    1. **Start the API Server:**
       ```bash
       uvicorn api.app:app --host 127.0.0.1 --port 8001
       ```

    2. **Run this Streamlit App:**
       ```bash
       streamlit run streamlit_app.py
       ```

    3. **Make Predictions:**
       - Adjust the years of experience slider
       - Click "Predict Salary"
       - View results and visualizations

    4. **API Endpoints:**
       - `GET /` - API information
       - `POST /predict` - Make predictions
    """)