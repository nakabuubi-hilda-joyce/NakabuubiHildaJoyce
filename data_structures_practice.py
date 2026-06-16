"""
Data Structures Practice Assignment
Solutions for Exercise 1-5 (Lists, Tuples, Sets, Strings, Dictionaries)
"""

# ==================== EXERCISE 1: LISTS ====================

print("=" * 60)
print("EXERCISE 1: LISTS")
print("=" * 60)

# 1. Create a list with 5 items (names of people) and output the 2nd item
names = ["Alice", "Bob", "Charlie", "Diana", "Eve"]
print("\n1. List of names:", names)
print("   2nd item:", names[1])

# 2. Change the value of the first item
names[0] = "Alexander"
print("\n2. After changing first item:", names)

# 3. Add a sixth item to the list
names.append("Frank")
print("\n3. After adding sixth item:", names)

# 4. Add "Bathel" as the 3rd item
names.insert(2, "Bathel")
print("\n4. After inserting 'Bathel' at 3rd position:", names)

# 5. Remove the 4th item
names.pop(3)
print("\n5. After removing 4th item:", names)

# 6. Use negative indexing to print the last item
print("\n6. Last item (negative indexing):", names[-1])

# 7. Create a new list and print items at range of indexes
items = ["Apple", "Banana", "Cherry", "Date", "Elderberry", "Fig", "Grape"]
print("\n7. Items list:", items)
print("   Items at index 2, 3, 4:", items[2:5])

# 8. List of countries and make a copy
countries = ["Uganda", "Kenya", "Tanzania", "Rwanda"]
countries_copy = countries.copy()
print("\n8. Original countries:", countries)
print("   Copy of countries:", countries_copy)

# 9. Loop through the list of countries
print("\n9. Looping through countries:")
for country in countries:
    print(f"   - {country}")

# 10. List of animals and sort in ascending and descending order
animals = ["Zebra", "Lion", "Elephant", "Giraffe", "Antelope"]
print("\n10. Original animals:", animals)
animals_asc = sorted(animals)
animals_desc = sorted(animals, reverse=True)
print("    Ascending order:", animals_asc)
print("    Descending order:", animals_desc)

# 11. Output only animal names with the letter 'a' in them
print("\n11. Animals with letter 'a':")
animals_with_a = [animal for animal in animals if 'a' in animal.lower()]
for animal in animals_with_a:
    print(f"    - {animal}")

# 12. Join two lists (first names and second names)
first_names = ["John", "Mary", "Peter"]
second_names = ["Doe", "Smith", "Johnson"]
full_names = first_names + second_names
print("\n12. First names:", first_names)
print("    Second names:", second_names)
print("    Joined lists:", full_names)


# ==================== EXERCISE 2: TUPLES ====================

print("\n" + "=" * 60)
print("EXERCISE 2: TUPLES")
print("=" * 60)

# 1. Output favorite phone brand from tuple
phones = ("samsung", "iphone", "tecno", "redmi")
print("\n1. Phones tuple:", phones)
print("   My favorite:", phones[0])

# 2. Use negative indexing to print 2nd last item
print("\n2. 2nd last item (negative indexing):", phones[-2])

# 3. Update "iphone" to "itel" (create new tuple since tuples are immutable)
phones_list = list(phones)
phones_list[phones_list.index("iphone")] = "itel"
phones = tuple(phones_list)
print("\n3. After updating 'iphone' to 'itel':", phones)

# 4. Add "Huawei" to tuple
phones = phones + ("Huawei",)
print("\n4. After adding 'Huawei':", phones)

# 5. Loop through the tuple
print("\n5. Looping through phones:")
for phone in phones:
    print(f"   - {phone}")

# 6. Remove/delete the first item
phones = phones[1:]
print("\n6. After removing first item:", phones)

# 7. Create a tuple of cities in Uganda using tuple() constructor
cities = tuple(["Kampala", "Gulu", "Mbarara", "Jinja"])
print("\n7. Cities in Uganda:", cities)

# 8. Unpack the tuple
print("\n8. Unpacking cities tuple:")
city1, city2, city3, city4 = cities
print(f"   city1: {city1}, city2: {city2}, city3: {city3}, city4: {city4}")

# 9. Range of indexes to print 2nd, 3rd and 4th cities
print("\n9. 2nd, 3rd and 4th cities:", cities[1:4])

# 10. Join two tuples (first names and second names)
first_names_t = ("John", "Mary", "Peter")
second_names_t = ("Doe", "Smith", "Johnson")
joined_tuples = first_names_t + second_names_t
print("\n10. First names tuple:", first_names_t)
print("    Second names tuple:", second_names_t)
print("    Joined tuples:", joined_tuples)

# 11. Create a tuple of colors and multiply by 3
colors = ("Red", "Blue", "Green")
colors_multiplied = colors * 3
print("\n11. Colors tuple:", colors)
print("    Colors multiplied by 3:", colors_multiplied)

