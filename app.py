import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="Dataset Analyzer",
    page_icon="📊",
    layout="wide"
)

# ---------------- CUSTOM CSS ---------------- #

# ---------------- CUSTOM CSS ---------------- #

st.markdown("""
<style>

/* Main Background */
.stApp {
    background-color: #f1f5f9;
}

/* Main Title */
h1 {
    text-align: center;
    color: #2563eb;
    font-size: 42px;
    font-weight: bold;
}

/* Section Headers */
h2, h3 {
    color: #1e293b;
}

/* Upload Box */
[data-testid="stFileUploader"] {
    background-color: white;
    padding: 20px;
    border-radius: 15px;
    border: 2px solid #cbd5e1;
}

/* Dataframe */
.stDataFrame {
    background-color: white;
    border-radius: 12px;
    padding: 10px;
}

/* Metrics */
[data-testid="metric-container"] {
    background-color: white;
    border: 1px solid #cbd5e1;
    padding: 15px;
    border-radius: 12px;
}

/* Buttons */
.stButton>button,
.stDownloadButton>button {
    background: linear-gradient(to right, #2563eb, #06b6d4);
    color: white;
    border: none;
    border-radius: 10px;
    height: 3em;
    width: 100%;
    font-size: 16px;
    font-weight: bold;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #e2e8f0;
}

/* Success Message */
.stSuccess {
    background-color: #dcfce7;
    color: #166534;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ---------------- #

st.title("📊 Automated Dataset Analysis Tool")

st.write(
    "Upload a CSV dataset to perform automatic analysis, cleaning, and visualization."
)

# ---------------- FILE UPLOAD ---------------- #

uploaded_file = st.file_uploader(
    "📁 Upload CSV File",
    type=["csv"]
)

# ---------------- PROCESS DATA ---------------- #

if uploaded_file is not None:

    # Read Dataset
    df = pd.read_csv(uploaded_file)

    # ---------------- PREVIEW ---------------- #

    st.subheader("📌 Dataset Preview")

    st.dataframe(df.head())

    # ---------------- INFO ---------------- #

    st.subheader("📊 Dataset Information")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Rows", df.shape[0])

    with col2:
        st.metric("Columns", df.shape[1])

    # ---------------- MISSING VALUES ---------------- #

    st.subheader("❌ Missing Values")

    st.write(df.isnull().sum())

    # ---------------- NULL PERCENTAGE ---------------- #

    st.subheader("📉 Null Value Percentage")

    null_percent = (df.isnull().sum() / len(df)) * 100

    st.write(null_percent)

    # ---------------- SUMMARY ---------------- #

    st.subheader("📈 Statistical Summary")

    st.dataframe(df.describe())

    # ---------------- HEATMAP ---------------- #

    st.subheader("🔥 Correlation Heatmap")

    numeric_df = df.select_dtypes(include=['number'])

    if not numeric_df.empty:

        fig, ax = plt.subplots(figsize=(5, 3))

        sns.heatmap(
            numeric_df.corr(),
            annot=True,
            cmap='Blues',
            ax=ax
        )

        plt.title("Correlation Heatmap", color='white')

        fig.patch.set_facecolor('#0f172a')
        ax.set_facecolor('#0f172a')

        st.pyplot(fig)

    # ---------------- VISUALIZATION ---------------- #

    st.subheader("📊 Automatic Visualization")

    column = st.selectbox(
        "Select Column",
        df.columns
    )

    # -------- CATEGORICAL -------- #

    if df[column].dtype == 'object':

        fig, ax = plt.subplots(figsize=(4, 3))

        df[column].value_counts().head(10).plot(
            kind='bar',
            color='#06b6d4',
            ax=ax
        )

        plt.xticks(rotation=45)

        plt.title(f"{column} Distribution")

        fig.patch.set_facecolor('#0f172a')
        ax.set_facecolor('#0f172a')

        st.pyplot(fig)

    # -------- NUMERICAL -------- #

    else:

        fig, ax = plt.subplots(figsize=(4, 3))

        sns.histplot(
            df[column],
            kde=True,
            color='#2563eb',
            ax=ax
        )

        plt.title(f"{column} Histogram")

        fig.patch.set_facecolor('#0f172a')
        ax.set_facecolor('#0f172a')

        st.pyplot(fig)

    # ---------------- DUPLICATES ---------------- #

    st.subheader("🧾 Duplicate Records")

    st.write(
        "Duplicate Rows:",
        df.duplicated().sum()
    )

    # ---------------- DOWNLOAD ---------------- #

    st.subheader("⬇ Download Cleaned Dataset")

    cleaned_df = df.dropna()

    csv = cleaned_df.to_csv(index=False).encode('utf-8')

    st.download_button(
        label="Download Cleaned CSV",
        data=csv,
        file_name="cleaned_dataset.csv",
        mime="text/csv"
    )

    # ---------------- SUCCESS ---------------- #

    st.success("✅ Analysis Completed Successfully!")