"""Exercise 7.0 — Collecting data and saving it

WHAT THE PROGRAM MUST DO
    Ask the user for the information needed to record one entry, then save it to a CSV
    file. Running the program twice must produce two entries, not overwrite the first.

ANSWER THESE FIRST, in comments at the top of your file
    1. What goes in?
    2. What happens to it?
    3. What comes out?  (name your file, and list your columns)
    4. Which columns did you choose, and what would you actually do with this file once
       it has two hundred rows in it?

WHAT THE AI CANNOT KNOW
    Your columns. They must be the ones you would really need to collect for a purpose
    you can state. See 7.0_student_data.csv for the shape of a header line, not for
    the columns to use.

    Two behaviours are yours to decide, and an assistant will guess them wrong:
    what happens the very first time, when the file does not exist yet and needs its
    header line, and what happens when a value the user typed is not acceptable.

CHECK IT YOURSELF
    Run your program three times with different values. Then open the file and count
    the lines. You should have three entries and exactly one header line. If you have
    three header lines, or one entry, your program is wrong.

DELIVERABLE
    This file, plus the CSV your program produced.
"""

# 1. In: one internship application, typed by me: company, role, city, sector, and how
#    I applied (website, LinkedIn, email, referral). The date is added automatically.
# 2. Process: each answer is checked. Empty answers are refused and the question is asked
#    again. Sector and channel must be one of a fixed list, so the same thing is always
#    spelled the same way (otherwise "linkedin", "LinkedIn" and "Linkedin" count as three).
#    Then the entry is added to the END of the file (append mode), so nothing is overwritten.
#    The very first time, when the file does not exist yet (or is empty), the header line is
#    written first. After that, the header is never written again.
# 3. Out, file name and columns: internship_applications.csv, separated by ";" like the
#    example file (Excel in French opens ";" files correctly).
#    Columns: date_applied;company;role;city;sector;channel
# 4. Why these columns, and what this file is for:
#    With 200 applications I want to know which approach actually works: which channel
#    (LinkedIn vs. company website vs. referral) and which sector gets me answers, and
#    how many applications I send per week. Each row is one application sent: an event
#    that happened once and never changes. That's why there is no "status" column:
#    a status changes over time, and this program can only add rows, not edit them.


import csv
import os
from datetime import date

FILE_NAME = "internship_applications.csv"
COLUMNS = ["date_applied", "company", "role", "city", "sector", "channel"]
SECTORS = ["marketing", "luxury", "tech", "media", "motorsport", "other"]
CHANNELS = ["website", "linkedin", "email", "referral"]


def ask_text(question):
    """Ask until the user types something that isn't empty. ';' is removed so it can't break columns."""
    while True:
        answer = input(question).strip().replace(";", ",")
        if answer != "":
            return answer
        print("  This can't be empty. Try again.")


def ask_choice(question, options):
    """Ask until the user types one of the allowed options."""
    while True:
        answer = input(question + " (" + "/".join(options) + "): ").strip().lower()
        if answer in options:
            return answer
        print("  '" + answer + "' is not an option. Choose one of: " + ", ".join(options))


# --- Collect one entry ---
company = ask_text("Company: ")
role = ask_text("Role: ")
city = ask_text("City: ")
sector = ask_choice("Sector", SECTORS)
channel = ask_choice("How did you apply", CHANNELS)
today = date.today().isoformat()          # e.g. 2026-10-26

# --- First time? The file needs its header line ---
file_is_new = not os.path.exists(FILE_NAME) or os.path.getsize(FILE_NAME) == 0

# --- Save: "a" = append, adds to the end instead of overwriting ---
with open(FILE_NAME, "a", newline="", encoding="utf-8") as file:
    writer = csv.writer(file, delimiter=";")
    if file_is_new:
        writer.writerow(COLUMNS)
    writer.writerow([today, company, role, city, sector, channel])

print("Saved to", FILE_NAME)
