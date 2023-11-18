import os
api_key = os.environ['FRED_API_KEY']
FROM = "2006-03-01"
TO = "2023-11-01"
ids = ["AWHAEMAL",
       "AWHAECON",
       "AWHAEMAN",
       "AWHAETTU",
       "AWHAEINFO",
       "AWHAEFA",
       "AWHAEPBS",
       "AWHAEEHS",
       "AWHAELAH"
       ]
request_template = "https://api.stlouisfed.org/fred/series?series_id={series_id}&api_key={api_key}&file_type=json&realtime_start={from}&realtime_end={to}"

