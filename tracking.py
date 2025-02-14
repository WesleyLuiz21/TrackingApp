import csv
import os

# File path
filename = 'tickets.csv'

# Function to load or create a new CSV file
def load_or_create_csv():
    if not os.path.exists(filename):
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Ticket Number", "Status"])  # header row

# Function to add a new ticket
def add_ticket():
    ticket_number = input("\nEnter a ticket number if available:\n ")
    status = select_status()
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([ticket_number, status])

# Function to select status
def select_status():
    statuses = ["OnHold", "In Progress", "Urgent", "Medium", "Low Urgency", "Done"]
    for i, status in enumerate(statuses, 1):
        print(f"{i}. {status}")
    choice = int(input("Select status: "))
    return statuses[choice - 1]

# Function to update a ticket
def update_ticket():
    temp_filename = 'temp_' + filename
    found = False
    ticket_number = input("\nEnter the ticket number to update:\n ")
    with open(filename, mode='r', newline='') as infile, open(temp_filename, mode='w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        for row in reader:
            if row[0] == ticket_number:
                print(f"Current Status: {row[1]}")
                row[1] = select_status()
                found = True
            writer.writerow(row)
    os.replace(temp_filename, filename)
    if not found:
        print("\nTicket number not found.\n")

# Function to view all tickets
def view_tickets():
    with open(filename, mode='r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            print("\n")
            print(f"Ticket Number: {row[0]}, Status: {row[1]}")

# Function to remove a ticket
def remove_ticket():
    temp_filename = 'temp_' + filename
    found = False
    ticket_number = input("\nEnter the ticket number to remove:\n ")
    with open(filename, mode='r', newline='') as infile, open(temp_filename, mode='w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        for row in reader:
            if row[0] == ticket_number:
                found = True
                continue  # skip this row
            writer.writerow(row)
    os.replace(temp_filename, filename)
    if not found:
        print("\nTicket number not found.")

# Main function
def main():
    load_or_create_csv()
    while True:
        print("\nMain Menu:\n")
        print("1. Add Ticket")
        print("2. Update Ticket Status")
        print("3. View All Available Tickets")
        print("4. Remove Ticket")
        print("5. Exit")
        choice = input("\nEnter your choice: \n")
        if choice == "1":
            add_ticket()
        elif choice == "2":
            update_ticket()
        elif choice == "3":
            view_tickets()
        elif choice == "4":
            remove_ticket()
        elif choice == "5":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.\n")

if __name__ == "__main__":
    main()
