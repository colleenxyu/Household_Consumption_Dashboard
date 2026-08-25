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

    st.title("Vegetable Marketing Page")

    st.subheader ("Purchase Data")

    st.sidebar.image ("Plattered Logo.png")

    st.sidebar.title("Page Navigation")

    st.sidebar.page_link ("streamlit_app.py", label ="Meat Marketing")
    st.sidebar.page_link("pages/Vegetable_Marketing.py", label ="Vegetable Marketing")


    st.sidebar.header("Vegetable Purchase Filters")
    #LOAD DATA
    vegpurchasedate_df = pd.read_csv ("VegPurchaseDate.csv")
    vegduration_df = pd.read_csv ("VegDuration.csv")
    vegamount_df = pd.read_csv ("VegTotalAmt.csv") 

    #SELECTOR
    selected_month = st.sidebar.selectbox(
        "Select Month",
        vegpurchasedate_df["Month"].dropna()
    )

    vegpurchasedate_df = vegpurchasedate_df[vegpurchasedate_df["Month"] == selected_month].iloc[0]
    vegduration_df = vegduration_df[vegduration_df["Month"] == selected_month].iloc[0]
    vegamount_df = vegamount_df[vegamount_df["Month"] == selected_month].iloc[0]



    st.sidebar.header("Meat Purchase Filters")
    
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
       
        st.metric("Purchase Date", vegpurchasedate_df["Purchase_Date_Veg"])
    

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
        
        st.metric("Purchase Duration", f"{vegduration_df["Veg_Duration"]} days")
       

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
        
        st.metric("Amount Spent", f" ₱ {vegamount_df['Total_Amt_Veg']:,.2f}")


    

   
    

        

# ----------------------------
# APP CONTROLLER (OUTSIDE FUNCTIONS)
# ----------------------------
if st.session_state.authenticated:
    dashboard()
else:
    login_screen()
