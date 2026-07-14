import streamlit as st
import pandas as pd
import base64
import html
from pathlib import Path

# Resolve images relative to this script so the app works no matter
# which folder Streamlit is launched from
APP_DIR = Path(__file__).parent

# Self-contained grey placeholder (no internet needed) shown if an image file is missing
PLACEHOLDER_IMG = (
    "data:image/svg+xml;base64,"
    + base64.b64encode(
        b'<svg xmlns="http://www.w3.org/2000/svg" width="130" height="130">'
        b'<rect width="130" height="130" fill="#e2e8f0"/>'
        b'<text x="65" y="70" font-family="sans-serif" font-size="14" fill="#64748b" '
        b'text-anchor="middle">No Image</text></svg>'
    ).decode()
)

# ══════════════════════════════════════════════════════════════
# 1. PAGE CONFIGURATION
# ══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="DCS-FYP Schedule Checker | ViTrox College",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ══════════════════════════════════════════════════════════════
# 2. GLOBAL DESIGN SYSTEM (CSS)
# ══════════════════════════════════════════════════════════════
st.markdown("""
    <style>
    /* ---------- FONT ---------- */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"], .stMarkdown, button, input, select {
        font-family: 'Plus Jakarta Sans', 'Segoe UI', sans-serif !important;
    }

    /* ---------- HIDE STREAMLIT CHROME (menu, footer, toolbar) ---------- */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    [data-testid="stToolbar"] { display: none !important; }
    [data-testid="stDecoration"] { display: none !important; }

    /* ---------- APP BACKGROUND: layered professional gradient ---------- */
    .stApp {
        background:
            radial-gradient(ellipse 80% 50% at 20% -10%, rgba(30, 58, 138, 0.18), transparent),
            radial-gradient(ellipse 60% 40% at 90% 0%, rgba(17, 153, 142, 0.14), transparent),
            linear-gradient(160deg, #eef2f9 0%, #dde7f3 55%, #d3e0ee 100%) !important;
        background-attachment: fixed !important;
    }

    header[data-testid="stHeader"] {
        background: transparent !important;
    }

    /* ---------- MAIN CONTENT: floating glass card ---------- */
    .block-container {
        background: rgba(255, 255, 255, 0.92) !important;
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.7);
        border-radius: 24px;
        padding: 2rem 2.5rem 3rem 2.5rem !important;
        margin-top: 1.5rem;
        margin-bottom: 2.5rem;
        box-shadow:
            0 24px 60px -12px rgba(15, 37, 87, 0.18),
            0 4px 12px rgba(15, 37, 87, 0.06);
        max-width: 1200px;
    }

    /* ---------- ENTRANCE ANIMATION ---------- */
    @keyframes fadeUp {
        from { opacity: 0; transform: translateY(14px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    .fade-in { animation: fadeUp 0.55s ease both; }

    /* ---------- HEADINGS ---------- */
    h1, h2, h3 { color: #0f2557 !important; letter-spacing: -0.02em; }

    h2, h3 {
        font-weight: 700 !important;
    }

    /* Section heading with accent bar */
    .section-title {
        display: flex;
        align-items: center;
        gap: 12px;
        margin: 0.5rem 0 1.2rem 0;
    }
    .section-title .bar {
        width: 5px;
        height: 26px;
        border-radius: 3px;
        background: linear-gradient(180deg, #11998e, #38ef7d);
        flex-shrink: 0;
    }
    .section-title h3 {
        margin: 0 !important;
        padding: 0 !important;
        font-size: 1.25rem !important;
    }
    .section-title .subtitle {
        font-size: 0.85rem;
        color: #64748b;
        font-weight: 500;
        margin-left: auto;
    }

    /* ---------- PRIMARY BUTTONS: emerald gradient ---------- */
    button[kind="primary"] {
        background: linear-gradient(90deg, #11998e 0%, #38ef7d 100%) !important;
        border: none !important;
        color: white !important;
        font-weight: 700 !important;
        letter-spacing: 0.02em;
        border-radius: 12px !important;
        box-shadow: 0 6px 18px -4px rgba(17, 153, 142, 0.55) !important;
        transition: transform 0.15s ease, box-shadow 0.15s ease !important;
    }
    button[kind="primary"]:hover {
        background: linear-gradient(90deg, #0f8a80 0%, #2fd96c 100%) !important;
        transform: translateY(-1px);
        box-shadow: 0 10px 24px -4px rgba(17, 153, 142, 0.65) !important;
    }

    /* ---------- SECONDARY BUTTONS ---------- */
    button[kind="secondary"] {
        border-radius: 12px !important;
        border: 1.5px solid #cbd5e1 !important;
        color: #334155 !important;
        font-weight: 600 !important;
        background: #ffffff !important;
        transition: all 0.15s ease !important;
    }
    button[kind="secondary"]:hover {
        border-color: #11998e !important;
        color: #0f8a80 !important;
        background: #f0fdf9 !important;
    }

    /* ---------- FILTER CARD (st.container border) ---------- */
    [data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 16px !important;
        border-color: #e2e8f0 !important;
        background: linear-gradient(180deg, #fbfdff 0%, #f4f8fc 100%);
        box-shadow: 0 4px 14px -6px rgba(15, 37, 87, 0.08);
    }

    /* ---------- SELECTBOX ---------- */
    [data-testid="stSelectbox"] > div > div {
        border-radius: 10px !important;
        border-color: #dbe4ef !important;
    }
    [data-testid="stSelectbox"] label {
        font-weight: 600 !important;
        color: #334155 !important;
    }

    /* ---------- ALERTS (info / warning) softer look ---------- */
    [data-testid="stAlert"] {
        border-radius: 12px;
    }

    /* ---------- DIVIDER ---------- */
    hr {
        border-color: #e2e8f0 !important;
        margin: 1.8rem 0 !important;
    }

    /* ---------- STAT TILES ---------- */
    .stat-row {
        display: flex;
        gap: 14px;
        flex-wrap: wrap;
        margin: 4px 0 6px 0;
    }
    .stat-tile {
        flex: 1;
        min-width: 140px;
        background: linear-gradient(145deg, #ffffff 0%, #f6f9fd 100%);
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 14px 18px;
        box-shadow: 0 3px 10px -4px rgba(15, 37, 87, 0.10);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    .stat-tile:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 18px -6px rgba(15, 37, 87, 0.18);
    }
    .stat-tile .stat-label {
        font-size: 0.72rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #64748b;
        margin-bottom: 2px;
    }
    .stat-tile .stat-value {
        font-size: 1.55rem;
        font-weight: 800;
        color: #0f2557;
        line-height: 1.15;
    }
    .stat-tile .stat-accent {
        display: inline-block;
        width: 28px;
        height: 3px;
        border-radius: 2px;
        background: linear-gradient(90deg, #11998e, #38ef7d);
        margin-top: 6px;
    }

    /* ---------- LECTURER CARDS ---------- */
    .lecturer-row {
        display: flex;
        flex-direction: row;
        justify-content: center;
        align-items: stretch;
        gap: 16px;
        flex-wrap: nowrap;
        overflow-x: auto;
        padding: 6px 2px 14px 2px;
    }
    .lecturer-card {
        flex: 1;
        min-width: 22%;
        max-width: 190px;
        text-align: center;
        background: #ffffff;
        border: 1px solid #e8eef5;
        border-radius: 16px;
        padding: 18px 12px 14px 12px;
        box-shadow: 0 4px 12px -4px rgba(15, 37, 87, 0.10);
        transition: transform 0.18s ease, box-shadow 0.18s ease;
    }
    .lecturer-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 14px 28px -8px rgba(15, 37, 87, 0.22);
    }
    .lecturer-card img {
        width: 100%;
        max-width: 120px;
        aspect-ratio: 1 / 1;
        object-fit: cover;
        border-radius: 50%;
        border: 3px solid transparent;
        background:
            linear-gradient(white, white) padding-box,
            linear-gradient(135deg, #1E3A8A, #11998e, #38ef7d) border-box;
        box-shadow: 0 4px 10px rgba(15, 37, 87, 0.18);
    }
    .lecturer-card .name {
        font-size: 0.88rem;
        margin-top: 10px;
        color: #0f2557;
        font-weight: 700;
        line-height: 1.25;
    }
    .lecturer-card .role {
        font-size: 0.72rem;
        color: #11998e;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-top: 2px;
    }

    /* ---------- CUSTOM SCHEDULE TABLE ---------- */
    .schedule-wrap {
        border-radius: 14px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 8px 20px -6px rgba(15, 37, 87, 0.12);
        overflow: hidden;
        background: #ffffff;
    }
    .schedule-scroll {
        max-height: 580px;
        overflow: auto;
    }
    table.schedule {
        width: 100%;
        border-collapse: collapse;
        font-size: 0.86rem;
    }
    table.schedule thead th {
        position: sticky;
        top: 0;
        z-index: 2;
        background: linear-gradient(90deg, #0f2557 0%, #1E3A8A 100%);
        color: #ffffff;
        padding: 13px 14px;
        text-align: left;
        font-size: 0.72rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.07em;
        white-space: nowrap;
    }
    table.schedule tbody td {
        padding: 11px 14px;
        border-bottom: 1px solid #eef2f7;
        color: #334155;
        vertical-align: top;
        line-height: 1.45;
    }
    table.schedule tbody tr:nth-child(even) { background: #f8fafc; }
    table.schedule tbody tr:hover { background: #ecfdf5; }
    table.schedule tbody tr:last-child td { border-bottom: none; }

    .td-student { font-weight: 700; color: #0f2557; white-space: nowrap; }
    .td-title { min-width: 220px; color: #475569; }

    .pill {
        display: inline-block;
        padding: 3px 11px;
        border-radius: 999px;
        font-size: 0.76rem;
        font-weight: 600;
        white-space: nowrap;
    }
    .pill-date  { background: #eff6ff; color: #1E3A8A; border: 1px solid #dbeafe; }
    .pill-time  { background: #f0fdf4; color: #0f8a80; border: 1px solid #d1fae5; }
    .pill-venue { background: #fef9ec; color: #b45309; border: 1px solid #fde8c8; }

    .table-caption {
        text-align: center;
        color: #94a3b8;
        font-size: 0.78rem;
        padding: 10px 0 2px 0;
    }

    /* Mobile: table collapses into stacked cards */
    @media (max-width: 640px) {
        .schedule-scroll { max-height: none; }
        table.schedule thead { display: none; }
        table.schedule, table.schedule tbody,
        table.schedule tr, table.schedule td { display: block; width: 100%; }
        table.schedule tbody tr {
            border: 1px solid #e2e8f0;
            border-radius: 14px;
            margin: 12px 10px;
            padding: 8px 2px;
            background: #ffffff !important;
            box-shadow: 0 3px 10px -4px rgba(15, 37, 87, 0.12);
        }
        table.schedule tbody td {
            border: none;
            padding: 5px 14px;
            display: flex;
            gap: 10px;
            align-items: baseline;
        }
        table.schedule tbody td::before {
            content: attr(data-label);
            font-weight: 700;
            color: #64748b;
            font-size: 0.68rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            min-width: 88px;
            flex-shrink: 0;
        }
        .td-student, .td-title { white-space: normal; min-width: 0; }
    }

    /* ---------- VOTE CTA CARD ---------- */
    .vote-card {
        background:
            radial-gradient(ellipse 70% 90% at 85% 10%, rgba(56, 239, 125, 0.22), transparent),
            linear-gradient(135deg, #0f2557 0%, #1E3A8A 60%, #16437e 100%);
        border-radius: 18px;
        padding: 28px 30px 24px 30px;
        margin: 6px 0 18px 0;
        box-shadow: 0 16px 36px -10px rgba(15, 37, 87, 0.45);
        color: #ffffff;
    }
    .vote-card h2 {
        color: #ffffff !important;
        margin: 0 0 6px 0 !important;
        padding: 0 !important;
        font-size: 1.5rem !important;
    }
    .vote-card p {
        color: #cbd8f0;
        font-size: 0.95rem;
        margin: 0;
        line-height: 1.55;
    }
    .vote-badge {
        display: inline-block;
        background: rgba(56, 239, 125, 0.16);
        border: 1px solid rgba(56, 239, 125, 0.45);
        color: #6ef5a3;
        font-size: 0.72rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        padding: 4px 12px;
        border-radius: 999px;
        margin-bottom: 12px;
    }

    /* ---------- FOOTER ---------- */
    .app-footer {
        text-align: center;
        color: #94a3b8;
        font-size: 0.8rem;
        padding-top: 8px;
    }
    .app-footer b { color: #64748b; }

    /* ---------- MOBILE TWEAKS ---------- */
    @media (max-width: 640px) {
        .block-container {
            padding: 1.2rem 1rem 2rem 1rem !important;
            border-radius: 16px;
        }
        .stat-tile { min-width: 42%; padding: 10px 14px; }
        .stat-tile .stat-value { font-size: 1.2rem; }
        .lecturer-card { min-width: 40%; padding: 12px 8px 10px 8px; }
        .lecturer-card img { max-width: 84px; }
        .vote-card { padding: 20px 18px; }
    }
    </style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# 3. DATA LOADING (Google Sheets)
# ══════════════════════════════════════════════════════════════
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

# ══════════════════════════════════════════════════════════════
# 4. STICKY HERO HEADER (Title, Semester Badge & Flags)
# ══════════════════════════════════════════════════════════════
MIME_TYPES = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
              ".avif": "image/avif", ".webp": "image/webp", ".gif": "image/gif"}

def get_base64_img(img_path):
    try:
        path = APP_DIR / img_path
        mime = MIME_TYPES.get(path.suffix.lower(), "image/png")
        with open(path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode()
        return f"data:{mime};base64,{encoded}"
    except FileNotFoundError:
        return PLACEHOLDER_IMG

img_national = get_base64_img("national-flag.avif")
img_penang = get_base64_img("penang-state-flag.avif")
img_vitrox = get_base64_img("v-logo.jpeg")

sticky_header_html = f"""
<style>
.sticky-header-container {{
    position: sticky;
    top: 0px;
    z-index: 9999;
    background: linear-gradient(90deg, rgba(255,255,255,0.99) 0%, rgba(248,251,255,0.99) 100%);
    padding: 14px 20px;
    border: 1px solid #e6edf5;
    border-bottom: 3px solid transparent;
    border-image: linear-gradient(90deg, #1E3A8A, #11998e, #38ef7d) 1;
    border-radius: 14px 14px 0 0;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 22px;
    margin-top: -10px;
    box-shadow: 0 6px 18px -8px rgba(15, 37, 87, 0.18);
}}
.header-title-box h1 {{
    margin: 0;
    padding: 0;
    font-size: 1.45rem;
    font-weight: 800;
    color: #0f2557;
    line-height: 1.25;
    letter-spacing: -0.02em;
}}
.header-title-box .sem-badge {{
    display: inline-block;
    margin-top: 6px;
    background: linear-gradient(90deg, #11998e, #38ef7d);
    color: white;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    padding: 3px 12px;
    border-radius: 999px;
    box-shadow: 0 2px 8px -2px rgba(17, 153, 142, 0.5);
}}
.header-logos-box {{
    display: flex;
    gap: 12px;
    align-items: center;
}}
.header-logos-box img {{
    height: 38px;
    width: auto;
    border-radius: 6px;
    box-shadow: 0 2px 6px rgba(15, 37, 87, 0.18);
    transition: transform 0.15s ease;
}}
.header-logos-box img:hover {{
    transform: scale(1.08);
}}

@media (max-width: 600px) {{
    .sticky-header-container {{
        flex-direction: column;
        gap: 10px;
        align-items: center;
        text-align: center;
        padding-top: 15px;
    }}
    .header-logos-box img {{ height: 28px; }}
    .header-title-box h1 {{ font-size: 1.15rem; }}
}}
</style>

<div class="sticky-header-container fade-in">
    <div class="header-title-box">
        <h1>🎓 Diploma in Computer Science — FYP Schedule Checker</h1>
        <span class="sem-badge">Semester June 2026</span>
    </div>
    <div class="header-logos-box">
        <img src="{img_national}" alt="National Flag" title="National Flag"/>
        <img src="{img_penang}" alt="Penang Flag" title="Penang Flag"/>
        <img src="{img_vitrox}" alt="ViTrox Logo" title="ViTrox College Logo"/>
    </div>
</div>
"""
st.markdown(sticky_header_html, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# 5. LECTURER PROFILES — hover cards with gradient photo rings
# ══════════════════════════════════════════════════════════════
st.markdown("""
<div class="section-title fade-in">
    <div class="bar"></div>
    <h3>Panel of Lecturers</h3>
    <span class="subtitle">Supervisors &amp; Examiners</span>
</div>
""", unsafe_allow_html=True)

def get_lecturer_card(img_path, caption, role="Lecturer"):
    img_src = get_base64_img(img_path)

    return (
        f'<div class="lecturer-card">'
        f'<img src="{img_src}" alt="{caption}"/>'
        f'<p class="name">{caption}</p>'
        f'<p class="role">{role}</p>'
        f'</div>'
    )

lecturer_html = (
    '<div class="lecturer-row fade-in">'
    + get_lecturer_card("lim_seng_chee.png", "Ts. Dr. Lim Seng Chee")
    + get_lecturer_card("khor_jia_yun.png", "Ms. Khor Jia Yun")
    + get_lecturer_card("eng_yee_wei.png", "Mr. Eng Yee Wei")
    + get_lecturer_card("nursyahirah.png", "Ms. Syira")
    + '</div>'
)
st.markdown(lecturer_html, unsafe_allow_html=True)

st.divider()

# ══════════════════════════════════════════════════════════════
# 6. PHASE SELECTION
# ══════════════════════════════════════════════════════════════
if 'phase' not in st.session_state:
    st.session_state.phase = 'FYP 1'

st.markdown("""
<div class="section-title">
    <div class="bar"></div>
    <h3>View Schedules</h3>
    <span class="subtitle">Select the correct category before filtering</span>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    fyp1_type = "primary" if st.session_state.phase == 'FYP 1' else "secondary"
    if st.button("📘  FYP 1", use_container_width=True, type=fyp1_type):
        st.session_state.phase = 'FYP 1'
        st.rerun()

with col2:
    fyp2_type = "primary" if st.session_state.phase == 'FYP 2' else "secondary"
    if st.button("📗  FYP 2", use_container_width=True, type=fyp2_type):
        st.session_state.phase = 'FYP 2'
        st.rerun()

# ══════════════════════════════════════════════════════════════
# 7. FILTERS
# ══════════════════════════════════════════════════════════════
with st.container(border=True):
    st.markdown(f"**🔍 Filtering tools for: {st.session_state.phase}**")

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
        selected_student = st.selectbox("👤 Filter by Student", students)

    with filter_col2:
        supervisors = ['All'] + sorted(list(df_phase['Supervisor'].dropna().unique()))
        selected_sup = st.selectbox("🧑‍🏫 Filter by Supervisor", supervisors)

    with filter_col3:
        examiners = ['All'] + sorted(list(df_phase['Examiner'].dropna().unique()))
        selected_exam = st.selectbox("📝 Filter by Examiner", examiners)

# Apply filters
if selected_student != 'All':
    df_phase = df_phase[df_phase['Student Name'] == selected_student]
if selected_sup != 'All':
    df_phase = df_phase[df_phase['Supervisor'] == selected_sup]
if selected_exam != 'All':
    df_phase = df_phase[df_phase['Examiner'] == selected_exam]

# ══════════════════════════════════════════════════════════════
# 8. AT-A-GLANCE STATS + CUSTOM SCHEDULE TABLE
# ══════════════════════════════════════════════════════════════
st.markdown("<br>", unsafe_allow_html=True)

n_sessions = len(df_phase)
n_supervisors = df_phase['Supervisor'].nunique() if 'Supervisor' in df_phase.columns else 0
n_venues = df_phase['Venue'].nunique() if 'Venue' in df_phase.columns else 0
n_days = df_phase['Date'].nunique() if 'Date' in df_phase.columns else 0

st.markdown(f"""
<div class="stat-row">
    <div class="stat-tile">
        <div class="stat-label">Presentations</div>
        <div class="stat-value">{n_sessions}</div>
        <span class="stat-accent"></span>
    </div>
    <div class="stat-tile">
        <div class="stat-label">Supervisors</div>
        <div class="stat-value">{n_supervisors}</div>
        <span class="stat-accent"></span>
    </div>
    <div class="stat-tile">
        <div class="stat-label">Venues</div>
        <div class="stat-value">{n_venues}</div>
        <span class="stat-accent"></span>
    </div>
    <div class="stat-tile">
        <div class="stat-label">Days</div>
        <div class="stat-value">{n_days}</div>
        <span class="stat-accent"></span>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Column display config: header label, cell CSS class, pill CSS class
COLUMN_STYLES = {
    'Student Name': ('👤 Student Name', 'td-student', None),
    'Date':         ('📅 Date',        '',           'pill pill-date'),
    'Time':         ('🕐 Time',        '',           'pill pill-time'),
    'Venue':        ('📍 Venue',       '',           'pill pill-venue'),
    'Coach Name':   ('🤝 Coach',       '',           None),
    'FYP Title':    ('💡 FYP Title',   'td-title',   None),
    'Supervisor':   ('🧑‍🏫 Supervisor', '',          None),
    'Examiner':     ('📝 Examiner',    '',           None),
}

desired_columns = list(COLUMN_STYLES.keys())
actual_columns = [col for col in desired_columns if col in df_phase.columns]

def build_schedule_table(data, columns):
    header_cells = "".join(
        f"<th>{COLUMN_STYLES[c][0]}</th>" for c in columns
    )
    rows = []
    for _, row in data.iterrows():
        cells = []
        for c in columns:
            label, td_class, pill_class = COLUMN_STYLES[c]
            raw = row[c]
            value = "—" if pd.isna(raw) else html.escape(str(raw))
            if pill_class and value != "—":
                content = f'<span class="{pill_class}">{value}</span>'
            else:
                content = value
            cls = f' class="{td_class}"' if td_class else ""
            cells.append(f'<td{cls} data-label="{label}">{content}</td>')
        rows.append(f"<tr>{''.join(cells)}</tr>")

    return (
        '<div class="schedule-wrap fade-in"><div class="schedule-scroll">'
        f'<table class="schedule"><thead><tr>{header_cells}</tr></thead>'
        f'<tbody>{"".join(rows)}</tbody></table>'
        '</div></div>'
        f'<div class="table-caption">Showing {len(data)} scheduled presentation(s) · '
        'Data refreshes automatically every 60 seconds</div>'
    )

if df_phase.empty:
    st.info("🔎 No schedules found matching your current filters. Try widening your selection.")
else:
    st.markdown(build_schedule_table(df_phase, actual_columns), unsafe_allow_html=True)

st.divider()

# ══════════════════════════════════════════════════════════════
# 9. VOTING SECTION — gradient call-to-action card
# ══════════════════════════════════════════════════════════════
st.markdown("""
<div class="vote-card fade-in">
    <span class="vote-badge">🏆 Poster Competition</span>
    <h2>Cast Your Vote for the Best FYP2 Poster</h2>
    <p>
        Our DCS students' FYP2 posters are now on display at <b style="color:#ffffff;">Level 4, ViTrox College</b>.
        Come take a look and cast your vote for the project that impresses you the most!
    </p>
</div>
""", unsafe_allow_html=True)

st.warning("⚠️ **For the best experience:** If you face any login issues, please open the Google Form using **Google Chrome**.")

st.link_button(
    "🗳️  Click Here to Vote via Google Form",
    "https://forms.gle/y7P84Fds8VKjziDJA",
    type="primary",
    use_container_width=True
)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div class="app-footer">
    <b>ViTrox College</b> · Diploma in Computer Science · Final Year Project — Semester June 2026
</div>
""", unsafe_allow_html=True)
