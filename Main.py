import os
import csv
from datetime import datetime
import requests
import mysql.connector

FILENAME = "weather_logs.csv"
API_KEY = "Get Your own key here"   # Replace with your OpenWeatherMap API key

# ---- MySQL Config ----
DB_CONFIG = {
    "host": "localhost",
    "user": "root",         # replace with your MySQL username
    "password": "password", # replace with your MySQL password
    "database": "weather_db"
}

# ---- Setup CSV ----
if not os.path.exists(FILENAME):
    with open(FILENAME, "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Date", "City", "Temperature", "Condition"])

# ---- Setup MySQL Table ----
def init_db():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS weather_logs (
            id INT AUTO_INCREMENT PRIMARY KEY,
            log_date DATE NOT NULL,
            city VARCHAR(100) NOT NULL,
            temperature FLOAT NOT NULL,
            condition VARCHAR(50) NOT NULL,
            UNIQUE KEY unique_city_date (log_date, city)
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()

# ---- Log Weather ----
def log_weather():
    city = input("Enter your city name: ").strip()
    date = datetime.now().strftime("%Y-%m-%d")

    # Prevent duplicate in CSV
    with open(FILENAME, "r", newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["Date"] == date and row['City'].lower() == city.lower():
                print("Entry for this city and date exists (CSV check).")
                return

    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()
        if response.status_code != 200:
            print(f"API Error: {data.get('message', 'Unknown error')}")
            return

        temp = data["main"]["temp"]
        condition = data["weather"][0]["main"]

        # ---- Write to CSV ----
        with open(FILENAME, "a", newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([date, city.title(), temp, condition])

        # ---- Write to MySQL ----
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO weather_logs (log_date, city, temperature, condition)
                VALUES (%s, %s, %s, %s)
                """, (date, city.title(), temp, condition)
            )
            conn.commit()
        except mysql.connector.Error as err:
            if err.errno == 1062:  # Duplicate entry
                print("Entry for this city and date already exists in MySQL.")
            else:
                print(f"MySQL Error: {err}")
        finally:
            cursor.close()
            conn.close()

        print(f"Logged: {temp}°C {condition} in {city.title()} on {date}")

    except Exception as e:
        print(f"Failed to fetch API data: {e}")

# ---- View Logs ----
def view_logs():
    with open(FILENAME, "r", encoding="utf-8") as f:
        reader = list(csv.reader(f))
        if len(reader) <= 1:
            print("No Entries")
            return
        print("\n--- Weather Logs (CSV) ---")
        for row in reader[1:]:
            print(f"{row[0]} | {row[1]} | {row[2]}°C | {row[3]}")

    # Optional: also fetch from MySQL
    print("\n--- Weather Logs (MySQL) ---")
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("SELECT log_date, city, temperature, condition FROM weather_logs ORDER BY log_date DESC")
    for row in cursor.fetchall():
        print(f"{row[0]} | {row[1]} | {row[2]}°C | {row[3]}")
    cursor.close()
    conn.close()

# ---- Main ----
def main():
    init_db()
    while True:
        print("\nReal-Time Weather Logger")
        print("1. Add weather log")
        print("2. View weather logs")
        print("3. Exit")
        choice = input("Choose an option: ").strip()
        match choice:
            case "1": log_weather()
            case "2": view_logs()
            case "3": break
            case _: print("Invalid choice")

if __name__ == "__main__":
    main()
