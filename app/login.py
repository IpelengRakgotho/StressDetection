import streamlit as st
import requests
from firebase_admin import auth
from app.admin import admin_page
from app.user import user_page
from app.adminResources import admin_resources_page
from app.userResources import user_resources_page
from app.utils import initialize_firebase

admin_email = "admin@gmail.com"
firebase_api_key = "AIzaSyDgU2nNEQr1AvnY5_NJd-56AixMGAkLXIM"  # Replace with your Firebase API Key

def login_page():

    db, bucket = initialize_firebase()
    if 'username' not in st.session_state:
        st.session_state.username = ''
    if 'email' not in st.session_state:
        st.session_state.email = ''

    def login(email, password):
        try:
            # Use Firebase Authentication REST API for email and password login
            url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={firebase_api_key}"
            payload = {
                "email": email,
                "password": password,
                "returnSecureToken": True
            }
            response = requests.post(url, json=payload)
            
            if response.status_code == 200:
                user_data = response.json()
                st.session_state.username = user_data['localId']
                st.session_state.email = user_data['email']
                st.session_state.is_admin = (user_data['email'] == admin_email)
                st.session_state.signout = True
                st.session_state.signedout = True
               
            else:
                st.warning('Login Failed. Please check your email and password.')

        except Exception as e:
            st.error(f"An error occurred: {e}")

    def signout():
        st.session_state.signout = False
        st.session_state.signedout = False
        st.session_state.username = ''
        st.session_state.is_admin = False

    if 'signedout' not in st.session_state:
        st.session_state.signedout = False
    if 'signout' not in st.session_state:
        st.session_state.signout = False
    
    if not st.session_state['signedout']:
        choice = st.selectbox('Login/Signup', ['Login', 'Create Account'])

        if choice == 'Login':
            email = st.text_input('Email')
            password = st.text_input('Password', type='password')
            st.button('Login', on_click=lambda: login(email, password))
        else: 
            # Signup form (same as before)
            name = st.text_input('Name')
            surname = st.text_input('Surname') 
            #gender = st.text_input('Gender')
            #age = st.text_input('Age')
            email = st.text_input('Email')
            username = st.text_input('Username')
            password = st.text_input('Password', type='password')
            confirmPassword = st.text_input('ConfirmPassword', type='password')

            if password == confirmPassword and st.button('Submit'):
                try:
                    # Create Firebase Auth user
                    user = auth.create_user(email=email, password=password, uid=username)

                    # Store additional details in Firestore
                    user_data = {
                        'name': name,
                        'surname': surname,
                        #'gender': gender,
                        #'age': age,
                        'email': email,
                        'username': username
                    }
                    db.collection('users').document(user.uid).set(user_data)

                    st.success('Account has been created successfully!')
                    st.markdown('Please login using your email and password')
                except Exception as e:
                    st.error(f'Error creating account: {e}')

    # If user is signed in, allow them to enter health data
    if st.session_state.signout:
        # Sidebar logout button
        st.sidebar.text(f"Welcome, {st.session_state.username}")
        st.sidebar.button('Sign out', on_click=signout)

        if st.session_state.is_admin:
            #st.subheader("Admin Dashboard")
            admin_page()
            st.subheader("Manage Resources")
            admin_resources_page()
        else:
            #st.subheader("User Dashboard")
            user_page()
            #st.subheader("View Resources")
            user_resources_page()
