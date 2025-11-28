import calendar, datetime

all_events = {}

# ---------- Display Calendar ----------
def show_calendar(year, month):
    today = datetime.date.today()
    print(f"\n{calendar.month_name[month]} {year}\nMo Tu We Th Fr Sa Su")
    for week in calendar.monthcalendar(year, month):
        for day in week:
            if day == 0:
                print("   ", end=" ")
            else:
                s = f"{day:2}"

                # Add * if today or event exists
                if (day == today.day and month == today.month and year == today.year) or \
                   str(day) in all_events.get(f"{year}-{month}", {}):
                    s += "*"

                print(f"{s:3}", end=" ")
        print()

# ---------- View Events ----------
def view_events(year=None, month=None):
    # Specific month
    if year and month:
        events = all_events.get(f"{year}-{month}", {})
        if not events:
            print("\nNo events for this month.")
            return

        print(f"\nEvents for {calendar.month_name[month]} {year}:")
        for d, e in sorted(events.items(), key=lambda x: int(x[0])):
            print(f"Day {d}: {e}")
        return

    # All events
    if not all_events:
        print("\nNo events saved yet.")
        return

    for k, ev in sorted(all_events.items()):
        y, m = map(int, k.split("-"))
        print(f"\n{calendar.month_name[m]} {y}:")
        for d, e in sorted(ev.items(), key=lambda x: int(x[0])):
            print(f"  Day {d}: {e}")

# ---------- Add Event ----------
def add_event(year, month):
    max_day = calendar.monthrange(year, month)[1]

    while True:
        day = input(f"Day (1-{max_day}) or 'c' to cancel: ")

        if day.lower() == "c":
            print("⚠️ Cancelled.")
            return

        try:
            day = int(day)
        except ValueError:
            print("❌ Invalid number. Try again.")
            continue

        if not (1 <= day <= max_day):
            print(f"❌ Day must be 1–{max_day}.")
            continue

        if datetime.date(year, month, day) < datetime.date.today():
            print("❌ Cannot select a past day.")
            continue

        break

    event_name = input("Event: ")
    all_events.setdefault(f"{year}-{month}", {})[str(day)] = event_name
    print(f"✅ Event added on {calendar.month_name[month]} {day}, {year}.")

# ---------- Delete Event ----------
def delete_event(year, month):
    key = f"{year}-{month}"

    if key not in all_events or not all_events[key]:
        print("⚠️ No events to delete in this month.")
        return

    while True:
        day = input("Day to delete or 'c' to cancel: ")

        if day.lower() == "c":
            print("⚠️ Cancelled.")
            return

        if day in all_events.get(key, {}):
            del all_events[key][day]
            print("🗑️ Event deleted.")
            return
        else:
            print("❌ No event on that day. Try again.")

# ---------- Get Year & Month ----------
def get_year_month():
    today = datetime.date.today()

    # Year
    while True:
        y = input("Year (e.g., 2025) or 'c' to cancel: ")

        if y.lower() == "c":
            return None, None

        try:
            y = int(y)
        except ValueError:
            print("❌ Invalid year. Try again.")
            continue

        if y < today.year:
            print("❌ Cannot select past year.")
            continue

        break

    # Month
    while True:
        m = input("Month (1-12) or 'c' to cancel: ")

        if m.lower() == "c":
            return None, None

        try:
            m = int(m)
        except ValueError:
            print("❌ Invalid month. Try again.")
            continue

        if not 1 <= m <= 12:
            print("❌ Month must be 1–12.")
            continue

        if y == today.year and m < today.month:
            print("❌ Cannot select past month.")
            continue

        break

    return y, m

# ---------- Exit ----------
def exit_menu():
    return input("\n1. Confirm Exit\n2. Cancel\nChoose: ") == "1"

# ---------- Main ----------
def main():
    while True:
        print("\n--- CALENDAR MENU ---")
        print("1. View Calendar")
        print("2. Add Event")
        print("3. Delete Event")
        print("4. View Events for This Month")
        print("5. View All Events")
        print("6. Exit")

        choice = input("Choose option (1-6): ")

        if choice in ["1", "2", "3"]:
            y, m = get_year_month()
            if not y:
                print("⚠️ Cancelled.")
                continue

            if choice == "1":
                show_calendar(y, m)
            elif choice == "2":
                add_event(y, m)
            elif choice == "3":
                delete_event(y, m)

        elif choice == "4":
            today = datetime.date.today()
            view_events(today.year, today.month)

        elif choice == "5":
            view_events()

        elif choice == "6":
            if exit_menu():
                print("👋 Goodbye!")
                break

        else:
            print("❌ Invalid choice.")

# FIXED main block
if _name_ == "_main_":
    main()