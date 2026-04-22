import streamlit as st
import pandas as pd

# Set page configuration
st.set_page_config(page_title="FYP Schedule Checker", layout="wide")

# 1. Load Data from Google Sheets
# We use @st.cache_data so the app doesn't re-download the sheet every time a user clicks a button
@st.cache_data(ttl=60) # Caches the data for 60 seconds. You can increase this!
def load_data():
    # PASTE YOUR GOOGLE SHEETS CSV URL HERE:
    sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTrxhs8F35bpw09bdACGvLdoE08on92AHTr0Lkeg8d0GbAb6GmmMbePM-W1U-5Z0wsVA2gvwNNqLeJ_/pub?gid=87654321&single=true&output=csv"
    
    # Pandas can read directly from a URL!
    return pd.read_csv(sheet_url)

# Load the dataframe
df = load_data()

# 2. Main Title
st.title("🎓FYP Schedule Checker Semester Jan 2026")
st.markdown("---")

# 3. Lecturer Profiles (Images)
st.subheader("Meet the Lecturers")
img_col1, img_col2, img_col3, img_col4 = st.columns(4)

# Note: Ensure you have these image files in the same folder, or comment out if you don't have them yet.
try:
    with img_col1:
        st.image("lim_seng_chee.png", caption="Ts. Dr. Lim Seng Chee")
    with img_col2:
        st.image("khor_jia_yun.png", caption="Ms. Khor Jia Yun")
    with img_col3:
        st.image("eng_yee_wei.png", caption="Mr. Eng Yee Wei")
    with img_col4:
        st.image("nursyahirah.png", caption="Ms. Syira") # Assuming Ms. Syira maps to Ms. Nursyahirah
except FileNotFoundError:
    st.warning("⚠️ Image files not found. Please place lim.jpg, khor.jpg, eng.jpg, and syira.jpg in your folder.")

st.markdown("---")

# 4. Phase Selection (Big Buttons using Session State)
if 'phase' not in st.session_state:
    st.session_state.phase = 'FYP 1' # Default selection

col1, col2 = st.columns(2)
with col1:
    if st.button("🔵 FYP 1", use_container_width=True):
        st.session_state.phase = 'FYP 1'
with col2:
    if st.button("🟢 FYP 2", use_container_width=True):
        st.session_state.phase = 'FYP 2'

st.subheader(f"Showing schedules for: **{st.session_state.phase}**")

# Filter data based on selected phase
df_phase = df[df['FYP Phase'] == st.session_state.phase]

# 5. Dropdown Filters for Supervisor and Examiner
filter_col1, filter_col2 = st.columns(2)

with filter_col1:
    supervisors = ['All'] + list(df_phase['Supervisor'].unique())
    selected_sup = st.selectbox("Filter by Supervisor", supervisors)

with filter_col2:
    examiners = ['All'] + list(df_phase['Examiner'].unique())
    selected_exam = st.selectbox("Filter by Examiner", examiners)

# Apply filters
if selected_sup != 'All':
    df_phase = df_phase[df_phase['Supervisor'] == selected_sup]
if selected_exam != 'All':
    df_phase = df_phase[df_phase['Examiner'] == selected_exam]

# 6. Display the final Data Table
st.markdown("### Schedule Details")
# Displaying only the columns you requested
display_df = df_phase[['Time', 'Venue', 'Coach Name', 'Student Name', 'FYP Title', 'Supervisor', 'Examiner']]

if display_df.empty:
    st.info("No schedules found matching your filters.")
else:
    st.dataframe(display_df, use_container_width=True, hide_index=True)
