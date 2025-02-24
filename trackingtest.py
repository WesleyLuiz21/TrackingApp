import csv
import os
from datetime import datetime

# File paths for Tickets
ACTIVE_TICKETS_FILE = 'tickets.csv'
ARCHIVE_TICKETS_FILE = 'archived_tickets.csv'

# File paths for Reminders
ACTIVE_REMINDERS_FILE = 'reminders.csv'
ARCHIVED_REMINDERS_FILE = 'archived_reminders.csv'

def main():
    # Initialize CSV files for tickets and reminders
    initialize_active_csv()
    initialize_archive_csv()
    initialize_reminders_csv()
    initialize_archived_reminders_csv()

    while True:
        print("\nMain Menu:")
        print("1. Add Ticket")
        print("2. Update Ticket Status")
        print("3. View All Tickets")
        print("4. Remove Ticket")
        print("5. Add Reminder")
        print("6. Update Reminder Status")
        print("7. View All Reminders")
        print("8. Remove Reminder")
        print("9. Exit")
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
            add_reminder()
        elif choice == "6":
            update_reminder_status()
        elif choice == "7":
            view_reminders()
        elif choice == "8":
            remove_reminder()
        elif choice == "9":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

# ------------------------------------------------------------------------------
# Tickets Functions
# ------------------------------------------------------------------------------

