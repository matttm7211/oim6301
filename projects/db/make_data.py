"""Generate fake CSV data for the BabsonAI Labs database.

Writes one CSV per table (people, project, task, expenses, assignment)
into projects/db/data/. Run with:

    uv run python projects/db/make_data.py
"""

import csv
import random
from datetime import date, timedelta
from pathlib import Path

from faker import Faker

# Fixed seed so the script writes the same files every time it runs.
random.seed(42)
fake = Faker()
Faker.seed(42)

# "Today" for this fake company. All the "past 12 months" data counts
# back from this date instead of the real today, so re-running the
# script months from now still produces the same files.
AS_OF = date(2026, 11, 14)

DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)


def random_date(start, end):
    """Return a random date between start and end (inclusive)."""
    days_between = (end - start).days
    offset = random.randint(0, days_between)
    return start + timedelta(days=offset)


# ---------------------------------------------------------------------------
# People
# ---------------------------------------------------------------------------

TITLES_BY_LEVEL = {
    0: ["Founder & CEO", "Founder & CTO"],
    1: ["VP of Engineering", "VP of Data Science", "VP of Operations"],
    2: ["Engineering Manager", "Data Science Manager", "Product Manager"],
    3: [
        "Senior ML Engineer",
        "Senior Data Engineer",
        "Senior Data Scientist",
        "Business Analyst",
    ],
    4: ["ML Engineer", "Data Engineer", "Data Scientist", "Analyst"],
}

people_rows = []
person_level = {}  # person_id -> level, used to build the reporting chain
person_start_date = {}  # person_id -> start_date, used later by tasks

NUM_PEOPLE = 25
next_person_id = 1

# Level 0: the two founders. They report to nobody.
for title in TITLES_BY_LEVEL[0]:
    first = fake.first_name()
    last = fake.last_name()
    person_id = next_person_id
    next_person_id += 1
    # Founders started the company, so they get the earliest start dates.
    start = random_date(date(2022, 1, 1), date(2022, 6, 30))
    email = f"{first}.{last}@babsonailabs.com".lower()
    people_rows.append(
        [person_id, first, last, email, title, start.isoformat(), ""]
    )
    person_level[person_id] = 0
    person_start_date[person_id] = start

founder_ids = [1, 2]

# Levels 1-4: everyone else. Each new person reports to someone already
# created at the level above them, so managers always appear earlier in
# the file than the people who report to them.
level = 1
while len(people_rows) < NUM_PEOPLE:
    titles_here = TITLES_BY_LEVEL.get(level, TITLES_BY_LEVEL[4])
    # Roughly how many people to add at this level before moving deeper.
    how_many = min(6, NUM_PEOPLE - len(people_rows))
    for _ in range(how_many):
        if len(people_rows) >= NUM_PEOPLE:
            break
        # Pick a manager from the level directly above this one.
        manager_candidates = [
            pid for pid, lvl in person_level.items() if lvl == level - 1
        ]
        manager_id = random.choice(manager_candidates)
        first = fake.first_name()
        last = fake.last_name()
        person_id = next_person_id
        next_person_id += 1
        title = random.choice(titles_here)
        manager_start = person_start_date[manager_id]
        start = random_date(
            manager_start + timedelta(days=30), date(2026, 9, 1)
        )
        email = f"{first}.{last}@babsonailabs.com".lower()
        people_rows.append(
            [person_id, first, last, email, title, start.isoformat(), manager_id]
        )
        person_level[person_id] = level
        person_start_date[person_id] = start
    level += 1

with open(DATA_DIR / "people.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(
        [
            "person_id",
            "first_name",
            "last_name",
            "work_email",
            "title",
            "start_date",
            "manager_id",
        ]
    )
    writer.writerows(people_rows)

all_person_ids = [row[0] for row in people_rows]

# ---------------------------------------------------------------------------
# Project
# ---------------------------------------------------------------------------

CATEGORIES = ["LLM app", "data pipeline", "internal tool"]
STATUSES = ["planned", "active", "paused", "done"]
PROJECT_NAME_WORDS = [
    "Atlas",
    "Beacon",
    "Nimbus",
    "Forge",
    "Pulse",
    "Vertex",
    "Orbit",
    "Lattice",
    "Harbor",
    "Summit",
    "Cascade",
    "Horizon",
    "Anchor",
    "Prism",
]

