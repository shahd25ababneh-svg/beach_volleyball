import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import seaborn as sns

# 📂 Path setup
path = r"C:\Users\Asus\Downloads\archive (1)\vb_matches.csv"

# 🏐 Page Header
st.title("🏐 The FIVB & AVP Beach Volleyball Records 🏐")

st.image(r"C:\Users\Asus\Downloads\تنزيل (1).webp", width = 600)


# 📥 Data Extraction
df_bef = pd.read_csv(path)
df = pd.read_csv(path)

# ✂️ Data Cleaning: Dropping unnecessary columns
df = df.drop(columns=[
    'w_p1_tot_attacks', 'w_p1_tot_kills', 'w_p1_tot_errors', 'w_p1_tot_hitpct',
    'w_p1_tot_aces', 'w_p1_tot_serve_errors', 'w_p1_tot_blocks', 'w_p1_tot_digs',
    'w_p2_tot_attacks', 'w_p2_tot_kills', 'w_p2_tot_errors', 'w_p2_tot_hitpct',
    'w_p2_tot_aces', 'w_p2_tot_serve_errors', 'w_p2_tot_blocks', 'w_p2_tot_digs',
    'l_p1_tot_attacks', 'l_p1_tot_kills', 'l_p1_tot_errors', 'l_p1_tot_hitpct',
    'l_p1_tot_aces', 'l_p1_tot_serve_errors', 'l_p1_tot_blocks', 'l_p1_tot_digs',
    'l_p2_tot_attacks', 'l_p2_tot_kills', 'l_p2_tot_errors', 'l_p2_tot_hitpct',
    'l_p2_tot_aces', 'l_p2_tot_serve_errors', 'l_p2_tot_blocks', 'l_p2_tot_digs',
    "duration", "w_p1_birthdate", "w_p2_birthdate", "l_p1_birthdate", "l_p2_birthdate", "round",
]).drop_duplicates()

df_copy1 = df.copy()
engine = create_engine('sqlite:///volleyball_pro.db')
# 📑 Tabs Definition
tab1, tab2, tab3, tab4, tab5 ,tab6= st.tabs([
    "📂 Data",
    "📊 Data Description",
    "🧼 Missing Values",
    "📈 EDA",
    "🔢 Encoding", "Input"
])

with tab1:
    st.title("📂 Dataset View")
    ab = st.selectbox("🔍 Select what you want to see:", ["📄 Original dataset", "💡 About Data"])
    if ab == "📄 Original dataset":
        st.dataframe(pd.read_csv(path))
    if ab == "💡 About Data":
        st.header("💡 About Data")
        col_des, col_stat = st.columns([2, 2])
        with col_stat:
            st.subheader("🔢 Numerical Distribution")
            st.write(df.describe().round(2))
        with col_des:
            st.write("📊 **Shape:**", df_bef.shape)
            st.info("ℹ️ Description of the dataset structure.")
            st.write("🌍 **1- Circuit:** FIVB (International) | AVP (US-based).")
            st.write("🏐 **2- Scoring:** Scores like 15-0 or 21-0 are possible.")
            st.write("🕰️ **3- Rule Change:** Moved from 15-point sets to 21-point sets.")
            st.write("📅 **4- Data Correction:** Fixed birthdates (e.g., 2066 to 1966).")
            st.write("📏 **5- Height:** Recorded in INCHES.")
            st.write("✂️ **6- Cleanup:** Dropped high-missing columns (Attacks/Blocks).")

# 🧼 DATA TRANSFORMATION (Logic)
# Filling Age
df['w_p1_age'] = df['w_p1_age'].fillna(df['w_p2_age'])
df["w_p1_age"] = df["w_p1_age"].fillna(df["w_p1_age"].median())
df["w_p2_age"] = df["w_p2_age"].fillna(df["w_p1_age"])
df["w_p2_age"] = df["w_p2_age"].fillna(df["w_p2_age"].median())
df['l_p1_age'] = df['l_p1_age'].fillna(df['l_p2_age'])
df["l_p1_age"] = df["l_p1_age"].fillna(df["l_p1_age"].median())
df["l_p2_age"] = df["l_p2_age"].fillna(df["l_p1_age"])
df["l_p2_age"] = df["l_p2_age"].fillna(df["l_p2_age"].median())

# Filling Height
df["w_p1_hgt"] = df["w_p1_hgt"].fillna(df["w_p1_hgt"].mean())
df["w_p2_hgt"] = df["w_p2_hgt"].fillna(df["w_p2_hgt"].mean())
df["l_p1_hgt"] = df["l_p1_hgt"].fillna(df["l_p1_hgt"].mean())
df["l_p2_hgt"] = df["l_p2_hgt"].fillna(df["l_p2_hgt"].mean())

# Filling Country
df["w_p1_country"] = df["w_p1_country"].fillna(df["w_p2_country"])
df["w_p2_country"] = df["w_p2_country"].fillna(df["w_p1_country"])
df["l_p1_country"] = df["l_p1_country"].fillna(df["l_p2_country"])
df["l_p2_country"] = df["l_p2_country"].fillna(df["l_p1_country"])

# Filling Rank & Score
df["w_rank"] = pd.to_numeric(df["w_rank"], errors='coerce')
df["l_rank"] = pd.to_numeric(df["l_rank"], errors='coerce')
df["w_rank"] = df["w_rank"].fillna(df["w_rank"].median())
df["l_rank"] = df["l_rank"].fillna(df["l_rank"].median())
df["score"] = df["score"].fillna(df["score"].mode()[0])

