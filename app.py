import streamlit as st
import pandas as pd
import base64
import os

# 1. Set page configuration
st.set_page_config(
    page_title="Diploma in Computer Science FYP 1 and 2 Schedule Checker (School of Computing and Informatics)", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Custom CSS for True Background Gradient and Professional Styling
st.markdown("""
    <style>
    /* --- TRUE PROFESSIONAL BACKGROUND --- */
    /* Target the absolute background of the app */
    .stApp {
        background: linear-gradient(135deg, #f0f4f8 0%, #d9e2ec 100%) !important;
    }
    
    /* Make the top header transparent so it doesn't block the gradient */
    header[data-testid="stHeader"] {
        background-color: transparent !important;
    }
    
    /* Make the main content area look like a floating white card */
    .block-container {
        background-color: rgba(255, 255, 255, 0.95) !important;
        border-radius: 15px;
        padding-top: 2rem !important;
        padding-bottom: 3rem !important;
        margin-top: 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        max-width: 95%; /* Gives nice padding on the sides */
    }
    
    /* Style headers to a dark professional blue */
    h1, h2, h3 {
        color: #1E3A8A; 
    }
    
    /* --- CUSTOM GREEN GRADIENT FOR SELECTED BUTTONS --- */
    button[kind="primary"] {
        background: linear-gradient(90deg, #11998e 0%, #38ef7d 100%) !important;
        border: none !important;
        color: white !important;
        font-weight: 600 !important;
    }
    button[kind="primary"]:hover {
        background: linear-gradient(90deg, #0f8a80 0%, #31d46e 100%) !important;
    }

    /* Style the data table */
    [data-testid="stDataFrame"] {
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    </style>
""", unsafe_allow_html=True)

# 3. Load Data from Google Sheets
@st.cache_data(ttl=60)
def load_data():
    sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTrxhs8F35bpw09bdACGvLdoE08on92AHTr0Lkeg8d0GbAb6GmmMbePM-W1U-5Z0wsVA2gvwNNqLeJ_/pub?gid=87654321&single=true&output=csv"
    df = pd.read_csv(sheet_url)
    df.columns = df.columns.str.strip()
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"Could not load data from Google Sheets. Error: {e}")
    st.stop()

# 4. Main Title & Logo
header_col1, header_col2 = st.columns([1, 4]) 

with header_col1:
    try:
        st.image("vitrox-logo.png", use_container_width=True)
    except FileNotFoundError:
        st.info("Logo space: Add 'vitrox-logo.png'")

with header_col2:
    st.title("FYP Schedule Checker")
    st.markdown("**Semester Jan 2026**")

st.divider()

# 5. Lecturer Profiles (Fixed for Mobile - 4 in a line)
st.subheader("Lecturer Profiles")

def get_image_html(img_path, caption):
    try:
        with open(img_path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode()
        img_src = f"data:image/png;base64,{encoded}"
    except FileNotFoundError:
        img_src = "https://via.placeholder.com/130?text=No+Image"
        
    return f'<div style="flex: 1; text-align: center; min-width: 22%; padding: 0 5px;"><img src="{img_src}" style="width: 100%; max-width: 130px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);"><p style="font-size: 0.85rem; margin-top: 8px; color: #1E3A8A; font-weight: 600; line-height: 1.2;">{caption}</p></div>'

lecturer_html = f'<div style="display: flex; flex-direction: row; justify-content: space-around; align-items: flex-start; flex-wrap: nowrap; overflow-x: auto; padding-bottom: 10px;">{get_image_html("lim_seng_chee.png", "Ts. Dr. Lim Seng Chee")}{get_image_html("khor_jia_yun.png", "Ms. Khor Jia Yun")}{get_image_html("eng_yee_wei.png", "Mr. Eng Yee Wei")}{get_image_html("nursyahirah.png", "Ms. Syira")}</div>'

st.markdown(lecturer_html, unsafe_allow_html=True)

st.divider()

# 6. Phase Selection 
if 'phase' not in st.session_state:
    st.session_state.phase = 'FYP 1'

st.subheader("View Schedules")
col1, col2 = st.columns(2)

with col1:
    fyp1_type = "primary" if st.session_state.phase == 'FYP 1' else "secondary"
    if st.button("FYP 1", use_container_width=True, type=fyp1_type):
        st.session_state.phase = 'FYP 1'
        st.rerun()

with col2:
    fyp2_type = "primary" if st.session_state.phase == 'FYP 2' else "secondary"
    if st.button("FYP 2", use_container_width=True, type=fyp2_type):
        st.session_state.phase = 'FYP 2'
        st.rerun()

# 7. Filters 
with st.container(border=True):
    st.markdown(f"**Filtering tools for: {st.session_state.phase}**")
    
    if 'FYP Phase' in df.columns:
        df_phase = df[df['FYP Phase'] == st.session_state.phase]
    elif 'FYP Phas' in df.columns:
        df_phase = df[df['FYP Phas'] == st.session_state.phase]
    else:
        st.error("Could not find the 'FYP Phase' column in your Google Sheet.")
        st.stop()

    # Changed to 3 columns to accommodate the new Student filter
    filter_col1, filter_col2, filter_col3 = st.columns(3)

    with filter_col1:
        students = ['All'] + sorted(list(df_phase['Student Name'].dropna().unique()))
        selected_student = st.selectbox("Filter by Student", students)

    with filter_col2:
        supervisors = ['All'] + sorted(list(df_phase['Supervisor'].dropna().unique()))
        selected_sup = st.selectbox("Filter by Supervisor", supervisors)

    with filter_col3:
        examiners = ['All'] + sorted(list(df_phase['Examiner'].dropna().unique()))
        selected_exam = st.selectbox("Filter by Examiner", examiners)

# Apply filters
if selected_student != 'All':
    df_phase = df_phase[df_phase['Student Name'] == selected_student]
if selected_sup != 'All':
    df_phase = df_phase[df_phase['Supervisor'] == selected_sup]
if selected_exam != 'All':
    df_phase = df_phase[df_phase['Examiner'] == selected_exam]

# 8. Display Data Table
st.markdown("<br>", unsafe_allow_html=True) 
# Updated column order: 'Student Name' is now first
desired_columns = ['Student Name', 'Time', 'Venue', 'Coach Name', 'FYP Title', 'Supervisor', 'Examiner']
actual_columns = [col for col in desired_columns if col in df_phase.columns]

if df_phase.empty:
    st.info("No schedules found matching your current filters.")
else:
    st.dataframe(
        df_phase[actual_columns], 
        use_container_width=True, 
        hide_index=True
    )

st.divider()

# 9. Voting Section 
st.header("Cast Your Vote")
st.info("Our DCS students FYP2 poster are ready to be viewed at Level 4, ViTrox College. Please cast your vote for the best FYP project.")

st.link_button(
    "Click Here to Vote via Google Form", 
    "https://forms.gle/y7P84Fds8VKjziDJA", 
    type="primary", 
    use_container_width=True
)
