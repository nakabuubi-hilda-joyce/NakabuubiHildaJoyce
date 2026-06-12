# E-commerce assignment: checkout, coupons, tax, and login access levels

users = {
    "admin": {"password": "admin123", "role": "Admin"},
    "customer": {"password": "cust123", "role": "Customer"},
    "cashier": {"password": "cash123", "role": "Cashier"}
}

coupon_codes = {
    "SAVE10": 0.1,
    "SAVE20": 2,
    "FREESHIP": 0,
    "WELCOME": 1.5
}

tax_rates = {
    "KLA": 0.08,
    "MSK": 0.088,
    "NT": 0.062,
    "GZ": 0.06,
    "OTHER": 0.05
}


def get_tax_rate(state_code: str) -> float:
    state = state_code.strip().upper()
    return tax_rates.get(state, tax_rates["OTHER"])


def get_discount_rate(subtotal: float) -> float:
    if subtotal <= 0:
        return 0
    if subtotal < 100:
        return 0
    elif subtotal < 200:
        return 0.5
    elif subtotal < 500:
        return 0.1
    else:
        return 0.15


def apply_coupon(subtotal: float, coupon: str) -> float:
    coupon = coupon.strip().upper()
    if not coupon:
        return 0
    if coupon in coupon_codes:
        discount = coupon_codes[coupon]
        if coupon == "FREESHIP":
            print("Free shipping coupon applied. No extra price discount.")
            return 0
        return subtotal * discount
    else:
        print("Invalid coupon code entered.")
        return 0


def calculate_final_price(subtotal: float, coupon: str, state_code: str) -> dict:
    nested_discount_rate = get_discount_rate(subtotal)
    nested_discount_amount = subtotal * nested_discount_rate
    coupon_discount_amount = apply_coupon(subtotal - nested_discount_amount, coupon)
    discounted_subtotal = subtotal - nested_discount_amount - coupon_discount_amount
    tax_rate = get_tax_rate(state_code)
    tax_amount = max(discounted_subtotal, 0) * tax_rate
    total = max(discounted_subtotal, 0) + tax_amount
    return {
        "subtotal": subtotal,
        "base_discount_rate": nested_discount_rate,
        "base_discount_amount": nested_discount_amount,
        "coupon_discount_amount": coupon_discount_amount,
        "discounted_subtotal": discounted_subtotal,
        "tax_rate": tax_rate,
        "tax_amount": tax_amount,
        "total_price": total
    }


def print_order_summary(summary: dict) -> None:
    print("\n--- Order Summary ---")
    print(f"Subtotal: UGX{summary['subtotal']:.2f}")
    print(f"Base discount: {summary['base_discount_rate']*100:.0f}% -> -UGX{summary['base_discount_amount']:.2f}")
    print(f"Coupon discount: -UGX{summary['coupon_discount_amount']:.2f}")
    print(f"Tax rate: {summary['tax_rate']*100:.2f}%")
    print(f"Tax amount: +UGX{summary['tax_amount']:.2f}")
    print(f"Final total: UGX{summary['total_price']:.2f}")
    print("----------------------\n")


def handle_checkout(role: str) -> None:
    print(f"\nWelcome to checkout, {role}.")
    try:
        subtotal = float(input("Enter the product subtotal amount: UGX"))
    except ValueError:
        print("Please enter a valid numeric subtotal.")
        return

    if subtotal < 0:
        print("Subtotal cannot be negative.")
        return

    coupon = input("Enter coupon code (or press Enter to skip): ")
    state_code = input("Enter your state code for tax calculation (e.g. KLA, MSK, NT): ")
    if not state_code:
        state_code = "OTHER"

    summary = calculate_final_price(subtotal, coupon, state_code)
    print_order_summary(summary)


def admin_menu() -> None:
    print("\nAdmin menu: choose an action")
    print("1. Process a new order")
    print("2. Show available coupon codes")
    print("3. Exit")
    choice = input("Select an option: ")
    if choice == "1":
        handle_checkout("Admin")
    elif choice == "2":
        print("Available coupon codes:")
        for code, rate in coupon_codes.items():
            if code == "FREESHIP":
                print(f"- {code} (free shipping)")
            else:
                print(f"- {code} ({int(rate*100)}% off)")
    else:
        print("Exiting admin menu.")


def cashier_menu() -> None:
    print("\nCashier menu: choose an action")
    print("1. Process a customer checkout")
    print("2. Exit")
    choice = input("Select an option: ")
    if choice == "1":
        handle_checkout("Cashier")
    else:
        print("Exiting cashier menu.")


def customer_menu() -> None:
    print("\nCustomer checkout")
    handle_checkout("Customer")


def run_application() -> None:
    print("Welcome to the E-commerce assignment program.")
    username = input("Username: ")
    password = input("Password: ")

    if username not in users:
        print("Login failed: user not found.")
        return

    account = users[username]
    if password != account["password"]:
        print("Login failed: incorrect password.")
        return

    role = account["role"]
    print(f"Login successful. Role: {role}")

    if role == "Admin":
        admin_menu()
    elif role == "Cashier":
        cashier_menu()
    elif role == "Customer":
        customer_menu()
    else:
        print("Unknown role. Cannot continue.")


if __name__ == "__main__":
    run_application()
