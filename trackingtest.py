import csv
import os
from datetime import datetime

# CSV file paths
ACTIVE_FILE = 'tickets.csv'
ARCHIVE_FILE = 'archive_tickets.csv'

# CSV headers
ACTIVE_HEADER = ["Ticket Number", "Ticket Name", "Status", "Log Date"]
ARCHIVE_HEADER = ["Ticket Number", "Ticket Name", "Status", "Log Date", "Done Date"]

def main():
    """Main program loop."""
    # Ensure CSV files exist with proper headers
    initialize_csv(ACTIVE_FILE, ACTIVE_HEADER)
    initialize_csv(ARCHIVE_FILE, ARCHIVE_HEADER)

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
# Initialization and CSV Helper Functions
# ------------------------------------------------------------------------------

def initialize_csv(filepath: str, header: list):
    """
    Create or fix the CSV file so that it has the specified header.
    """
    if not os.path.exists(filepath):
        # Create a new file with the header
        with open(filepath, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(header)
    else:
        # Verify the file has the correct header; if not, overwrite it
        with open(filepath, 'r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            existing_header = next(reader, None)
            if existing_header != header:
                with open(filepath, 'w', newline='', encoding='utf-8') as fw:
                    writer = csv.writer(fw)
                    writer.writerow(header)

def read_tickets_from_csv(filepath: str, expected_columns: int):
    """
    Read tickets from the CSV, skipping the header and ignoring any malformed rows.
    Returns a list of valid rows, each row being a list of strings.
    """
    tickets = []
    if not os.path.exists(filepath):
        return tickets

    with open(filepath, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        _ = next(reader, None)  # Skip the header
        for row in reader:
            if len(row) == expected_columns:
                tickets.append(row)
    return tickets

def write_tickets_to_csv(filepath: str, header: list, tickets: list):
    """
    Overwrite the CSV with the given header and list of tickets.
    """
    with open(filepath, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(tickets)

def current_date():
    """Return the current date/time as a string."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# ------------------------------------------------------------------------------
# Core Features
# ------------------------------------------------------------------------------

def add_ticket():
    """Prompt user for new ticket info and add it to the active tickets file."""
    ticket_number = input("\nEnter a ticket number: ")
    ticket_name = input("Enter ticket name: ")
    status = select_status()

    # Prepare the new ticket with the current date (log date)
    log_date = current_date()
    new_ticket = [ticket_number, ticket_name, status, log_date]

    # Read existing tickets
    tickets = read_tickets_from_csv(ACTIVE_FILE, 4)
    tickets.append(new_ticket)

    # Write back to CSV
    write_tickets_to_csv(ACTIVE_FILE, ACTIVE_HEADER, tickets)

def select_status():
    """Prompt user to select a status from a predefined list."""
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
    """View all tickets currently in the active tickets file (excluding log date)."""
    tickets = read_tickets_from_csv(ACTIVE_FILE, 4)
    if not tickets:
        print("\nNo tickets available.")
        return

    print("\nAvailable Tickets:")
    for idx, ticket in enumerate(tickets, start=1):
        # ticket = [ticket_number, ticket_name, status, log_date]
        print(f"{idx}. Ticket Number: {ticket[0]}, Ticket Name: {ticket[1]}, Status: {ticket[2]}")

def update_ticket_status():
    """
    List all tickets, let user pick one by its displayed index, and update its status.
    If the new status is 'Done', move the ticket to the archive (with Done Date).
    """
    tickets = read_tickets_from_csv(ACTIVE_FILE, 4)
    if not tickets:
        print("\nNo tickets available to update.")
        return

    print("\nTickets:")
    for idx, ticket in enumerate(tickets, start=1):
        print(f"{idx}. Ticket Number: {ticket[0]}, Ticket Name: {ticket[1]}, Status: {ticket[2]}")

    # Get user selection
    try:
        choice = int(input("\nSelect a ticket to update (by number): "))
        if choice < 1 or choice > len(tickets):
            print("Invalid selection.")
            return
    except ValueError:
        print("Please enter a valid number.")
        return

    # Update the status
    new_status = select_status()
    tickets[choice - 1][2] = new_status  # index 2 = Status

    # Write back to the active tickets file
    write_tickets_to_csv(ACTIVE_FILE, ACTIVE_HEADER, tickets)

    # If the status is Done, move to archive
    if new_status == "Done":
        move_ticket_to_archive(tickets[choice - 1])

def remove_ticket():
    """Remove a ticket by its ticket number from the active tickets."""
    ticket_number = input("\nEnter the ticket number to remove: ")
    tickets = read_tickets_from_csv(ACTIVE_FILE, 4)

    # Filter out the ticket with the matching ticket number
    filtered_tickets = [t for t in tickets if t[0] != ticket_number]

    if len(filtered_tickets) == len(tickets):
        print("No matching ticket found.")
    else:
        write_tickets_to_csv(ACTIVE_FILE, ACTIVE_HEADER, filtered_tickets)
        print(f"Ticket '{ticket_number}' has been removed.")

def move_ticket_to_archive(ticket: list):
    """
    Append the given ticket to the archive file with an extra 'Done Date',
    and remove it from the active tickets.
    """
    # ticket = [ticket_number, ticket_name, status, log_date]
    done_date = current_date()
    archived_ticket = ticket + [done_date]  # now [num, name, status, log_date, done_date]

    # Append to archive
    archive_tickets = read_tickets_from_csv(ARCHIVE_FILE, 5)
    archive_tickets.append(archived_ticket)
    write_tickets_to_csv(ARCHIVE_FILE, ARCHIVE_HEADER, archive_tickets)

    # Remove from active
    active_tickets = read_tickets_from_csv(ACTIVE_FILE, 4)
    # Compare the first 4 columns, since the archived ticket has 5
    active_tickets = [t for t in active_tickets if t != ticket]
    write_tickets_to_csv(ACTIVE_FILE, ACTIVE_HEADER, active_tickets)

# ------------------------------------------------------------------------------
# Entry Point
# ------------------------------------------------------------------------------

if __name__ == "__main__":
    main()
