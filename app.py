import streamlit as st
import requests

# Set page configuration
st.set_page_config(page_title="Currency Converter", page_icon="💵")

st.header("💵 Currency Converter")
st.write("Effortlessly convert your money with real-time exchange rates! 🌟💵")


# Fetch currency full names
def get_currency_names():
    response = requests.get("https://api.frankfurter.app/currencies")
    return response.json()


# Fetch exchange rates based on selected currency
def get_exchange_rates(base_currency):
    response = requests.get(f"https://api.frankfurter.app/latest?from={base_currency}")
    return response.json()


# Get currency names
currency_names = get_currency_names()
currency_codes = list(currency_names.keys())  # ["EUR", "USD", "GBP", etc.]
currency_options = [f"{code} - {name}" for code, name in currency_names.items()]

# User input: Amount
amount = st.number_input(
    "Enter the amount you want to convert", min_value=0.01, value=1.00, step=1.00
)

# Currency selection
col1, col2 = st.columns(2)
with col1:
    current_currency_display = st.selectbox(
        "Select The Current Currency", currency_options
    )
with col2:
    new_currency_display = st.selectbox("Select The New Currency", currency_options)

# Extract currency codes from selection
current_currency = current_currency_display.split(" - ")[0]
new_currency = new_currency_display.split(" - ")[0]

# Convert button
if st.button("Convert"):
    if current_currency == new_currency:
        st.error("Please select different currencies!")
    else:
        data = get_exchange_rates(current_currency)
        if new_currency in data["rates"]:
            conversion_rate = data["rates"][new_currency]
            converted_amount = amount * conversion_rate
            st.success(
                f"{amount} {currency_names[current_currency]} is equal to {converted_amount:.2f} {currency_names[new_currency]}"
            )
        else:
            st.error("Conversion rate not available. Please try again later.")
