"""Exercise 7.1 — Loading a file, cleaning it, saving the result (homework)

This is the direct rehearsal for the final exam. Session 8 starts with it.

WHAT THE PROGRAM MUST DO
    Load names.txt, clean what is inside, sort it by last name, and write the result to
    a new file. The original file must not be modified.

DO THIS BEFORE ANYTHING ELSE
    Open names.txt and read it with your eyes. Then write, in comments at the top of
    your file, everything that is wrong with it. There are at least four different
    problems. Find them yourself.

    This step is not optional and it is graded. An assistant cannot see your file.

ANSWER THESE, in comments, after the list of problems
    1. What goes in?
    2. What happens to it?  (one line per problem you found, and how you deal with it)
    3. What comes out?
    4. What does "sort by last name" mean when a line contains two words, and how do you
       know which one is the last name?

WHAT THE AI CANNOT KNOW
    The actual content of names.txt. If you paste this brief into an assistant without
    describing the file, it will write a program for a clean file, and that program will
    crash or produce nonsense on the real one.

    Describe the file to it. That description is the exercise.

CHECK IT YOURSELF
    Count the lines in names.txt, then in your output file. The numbers should differ,
    and you should be able to say exactly why. Then check the first and last name of
    your sorted list by hand.

DELIVERABLE
    This file, plus the output file your program produced.
"""

# What is wrong with names.txt (found by reading it, not by guessing):
# - Extra spaces or a tab at the start or end of some lines ("  Lucas Martin", "Giulia Rossi  ", a tab before "Karim Benali")
# - Empty lines, and one line that only contains spaces
# - Inconsistent capitalisation: ALL CAPS ("SOPHIE BERNARD"), all lowercase ("thomas leroy")
# - Several spaces between first and last name ("Amina   Diallo", "Emma  Petit")
# - Two different formats: most lines are "First Last", but two are "Last, First" ("Chen, Wei", "Schmidt, Anna")
# - Duplicates: "Marie Dupont" and "Giulia Rossi" appear twice, and "lucas martin" is the same
#   person as "  Lucas Martin" once spaces and capitals are fixed
# - A last name made of two words: "Lucas van Dijk" (last name is "van Dijk", not just "Dijk")

# 1. In: names.txt — 20 lines, one name per line, messy.
# 2. Process, problem by problem:
#    - spaces/tab at start or end  -> strip() removes them
#    - empty or spaces-only lines  -> after strip() the line is "", so I skip it
#    - "Last, First" format        -> if there is a comma, split on it and swap the two parts
#    - several spaces in between   -> split() with no argument ignores extra spaces
#    - bad capitalisation          -> capitalize() each word, except small name particles
#                                     like "van" or "de" in the middle, which stay lowercase
#    - duplicates                  -> I only check for duplicates AFTER cleaning, otherwise
#                                     "lucas martin" and "  Lucas Martin" look different
#    - two-word last name          -> first word = first name, everything after = last name
#    Then sort by last name (and by first name if two people share a last name).
# 3. Out: names_clean.txt — 14 lines, one "First Last" per line, sorted by last name.
#    names.txt is only opened for reading, so it is never modified.
# 4. How I decide which word is the last name:
#    After converting "Last, First" lines, every line is "First Last". The first word is
#    the first name and everything after it is the last name. So "Lucas van Dijk" has
#    last name "van Dijk" and is sorted under V. (Dutch phone books would file it under D;
#    I chose V because it is the simple rule and it treats every line the same way.)


INPUT_FILE = "names.txt"
OUTPUT_FILE = "names_clean.txt"

# Small words that belong to a last name and stay lowercase, like "van" in "van Dijk"
PARTICLES = ["van", "von", "de", "der", "den", "da", "di", "du"]


def fix_capitals(words):
    """Capitalise each word, but keep particles like 'van' lowercase in the middle of a name."""
    fixed = []
    for position, word in enumerate(words):
        is_middle_word = 0 < position < len(words) - 1
        if is_middle_word and word.lower() in PARTICLES:
            fixed.append(word.lower())
        else:
            fixed.append(word.capitalize())
    return fixed


def clean_line(line):
    """Turn one messy line into (first_name, last_name), or None if the line is empty."""
    line = line.strip()                  # remove spaces, tabs and the newline at both ends
    if line == "":
        return None                      # empty line or spaces only: nothing to keep

    if "," in line:                      # "Chen, Wei" -> "Wei Chen"
        last, first = line.split(",", 1)
        line = first + " " + last

    words = line.split()                 # split() also throws away extra spaces
    words = fix_capitals(words)

    first_name = words[0]
    last_name = " ".join(words[1:])
    return (first_name, last_name)


def sort_key(person):
    """Sort by last name first, then by first name. lower() so capitals don't matter."""
    first_name, last_name = person
    return (last_name.lower(), first_name.lower())


# --- Read and clean ---
people = []
already_seen = []
lines_read = 0
empty_lines = 0
duplicates = 0

with open(INPUT_FILE, "r", encoding="utf-8") as file:
    for line in file:
        lines_read += 1
        person = clean_line(line)

        if person is None:
            empty_lines += 1
            continue

        if person in already_seen:
            duplicates += 1
            continue

        already_seen.append(person)
        people.append(person)

# --- Sort ---
people.sort(key=sort_key)

# --- Write to a NEW file ---
with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
    for first_name, last_name in people:
        file.write(first_name + " " + last_name + "\n")

# --- Report, so I can check the numbers myself ---
print("Lines read:", lines_read)
print("Empty lines skipped:", empty_lines)
print("Duplicates removed:", duplicates)
print("Names written:", len(people), "->", OUTPUT_FILE)
print("First:", people[0][0], people[0][1])
print("Last:", people[-1][0], people[-1][1])