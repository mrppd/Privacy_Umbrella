import streamlit as st
import pandas as pd
import json
from typing import Any, Dict
from io import StringIO
import base64

def flatten_dict(d: Dict[str, Any], parent_key: str = '', sep: str = '_') -> Dict[str, Any]:
    items = []
    for k, v in d.items():
        new_key = f'{parent_key}{sep}{k}' if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        elif isinstance(v, list):
            for i, item in enumerate(v):
                if isinstance(item, dict):
                    items.extend(flatten_dict(item, f'{new_key}{sep}{i}', sep=sep).items())
                else:
                    items.append((f'{new_key}{sep}{i}', item))
        else:
            items.append((new_key, v))
    return dict(items)

def parse_fhir(json_data: Dict[str, Any]) -> pd.DataFrame:
    all_data = []
    for entry in json_data['entry']:
        flattened_data = flatten_dict(entry)
        all_data.append(flattened_data)
    return pd.DataFrame(all_data)


st.title('FHIR to CSV Converter')

# Sidebar for file upload
with st.sidebar:
    st.sidebar.markdown("## Upload FHIR File")
    uploaded_files = st.sidebar.file_uploader("Choose FHIR files", type="json", accept_multiple_files=True)

# Main area for table preview and download
if uploaded_files:
    for uploaded_file in uploaded_files:
        # Read and process each file
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        string_data = stringio.read()
        json_data = json.loads(string_data)
        df = parse_fhir(json_data)
        columns = df.columns.tolist()

        # Sidebar for searching and selecting variables
        with st.sidebar:
            st.sidebar.markdown("## Search and Select Variables")
            search_query = st.sidebar.text_input("Search variables")

            # Filter columns based on search query
            filtered_columns = [col for col in columns if search_query.lower() in col.lower()]
            selected_columns = st.sidebar.multiselect("Choose columns", filtered_columns, key='select_vars')

        # Filter the DataFrame based on selected variables
        filtered_df = df[selected_columns] if selected_columns else df

        # Display the (filtered) converted table
        st.markdown(f"### Preview of {uploaded_file.name}")
        st.dataframe(filtered_df)

        # Create a CSV from the (filtered) DataFrame
        csv = filtered_df.to_csv(index=False)
        

        # Create a CSV from the DataFrame
        csv = df.to_csv(index=False)
        basename = uploaded_file.name.split('.')[0]  # Get the basename from the filename
        csv_filename = f'{basename}_converted.csv'  # Set the CSV filename based on the basename

        # Generate a download button for each file
        st.download_button(
            label=f"Download {csv_filename}",
            data=csv,
            file_name=csv_filename,
            mime='text/csv',
        )

def get_image_base64(path):
    with open(path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Path to your image
image_path_item = 'Fraunhofer_ITEM_Logo.jpg'
image_path_mainz = 'Mainz.png'
image_path_goethe='Goethe_University_logo.jpg'
# Convert the image to base64
encoded_image_item = get_image_base64(image_path_item)
encoded_image_mainz = get_image_base64(image_path_mainz)
encoded_image_goethe = get_image_base64(image_path_goethe)

# Function to add multiple images to the footer
def add_footer(encoded_image_item, encoded_image_mainz, encoded_image_goethe):
    st.markdown(
        f"""
        <style>
        .footer {{
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background-color: white;
            text-align: center;
            padding: 10px;
        }}
        </style>
        <div class='footer'>
            <img src='data:image/jpg;base64,{encoded_image_item}' width='120'>
            <img src='data:image/png;base64,{encoded_image_mainz}' width='120'>
            <img src='data:image/jpg;base64,{encoded_image_goethe}' width='120'>
        </div>
        """,
        unsafe_allow_html=True
    )

# Call the function with the three images
add_footer(encoded_image_item, encoded_image_mainz, encoded_image_goethe)
