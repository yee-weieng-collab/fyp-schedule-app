import streamlit as st
import pandas as pd

# 1. Set page configuration
st.set_page_config(
    page_title="FYP Schedule Checker", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Custom CSS for Background, Logo, Green Gradient, Image Scaling, and Professional Styling
st.markdown("""
    <style>
    /* --- PROFESSIONAL BACKGROUND & CARD EFFECT --- */
    /* Target the main app background */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #f0f4f8 0%, #d9e2ec 100%);
    }
    
    /* Make the main content area look like a floating white card */
    .block-container {
        background-color: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding-top: 2rem !important;
        padding-bottom: 3rem !important;
        margin-top: 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
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
    /* Hover effect for the green gradient */
    button[kind="primary"]:hover {
        background: linear-gradient(90deg, #0f8a80 0%, #31d46e 100%) !important;
    }

    /* --- MOBILE FRIENDLY LECTURER IMAGES --- */
    /* Forces images to stay small and centered on mobile instead of taking up the whole screen */
    [data-testid="stImage"] {
        text-align: center;
    }
    [data-testid="stImage"] img {
        max-width: 130px !important; /* Prevents stretching */
        border-radius: 8px; /* Slight rounded corners for a professional look */
        margin: 0 auto;
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

# 4. Main Title & Logo (Side by side)
header_col1, header_col2 = st.columns([1, 4]) # Adjust ratio if logo is too big/small

with header_col1:
    try:
        st.image("vitrox-logo.png", use_container_width=True)
    except FileNotFoundError:
        st.info("Logo space: Please add 'vitrox-logo.png' to your folder.")

with header_col2:
    st.title("FYP Schedule Checker")
    st.markdown("**Semester Jan 2026**")

st.divider()

# 5. Lecturer Profiles
st.subheader("Lecturer Profiles")
img_col1, img_col2, img_col3, img_col4 = st.columns(4)

try:
    with img_col1:
        st.image("lim_seng_chee.png", caption="Ts. Dr. Lim Seng Chee")
    with img_col2:
        st.image("khor_jia_yun.png", caption="Ms. Khor Jia Yun")
    with img_col3:
        st.image("eng_yee_wei.png", caption="Mr. Eng Yee Wei")
    with img_col4:
        st.image("nursyahirah.png", caption="Ms. Syira")
except FileNotFoundError:
    st.warning("Image files not found. Ensure lim_seng_chee.png, khor_jia_yun.png, eng_yee_wei.png, and nursyahirah.png are in your folder.")

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

    filter_col1, filter_col2 = st.columns(2)

    with filter_col1:
        supervisors = ['All'] + sorted(list(df_phase['Supervisor'].dropna().unique()))
        selected_sup = st.selectbox("Filter by Supervisor", supervisors)

    with filter_col2:
        examiners = ['All'] + sorted(list(df_phase['Examiner'].dropna().unique()))
        selected_exam = st.selectbox("Filter by Examiner", examiners)

# Apply filters
if selected_sup != 'All':
    df_phase = df_phase[df_phase['Supervisor'] == selected_sup]
if selected_exam != 'All':
    df_phase = df_phase[df_phase['Examiner'] == selected_exam]

# 8. Display Data Table
st.markdown("<br>", unsafe_allow_html=True) 
desired_columns = ['Time', 'Venue', 'Coach Name', 'Student Name', 'FYP Title', 'Supervisor', 'Examiner']
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

# This button will use the gradient green CSS we added at the top
st.link_button(
    "Click Here to Vote via Google Form", 
    "https://forms.gle/y7P84Fds8VKjziDJA", 
    type="primary", 
    use_container_width=True
)
