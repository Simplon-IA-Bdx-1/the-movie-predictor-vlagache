from datetime import datetime, timedelta
from tmdb import Tmdb
import os

api_key = os.environ['TMDB_API_KEY']
tmdb = Tmdb(api_key)


now = datetime.now()
now_format = now.strftime("%Y-%m-%d")

# print(f"date d'aujourdhui :  {now}")

date_before_onew = now - timedelta(days=7)
# print(f"date une semaine avant : {date_before_onew}")

date_format = date_before_onew.strftime("%Y-%m-%d")
print(date_format)

url = f"https://api.themoviedb.org/3/discover/movie?api_key={api_key}&language=en-US&primary_release_date.gte={date_format}&primary_release_date.lte={now_format}&with_runtime.gte=60"

print(tmdb.get_films_by_release(date_format,now_format))


# tmdb.get_film(args.550)


# now = datetime.now()
# print("Initial date : ", str(now))

# future_date_before_7days = now - timedelta(days=7) # date-time une semaine avant 

# print("La date - 1 semaine ", str(future_date_before_7days))
# print(type(future_date_before_7days))

# print(future_date_before_7days.year)
# print(future_date_before_7days.month)
# print(future_date_before_7days.day)

# xx = future_date_before_7days.strftime("%Y-%m-%d")
# print(type(xx))