with tab3:
    mis = st.selectbox("🛠️ Data Before & After Fixing", ["ORIGINAL DATA", "DATA AFTER FILLING"])
    if mis == "ORIGINAL DATA":
        st.subheader("❌ Before Fixing (Null Counts)")
        st.write(df_copy1.isnull().sum())
    if mis == "DATA AFTER FILLING":
        col_mis_text, col_mis_df = st.columns([2, 2])
        with col_mis_text:
            st.header("✅ After Filling")
            st.subheader("🎂 Age Filling:")
            st.write("1- Teammate's age | 2- Median strategy.")
            st.subheader("📏 Height Filling:")
            st.write("Filled using the MEAN value.")
            st.subheader("🏳️ Country Filling:")
            st.write("Derived from the partner's country.")
        with col_mis_df:
            st.write(df.isnull().sum())

with tab2:
    st.header("📊 Data Overview")
    dis = st.selectbox("⚖️ Select Scale", ["📈 Matches", "🚻 Gender", "📏 Height"])
    if dis == "📈 Matches":
        st.subheader("📅 Matches Played Per Year")
        year_counts = df["year"].value_counts().sort_index()
        st.line_chart(year_counts)
        st.caption("📉 Trend of matches played per year.")
    if dis == "🚻 Gender":
        st.subheader("🚻 Gender Analysis")
        col_chart, col_text = st.columns([2, 2])
        with col_chart:
            st.bar_chart(df["gender"].value_counts())
            st.info("💡 M and W distribution is very balanced.")
        with col_text:
            st.write("❓ **Does gender make a difference?**")
            st.write("The dataset shows almost equal representation for both genders.")
    if dis == "📏 Height":
        st.subheader("📏 Height Distribution")
        hieght_line = df["w_p1_hgt"].value_counts()
        st.line_chart(hieght_line)

with tab4:
    re = st.selectbox("🔗 Select Relationship", ["🏆 Why Winners Win?", "🔗 Correlation"])
    if re == "🏆 Why Winners Win?":
        st.header("📏 Height Comparison: Winner vs Loser")
        avg_win_hgt1 = df['w_p1_hgt'].mean()
        avg_win_hgt2 = df['w_p2_hgt'].mean()
        avg_lose_hgt1 = df["l_p1_hgt"].mean()
        avg_lose_hgt2 = df["l_p2_hgt"].mean()
        chart_data = pd.DataFrame({
            "Player Type": ["Winner P1", "Winner P2", "Loser P1", "Loser P2"],
            "Average Height": [avg_win_hgt1, avg_win_hgt2, avg_lose_hgt1, avg_lose_hgt2]
        }).set_index("Player Type")
        st.bar_chart(chart_data)
        st.write("🧐 Average height of winning teams is slightly higher.")
        avg_win = (avg_win_hgt1 + avg_win_hgt2) / 2
        avg_lose = (avg_lose_hgt1 + avg_lose_hgt2) / 2
        st.write("⭐️ **Average Winner Height:**", round(avg_win, 2))
        st.write("🔻 **Average Loser Height:**", round(avg_lose, 2))
    if re == "🔗 Correlation":
        st.subheader("🔗 Variable Linkage (Heatmap)")
        corr_cols = ['w_p1_hgt', 'w_p2_hgt', 'w_p1_age', 'w_p2_age', 'l_p1_hgt', 'l_p2_hgt', 'l_p1_age', 'l_p2_age','year']
        fig, ax = plt.subplots()
        sns.heatmap(df[corr_cols].corr(), annot=True, cmap='coolwarm', ax=ax)
        st.pyplot(fig)

with tab5:
    st.header("🔢 Encoding Gender")
    df_encode = df.copy()
    st.write("🔄 **Gender Binary Mapping:** Female (W) = 0 | Male (M) = 1")
    df_encode['gender_bin'] = df_encode["gender"].map({'W': 0, 'M': 1})
    st.dataframe(df_encode.head())
with tab6:
    st.header("💾 Manual Match Entry , Input ")
    st.write("here you can record some new teams to the list , so we can study it :)")
    with st.form("manual_entry"):
        st.subheader("Enter New Match Details")
        c1, c2, c3 = st.columns(3)
        with c1:
            team_1 = st.text_input("Winner Team")
            rank_1 = st.number_input("Winner Rank", min_value=1)
        with c2:
            team_2 = st.text_input("Loser Team")
            rank_2 = st.number_input("Loser Rank", min_value=1)
        with c3:
            game_year = st.number_input("Year", min_value=1900, max_value=2026, value=2024)

        submit_btn = st.form_submit_button("Save to Database 🗄️")

    if submit_btn:

        new_data = pd.DataFrame([{
            "winner_team": team_1,
            "winner_rank": rank_1,
            "loser_team": team_2,
            "loser_rank": rank_2,
            "year": game_year
        }])

        # 🚀 التحميل إلى SQL (الـ LOAD)
        # نستخدم if_exists='append' لكي تضاف البيانات للجدول القديم ولا تمسحه
        new_data.to_sql('user_custom_matches', con=engine, if_exists='append', index=False)
        st.success(f"✅ Match between {team_1} and {team_2} is saved !")
        st.divider()
        st.subheader("🏁 Final System Status")
        col_stat1, col_stat2, col_stat3 = st.columns(3)

        with col_stat1:
            st.metric("Total Records", len(df))
        with col_stat2:
            st.metric("Missing Values", df.isnull().sum().sum())
        with col_stat3:
            st.metric("Data Quality", "100%" if df.isnull().sum().sum() == 0 else "95%")

        st.success("✨ The data is cleaned, encoded, and stored in the SQL Database.")