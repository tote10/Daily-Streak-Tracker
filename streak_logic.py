from datetime import datetime, date, timedelta
def check_status(streak):
    last_date = streak["last_date"]
    if last_date:
        last_date_obj = datetime.fromisoformat(last_date).date()
        yesterday = date.today() - timedelta(days=1)
        if last_date_obj < yesterday:
            streak["count"] = 0
            return True
    return False
def check_in(streak):
    today = date.today().isoformat()
    if streak["last_date"] == today:
        return False#already checked in
    check_status(streak)
    streak["count"] += 1
    streak["last_date"] = today
    return True
def restore_streak(streak):
    today_month = date.today().month
    if streak["restore_month"] != today_month:
        streak["restores"] = 0
        streak["restore_month"] = today_month
    broken = check_status(streak)
    if not broken:
        return False, "Streak is not broken. Restore not allowed."
    if streak["restores"] < 5:
        streak["restores"] += 1
        streak["count"] += 1
        return True, f"Streak restored! Current streak: {streak['count']}"

    else:
        return False, "Maximum restores reached this month."