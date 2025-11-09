import os

USER_FILE = "vault_user.txt"
DATA_FILE = "vault_data.txt"
SECRET_SHIFT = 4  # tiny beginner-friendly "encryption" shift for characters

def encrypt(text):
    # Caesar-style shift over basic ASCII range
    return "".join(chr((ord(c) + SECRET_SHIFT) % 127) for c in text)

def decrypt(text):
    return "".join(chr((ord(c) - SECRET_SHIFT) % 127) for c in text)

def register():
    print("\n--- Register ---")
    username = input("Create username: ")
    password = input("Create master password: ")
    with open(USER_FILE, "w") as f:
        f.write(username + "\n")
        f.write(password)
    # create empty data file if not exists
    if not os.path.exists(DATA_FILE):
        open(DATA_FILE, "a").close()
    print("✅ Registration complete!")

def login():
    print("\n--- Login ---")
    username = input("Username: ")
    password = input("Master Password: ")

    if not os.path.exists(USER_FILE):
        print("❌ No user found. Please register first.")
        return False

    with open(USER_FILE, "r") as f:
        saved_user = f.readline().strip()
        saved_pass = f.readline().strip()

    if username == saved_user and password == saved_pass:
        print("✅ Login successful!")
        post_login_menu(username)
        return True
    else:
        print("❌ Incorrect credentials.")
        return False

def add_password():
    print("\n--- Add a Password ---")
    site = input("Site / App name: ").strip()
    user = input("Login/Email for this site: ").strip()
    pw   = input("Password for this site: ").strip()

    record = f"{site}||{user}||{pw}"
    safe = encrypt(record)
    with open(DATA_FILE, "a") as f:
        f.write(safe + "\n")
    print("🔐 Saved (encrypted).")

def view_passwords():
    print("\n--- Your Saved Passwords ---")
    if not os.path.exists(DATA_FILE):
        print("No saved passwords yet.")
        return
    any_rows = False
    with open(DATA_FILE, "r") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line:
                continue
            any_rows = True
            raw = decrypt(line)
            site, user, pw = raw.split("||")
            print(f"- Site: {site} | User: {user} | Password: {pw}")
    if not any_rows:
        print("No saved passwords yet.")

def post_login_menu(username):
    while True:
        print(f"\n--- Vault ({username}) ---")
        print("1. Add password")
        print("2. View passwords")
        print("3. Logout")
        choice = input("Choose option: ")
        if choice == "1":
            add_password()
        elif choice == "2":
            view_passwords()
        elif choice == "3":
            print("🔓 Logged out.")
            break
        else:
            print("Invalid choice.")

def main_menu():
    while True:
        print("\n--- Password Vault Menu ---")
        print("1. Register")
        print("2. Login")
        print("3. Quit")
        choice = input("Choose option: ")
        if choice == "1":
            register()
        elif choice == "2":
            login()
        elif choice == "3":
            print("👋 Goodbye!")
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main_menu()