def initialize_active_csv():
    header = ["Ticket Number", "Ticket Name", "Status", "Log Date"]
    if not os.path.exists(ACTIVE_TICKETS_FILE):
        with open(ACTIVE_TICKETS_FILE, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(header)
    else:
        with open(ACTIVE_TICKETS_FILE, 'r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            file_header = next(reader, None)
        if file_header != header:
            with open(ACTIVE_TICKETS_FILE, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(header)

def initialize_archive_csv():
    header = ["Ticket Number", "Ticket Name", "Status", "Log Date", "Closing Date", "Team"]
    if not os.path.exists(ARCHIVE_TICKETS_FILE):
        with open(ARCHIVE_TICKETS_FILE, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(header)
    else:
        with open(ARCHIVE_TICKETS_FILE, 'r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            file_header = next(reader, None)
        if file_header != header:
            with open(ARCHIVE_TICKETS_FILE, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(header)

def read_active_tickets():
    tickets = []
    if not os.path.exists(ACTIVE_TICKETS_FILE):
        return tickets
    with open(ACTIVE_TICKETS_FILE, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader, None)  # Skip header
        for row in reader:
            if len(row) == 4:
                tickets.append(row)
    return tickets

def write_active_tickets(tickets):
    header = ["Ticket Number", "Ticket Name", "Status", "Log Date"]
    with open(ACTIVE_TICKETS_FILE, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(tickets)

def read_archived_tickets():
    tickets = []
    if not os.path.exists(ARCHIVE_TICKETS_FILE):
        return tickets
    with open(ARCHIVE_TICKETS_FILE, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader, None)  # Skip header
        for row in reader:
            if len(row) == 6:
                tickets.append(row)
    return tickets

def write_archived_tickets(tickets):
    header = ["Ticket Number", "Ticket Name", "Status", "Log Date", "Closing Date", "Team"]
    with open(ARCHIVE_TICKETS_FILE, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(tickets)

def add_ticket():
    ticket_number = input("\nEnter a ticket number: ")
    ticket_name = input("Enter ticket name: ")
    status = select_status()
    log_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    tickets = read_active_tickets()
    tickets.append([ticket_number, ticket_name, status, log_date])
    write_active_tickets(tickets)

def view_tickets():
    tickets = read_active_tickets()
    if not tickets:
        print("\nNo tickets available.")
        return
    print("\nAvailable Tickets:")
    for idx, ticket in enumerate(tickets, start=1):
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
    active_tickets = read_active_tickets()
    active_tickets = [t for t in active_tickets if t[0] != ticket[0]]
    write_active_tickets(active_tickets)
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

# ------------------------------------------------------------------------------
# Reminders Functions
# ------------------------------------------------------------------------------

def initialize_reminders_csv():
    header = ["Reminder Name", "Description", "Status", "Log Date"]
    if not os.path.exists(ACTIVE_REMINDERS_FILE):
        with open(ACTIVE_REMINDERS_FILE, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(header)
    else:
        with open(ACTIVE_REMINDERS_FILE, 'r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            file_header = next(reader, None)
        if file_header != header:
            with open(ACTIVE_REMINDERS_FILE, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(header)

def initialize_archived_reminders_csv():
    header = ["Reminder Name", "Description", "Status", "Log Date", "Closing Date"]
    if not os.path.exists(ARCHIVED_REMINDERS_FILE):
        with open(ARCHIVED_REMINDERS_FILE, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(header)
    else:
        with open(ARCHIVED_REMINDERS_FILE, 'r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            file_header = next(reader, None)
        if file_header != header:
            with open(ARCHIVED_REMINDERS_FILE, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(header)

def read_reminders():
    reminders = []
    if not os.path.exists(ACTIVE_REMINDERS_FILE):
        return reminders
    with open(ACTIVE_REMINDERS_FILE, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader, None)  # Skip header
        for row in reader:
            if len(row) == 4:
                reminders.append(row)
    return reminders

def write_reminders(reminders):
    header = ["Reminder Name", "Description", "Status", "Log Date"]
    with open(ACTIVE_REMINDERS_FILE, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(reminders)

def read_archived_reminders():
    reminders = []
    if not os.path.exists(ARCHIVED_REMINDERS_FILE):
        return reminders
    with open(ARCHIVED_REMINDERS_FILE, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader, None)  # Skip header
        for row in reader:
            if len(row) == 5:
                reminders.append(row)
    return reminders

def write_archived_reminders(reminders):
    header = ["Reminder Name", "Description", "Status", "Log Date", "Closing Date"]
    with open(ARCHIVED_REMINDERS_FILE, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(reminders)

def add_reminder():
    reminder_name = input("\nEnter reminder name: ")
    description = input("Enter reminder description: ")
    status = select_status()
    log_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    reminders = read_reminders()
    reminders.append([reminder_name, description, status, log_date])
    write_reminders(reminders)

def view_reminders():
    reminders = read_reminders()
    if not reminders:
        print("\nNo reminders available.")
        return
    print("\nAvailable Reminders:")
    for idx, reminder in enumerate(reminders, start=1):
        print(f"{idx}. Reminder: {reminder[0]}, Description: {reminder[1]}, Status: {reminder[2]}")

def update_reminder_status():
    reminders = read_reminders()
    if not reminders:
        print("\nNo reminders available to update.")
        return
    print("\nReminders:")
    for idx, reminder in enumerate(reminders, start=1):
        print(f"{idx}. Reminder: {reminder[0]}, Description: {reminder[1]}, Status: {reminder[2]}")
    try:
        choice = int(input("\nSelect a reminder to update (by number): "))
        if choice < 1 or choice > len(reminders):
            print("Invalid selection.")
            return
    except ValueError:
        print("Please enter a valid number.")
        return
    new_status = select_status()
    reminders[choice - 1][2] = new_status
    write_reminders(reminders)
    if new_status == "Done":
        closing_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        reminder_to_archive = reminders[choice - 1]
        move_reminder_to_archive(reminder_to_archive, closing_date)

def move_reminder_to_archive(reminder, closing_date):
    active_reminders = read_reminders()
    active_reminders = [r for r in active_reminders if r[0] != reminder[0]]
    write_reminders(active_reminders)
    archived_reminder = reminder + [closing_date]
    archived_reminders = read_archived_reminders()
    archived_reminders.append(archived_reminder)
    write_archived_reminders(archived_reminders)

def remove_reminder():
    reminder_name = input("\nEnter the reminder name to remove: ")
    reminders = read_reminders()
    filtered_reminders = [r for r in reminders if r[0] != reminder_name]
    if len(filtered_reminders) == len(reminders):
        print("No matching reminder found.")
    else:
        write_reminders(filtered_reminders)
        print(f"Reminder '{reminder_name}' has been removed.")

if __name__ == "__main__":
    main()
