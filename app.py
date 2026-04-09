import streamlit as st
import pandas as pd
import os
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

# Set page configuration
st.set_page_config(
    page_title="Ходимлар Мотивацияси ва Иш Шароити Сўрови",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# ADMIN CREDENTIALS — change these to set your login/password
# ============================================================
ADMIN_LOGIN = "admin"
ADMIN_PASSWORD = "sevinch2024"

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'survey'
if 'test_completed' not in st.session_state:
    st.session_state.test_completed = False
if 'admin_logged_in' not in st.session_state:
    st.session_state.admin_logged_in = False
if 'show_admin_login' not in st.session_state:
    st.session_state.show_admin_login = False

# Options for radio buttons
RADIO_OPTIONS = [
    "1 — Қатъиян қўшилмайман",
    "2 — Қўшилмайман",
    "3 — Қисман қўшиламан",
    "4 — Қўшиламан",
    "5 — Тўлиқ қўшиламан"
]

def calculate_score(response):
    score_map = {
        "1 — Қатъиян қўшилмайман": 1,
        "2 — Қўшилмайман": 2,
        "3 — Қисман қўшиламан": 3,
        "4 — Қўшиламан": 4,
        "5 — Тўлиқ қўшиламан": 5
    }
    return score_map[response]

# Function to initialize CSV file
def initialize_csv():
    if not os.path.exists('results.csv'):
        df = pd.DataFrame(columns=[
            'Name', 'Department', 'Date', 
            'Моддий мотивация', 'Иш шароити',
            'Раҳбарият ва бошқарув', 'Касбий ривожланиш',
            'Ички мотивация'
        ])
        df.to_csv('results.csv', index=False)

# Function to save results to CSV
def save_results(name, dept, scores):
    new_row = {
        'Name': name,
        'Department': dept,
        'Date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'Моддий мотивация': scores['material'],
        'Иш шароити': scores['conditions'],
        'Раҳбарият ва бошқарув': scores['management'],
        'Касбий ривожланиш': scores['development'],
        'Ички мотивация': scores['internal']
    }
    
    df = pd.read_csv('results.csv')
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv('results.csv', index=False)

# Sidebar — survey only, no admin link visible
st.sidebar.title("🧠 Сўровнома тизими")

# Initialize CSV file
initialize_csv()

# ============================================================
# Determine which page to show
# ============================================================
show_admin = st.session_state.show_admin_login or st.session_state.admin_logged_in

if not show_admin:
    # ====================== SURVEY PAGE ======================
    st.title("🧠 Ходимлар Мотивацияси ва Иш Шароити Сўрови")
    st.markdown("---")
    
    # User Profile Section
    st.header("👤 Маълумотларингиз")
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("Исм ва фамилиянгизни киритинг:", placeholder="Масалан, Алишер Валиев")
    
    with col2:
        department = st.selectbox("Бўлимни танланг:", 
                                ["Муҳандислик", "Савдо", "Маркетинг", "Кадрлар бўлими", "Молия", "Операцион бўлим", "Бошқа"])
    
    if not name:
        st.warning("Давом этиш учун исмингизни киритинг.")
        st.stop()
    
    st.markdown("---")
    
    # Motivation and Stress Test
    st.header("📋 Сўровнома саволлари")
    st.write("Илтимос, барча саволларга холисона жавоб беринг.")
    
    st.subheader("💰 Моддий мотивация")
    q1 = st.radio("1. Мен олаётган иш ҳақим меҳнатимга муносиб деб ҳисоблайман.", RADIO_OPTIONS, index=2)
    q2 = st.radio("2. Муассасадаги мукофот ва қўшимча тўловлар мени рағбатлантиради.", RADIO_OPTIONS, index=2)
    q3 = st.radio("3. Моддий рағбат (премия, устама) иш самарадорлигимни оширади.", RADIO_OPTIONS, index=2)

    st.subheader("🏢 Иш шароити")
    q4 = st.radio("4. Иш жойимдаги шароитлар (жиҳозлар, тозалик, қулайлик) мени қониқтиради.", RADIO_OPTIONS, index=2)
    q5 = st.radio("5. Иш юкламаси адолатли тақсимланган деб ўйлайман.", RADIO_OPTIONS, index=2)
    q6 = st.radio("6. Иш жадвалим мен учун мақбул.", RADIO_OPTIONS, index=2)

    st.subheader("👔 Раҳбарият ва бошқарув")
    q7 = st.radio("7. Раҳбарият менинг меҳнатимни муносиб баҳолайди.", RADIO_OPTIONS, index=2)
    q8 = st.radio("8. Раҳбарим билан очиқ мулоқот қилиш имкониятига эгаман.", RADIO_OPTIONS, index=2)
    q9 = st.radio("9. Муассасада қарорлар адолатли қабул қилинади.", RADIO_OPTIONS, index=2)

    st.subheader("📈 Касбий ривожланиш")
    q10 = st.radio("10. Муассасада малакамни ошириш имкониятлари етарли.", RADIO_OPTIONS, index=2)
    q11 = st.radio("11. Янги кўникмалар ўрганишга рағбатлантириламан.", RADIO_OPTIONS, index=2)
    q12 = st.radio("12. Касбий ўсиш истиқболим бор деб ҳис қиламан.", RADIO_OPTIONS, index=2)

    st.subheader("❤️ Ички (номоддий) мотивация")
    q13 = st.radio("13. Ишдан маънавий қониқиш оламан.", RADIO_OPTIONS, index=2)
    q14 = st.radio("14. Жамоада ишлаш муҳити менга ёқади.", RADIO_OPTIONS, index=2)
    q15 = st.radio("15. Яқин келажакда шу муассасада ишлашни давом эттирмоқчиман.", RADIO_OPTIONS, index=2)

    if st.button("🚀 Натижаларни юбориш", type="primary"):
        scores = {
            'material': round((calculate_score(q1) + calculate_score(q2) + calculate_score(q3)) / 3, 1),
            'conditions': round((calculate_score(q4) + calculate_score(q5) + calculate_score(q6)) / 3, 1),
            'management': round((calculate_score(q7) + calculate_score(q8) + calculate_score(q9)) / 3, 1),
            'development': round((calculate_score(q10) + calculate_score(q11) + calculate_score(q12)) / 3, 1),
            'internal': round((calculate_score(q13) + calculate_score(q14) + calculate_score(q15)) / 3, 1)
        }
        
        # Save results
        save_results(name, department, scores)
        
        # Display results
        st.success("✅ Сўровнома муваффақиятли якунланди!")
        st.markdown("---")
        
        st.header("📊 Сизнинг натижаларингиз (Ўртача баллар 1-5)")
        
        fig = go.Figure(data=[
            go.Bar(name='Кўрсаткичлар', x=['Моддий мотивация', 'Иш шароити', 'Раҳбарият ва бошқарув', 'Касбий ривожланиш', 'Ички мотивация'], 
                   y=[scores['material'], scores['conditions'], scores['management'], scores['development'], scores['internal']], 
                   marker_color=['#2196F3', '#FF9800', '#F44336', '#9C27B0', '#4CAF50'])
        ])
        fig.update_layout(yaxis=dict(range=[0, 5]))
        st.plotly_chart(fig, use_container_width=True)

        st.session_state.test_completed = True

    # ====================== FOOTER ======================
    st.markdown("---")
    st.markdown("💚 *Ходимлар сўровномаси тизими*")

    # Hidden admin button — very small, at the very bottom, looks like a footer link
    st.markdown("")
    st.markdown("")
    st.markdown("")
    if st.button("⚙️", help="Тизим созламалари", key="admin_access_btn"):
        st.session_state.show_admin_login = True
        st.rerun()

elif st.session_state.show_admin_login and not st.session_state.admin_logged_in:
    # ====================== ADMIN LOGIN PAGE ======================
    st.title("🔐 Тизимга кириш")
    st.markdown("---")

    with st.form("admin_login_form"):
        login_input = st.text_input("Логин:", placeholder="Логинни киритинг")
        password_input = st.text_input("Парол:", type="password", placeholder="Паролни киритинг")
        submitted = st.form_submit_button("Кириш", type="primary")

        if submitted:
            if login_input == ADMIN_LOGIN and password_input == ADMIN_PASSWORD:
                st.session_state.admin_logged_in = True
                st.session_state.show_admin_login = False
                st.rerun()
            else:
                st.error("❌ Логин ёки парол нотўғри!")

    if st.button("⬅️ Орқага"):
        st.session_state.show_admin_login = False
        st.rerun()

else:
    # ====================== ADMIN DASHBOARD ======================
    st.title("📊 Админ Панель")
    st.markdown("---")

    # Logout button in sidebar
    if st.sidebar.button("🚪 Чиқиш (Админ)"):
        st.session_state.admin_logged_in = False
        st.session_state.show_admin_login = False
        st.rerun()
    
    try:
        df = pd.read_csv('results.csv')
        
        if df.empty:
            st.warning("Ҳозирча сўровнома маълумотлари йўқ.")
        else:
            st.header("📈 Умумий статистика")
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Умумий иштирокчилар", len(df))
            with col2:
                dept_count = df['Department'].nunique()
                st.metric("Бўлимлар сони", dept_count)
            
            st.markdown("---")
            
            st.header("🏢 Бўлимлар бўйича таҳлил")
            
            # Average score by department
            avg_cols = ['Моддий мотивация', 'Иш шароити', 'Раҳбарият ва бошқарув', 'Касбий ривожланиш', 'Ички мотивация']
            dept_avg = df.groupby('Department')[avg_cols].mean().reset_index()

            fig_dept = go.Figure()
            colors = ['#2196F3', '#FF9800', '#F44336', '#9C27B0', '#4CAF50']
            for idx, col in enumerate(avg_cols):
                fig_dept.add_trace(go.Bar(name=col, x=dept_avg['Department'], y=dept_avg[col], marker_color=colors[idx]))
            
            fig_dept.update_layout(barmode='group', title='Бўлимлар бўйича ўртача кўрсаткичлар')
            st.plotly_chart(fig_dept, use_container_width=True)
            
            st.markdown("---")
            
            # Detailed Results Table
            st.header("📋 Батафсил натижалар")
            
            col1, col2 = st.columns(2)
            with col1:
                selected_dept = st.selectbox("Бўлим бўйича филтрлаш:", ["Барчаси"] + list(df['Department'].unique()))
            with col2:
                date_range = st.date_input("Сана бўйича филтрлаш:", [])
            
            filtered_df = df.copy()
            if selected_dept != "Барчаси":
                filtered_df = filtered_df[filtered_df['Department'] == selected_dept]
            
            if len(date_range) == 2:
                filtered_df['Date'] = pd.to_datetime(filtered_df['Date'])
                start_date = pd.to_datetime(date_range[0])
                end_date = pd.to_datetime(date_range[1])
                filtered_df = filtered_df[(filtered_df['Date'] >= start_date) & (filtered_df['Date'] <= end_date)]
            
            st.dataframe(filtered_df, use_container_width=True)
            
            if st.button("📥 Натижаларни юклаб олиш (CSV)"):
                csv = filtered_df.to_csv(index=False)
                st.download_button(
                    label="CSV файлни юклаб олиш",
                    data=csv,
                    file_name=f"sorovnoma_natijalari_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
    
    except FileNotFoundError:
        st.error("Маълумотлар файли топилмади.")
    except Exception as e:
        st.error(f"Хатолик: {str(e)}")

    st.markdown("---")
    st.markdown("💚 *Ходимлар сўровномаси тизими*")
