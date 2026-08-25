import pandas as pd
import streamlit as st
import plotly.express as px 

st.set_page_config(page_title="Household Dashboard", page_icon="🍽", layout="wide")

PASSWORD = st.secrets["dashboard_password"]

# ----------------------------
# SESSION STATE
# ----------------------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# ----------------------------
# LOGIN
# ----------------------------
def login_screen():
    st.title("🔐 User Login")

    password = st.text_input("Enter password", type="password")

    if st.button("Enter Dashboard"):
        if password == PASSWORD:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Incorrect password")

# ----------------------------
# LOGOUT
# ----------------------------
def logout():
    st.session_state.authenticated = False
    st.rerun()

# ----------------------------
# DASHBOARD
# ----------------------------
def dashboard():

    st.title("Household Consumption Dashboard")

    st.subheader ("Purchase Data")

    st.sidebar.image ("Plattered Logo.png")
    st.sidebar.header("Purchase Data Filter")
    

    # LOAD DATA
    purchasedate_df = pd.read_csv("Purchase_Date.csv")
    purchasedur_df = pd.read_csv("Purchase_Duration.csv")
    amtspent_df = pd.read_csv("Total_Amount_Spent.csv")

    selected_month = st.sidebar.selectbox(
        "Select Month",
        purchasedate_df["Month"].dropna()
    )

    purchasedate_df = purchasedate_df[purchasedate_df["Month"] == selected_month].iloc[0]
    purchasedur_df = purchasedur_df[purchasedur_df["Month"] == selected_month].iloc[0]
    amtspent_df = amtspent_df[amtspent_df["Month"] == selected_month].iloc[0]

   

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
    <style>
    .kpi-card {
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.15);
        padding: 18px;
        border-radius: 15px;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)
       
        st.metric("Purchase Date", purchasedate_df["Purchase_Date"])
    

    with col2:
        st.markdown("""
    <style>
    .kpi-card {
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.15);
        padding: 18px;
        border-radius: 15px;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)
        
        st.metric("Purchase Duration", purchasedur_df["Duration"])
       

    with col3:
        st.markdown("""
    <style>
    .kpi-card {
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.15);
        padding: 18px;
        border-radius: 15px;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)
        
        st.metric("Amount Spent", f" ₱ {amtspent_df['Amt_Spent']:,.2f}")


    

   
    st.subheader ("Purchase Breakdown")

    df = pd.read_csv("Purchase_Breakdown.csv")
    
        # Create dropdown of months
    month_list = sorted(df["Month"].dropna().unique())

    #piechart selectbox
    st.sidebar.header ("Purchase Breakdown Filter")
    selected_month = st.sidebar.selectbox(
        "Select Month",
        month_list
    )

    st.sidebar.button("Logout", on_click=logout)

    # Filter dataframe
    filtered_df = df[df["Month"] == selected_month]

    # Create pie chart
    fig = px.pie(
        filtered_df,
        values="Amt_Spent",
        names="Purchase_Category",
        
)

    

     # ✨ Transparent / frosted-style background
    fig.update_layout(
            paper_bgcolor="rgba(255,255,255,0.6)",
            plot_bgcolor="rgba(255,255,255,0.6)"
    )

    st.plotly_chart(fig)


        

# ----------------------------
# APP CONTROLLER (OUTSIDE FUNCTIONS)
# ----------------------------
if st.session_state.authenticated:
    dashboard()
else:
    login_screen()
