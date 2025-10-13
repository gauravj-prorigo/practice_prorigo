import json
import os

FILE_NAME = "phonebook.json"
phDictionary = {}

# ---------- Load and Save ----------
def load_phonebook():
    """Load phonebook data from JSON file."""
    global phDictionary
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r") as file:
                phDictionary = json.load(file)
        except json.JSONDecodeError:
            phDictionary = {}
    else:
        phDictionary = {}

def save_phonebook():
    """Save current phonebook data to JSON file."""
    with open(FILE_NAME, "w") as file:
        json.dump(phDictionary, file, indent=4)


# ---------- Validation Functions ----------
def validate_email(email):
    """Check if the email format is valid."""
    if "@" in email and "." in email and email.index("@") < email.rindex(".") and email.endswith(".com"):
        return True
    return False

def validate_phone(phone):
    """Check if the phone number contains only digits and is up to 10 digits."""
    if phone.isdigit() and len(phone) <= 10:
        return True
    return False


# ---------- CRUD Operations ----------
def add_contact():
    """Add a new contact."""
    name = input("Enter Name: ")

    while True:
        email = input("Enter Email: ")
        if validate_email(email):
            break
        print("Invalid email format! Try again.")

    while True:
        phone = input("Enter Phone: ")
        if validate_phone(phone):
            break
        print("Invalid phone number! Must be digits and up to 10 numbers.")

    phDictionary[name] = {"Name": name, "Email": email, "Phone": phone}
    save_phonebook()
    print(f"✅ Contact '{name}' added successfully!")


def show_contacts():
    """Display all contacts."""
    if not phDictionary:
        print("📭 Phonebook is empty!")
        return
    print("\n---- Your Phonebook ----")
    for contact in phDictionary.values():
        print(f"Name: {contact['Name']}, Email: {contact['Email']}, Phone: {contact['Phone']}")


def search_contact():
    """Search a contact by name."""
    name = input("Enter name to search: ")
    if name in phDictionary:
        c = phDictionary[name]
        print(f"Found: Name: {c['Name']}, Email: {c['Email']}, Phone: {c['Phone']}")
    else:
        print("❌ Contact not found!")


def update_contact():
    """Update an existing contact."""
    name = input("Enter name to update: ")
    if name in phDictionary:
        print("Leave field blank to keep old value.")
        new_email = input(f"New Email (old: {phDictionary[name]['Email']}): ") or phDictionary[name]['Email']
        new_phone = input(f"New Phone (old: {phDictionary[name]['Phone']}): ") or phDictionary[name]['Phone']

        if validate_email(new_email) and validate_phone(new_phone):
            phDictionary[name]["Email"] = new_email
            phDictionary[name]["Phone"] = new_phone
            save_phonebook()
            print(f"✅ Contact '{name}' updated successfully!")
        else:
            print("❌ Invalid email or phone. Update failed.")
    else:
        print("❌ Contact not found!")


def delete_contact():
    """Delete a contact by name."""
    name = input("Enter name to delete: ")
    if name in phDictionary:
        confirm = input(f"Are you sure you want to delete '{name}'? (y/n): ").lower()
        if confirm == "y":
            del phDictionary[name]
            save_phonebook()
            print(f"🗑️ Contact '{name}' deleted successfully!")
    else:
        print("❌ Contact not found!")


# ---------- Menu Loop ----------
def main():
    load_phonebook()
    while True:
        print("\n========== PHONEBOOK MENU ==========")
        print("1. Add Contact")
        print("2. Show All Contacts")
        print("3. Search Contact")
        print("4. Update Contact")
        print("5. Delete Contact")
        print("6. Exit")
        choice = input("Enter your choice (1-6): ")

        if choice == "1":
            add_contact()
        elif choice == "2":
            show_contacts()
        elif choice == "3":
            search_contact()
        elif choice == "4":
            update_contact()
        elif choice == "5":
            delete_contact()
        elif choice == "6":
            print("👋 Exiting... Goodbye!")
            break
        else:
            print("❌ Invalid choice! Please select between 1–6.")


# ---------- Run Program ----------
if __name__ == "__main__":
    main()
