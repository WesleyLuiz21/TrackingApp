import threading
import time
from datetime import datetime

def schedule_reminder(reminder_date_str, reminder_message):
    """
    Schedules a reminder for 10:00 AM on the provided date.
    
    Parameters:
      reminder_date_str (str): Date in "YYYY-MM-DD" format.
      reminder_message (str): The message to display when the reminder is triggered.
    """
    try:
        # Convert the input date string to a date object and then build the scheduled datetime at 10:00 AM.
        reminder_date = datetime.strptime(reminder_date_str, "%Y-%m-%d").date()
        scheduled_time = datetime.combine(reminder_date, datetime.min.time()).replace(hour=10)
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.")
        return

    now = datetime.now()
    delay = (scheduled_time - now).total_seconds()

    if delay <= 0:
        print("The scheduled time is already past!")
        return

    def reminder_job():
        print(f"Reminder: {reminder_message}")

    def thread_function():
        time.sleep(delay)
        reminder_job()

    # Launch the reminder in a separate thread.
    threading.Thread(target=thread_function, daemon=True).start()
    print(f"Reminder scheduled for {scheduled_time}.")

# For testing the module independently.
if __name__ == "__main__":
    schedule_reminder("2025-02-21", "This is your reminder!")
