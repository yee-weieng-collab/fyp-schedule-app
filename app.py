import streamlit as st
import pandas as pd

# 1. Set page configuration (must be the first Streamlit command)
st.set_page_config(
    page_title="FYP Schedule Checker", 
    page_icon="🎓", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Custom CSS for a professional, polished look
st.markdown("""
    <style>
    /* Adjust main container padding for mobile/desktop */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
    }
    /* Style headers */
    h1, h2, h3 {
        color: #1E3A8A; /* Dark blue professional theme */
    }
    /* Make dataframe headers stand out */
    [data-testid="stDataFrame"] {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    </style>
""", unsafe_allow_html=True)

# 3. Load Data from Google Sheets
@st.cache_data(ttl=60)
def load_data():
    sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTrxhs8F35bpw09bdACGvLdoE08on92AHTr0Lkeg8d0GbAb6GmmMbePM-W1U-5Z0wsVA2gvwNNqLeJ_/pub?gid=87654321&single=true&output=csv"
    
    # Load the dataframe and clean column names to avoid trailing spaces
    df = pd.read_csv(sheet_url)
    df.columns = df.columns.str.strip()
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"⚠️ Could not load data from Google Sheets. Please check your link. Error: {e}")
    st.stop()

# 4. Main Title & Header
st.title("🎓 FYP Schedule Checker")
st.markdown("**Semester Jan 2026**")
st.divider()

# 5. Lecturer Profiles
st.subheader("👨‍🏫 Meet the Lecturers")
img_col1, img_col2, img_col3, img_col4 = st.columns(4)

# using use_container_width=True ensures images scale perfectly on mobile
try:
    with img_col1:
        st.image("lim_seng_chee.png", caption="Ts. Dr. Lim Seng Chee", use_container_width=True)
    with img_col2:
        st.image("khor_jia_yun.png", caption="Ms. Khor Jia Yun", use_container_width=True)
    with img_col3:
        st.image("eng_yee_wei.png", caption="Mr. Eng Yee Wei", use_container_width=True)
    with img_col4:
        st.image("nursyahirah.png", caption="Ms. Syira", use_container_width=True)
except FileNotFoundError:
    st.warning("⚠️ Image files not found. Ensure lim_seng_chee.png, khor_jia_yun.png, eng_yee_wei.png, and nursyahirah.png are in the same folder.")

st.divider()

# 6. Phase Selection (Dynamic Tabs)
if 'phase' not in st.session_state:
    st.session_state.phase = 'FYP 1'

st.subheader("📅 View Schedules")
col1, col2 = st.columns(2)

# Dynamic button styling: Highlights the currently selected phase
with col1:
    fyp1_type = "primary" if st.session_state.phase == 'FYP 1' else "secondary"
    if st.button("🔵 FYP 1", use_container_width=True, type=fyp1_type):
        st.session_state.phase = 'FYP 1'
        st.rerun()

with col2:
    fyp2_type = "primary" if st.session_state.phase == 'FYP 2' else "secondary"
    if st.button("🟢 FYP 2", use_container_width=True, type=fyp2_type):
        st.session_state.phase = 'FYP 2'
        st.rerun()

# 7. Filters (Wrapped in a visually distinct container)
with st.container(border=True):
    st.markdown(f"**Filtering tools for: {st.session_state.phase}**")
    
    # Ensure column exists before filtering to prevent app crashes
    if 'FYP Phase' in df.columns:
        df_phase = df[df['FYP Phase'] == st.session_state.phase]
    elif 'FYP Phas' in df.columns: # Fallback just in case of typos in the sheet
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
st.markdown("<br>", unsafe_allow_html=True) # Add a little breathing space
# Attempt to display requested columns; ignore missing ones
desired_columns = ['Time', 'Venue', 'Coach Name', 'Student Name', 'FYP Title', 'Supervisor', 'Examiner']
actual_columns = [col for col in desired_columns if col in df_phase.columns]

if df_phase.empty:
    st.info("🔍 No schedules found matching your current filters.")
else:
    st.dataframe(
        df_phase[actual_columns], 
        use_container_width=True, 
        hide_index=True
    )

st.divider()

# 9. Voting Section (New Addition)
st.header("🗳️ Cast Your Vote")
st.info("Have you attended the presentations? Don't forget to cast your vote for the best FYP project!")

# A prominent, mobile-friendly button that links directly to the Google Form
st.link_button(
    "👉 Click Here to Vote via Google Form", 
    "https://forms.gle/y7P84Fds8VKjziDJA", 
    type="primary", 
    use_container_width=True
)