# 12. Count occurrences of 8 in the tuple
thistuple = (1, 3, 7, 8, 7, 5, 4, 6, 8, 5)
count_8 = thistuple.count(8)
print("\n12. Tuple:", thistuple)
print("    Number of times 8 appears:", count_8)


# ==================== EXERCISE 3: SETS ====================

print("\n" + "=" * 60)
print("EXERCISE 3: SETS")
print("=" * 60)

# 1. Create a set of beverages using set() constructor
beverages = {"Coffee", "Tea", "Juice"}
print("\n1. Beverages set:", beverages)

# 2. Add 2 more items to the beverages set
beverages.add("Water")
beverages.add("Soda")
print("\n2. After adding 2 items:", beverages)

# 3. Check if microwave is in the set
mySet = {"oven", "kettle", "microwave", "refrigerator"}
print("\n3. Set:", mySet)
print("    Is 'microwave' in the set?", "microwave" in mySet)

# 4. Remove "kettle" from the set
mySet.remove("kettle")
print("\n4. After removing 'kettle':", mySet)

# 5. Loop through the set
print("\n5. Looping through the set:")
for item in mySet:
    print(f"   - {item}")

# 6. Set of 4 items and list of 2 items, add list elements to set
set_items = {"pen", "pencil", "eraser", "ruler"}
list_items = ["sharpener", "notebook"]
print("\n6. Original set:", set_items)
print("    List items:", list_items)
for item in list_items:
    set_items.add(item)
print("    After adding list items to set:", set_items)

# 7. Join two sets (ages and first names)
ages = {18, 20, 22, 25}
first_names_set = {"John", "Mary", "Peter", "Alice"}
joined_sets = ages.union(first_names_set)
print("\n7. Ages set:", ages)
print("    First names set:", first_names_set)
print("    Joined sets:", joined_sets)


# ==================== EXERCISE 4: STRINGS ====================

print("\n" + "=" * 60)
print("EXERCISE 4: STRINGS")
print("=" * 60)

# 1. Concatenate integer and string
num = 42
text = "is the answer"
result = str(num) + " " + text
print("\n1. Concatenated result:", result)

# 2. Remove spaces at beginning, middle and end
txt = "      Hello,       Uganda!       "
cleaned_txt = txt.strip()
cleaned_txt = " ".join(cleaned_txt.split())
print("\n2. Original string:", repr(txt))
print("    Cleaned string:", repr(cleaned_txt))

# 3. Convert string to uppercase
print("\n3. Uppercase:", cleaned_txt.upper())

# 4. Replace character 'U' with 'V'
replaced_txt = cleaned_txt.replace("U", "V")
print("\n4. After replacing 'U' with 'V':", replaced_txt)

# 5. Return characters at 2nd, 3rd and 4th position
y = "I am proudly Ugandan"
print("\n5. String:", y)
print("    Characters at positions 2, 3, 4:", y[1:4])

# 6. Fix the error in the string with quotes
x = 'All "Data Scientists" are cool!'
print("\n6. Corrected string:", x)


# ==================== EXERCISE 5: DICTIONARIES ====================

print("\n" + "=" * 60)
print("EXERCISE 5: DICTIONARIES")
print("=" * 60)

# 1. Print the shoe size
Shoes = {
    "brand": "Nick",
    "color": "black",
    "size": 40
}
print("\n1. Shoes dictionary:", Shoes)
print("    Shoe size:", Shoes["size"])

# 2. Change "Nick" to "Adidas"
Shoes["brand"] = "Adidas"
print("\n2. After changing brand to 'Adidas':", Shoes)

# 3. Add key/value pair "type": "sneakers"
Shoes["type"] = "sneakers"
print("\n3. After adding 'type':", Shoes)

# 4. Return list of all keys
keys = list(Shoes.keys())
print("\n4. All keys:", keys)

# 5. Return list of all values
values = list(Shoes.values())
print("\n5. All values:", values)

# 6. Check if "size" key exists
print("\n6. Does 'size' key exist?", "size" in Shoes)

# 7. Loop through the dictionary
print("\n7. Looping through dictionary:")
for key, value in Shoes.items():
    print(f"   {key}: {value}")

# 8. Remove "color" from dictionary
Shoes.pop("color")
print("\n8. After removing 'color':", Shoes)

# 9. Empty the dictionary
Shoes_copy = Shoes.copy()
Shoes.clear()
print("\n9. After clearing dictionary:", Shoes)

# 10. Create a dictionary and make a copy
student = {"name": "John", "age": 20, "grade": "A"}
student_copy = student.copy()
print("\n10. Original dictionary:", student)
print("    Copy of dictionary:", student_copy)

# 11. Show nested dictionaries
nested_dict = {
    "person1": {
        "name": "Alice",
        "age": 25,
        "city": "Kampala"
    },
    "person2": {
        "name": "Bob",
        "age": 30,
        "city": "Gulu"
    }
}
print("\n11. Nested dictionaries:", nested_dict)
print("    Accessing person1's name:", nested_dict["person1"]["name"])
print("    Accessing person2's city:", nested_dict["person2"]["city"])

print("\n" + "=" * 60)
print("END OF EXERCISES")
print("=" * 60)