NUM_PROJECTS = 14
project_rows = []
project_category = {}
project_status = {}
project_start_date = {}

zero_expense_project_id = None
internal_no_client_project_id = None

for i in range(NUM_PROJECTS):
    project_id = i + 1
    name = PROJECT_NAME_WORDS[i % len(PROJECT_NAME_WORDS)] + " " + str(1 + i // len(PROJECT_NAME_WORDS))
    category = CATEGORIES[i % len(CATEGORIES)]
    status = random.choice(STATUSES)
    budget = round(random.uniform(15000, 500000), 2)
    start = random_date(AS_OF - timedelta(days=365), AS_OF - timedelta(days=14))

    if category == "internal tool":
        client_name = ""
    else:
        client_name = fake.company()

    # Force the first internal-tool project to have no client on purpose,
    # even though internal projects usually lack one anyway.
    if category == "internal tool" and internal_no_client_project_id is None:
        internal_no_client_project_id = project_id
        client_name = ""

    project_rows.append(
        [project_id, name, client_name, category, budget, start.isoformat(), status]
    )
    project_category[project_id] = category
    project_status[project_id] = status
    project_start_date[project_id] = start

# Pick the last project to be the one that will get zero expenses on purpose.
zero_expense_project_id = NUM_PROJECTS

with open(DATA_DIR / "project.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(
        ["project_id", "name", "client_name", "category", "budget", "start_date", "status"]
    )
    writer.writerows(project_rows)

all_project_ids = [row[0] for row in project_rows]

# ---------------------------------------------------------------------------
# Assignment (who works on which project)
# ---------------------------------------------------------------------------

ROLES = ["Project Lead", "Engineer", "Data Scientist", "Analyst", "Contributor"]

assignment_rows = []
# project_id -> list of person_ids working on it; used by task generation
# to keep tasks assigned to someone who actually works on that project.
project_team = {}

for project_id in all_project_ids:
    project_team[project_id] = []
    team_size = random.randint(3, 6)
    # Only people who had already started by the project's start date
    # can join it, otherwise date_joined could come before they existed here.
    eligible = [
        pid for pid in all_person_ids
        if person_start_date[pid] <= AS_OF - timedelta(days=1)
    ]
    team = random.sample(eligible, min(team_size, len(eligible)))
    for person_id in team:
        role = random.choice(ROLES)
        hours_per_week = random.randint(1, 40)
        earliest_join = max(person_start_date[person_id], project_start_date[project_id])
        date_joined = random_date(earliest_join, AS_OF)
        assignment_rows.append(
            [person_id, project_id, role, hours_per_week, date_joined.isoformat()]
        )
        project_team[project_id].append(person_id)

with open(DATA_DIR / "assignment.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["person_id", "project_id", "role", "hours_per_week", "date_joined"])
    writer.writerows(assignment_rows)

# ---------------------------------------------------------------------------
# Task
# ---------------------------------------------------------------------------

TASK_DESCRIPTIONS = [
    "Write unit tests",
    "Clean up raw dataset",
    "Review pull request",
    "Set up GPU cluster",
    "Draft client proposal",
    "Tune model hyperparameters",
    "Build dashboard",
    "Fix data pipeline bug",
    "Prepare status report",
    "Label training data",
    "Deploy model to production",
    "Meet with client",
    "Document API",
    "Run evaluation suite",
]

NUM_TASKS = 260
task_rows = []
broken_task_ids = []  # the two tasks we deliberately break

# Reserve task_ids 1 and 2 for the on-purpose broken rows, and task_id 3
# for the on-purpose unassigned task, so they are easy to find later.
unassigned_task_id = 3

def random_weekday_biased_date(start, end, weekend_prob=0.1):
    while True:
        d = random_date(start, end)
        if d.weekday() < 5 or random.random() < weekend_prob:
            return d


for task_id in range(1, NUM_TASKS + 1):
    project_id = random.choice(all_project_ids)
    team = project_team[project_id]

    if task_id in (1, 2):
        # On purpose: assign this task to someone who does NOT work on
        # this project, breaking the "assigned person works on the
        # project" rule. Collect everyone who is NOT on this project's
        # team (checking every other project), then pick one of them.
        outsiders = []
        for other_id in all_project_ids:
            if other_id == project_id:
                continue
            for pid in project_team[other_id]:
                if pid not in project_team[project_id] and pid not in outsiders:
                    outsiders.append(pid)
        assigned_person_id = random.choice(outsiders)
        broken_task_ids.append(task_id)
        earliest = max(person_start_date[assigned_person_id], project_start_date[project_id])
    elif task_id == unassigned_task_id:
        # On purpose: an unassigned task.
        assigned_person_id = ""
        earliest = project_start_date[project_id]
    elif team:
        assigned_person_id = random.choice(team)
        # A task can't be created before the assigned person started.
        earliest = max(person_start_date[assigned_person_id], project_start_date[project_id])
    else:
        assigned_person_id = ""
        earliest = project_start_date[project_id]

    date_created = random_weekday_biased_date(earliest, AS_OF)
    due_date = date_created + timedelta(days=random.randint(3, 45))

    # About 60% of tasks are already completed.
    if random.random() < 0.6:
        completed_start = date_created
        completed_end = min(due_date + timedelta(days=20), AS_OF)
        if completed_end < completed_start:
            completed_end = completed_start
        date_completed = random_date(completed_start, completed_end).isoformat()
    else:
        date_completed = ""

    description = random.choice(TASK_DESCRIPTIONS)
    task_rows.append(
        [
            task_id,
            project_id,
            description,
            date_created.isoformat(),
            assigned_person_id,
            due_date.isoformat(),
            date_completed,
        ]
    )

with open(DATA_DIR / "task.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(
        [
            "task_id",
            "project_id",
            "description",
            "date_created",
            "assigned_person_id",
            "due_date",
            "date_completed",
        ]
    )
    writer.writerows(task_rows)

# ---------------------------------------------------------------------------
# Expenses
# ---------------------------------------------------------------------------

EXPENSE_CATEGORIES = ["GPU cloud", "data labeling", "software", "travel"]
EXPENSE_NOTES = {
    "GPU cloud": ["Monthly compute bill", "Training run", ""],
    "data labeling": ["Vendor invoice", "Batch labeling job", ""],
    "software": ["Annual license", "Subscription renewal", ""],
    "travel": ["Client site visit", "Conference travel", ""],
}

NUM_EXPENSES = 160
expense_rows = []

# Every project except the reserved one gets at least one expense, so the
# zero-expense project really ends up with none.
expense_eligible_projects = [p for p in all_project_ids if p != zero_expense_project_id]

for expense_id in range(1, NUM_EXPENSES + 1):
    project_id = random.choice(expense_eligible_projects)
    category = random.choice(EXPENSE_CATEGORIES)
    amount = round(random.uniform(50, 20000), 2)
    expense_date = random_date(AS_OF - timedelta(days=365), AS_OF)
    note = random.choice(EXPENSE_NOTES[category])
    expense_rows.append(
        [expense_id, project_id, expense_date.isoformat(), amount, category, note]
    )

with open(DATA_DIR / "expenses.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(
        ["expense_id", "project_id", "expense_date", "amount", "category", "note"]
    )
    writer.writerows(expense_rows)

# ---------------------------------------------------------------------------
# Report what was generated
# ---------------------------------------------------------------------------

print(f"Wrote {len(people_rows)} people to {DATA_DIR / 'people.csv'}")
print(f"Wrote {len(project_rows)} projects to {DATA_DIR / 'project.csv'}")
print(f"Wrote {len(assignment_rows)} assignments to {DATA_DIR / 'assignment.csv'}")
print(f"Wrote {len(task_rows)} tasks to {DATA_DIR / 'task.csv'}")
print(f"Wrote {len(expense_rows)} expenses to {DATA_DIR / 'expenses.csv'}")
print()
print(f"On purpose, project {zero_expense_project_id} has zero expenses.")
print(f"On purpose, project {internal_no_client_project_id} is an internal tool with no client_name.")
print(f"On purpose, task {unassigned_task_id} has no assigned_person_id.")
print(f"On purpose, these tasks are assigned to someone off the project: {broken_task_ids}")
