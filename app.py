import streamlit as st
import pandas as pd
import base64
import os

# 1. Set page configuration
st.set_page_config(
    page_title="DCS-FYP Schedule Checker", 
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

# 4. FIXED STICKY HEADER (Title & Flags)
# Helper function to convert local images to base64 for HTML embedding
def get_base64_img(img_path):
    try:
        with open(img_path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode()
        return f"data:image/png;base64,{encoded}"
    except FileNotFoundError:
        return "https://via.placeholder.com/60?text=Missing"

img_national = get_base64_img("national-flag.avif")
img_penang = get_base64_img("penang-state-flag.avif")
img_vitrox = get_base64_img("vitrox-logo.png")

# HTML and CSS for a mobile-friendly, sticky row header
sticky_header_html = f"""
<style>
.sticky-header-container {{
    position: sticky;
    top: 0px; /* Sticks to the top of the white card */
    z-index: 9999;
    background-color: rgba(255, 255, 255, 0.98); /* Solid white to hide scrolling text behind it */
    padding: 10px 15px;
    border-bottom: 2px solid #e2e8f0;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
    margin-top: -10px; /* Pulls it up slightly to align with card top */
}}
.header-title-box h1 {{
    margin: 0;
    padding: 0;
    font-size: 1.5rem;
    color: #1E3A8A;
    line-height: 1.2;
}}
.header-title-box p {{
    margin: 0;
    padding: 0;
    font-size: 0.9rem;
    font-weight: bold;
    color: #475569;
}}
.header-logos-box {{
    display: flex;
    gap: 12px;
    align-items: center;
}}
/* Shrink images for the row header */
.header-logos-box img {{
    height: 35px; 
    width: auto;
    border-radius: 4px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}}

/* Stack nicely if the phone screen is extremely narrow */
@media (max-width: 600px) {{
    .sticky-header-container {{
        flex-direction: column;
        gap: 10px;
        align-items: center;
        text-align: center;
        padding-top: 15px;
    }}
    .header-logos-box img {{
        height: 28px; /* Shrink even more for small phones */
    }}
    .header-title-box h1 {{
        font-size: 1.3rem;
    }}
}}
</style>

<div class="sticky-header-container">
    <div class="header-title-box">
        <h1>Diploma in Computer Science FYP Schedule Checker</h1>
        <p>Semester Jan 2026</p>
    </div>
    <div class="header-logos-box">
        <img src="{img_national}" alt="National Flag" title="National Flag"/>
        <img src="{img_penang}" alt="Penang Flag" title="Penang Flag"/>
        <img src="{img_vitrox}" alt="ViTrox Logo" title="ViTrox College Logo"/>
    </div>
</div>
"""
st.markdown(sticky_header_html, unsafe_allow_html=True)

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

st.subheader("View Schedules (Select correct category before filtering)")
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

desired_columns = ['Student Name', 'Date', 'Time', 'Venue', 'Coach Name', 'FYP Title', 'Supervisor', 'Examiner']
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
# Add a warning message to guide the user
st.warning("⚠️ **For the best experience:** If you face any login issues, please ensure you open the Google Form using **Google Chrome**.")

st.link_button(
    "Click Here to Vote via Google Form", 
    "https://forms.gle/y7P84Fds8VKjziDJA", 
    type="primary", 
    use_container_width=True
)
