import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import streamlit as st
from app.login import login_page
from app.about import about_page
from app.user import user_page

def app():
    
    # Background image styling for main content and sidebar
    page_bg_img = """
    <style>
    /* Main content background */
    [data-testid="stAppViewContainer"] {
        background-image: url("https://www.zmo.ai/wp-content/uploads/2023/09/png-transparent-abstract-blue-background-wave.png");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }

    /* Sidebar background */
    [data-testid="stSidebar"] {
        background-image: url("https://png.pngtree.com/background/20220715/original/pngtree-light-blue-background-picture-picture-image_1626628.jpg");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }

    /* Header transparent */
    [data-testid="stHeader"] {
        background-color: rgba(0, 0, 0, 0);
    }

    /* Toolbar position */
    [data-testid="stToolbar"] {
        right: 2rem;
    }
    </style>
    """

    # Hide unwanted icons the were appearing after deploying the app
    hide_icons_css = """
    <style>
    header > div:nth-child(2) > button,
    header > div:nth-child(2) > div {
        display: none !important;
    }
    </style>
    """
    
    # background styling and hide icons
    st.markdown(page_bg_img, unsafe_allow_html=True)
    st.markdown(hide_icons_css, unsafe_allow_html=True)

    st.markdown("# *StressGuard*")

    # Sidebar navigation
    page = st.sidebar.selectbox('Navigate', ['Login', 'About'])

    # Page routing
    if page == 'Login':
        login_page()
    elif page == 'About':
        about_page()
    
if __name__ == '__main__':
    app()
