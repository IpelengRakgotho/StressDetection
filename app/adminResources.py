import streamlit as st
from firebase_admin import firestore

# This method enables the admin to load, edit and delete resourses
# Resources can be in a form of videos or written text
def admin_resources_page():
    st.header("Manage Stress Resources")

    # Initialize Firestore
    db = firestore.client()
    resources_ref = db.collection('stress_resources')

    # Add New Resource
    st.subheader("Add New Resource")
    resource_type = st.selectbox("Resource Type", ["Tip", "Video"])
    resource_title = st.text_input("Title")
    resource_content = st.text_area("Content (for tips) or URL (for videos)")
    if st.button("Add Resource"):
        if resource_title and resource_content:
            resources_ref.add({
                'type': resource_type,
                'title': resource_title,
                'content': resource_content
            })
            st.success("Resource added successfully!")
        else:
            st.error("Please fill out all fields.")

    # Edit or Delete Existing Resources
    st.subheader("Edit or Delete Existing Resources")
    all_resources = resources_ref.stream()
    resources = {doc.id: doc.to_dict() for doc in all_resources}
    
    resource_ids = list(resources.keys())
    selected_resource_id = st.selectbox("Select Resource to Edit/Delete", resource_ids, format_func=lambda x: resources[x]['title'])

    if selected_resource_id:
        selected_resource = resources[selected_resource_id]
        st.write(f"Editing: {selected_resource['title']}")
        new_title = st.text_input("New Title", value=selected_resource['title'])
        new_content = st.text_area("New Content", value=selected_resource['content'])
        
        if st.button("Save Changes"):
            resources_ref.document(selected_resource_id).update({
                'title': new_title,
                'content': new_content
            })
            st.success("Resource updated successfully!")

        if st.button("Delete Resource"):
            resources_ref.document(selected_resource_id).delete()
            st.success("Resource deleted successfully!")
         

