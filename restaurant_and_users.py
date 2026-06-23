# restaurant_and_users.py
"""
Solutions to Exercises 9-1, 9-2, and 9-3 from Python Crash Course Chapter 9.
"""

# ==============================================================================
# Exercise 9-1: Restaurant
# ==============================================================================
class Restaurant:
    """A simple class representing a restaurant."""

    def __init__(self, restaurant_name, cuisine_type):
        """Initialize restaurant name and cuisine type attributes."""
        self.restaurant_name = restaurant_name
        self.cuisine_type = cuisine_type

    def describe_restaurant(self):
        """Print the restaurant name and cuisine type."""
        print(f"\nRestaurant Name: {self.restaurant_name.title()}")
        print(f"Cuisine Type: {self.cuisine_type.title()}")

    def open_restaurant(self):
        """Print a message indicating the restaurant is open."""
        print(f"{self.restaurant_name.title()} is now open!")


print("--- Exercise 9-1: Restaurant ---")
# Create an instance called restaurant
restaurant = Restaurant("the golden fork", "italian")

# Print the two attributes individually
print(f"Restaurant Name attribute: {restaurant.restaurant_name}")
print(f"Cuisine Type attribute: {restaurant.cuisine_type}")

# Call both methods
restaurant.describe_restaurant()
restaurant.open_restaurant()


# ==============================================================================
# Exercise 9-2: Three Restaurants
# ==============================================================================
print("\n--- Exercise 9-2: Three Restaurants ---")
# Create three different instances
restaurant_1 = Restaurant("sushi house", "japanese")
restaurant_2 = Restaurant("taco loco", "mexican")
restaurant_3 = Restaurant("burger palace", "american fast food")

# Call describe_restaurant() for each instance
restaurant_1.describe_restaurant()
restaurant_2.describe_restaurant()
restaurant_3.describe_restaurant()


# ==============================================================================
# Exercise 9-3: Users
# ==============================================================================
class User:
    """A simple class representing a user profile."""

    def __init__(self, first_name, last_name, username, email, location):
        """Initialize the user attributes."""
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email = email
        self.location = location

    def describe_user(self):
        """Print a summary of the user's information."""
        print(f"\nUser Profile Summary for: {self.username}")
        print(f"  Full Name: {self.first_name.title()} {self.last_name.title()}")
        print(f"  Email: {self.email}")
        print(f"  Location: {self.location.title()}")

    def greet_user(self):
        """Print a personalized greeting to the user."""
        print(f"Welcome back, {self.first_name.title()}! Hope you're having a great day.")


print("\n--- Exercise 9-3: Users ---")
# Create several instances representing different users
user_1 = pride = User("pride", "ndlovu", "pridendlovu", "pride@example.com", "johannesburg")
user_2 = sarah = User("sarah", "connor", "sconnor", "sconnor@example.com", "los angeles")
user_3 = kenji = User("kenji", "sato", "ksato", "ksato@example.co.jp", "tokyo")

# Call both methods for each user
user_1.describe_user()
user_1.greet_user()

user_2.describe_user()
user_2.greet_user()

user_3.describe_user()
user_3.greet_user()
