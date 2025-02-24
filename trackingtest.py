import csv
import os
from datetime import datetime

ACTIVE_FILE = 'tickets.csv'
ARCHIVE_FILE = 'archive_tickets.csv'

def main():
    initialize_active_csv()
    initialize_archive_csv()
    while True:
        print("\nMain Menu:")
        print("1. Add Ticket")
        print("2. Update Ticket Status")
        print("3. View All Available Tickets")
        print("4. Remove Ticket")
        print("5. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            add_ticket()
        elif choice == "2":
            update_ticket_status()
        elif choice == "3":
            view_tickets()
        elif choice == "4":
            remove_ticket()
        elif choice == "5":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

# ------------------------------------------------------------------------------
# CSV Initialization
# ------------------------------------------------------------------------------

def initialize_active_csv():
    header = ["Ticket Number", "Ticket Name", "Status", "Log Date"]
    if not os.path.exists(ACTIVE_FILE):
        with open(ACTIVE_FILE, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(header)
    else:
        with open(ACTIVE_FILE, 'r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            file_header = next(reader, None)
        if file_header != header:
            with open(ACTIVE_FILE, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(header)

def initialize_archive_csv():
    header = ["Ticket Number", "Ticket Name", "Status", "Log Date", "Closing Date", "Team"]
    if not os.path.exists(ARCHIVE_FILE):
        with open(ARCHIVE_FILE, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(header)
    else:
        with open(ARCHIVE_FILE, 'r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            file_header = next(reader, None)
        if file_header != header:
            with open(ARCHIVE_FILE, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(header)

# ------------------------------------------------------------------------------
# CSV Read/Write Helpers
# ------------------------------------------------------------------------------

def read_active_tickets():
    tickets = []
    if not os.path.exists(ACTIVE_FILE):
        return tickets
    with open(ACTIVE_FILE, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader, None)  # skip header
        for row in reader:
            if len(row) == 4:
                tickets.append(row)
    return tickets

def write_active_tickets(tickets):
    header = ["Ticket Number", "Ticket Name", "Status", "Log Date"]
    with open(ACTIVE_FILE, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(tickets)

def read_archived_tickets():
    tickets = []
    if not os.path.exists(ARCHIVE_FILE):
        return tickets
    with open(ARCHIVE_FILE, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader, None)  # skip header
        for row in reader:
            if len(row) == 6:
                tickets.append(row)
    return tickets

def write_archived_tickets(tickets):
    header = ["Ticket Number", "Ticket Name", "Status", "Log Date", "Closing Date", "Team"]
    with open(ARCHIVE_FILE, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(tickets)

# ------------------------------------------------------------------------------
# Core Functions
# ------------------------------------------------------------------------------

def add_ticket():
    ticket_number = input("\nEnter a ticket number: ")
    ticket_name = input("Enter ticket name: ")
    status = select_status()
    log_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    tickets = read_active_tickets()
    tickets.append([ticket_number, ticket_name, status, log_date])
    write_active_tickets(tickets)

def select_status():
    statuses = ["OnHold", "In Progress", "Urgent", "Medium", "Low Urgency", "Done"]
    print("\nSelect a status:")
    for i, s in enumerate(statuses, start=1):
        print(f"{i}. {s}")
    while True:
        try:
            choice = int(input("Your choice: "))
            if 1 <= choice <= len(statuses):
                return statuses[choice - 1]
            else:
                print(f"Please select a valid option between 1 and {len(statuses)}.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def view_tickets():
    tickets = read_active_tickets()
    if not tickets:
        print("\nNo tickets available.")
        return
    print("\nAvailable Tickets:")
    for idx, ticket in enumerate(tickets, start=1):
        # Display only ticket number, name, and status
        print(f"{idx}. Ticket Number: {ticket[0]}, Ticket Name: {ticket[1]}, Status: {ticket[2]}")

def update_ticket_status():
    tickets = read_active_tickets()
    if not tickets:
        print("\nNo tickets available to update.")
        return

    print("\nTickets:")
    for idx, ticket in enumerate(tickets, start=1):
        print(f"{idx}. Ticket Number: {ticket[0]}, Ticket Name: {ticket[1]}, Status: {ticket[2]}")

    try:
        choice = int(input("\nSelect a ticket to update (by number): "))
        if choice < 1 or choice > len(tickets):
            print("Invalid selection.")
            return
    except ValueError:
        print("Please enter a valid number.")
        return

    new_status = select_status()
    tickets[choice - 1][2] = new_status
    write_active_tickets(tickets)

    if new_status == "Done":
        # Ask the user to select the team using numeric choices
        while True:
            print("\nIs this ticket EUS or Asset?")
            print("1. Asset")
            print("2. EUS")
            team_choice = input("Enter your response: ").strip()
            if team_choice == "1":
                team = "Asset"
                break
            elif team_choice == "2":
                team = "EUS"
                break
            else:
                print("Invalid selection. Please enter 1 for Asset or 2 for EUS.")

        closing_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ticket_to_archive = tickets[choice - 1]
        move_ticket_to_archive(ticket_to_archive, closing_date, team)

def move_ticket_to_archive(ticket, closing_date, team):
    # Remove the ticket from active tickets
    active_tickets = read_active_tickets()
    active_tickets = [t for t in active_tickets if t[0] != ticket[0]]
    write_active_tickets(active_tickets)
    # Build the archived ticket: add closing date and team info.
    archived_ticket = ticket + [closing_date, team]
    archived_tickets = read_archived_tickets()
    archived_tickets.append(archived_ticket)
    write_archived_tickets(archived_tickets)

def remove_ticket():
    ticket_number = input("\nEnter the ticket number to remove: ")
    tickets = read_active_tickets()
    filtered_tickets = [ticket for ticket in tickets if ticket[0] != ticket_number]
    if len(filtered_tickets) == len(tickets):
        print("No matching ticket found.")
    else:
        write_active_tickets(filtered_tickets)
        print(f"Ticket '{ticket_number}' has been removed.")

# ------------------------------------------------------------------------------
# Entry Point
# ------------------------------------------------------------------------------

if __name__ == "__main__":
    main()
