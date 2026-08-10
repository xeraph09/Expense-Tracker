import streamlit as st

st.title("Expense Tracker")

EXCHANGE_RATES = {
    "USD": 1.0,
    "PHP": 55.0,
    "EUR": 0.92,
    "JPY": 150.0,
    "GBP": 0.80,
}
CURRENCY_SYMBOLS = {
    "USD": "$",
    "PHP": "₱",
    "EUR": "€",
    "JPY": "¥",
    "GBP": "£",
}
CATEGORIES = ["Food", "Transport", "Bills", "Entertainment", "Shopping", "Health", "Education", "Other"]

if "expenses" not in st.session_state:
    st.session_state.expenses = []
    st.session_state.edit_index = None

def parse_amount(value: str) -> float | None:
    try:
        parsed = float(value)
        return parsed if parsed >= 0 else None
    except ValueError:
        return None

with st.form("add_expense_form"):
    description = st.text_input("Expense description")
    amount_text = st.text_input("Amount", placeholder="Enter amount")
    currency = st.selectbox("Currency", list(EXCHANGE_RATES.keys()))
    category = st.selectbox("Category", CATEGORIES)
    add_expense = st.form_submit_button("Add Expense")

if add_expense:
    amount = parse_amount(amount_text)
    if amount is None:
        st.error("Please enter a valid amount greater than or equal to 0.")
    else:
        st.session_state.expenses.append({
            "description": description,
            "amount": amount,
            "currency": currency,
            "category": category,
        })
        st.success("Expense added")

if st.session_state.edit_index is not None:
    index = st.session_state.edit_index
    expense = st.session_state.expenses[index]
    st.subheader(f"Edit expense #{index + 1}")

    edit_description = st.text_input("Description", value=expense["description"], key="edit_description")
    edit_amount_text = st.text_input("Amount", value=str(expense["amount"]), key="edit_amount")
    edit_currency = st.selectbox(
        "Currency",
        list(EXCHANGE_RATES.keys()),
        index=list(EXCHANGE_RATES.keys()).index(expense["currency"]),
        key="edit_currency",
    )
    edit_category = st.selectbox(
        "Category",
        CATEGORIES,
        index=CATEGORIES.index(expense["category"]),
        key="edit_category",
    )

    if st.button("Save Changes", key="save_changes"):
        amount = parse_amount(edit_amount_text)
        if amount is None:
            st.error("Please enter a valid amount greater than or equal to 0.")
        else:
            st.session_state.expenses[index] = {
                "description": edit_description,
                "amount": amount,
                "currency": edit_currency,
                "category": edit_category,
            }
            st.session_state.edit_index = None
            st.success("Expense updated")

    if st.button("Cancel", key="cancel_edit"):
        st.session_state.edit_index = None

st.subheader("Your Expenses")

if not st.session_state.expenses:
    st.info("No expenses yet. Add one above.")
else:
    totals_by_currency = {}

    for index, expense in enumerate(st.session_state.expenses):
        totals_by_currency.setdefault(expense["currency"], 0.0)
        totals_by_currency[expense["currency"]] += expense["amount"]

        cols = st.columns([4, 2, 1, 1])
        cols[0].write(f"**{expense['description']}**")
        cols[0].write(f"{expense['category']} ({expense['currency']})")
        cols[1].write(f"{CURRENCY_SYMBOLS[expense['currency']]}{expense['amount']:.2f} {expense['currency']}")

        if cols[2].button("Edit", key=f"edit-{index}"):
            st.session_state.edit_index = index

        if cols[3].button("Delete", key=f"delete-{index}"):
            st.session_state.expenses.pop(index)
            st.success("Expense deleted")

    for currency, total_amount in totals_by_currency.items():
        symbol = CURRENCY_SYMBOLS.get(currency, "")
        st.write(f"**Total ({currency}):** {symbol}{total_amount:.2f} {currency}")

