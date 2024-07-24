import sqlite3

def create_database():
    conn = sqlite3.connect('employee_database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            age INTEGER,
            gender TEXT
        )
    ''')
    conn.commit()
    conn.close()


class Employee:
    name: str
    email: str
    age: str
    gender: str
    
    def __init__(self, name, email, age, gender):
        self.name = name
        self.email = email
        self.age = age
        self.gender = gender

def onboarding():
    print("Employee Onboarding")
    name = input("Enter employee name: ")
    email = input("Enter personal email: ")
    age = int(input("Enter age: "))
    gender = input("Enter gender: ")
    
    employee = Employee(name, email, age, gender)

    conn = sqlite3.connect('employee_database.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO employees (name, email, age, gender)
        VALUES (?, ?, ?, ?)
    ''', (name, email, age, gender))
    conn.commit()
    conn.close()

    print("Employee details saved successfully.")
    
    # send the welcome email by calling the tool url to user
    # send the email to the department manager by again tool url
    # annonce the new joinee on social media by tool url
    
    

def main():
    create_database()

    while True:
        print("\nChoose an option:")
        print("1. Onboarding")
        print("2. Employee Support")
        print("3. Exit")

        choice = input("Enter your choice (1/2/3): ")

        if choice == '1':
            onboarding()
        elif choice == '2':
            print("Employee Support is not implemented yet.")
        elif choice == '3':
            print("Exiting the application.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()