import pandas as pd
df = pd.read_csv("netflix_titles.csv")
print(df.shape)
print(df.head())
print(df.info())
print(df.isnull().sum())

df['director'] = df['director'].fillna('Unknown')
df['cast'] = df['cast'].fillna('Unknown')
df['country'] = df['country'].fillna('Unknown')

# date_added ko convert karo, fillna mat karo
df['date_added'] = pd.to_datetime(df['date_added'].str.strip(), errors='coerce')

# thodi rows wale missing values ko drop karo
df = df.dropna(subset=['date_added', 'rating', 'duration'])

print(df.isnull().sum())
print(df.shape)
print(df.duplicated().sum())
print(df['type'].unique())
print(df['rating'].unique())

# Genre ko explode karo
genres = df.assign(genre=df['listed_in'].str.split(', ')).explode('genre')
genres['genre'] = genres['genre'].str.strip()

# Country ko explode karo
countries = df.assign(country_single=df['country'].str.split(', ')).explode('country_single')
countries['country_single'] = countries['country_single'].str.strip()

# Check karo kaisa dikhta hai
print(genres[['title','genre']].head(10))
print(countries[['title','country_single']].head(10))

# Ab teeno cleaned files ko save kar do — ye tumhari SQL/Excel/PowerBI ke liye base files hongi
df.to_csv("netflix_cleaned.csv", index=False)
genres.to_csv("netflix_genres_long.csv", index=False)
countries.to_csv("netflix_countries_long.csv", index=False)

print("Files saved successfully!")

# Duration ko clean karo — Movies aur TV Shows alag treat karne padenge
df['duration_minutes'] = df[df['type']=='Movie']['duration'].str.extract('(\d+)').astype(float)
df['duration_seasons'] = df[df['type']=='TV Show']['duration'].str.extract('(\d+)').astype(float)

# Check karo dono columns sahi bane
print(df[['type','duration','duration_minutes','duration_seasons']].head(10))

# Movies ka duration distribution
print(df['duration_minutes'].describe())

# TV Shows ka season distribution
print(df['duration_seasons'].value_counts().sort_index())

print(df[df['duration']==df['duration_minutes'].min()][['title','duration_minutes']])
print(df[df['duration_minutes']==df['duration_minutes'].max()][['title','duration_minutes']])

df.to_csv("netflix_cleaned.csv", index=False)
print("Final cleaned file updated")