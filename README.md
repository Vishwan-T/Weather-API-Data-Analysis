# Weather-API-Data-Analysis

# 🌦️ Real-Time Weather Logger (CSV + MySQL)

A Python CLI tool that fetches **real-time weather data** for a given city using the [OpenWeatherMap API](https://openweathermap.org/api) and logs it into:

- **CSV file** (`weather_logs.csv`)  
- **MySQL database** (`weather_logs` table in `weather_db`)  

It also provides basic analytics and prevents duplicate entries (same city, same date).

---

## 📂 Project Structure
```plaintext
weather-logger/
│── main.py              # Main Python CLI program 
│── transformations.sql  # Database schema setup and SQL queries for insights/analytics
│── README.md            # Project documentation
│── weather_logs.csv     # CSV logs (auto-created)

Real-Time Weather Tracking – Fetches live weather data (temperature & condition) for any city using the OpenWeatherMap API.

Dual Storage System – Logs data into both a CSV file (weather_logs.csv) and a MySQL database (weather_logs table), ensuring persistence and scalability.

Duplicate Prevention – Avoids multiple entries for the same city on the same date, keeping logs clean and accurate.

Analytics & Transformations – Provides insights like average, highest, and lowest temperatures, most frequent conditions, daily & monthly summaries, and rolling averages using SQL transformations.

User-Friendly CLI – Simple command-line interface with options to add new logs, view existing logs, and extend for analytics dashboards or automation in the future.
