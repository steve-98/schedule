import random
from fpdf import FPDF
from datetime import datetime, timedelta
import os

# Subjects and Timeslots
subjects = ["PhD Research", "DS Masters", "French Grammar","Photography"]

# Weekday times
weekday_times = [
    "9:00 AM - 12:00 PM",
    "1:00 PM - 3:00 PM",
    "3:00 PM - 4:00 PM",
    "9:00 PM - 12:00 AM",
]

# Weekend times
weekend_times = [
    "9:00 AM - 9:45 AM",
    "10:00 AM - 10:30 AM",
    "10:45 AM - 11:15 AM",
    "11:30 AM - 12:00 PM",
]

# Randomize subjects for weekdays and weekends
def generate_weekly_schedule():
    schedule = {"Weekdays": {}, "Weekend": {}}

    # Generate weekday schedule
    for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]:
        daily_subjects = subjects[:]
        random.shuffle(daily_subjects)
        schedule["Weekdays"][day] = {
            weekday_times[0]: daily_subjects[0],
            weekday_times[1]: daily_subjects[1],
            weekday_times[2]: daily_subjects[2],
            weekday_times[3]: random.choice(subjects),  # Flexible evening slot
        }

    # Generate weekend schedule
    for day in ["Saturday", "Sunday"]:
        daily_subjects = subjects[:]
        random.shuffle(daily_subjects)
        schedule["Weekend"][day] = {
            weekend_times[0]: daily_subjects[0],
            weekend_times[1]: daily_subjects[1],
            weekend_times[2]: daily_subjects[2],
            weekend_times[3]: daily_subjects[2],
        }

    return schedule

# Create PDF from schedule
def create_schedule_pdf(schedule):
    # Determine week start and end dates
    today = datetime.now()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)

    week_start_str = start_of_week.strftime("%Y-%m-%d")
    week_end_str = end_of_week.strftime("%Y-%m-%d")
    filename = f"weekly/Weekly_Schedule_{week_start_str}_to_{week_end_str}.pdf"

    # Ensure the "weekly" folder exists
    os.makedirs("weekly", exist_ok=True)

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page(orientation="landscape")
    pdf.set_font("Arial", size=12)

    pdf.set_font("Arial", style="B", size=16)
    pdf.cell(200, 10, "Weekly Study Schedule", ln=True, align='C')

    pdf.set_font("Arial", size=12)
    pdf.ln(10)  # Line break

    # Add weekdays schedule in table format
    pdf.set_font("Arial", style="B", size=14)
    pdf.cell(0, 10, "Weekdays", ln=True)

    # Header row
    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(50, 10, "Day", border=1)
    for time in weekday_times:
        pdf.cell(40, 10, time, border=1)
    pdf.ln()

    # Data rows
    pdf.set_font("Arial", size=12)
    for day, slots in schedule["Weekdays"].items():
        pdf.cell(50, 10, day, border=1)
        for time in weekday_times:
            subject = slots.get(time, "")
            pdf.cell(40, 10, subject, border=1)
        pdf.ln()

    pdf.ln(10)  # Line break

    # Add weekend schedule in table format
    pdf.set_font("Arial", style="B", size=14)
    pdf.cell(0, 10, "Weekend", ln=True)

    # Header row
    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(50, 10, "Day", border=1)
    for time in weekend_times:
        pdf.cell(50, 10, time, border=1)
    pdf.ln()

    # Data rows
    pdf.set_font("Arial", size=12)
    for day, slots in schedule["Weekend"].items():
        pdf.cell(50, 10, day, border=1)
        for time in weekend_times:
            subject = slots.get(time, "")
            pdf.cell(50, 10, subject, border=1)
        pdf.ln()

    pdf.output(filename)
    print(f"PDF schedule generated as '{filename}'.")

# Generate schedule and create PDF
schedule = generate_weekly_schedule()
create_schedule_pdf(schedule)
