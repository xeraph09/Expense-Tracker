import streamlit as st

st.title("Expense Tracker")

# Currency exchange rates (update these or fetch from an API)
EXCHANGE_RATES = {
    "USD": 1.0,
    "PHP": 56.5,  # Philippine Peso
    "EUR": 0.92,
    "GBP": 0.79,
    "JPY": 154.5
}

# Initialize session state
if "expenses" not in st.session_state:
    st.session_state.expenses = []
if "next_id" not in st.session_state:
    st.session_state.next_id = 0

# Sidebar for currency selection
st.sidebar.header("Settings")
display_currency = st.sidebar.selectbox("Display Currency", list(EXCHANGE_RATES.keys()), index=0)
input_currency = st.sidebar.selectbox("Input Currency", list(EXCHANGE_RATES.keys()), index=0)

def convert_currency(amount, from_currency, to_currency):
    """Convert amount from one currency to another"""
    if from_currency == to_currency:
        return amount
    amount_in_usd = amount / EXCHANGE_RATES[from_currency]
    return amount_in_usd * EXCHANGE_RATES[to_currency]

# Add Expense Section
st.header("Add New Expense")
col1, col2, col3 = st.columns(3)

with col1:
    description = st.text_input("Expense name", key="new_description")
with col2:
    amount = st.number_input("Amount", min_value=0.0, key="new_amount")
with col3:
    category = st.selectbox("Category", ["Food", "Transport", "Bills", "Entertainment", "Shopping", "Health", "Education", "Other"], key="new_category")

if st.button("Add Expense", type="primary"):
    if description.strip():
        st.session_state.expenses.append({
            "id": st.session_state.next_id,
            "description": description,
            "amount": amount,
            "category": category,
            "currency": input_currency
        })
        st.session_state.next_id += 1
        st.success("Expense added!")
        st.rerun()
    else:
        st.error("Please enter an expense name")

# Display Expenses Section
st.header("Your Expenses")

if st.session_state.expenses:
    total_usd = 0
    for expense in st.session_state.expenses:
        # Convert to display currency
        converted_amount = convert_currency(
            expense["amount"],
            expense["currency"],
            display_currency
        )
        total_usd += convert_currency(expense["amount"], expense["currency"], "USD")
        
        col1, col2, col3, col4, col5 = st.columns([2, 1, 1.5, 0.8, 0.8])
        
        with col1:
            st.write(f"**{expense['description']}**")
            st.caption(f"Category: {expense['category']}")
        
        with col2:
            currency_label = f" ({expense['currency']})"
            st.metric("Amount", f"{converted_amount:.2f}", label_visibility="collapsed")
        
        with col3:
            if display_currency != expense['currency']:
                st.caption(f"Orig: {expense['amount']:.2f} {expense['currency']}")
        
        with col4:
            if st.button("✏️ Edit", key=f"edit_{expense['id']}"):
                st.session_state.editing_id = expense['id']
                st.rerun()
        
        with col5:
            if st.button("🗑️ Delete", key=f"delete_{expense['id']}"):
                st.session_state.expenses = [e for e in st.session_state.expenses if e['id'] != expense['id']]
                st.success("Expense deleted!")
                st.rerun()
        
        st.divider()
    
    # Display Total
    total_converted = convert_currency(total_usd, "USD", display_currency)
    st.subheader(f"Total: {total_converted:.2f} {display_currency}")
else:
    st.info("No expenses yet. Add one to get started!")

# Edit Expense Modal
if "editing_id" in st.session_state:
    expense_to_edit = next((e for e in st.session_state.expenses if e['id'] == st.session_state.editing_id), None)
    
    if expense_to_edit:
        st.header("Edit Expense")
        
        edit_description = st.text_input("Expense name", value=expense_to_edit["description"], key="edit_description")
        edit_amount = st.number_input("Amount", value=expense_to_edit["amount"], min_value=0.0, key="edit_amount")
        edit_category = st.selectbox("Category", ["Food", "Transport", "Bills", "Entertainment", "Shopping", "Health", "Education", "Other"], 
                                     index=["Food", "Transport", "Bills", "Entertainment", "Shopping", "Health", "Education", "Other"].index(expense_to_edit["category"]),
                                     key="edit_category")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Save Changes", type="primary"):
                expense_to_edit["description"] = edit_description
                expense_to_edit["amount"] = edit_amount
                expense_to_edit["category"] = edit_category
                del st.session_state.editing_id
                st.success("Expense updated!")
                st.rerun()
        
        with col2:
            if st.button("Cancel"):
                del st.session_state.editing_id
                st.rerun()