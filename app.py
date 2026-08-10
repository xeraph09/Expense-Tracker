import streamlit as st

st.title("Expense Tracker")

if "expenses" not in st.session_state:
    st.session_state.expenses = []

description = st.text_input("Expense name")
amount = st.number_input("Amount", min_value=0.0)
category = st.selectbox("Category", ["Food", "Transport", "Bills", "Entertainment", "Shopping", "Health", "Education", "Other"])

if st.button("Add Expense"):
    st.session_state.expenses.append({
        "description": description,
        "amount": amount,
        "category": category
    })
    st.success("Expense added")

st.subheader("Your Expenses")

for expense in st.session_state.expenses:
    st.write(f"{expense['description']} - {expense['category']} - ${expense['amount']:.2f}")

total = sum(expense["amount"] for expense in st.session_state.expenses)
st.write(f"Total: ${total:.2f}")