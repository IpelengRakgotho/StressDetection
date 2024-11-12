import streamlit as st
from firebase_admin import firestore

# Method to fetch the resources and display them
def user_resources_page():
    st.header("Stress Management Resources")

    # Initialize Firestore
    db = firestore.client()
    resources_ref = db.collection('stress_resources')
    
    # Fetch and display resources
    all_resources = resources_ref.stream()
    resources = {doc.id: doc.to_dict() for doc in all_resources}

    if not resources:
        st.write("No resources available.")
    else:
        for resource_id, resource in resources.items():    # Resources can be in a form of videos or written text
            st.subheader(resource['title'])
            if resource['type'] == 'Tip':
                st.write(resource['content'])
            elif resource['type'] == 'Video':
                st.video(resource['content'])  
