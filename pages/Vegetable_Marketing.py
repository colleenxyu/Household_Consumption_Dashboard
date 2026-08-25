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

    st.title("Purchase Breakdown")

    # 1. Load local CSV file directly
    vegpurchasebd_df = pd.read_csv("VegPurchaseBD.csv")

    # Clean column headers (strips hidden trailing/leading spaces)
    vegpurchasebd_df.columns = vegpurchasebd_df.columns.str.strip()

    # Clean text columns (strips extra spaces)
    for text_col in ["Month", "Purchase_Name", "Unit_Name"]:
        if text_col in vegpurchasebd_df.columns:
            vegpurchasebd_df[text_col] = vegpurchasebd_df[text_col].astype(str).str.strip()

    # 2. Robust Numeric Cleaning
    # Extract numbers and decimals from Purchase_Qty (handles "1.4 kg", "500 g", etc.)
        vegpurchasebd_df["Purchase_Qty"] = (
        vegpurchasebd_df["Purchase_Qty"]
        .astype(str)
        .str.extract(r"([\d.]+)", expand=False)
)
    vegpurchasebd_df["Purchase_Qty"] = pd.to_numeric(vegpurchasebd_df["Purchase_Qty"], errors="coerce").fillna(0)

    # Clean Unit_Price and Amount (removes currency symbols, commas, and spaces)
    for col in ["Amount", "Unit_Price"]:
        if col in vegpurchasebd_df.columns:
            vegpurchasebd_df[col] = (
            vegpurchasebd_df[col]
            .astype(str)
            .str.replace(r"[^\d.]", "", regex=True)
        )
        vegpurchasebd_df[col] = pd.to_numeric(vegpurchasebd_df[col], errors="coerce").fillna(0)

    # 3. Filter Widgets (Month & Item Name)
    col_filter1, col_filter2 = st.columns(2)

    with col_filter1:
        months_list = ["All Months"] + sorted(list(vegpurchasebd_df["Month"].dropna().unique()))
        selected_month = st.selectbox("Filter by Month", options=months_list)

    with col_filter2:
        items_list = ["All Items"] + sorted(list(vegpurchasebd_df["Purchase_Name"].dropna().unique()))
        selected_item = st.selectbox("Filter by Item", options=items_list)

    # Apply Filters
    filtered_df = vegpurchasebd_df.copy()

    if selected_month != "All Months":
        filtered_df = filtered_df[filtered_df["Month"] == selected_month]

    if selected_item != "All Items":
        filtered_df = filtered_df[filtered_df["Purchase_Name"] == selected_item]

    # Calculate relative cost share for micro-bars
    max_amount = filtered_df["Amount"].max() if not filtered_df.empty and filtered_df["Amount"].max() > 0 else 1
    filtered_df["Cost Share"] = filtered_df["Amount"] / max_amount

    # 4. Key Metrics Summary (Total Spent, Items Count, Total Qty)
    total_spent = filtered_df["Amount"].sum()
    total_items = len(filtered_df)
    total_qty = filtered_df["Purchase_Qty"].sum()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Spent", f"₱{total_spent:,.2f}")
    col2.metric("Items Purchased", f"{total_items} items")
    col3.metric("Total Quantity", f"{total_qty:,.2f}")

    st.divider()

    # 5. Interactive Micro-Bar Table
    st.dataframe(
        filtered_df[[
        "Month", 
        "Purchase_Name", 
        "Unit_Price", 
        "Unit_Name", 
        "Purchase_Qty", 
        "Amount", 
        "Cost Share"
    ]],
    column_config={
        "Month": st.column_config.TextColumn("Month", width="small"),
        "Purchase_Name": st.column_config.TextColumn("Item Name", width="medium"),
        "Unit_Price": st.column_config.NumberColumn("Unit Price", format="₱%.2f"),
        "Unit_Name": st.column_config.TextColumn("Unit", width="small"),
        "Purchase_Qty": st.column_config.NumberColumn("Qty", format="%.2f"),
        "Amount": st.column_config.NumberColumn("Final Cost", format="₱%.2f"),
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
