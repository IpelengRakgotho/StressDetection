import streamlit as st

def about_page():
    st.title("About StressGuard")
    st.write("""
        **StressGuard** is a comprehensive tool for monitoring and managing stress levels.
        The application uses data from smartwatches, including heart rate, sleep hours, and blood oxygen levels,
        to predict stress levels and provide insights over time.
        \n
        **Features:**
        - Predict stress levels based on smartwatch data.
        - View historical stress levels with a line graph.
        - Stress management tips.
        \n
        **Developed by:** Lerato Rakgotho
        \n
        For more information, please contact lerato.rakgotho@gmail.com
    """)