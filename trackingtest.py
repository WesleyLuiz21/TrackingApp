import csv
import os

# File paths
ACTIVE_FILE = 'tickets.csv'
ARCHIVE_FILE = 'archive_tickets.csv'

def main():
    """Main menu loop."""
    # Ensure files exist and have correct headers
    initialize_csv(ACTIVE_FILE)
    initialize_csv(ARCHIVE_FILE)

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

def initialize_csv(filepath: str):
    """
    Create the CSV file with a header if it doesn't exist or if the header is incorrect.
    """
    if not os.path.exists(filepath):
        with open(filepath, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Ticket Number", "Ticket Name", "Status"])
    else:
        # Check if file has correct header; if not, rewrite it
        with open(filepath, 'r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            header = next(reader, None)
            # If header is missing or malformed, rewrite the file
            if not header or len(header) < 3:
                with open(filepath, 'w', newline='', encoding='utf-8') as fw:
                    writer = csv.writer(fw)
                    writer.writerow(["Ticket Number", "Ticket Name", "Status"])

def read_tickets_from_csv(filepath: str):
    """
    Read tickets from the CSV, skipping the header and ignoring any malformed rows.
    Returns a list of valid [ticket_number, ticket_name, status] rows.
    """
    tickets = []
    if not os.path.exists(filepath):
        return tickets  # File doesn't exist, return empty list

    with open(filepath, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        header = next(reader, None)  # skip the header row
        # Read valid rows (exactly 3 columns)
        for row in reader:
            if len(row) == 3:
                tickets.append(row)
    return tickets

def write_tickets_to_csv(filepath: str, tickets: list):
    """
    Write the list of tickets to the CSV file, overwriting existing data,
    and re-adding the header row.
    """
    with open(filepath, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Ticket Number", "Ticket Name", "Status"])
        writer.writerows(tickets)

# ------------------------------------------------------------------------------
# Core Features
# ------------------------------------------------------------------------------

def add_ticket():
    """Prompt user for new ticket info and add it to the active tickets file."""
    ticket_number = input("\nEnter a ticket number: ")
    ticket_name = input("Enter ticket name: ")
    status = select_status()

    # Read existing tickets
    tickets = read_tickets_from_csv(ACTIVE_FILE)
    # Append the new ticket
    tickets.append([ticket_number, ticket_name, status])
    # Write back to CSV
    write_tickets_to_csv(ACTIVE_FILE, tickets)

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
    """View all tickets currently in the active tickets file."""
    tickets = read_tickets_from_csv(ACTIVE_FILE)
    if not tickets:
        print("\nNo tickets available.")
        return

    print("\nAvailable Tickets:")
    for idx, ticket in enumerate(tickets, start=1):
        print(f"{idx}. Ticket Number: {ticket[0]}, Ticket Name: {ticket[1]}, Status: {ticket[2]}")

def update_ticket_status():
    """
    List all tickets, let user pick one by its displayed index, and update its status.
    If the new status is 'Done', move the ticket to the archive.
    """
    tickets = read_tickets_from_csv(ACTIVE_FILE)
    if not tickets:
        print("\nNo tickets available to update.")
        return

    # Display the tickets
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
    tickets[choice - 1][2] = new_status
    write_tickets_to_csv(ACTIVE_FILE, tickets)

    # If the status is Done, move to archive
    if new_status == "Done":
        move_ticket_to_archive(tickets[choice - 1])

def remove_ticket():
    """
    Remove a ticket by its ticket number from the active tickets.
    """
    ticket_number = input("\nEnter the ticket number to remove: ")

    tickets = read_tickets_from_csv(ACTIVE_FILE)
    # Filter out the ticket with the matching ticket number
    filtered_tickets = [t for t in tickets if t[0] != ticket_number]

    if len(filtered_tickets) == len(tickets):
        print("No matching ticket found.")
    else:
        write_tickets_to_csv(ACTIVE_FILE, filtered_tickets)
        print(f"Ticket '{ticket_number}' has been removed.")

def move_ticket_to_archive(ticket: list):
    """
    Append the given ticket to the archive file and remove it from the active tickets.
    """
    # Read archive tickets, append the new one, write back
    archive_tickets = read_tickets_from_csv(ARCHIVE_FILE)
    archive_tickets.append(ticket)
    write_tickets_to_csv(ARCHIVE_FILE, archive_tickets)

    # Remove from active tickets
    active_tickets = read_tickets_from_csv(ACTIVE_FILE)
    active_tickets = [t for t in active_tickets if t != ticket]
    write_tickets_to_csv(ACTIVE_FILE, active_tickets)

# ------------------------------------------------------------------------------
# Entry Point
# ------------------------------------------------------------------------------

if __name__ == "__main__":
    main()
