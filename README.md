# 🎬 Netflix Content Library Analysis

An end-to-end data analysis project on the [Netflix Movies and TV Shows dataset](https://www.kaggle.com/datasets/shivamb/netflix-shows) from Kaggle — covering data cleaning, SQL analysis, and an interactive Power BI dashboard.

---

## 📌 Project Overview

This project explores Netflix's content library to answer questions like:
- Which genres are most common on Netflix, and how have they trended over time?
- Which countries produce the most content for Netflix?
- How long are Netflix movies, and how many seasons do TV shows typically run?
- How has Netflix's content library grown year over year?

The project uses a three-tool pipeline: **Python** for cleaning, **SQL** for querying, and **Power BI** for visualization — mirroring a real-world data analytics workflow.

---

## 🛠️ Tools & Tech Stack

| Tool | Purpose |
|---|---|
| **Python (pandas)** | Data cleaning — handling missing values, removing duplicates, splitting multi-value columns, fixing data types |
| **SQL (SQLite)** | Querying cleaned data for genre trends, country-wise content, and duration analysis |
| **Power BI** | Interactive dashboard with genre, country, and year filters |

---

## 📂 Project Structure

```
netflix-content-analysis/
│
├── netflix_titles.csv              # Raw dataset (from Kaggle)
├── clean_data.py                   # Python script: cleans and prepares the data
├── load_to_sql.py                  # Python script: loads cleaned CSVs into a SQLite database
├── queries.sql                     # All SQL queries used for analysis
│
├── netflix_cleaned.csv             # Cleaned dataset (missing values handled, duration split)
├── netflix_genres_long.csv         # Genre column exploded into one genre per row
├── netflix_countries_long.csv      # Country column exploded into one country per row
│
├── Netflix_Dashboard.pbix          # Power BI dashboard file
└── README.md                       # Project documentation (this file)
```

---

## 🧹 Step 1: Data Cleaning (Python)

The raw dataset had several data quality issues that were addressed in `clean_data.py`:

- **Missing values:**
  - `director`, `cast`, `country` had a large number of missing values → filled with `"Unknown"` to avoid losing data
  - `date_added`, `rating`, `duration` had very few missing rows (~17 total) → dropped, since removing them had negligible impact on the dataset
- **Date formatting:** `date_added` was stored as text → converted to a proper datetime format using `pd.to_datetime()`
- **Duplicate check:** verified with `df.duplicated().sum()` — no duplicate rows found
- **Multi-value columns split (exploded):**
  - `listed_in` (genres) and `country` contained comma-separated values (e.g. `"Drama, Comedy"`) → split into one value per row using `.str.split()` + `.explode()`, so each genre/country could be counted accurately
- **Duration column split:** since `duration` mixed two units (`"90 min"` for movies, `"2 Seasons"` for TV shows), it was split into two separate numeric columns — `duration_minutes` and `duration_seasons` — using regex extraction

---

## 🔍 Step 2: SQL Analysis

The cleaned CSVs were loaded into a SQLite database (`netflix.db`) using `load_to_sql.py`, then queried in `queries.sql`. Key queries include:

1. **Genre trend over time** — count of titles per genre, per year added
2. **Content by country** — total titles, movies, and TV shows per country
3. **Movie duration buckets** — movies grouped into Under 60 min / 60–120 min / Over 120 min
4. **TV show season distribution** — count of shows by number of seasons
5. **Top trending genre per year** — using a `RANK()` window function to find each year's most-added genre

> **Note:** In early years (2008–2010), multiple genres are tied for "top genre" because very little content was added to Netflix during that period — this is expected, not an error.

---

## 📊 Step 3: Power BI Dashboard

The dashboard (`Netflix_Dashboard.pbix`) brings the analysis together into four interactive visuals:

- **Top Genres on Netflix** — bar chart of title count by genre
- **Content Growth Over Time** — line chart showing titles added per year (2008–2021)
- **Global Content Distribution** — map showing content volume by country
- **Movie Duration Breakdown** — pie chart of movies by duration bucket

A **year slicer** allows viewers to filter the entire dashboard interactively.

> **Note on 2020–2021 dip:** the line chart shows a drop in titles added after 2019. This isn't a real decline — the dataset was collected before 2021 ended, so that year's data is incomplete.

---

## 🚀 How to Run This Project

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/netflix-content-analysis.git
   ```
2. **Run the cleaning script**
   ```bash
   python clean_data.py
   ```
   This generates `netflix_cleaned.csv`, `netflix_genres_long.csv`, and `netflix_countries_long.csv`.
3. **Load data into SQLite**
   ```bash
   python load_to_sql.py
   ```
   This creates `netflix.db` with three tables ready to query.
4. **Run SQL queries**
   Open `netflix.db` in [DB Browser for SQLite](https://sqlitebrowser.org/) and run the queries in `queries.sql`.
5. **Open the dashboard**
   Open `Netflix_Dashboard.pbix` in [Power BI Desktop](https://powerbi.microsoft.com/desktop/).

---

## 📈 Key Insights

- **International Movies** and **Dramas** are the most common genres on Netflix
- The **United States** and **India** are the top content-producing countries
- Most Netflix movies run between **87–114 minutes**
- Most Netflix TV shows last just **1–2 seasons**
- Netflix's content library grew sharply between **2015 and 2019**

---

## 📚 Dataset Source

[Netflix Movies and TV Shows — Kaggle](https://www.kaggle.com/datasets/shivamb/netflix-shows)
