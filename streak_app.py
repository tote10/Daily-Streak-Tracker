from datetime import date
streak = {
"name":"Github"
,"count":0
,"last_date":None
,"restores":0}
today = date.today().isoformat()
if streak["last_date"] != today:
    streak["count"] += 1
    streak["last_date"]=today
print(streak)
