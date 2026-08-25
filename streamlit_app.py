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
    # Hide the sidebar DOM container on the login page
    st.markdown(
        """
        <style>
            [data-testid="stSidebar"] {
                display: none !important;
            }
            [data-testid="stSidebarCollapsedControl"] {
                display: none !important;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )








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
    
    






# ----------------------------
# DASHBOARD
# ----------------------------
def dashboard():


    st.title("Meat Marketing Page")

    st.sidebar.image ("Plattered Logo.png")
   

    st.sidebar.title("Page Navigation")

    st.sidebar.page_link ("streamlit_app.py", label ="Meat Marketing")
    st.sidebar.page_link("pages/Vegetable_Marketing.py", label ="Vegetable Marketing")


    st.sidebar.header("Vegetable Purchase Filters")
    #LOAD DATA
    vegpurchasedate_df = pd.read_csv ("VegPurchaseDate.csv")
    vegduration_df = pd.read_csv ("VegDuration.csv")
    vegamount_df = pd.read_csv ("VegTotalAmt.csv") 
    vegpurchasebd_df = pd.read_csv ("VegPurchaseBD.csv")

    #SELECTOR
    selected_month = st.sidebar.selectbox(
        "Select Month",
        vegpurchasedate_df["Month"].dropna()
    )

    vegpurchasedate_df = vegpurchasedate_df[vegpurchasedate_df["Month"] == selected_month].iloc[0]
    vegduration_df = vegduration_df[vegduration_df["Month"] == selected_month].iloc[0]
    vegamount_df = vegamount_df[vegamount_df["Month"] == selected_month].iloc[0]



    ########### PURCHASE DATA 
    st.sidebar.title("Meat Purchase Filters")

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

    st.sidebar.button("Logout", on_click=logout)

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

    st.title("Purchase Breakdown")

    # 1. Load local CSV file directly
    purchase_df = pd.read_csv("Purchase_Breakdown.csv")

    # Clean column headers (strips hidden trailing/leading spaces)
    purchase_df.columns = purchase_df.columns.str.strip()

    # 2. Robust Numeric Cleaning
    # Extract only numbers and decimals from Purchase_Quantity (handles "1.5 kg", "500g", etc.)
    purchase_df["Purchase_Quantity"] = (
    purchase_df["Purchase_Quantity"]
    .astype(str)
    .str.extract(r"([\d.]+)", expand=False)
    )
    purchase_df["Purchase_Quantity"] = pd.to_numeric(purchase_df["Purchase_Quantity"], errors="coerce").fillna(0)

    # Clean Unit_Price and Amt_Spent (removes currency symbols, commas, and spaces)
    for col in ["Amt_Spent", "Unit_Price"]:
        if col in purchase_df.columns:
         purchase_df[col] = (
            purchase_df[col]
            .astype(str)
            .str.replace(r"[^\d.]", "", regex=True)
        )
        purchase_df[col] = pd.to_numeric(purchase_df[col], errors="coerce").fillna(0)

    # 3. Filter Widgets (Month & Category)
    col_filter1, col_filter2 = st.columns(2)

    with col_filter1:
        months_list = ["All Months"] + list(purchase_df["Month"].dropna().unique())
        selected_month = st.selectbox("Filter by Month", options=months_list)

    with col_filter2:
        categories_list = ["All Categories"] + list(purchase_df["Purchase_Category"].dropna().unique())
        selected_category = st.selectbox("Filter by Category", options=categories_list)

    # Apply Filters
    filtered_df = purchase_df.copy()

    if selected_month != "All Months":
        filtered_df = filtered_df[filtered_df["Month"] == selected_month]

    if selected_category != "All Categories":
        filtered_df = filtered_df[filtered_df["Purchase_Category"] == selected_category]

    # Calculate relative cost share for micro-bars
    max_amount = filtered_df["Amt_Spent"].max() if not filtered_df.empty and filtered_df["Amt_Spent"].max() > 0 else 1
    filtered_df["Cost Share"] = filtered_df["Amt_Spent"] / max_amount

    # 4. Key Metrics Summary
    total_spent = filtered_df["Amt_Spent"].sum()
    col1, col2 = st.columns(2)
    col1.metric("Total Spent", f"₱{total_spent:,.2f}")
    col2.metric("Items Purchased", f"{len(filtered_df)} items")

    st.divider()

    # 5. Interactive Micro-Bar Table
    st.dataframe(
        filtered_df[[
        "Month", 
        "Purchase_Name", 
        "Purchase_Category",
        "Unit_Price", 
        "Purchase_Quantity", 
        "Amt_Spent", 
        "Cost Share"
    ]],
    column_config={
        "Month": st.column_config.TextColumn("Month", width="small"),
        "Purchase_Name": st.column_config.TextColumn("Item Name", width="medium"),
        "Purchase_Category": st.column_config.TextColumn("Category", width="small"),
        "Unit_Price": st.column_config.NumberColumn("Unit Price", format="₱%.2f"),
        "Purchase_Quantity": st.column_config.NumberColumn("Qty", format="%.2f"),
        "Amt_Spent": st.column_config.NumberColumn("Final Cost", format="₱%.2f"),
        "Cost Share": st.column_config.ProgressColumn(
            "Relative Cost",
            help="Cost scaled relative to the highest purchase in the current view",
            format=" ",
            min_value=0.0,
            max_value=1.0,
            width="medium"
        )
    },
    hide_index=True,
    use_container_width=True
)












    

   
   

   

# ----------------------------
# APP CONTROLLER (OUTSIDE FUNCTIONS)
# ----------------------------
if st.session_state.authenticated:
    dashboard()
else:
    login_screen()
