import streamlit as st
import pandas as pd
import math

# Function to apply Excel-like CEILING function in Python
def ceiling(value, multiple):
    """Rounds value up to the nearest specified multiple (like Excel's CEILING function)."""
    return math.ceil(value / multiple) * multiple

# Function to calculate prices based on purchase cost
def calculate_prices(purchase_price):
    """Calculate various prices based on the given purchase price for all price ranges."""

    if 1 <= purchase_price < 10:  # Price range: $1 - $10
        club_resell_excl = round(purchase_price * 1.44, 2)
        gap_trade_excl = ceiling(purchase_price * 2, 0.05)  # CEILING applied
        wholesale_excl = round(purchase_price * 1.35, 2)
        other = round(purchase_price * 1.1, 2)
        wam_normal = round(purchase_price * 1.3, 2)
        wam_bulk = round(purchase_price * 1.2, 2)
        gap_rrp_incl = ceiling(gap_trade_excl * 1.45, 0.1)  # CEILING applied
    
    elif 10 <= purchase_price <= 100:  # Price range: $10 - $100
        club_resell_excl = round(purchase_price * 1.44, 2)
        gap_trade_excl = ceiling(purchase_price * 1.6, 0.05)  # CEILING applied
        wholesale_excl = round(purchase_price * 1.35, 2)
        other = round(purchase_price * 1.1, 2)
        wam_normal = round(purchase_price * 1.3, 2)
        wam_bulk = round(purchase_price * 1.2, 2)
        gap_rrp_incl = ceiling(gap_trade_excl * 1.34, 0.1)  # CEILING applied

    elif purchase_price > 100:  # Price range: Above $100
        club_resell_excl = round(purchase_price * 1.35, 2)
        gap_trade_excl = ceiling(purchase_price * 1.5, 0.05)  # CEILING applied
        wholesale_excl = round(purchase_price * 1.3, 2)
        other = round(purchase_price * 1.1, 2)
        wam_normal = round(purchase_price * 1.2, 2)
        wam_bulk = round(purchase_price * 1.2, 2)
        gap_rrp_incl = ceiling(gap_trade_excl * 1.35, 0.1)  # CEILING applied

    else:
        return {}  # Ignore prices outside the specified range

    # Return calculated values
    return {
        "Club R'sell Excl": club_resell_excl,
        "GAP Trade Excl": gap_trade_excl,
        "Gold, Wholesale and Buddah Excl": wholesale_excl,
        "Other": other,
        "WAM NORMAL": wam_normal,
        "WAM BULK": wam_bulk,
        "GAP RRP Incl": gap_rrp_incl
    }

# Streamlit UI
st.title("📊 GAP LG Price Calculator (All Price Ranges)")
st.write("Upload an Excel file with product costs, and get the calculated prices.")

# File upload
uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])

if uploaded_file:
    # Load data
    df = pd.read_excel(uploaded_file)

    # Check if "Purchase Price" column exists
    if "Purchase Price" not in df.columns:
        st.error("⚠️ Please make sure your file has a column named 'Purchase Price'.")
    else:
        # Apply calculations to all purchase prices
        results = df["Purchase Price"].apply(calculate_prices).apply(pd.Series)

        # Merge results with original data
        df_final = pd.concat([df, results], axis=1)

        # Display results
        st.write("✅ **Calculated Prices:**")
        st.dataframe(df_final)

        # Export to Excel
        output_file = "Calculated_Prices.xlsx"
        df_final.to_excel(output_file, index=False)

        # Download button
        with open(output_file, "rb") as f:
            st.download_button(
                label="📥 Download Excel File",
                data=f,
                file_name="Calculated_Prices.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
