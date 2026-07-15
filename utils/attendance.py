import os
import csv
from datetime import datetime
ATTENDANCE_FILE = "data/attendance.csv"
def create_attendance_file() :
    os.makedirs("data", exist_ok=True)
    if not os.path.exists(ATTENDANCE_FILE):
        with open(ATTENDANCE_FILE, "w", newline="") as file :
            writer = csv.writer(file)
            writer.writerow(["Name", "Date", "Time", "Status"])
def attendance_exists(student_name):
    create_attendance_file()
    today = datetime.now().strftime("%d-%m-%Y")
    with open(ATTENDANCE_FILE, "r") as file :
        reader = csv.DictReader(file)
        for row in reader :
            if (row["Name"]==student_name and row["Date"]==today):
                return True
    return False
def mark_attendance(student_name):
    create_attendance_file()
    if attendance_exists(student_name):
        return False
    now = datetime.now()
    date = now.strftime("%d-%m-%Y")
    time = now.strftime("%I:%M:%S %p")
    with open(ATTENDANCE_FILE, "a", newline="") as file :
        writer = csv.writer(file)
        writer.writerow([student_name, date, time, "Present"])
        return True
def get_attendance() :
    create_attendance_file()
    records = []
    with open(ATTENDANCE_FILE, "r") as file :
        reader = csv.DictReader(file)
        for row in reader :
            records.append(row)
    return records