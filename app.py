import streamlit as st
import pandas as pd

# Set page configuration
st.set_page_config(page_title="FYP Schedule Checker", layout="wide")

# 1. Mock Data (Replace this with pd.read_csv('your_file.csv') in the future)
data = {
    'FYP Phase': ['FYP 1', 'FYP 1', 'FYP 1', 'FYP 1', 'FYP 2', 'FYP 2', 'FYP 2', 'FYP 2'],
    'Date': ['24 April 2026', '24 April 2026', '24 April 2026', '24 April 2026', '30 April 2026', '30 April 2026', '30 April 2026', '30 April 2026'],
    'Time': ['2:00 PM - 2:30 PM', '2:45 PM - 3:15 PM', '10:30 AM - 11:00 AM', '9:45 AM - 10:15 AM', '10:30 AM - 11:00 AM', '1:30 PM - 2:00 PM', '2:15 PM - 2:45 PM', '3:00 PM - 3:30 PM'],
    'Student Name': ['Aaron Koay Beng Liang', 'Chan Qin Ken', 'Dedric Yee Qi Xian', 'Sim Zi Ming', 'Amelia Chan Bing Li', 'Celine Tan Si Ning', 'Goh Yee Ern', 'Leng Jung Xung'],
    'FYP Title': ['Intelligent Multi-Camera Diagnostic Platform', 'Agritech Kiosk System', 'Task Management System', 'E-commerce Platform', 'Scalable Facial Recognition', 'V-DataSuite: CRUD', 'Automated RMA Defect', 'V-DataSuite: Backup'],
    'Coach Name': ['Mr. Tan Chin Kwang', 'Mr. Vincent Ong', 'Mr. Jack Ng', 'Mr. Mohamad Rizuan', 'Mr. Chew Yang Kun', 'Mr. Yeap Beng Heong', 'Mr. Leong Tan Kam Meng', 'Mr. Yeap Beng Heong'],
    'Supervisor': ['Ms. Khor Jia Yun', 'Ms. Nursyahirah Binti Tarmizi', 'Ms. Khor Jia Yun', 'Ts. Dr. Lim Seng Chee', 'Ts. Dr. Lim Seng Chee', 'Mr. Eng Yee Wei', 'Mr. Eng Yee Wei', 'Mr. Eng Yee Wei'],
    'Examiner': ['Mr. Eng Yee Wei', 'Ms. Khor Jia Yun', 'Ts. Dr. Lim Seng Chee', 'Mr. Eng Yee Wei', 'Ms. Nursyahirah Binti Tarmizi', 'Ts. Dr. Lim Seng Chee', 'Ms. Nursyahirah Binti Tarmizi', 'Ts. Dr. Lim Seng Chee'],
    'Venue': ['Block C-G-BOARD ROOM 1', 'Block C-G-BOARD ROOM 1', 'Block C-G-BOARD ROOM 2', 'Block C-G-BOARD ROOM 2', 'Block C-G-BOARD ROOM 2', 'Block C-G-BOARD ROOM 2', 'Block C-G-BOARD ROOM 2', 'Block C-G-BOARD ROOM 2']
}
df = pd.DataFrame(data)

# 2. Main Title
st.title("🎓 FYP Schedule Checker")
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
