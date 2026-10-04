--Q1 genre trend over time
SELECT genre, strftime('%Y', date_added) AS year_added, COUNT(*) AS titles
FROM netflix_genres_long
GROUP BY genre, year_added
ORDER BY year_added, titles DESC;


--Q2 content by country
SELECT country_single AS country, COUNT(*) AS total_titles,
       SUM(CASE WHEN type='Movie' THEN 1 ELSE 0 END) AS movies,
       SUM(CASE WHEN type='TV Show' THEN 1 ELSE 0 END) AS tv_shows
FROM netflix_countries_long
GROUP BY country
ORDER BY total_titles DESC
LIMIT 20;
--Q3 movie duration buckets
SELECT
  CASE WHEN duration_minutes < 60 THEN 'Under 60 min'
       WHEN duration_minutes BETWEEN 60 AND 120 THEN '60-120 min'
       ELSE 'Over 120 min' END AS duration_bucket,
  COUNT(*) AS movie_count
FROM netflix_titles
WHERE type = 'Movie'
GROUP BY duration_bucket;

--Q4 TV show season distribution
SELECT duration_seasons, COUNT(*) AS show_count
FROM netflix_titles
WHERE type = 'TV Show'
GROUP BY duration_seasons
ORDER BY duration_seasons;

--Q5 top trending genre per year
SELECT year_added, genre, titles
FROM (
    SELECT genre, strftime('%Y', date_added) AS year_added, COUNT(*) AS titles,
           RANK() OVER (PARTITION BY strftime('%Y', date_added) ORDER BY COUNT(*) DESC) AS rnk
    FROM netflix_genres_long
    GROUP BY genre, year_added
)
WHERE rnk = 1
ORDER BY year_added;