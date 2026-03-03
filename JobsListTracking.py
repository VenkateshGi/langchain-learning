import http.client
import json
import csv
import os

# Build connection and headers for RapidAPI jsearch
conn = http.client.HTTPSConnection("jsearch.p.rapidapi.com")

headers = {
    'x-rapidapi-key': os.environ.get("RAPIDAPI_KEY", ""),
    'x-rapidapi-host': "jsearch.p.rapidapi.com"
}

# Query parameters can be modified below
query = "Gen AI jobs in Hyderabad"
country = "in"
page = 1
num_pages = 1

conn.request(
    "GET",
    f"/search?query={query.replace(' ', '%20')}&page={page}&num_pages={num_pages}&country={country}&date_posted=week",
    headers=headers,
)

res = conn.getresponse()
raw_data = res.read()

# decode and parse JSON
text = raw_data.decode("utf-8")
response = json.loads(text)

# extract job information and write to CSV
output_file = "jobs.csv"
fields = ["job_title", "employer_name", "job_apply_link", "job_location", "job_description", "job_posted_at_datetime_utc"]

with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fields)
    writer.writeheader()
    for job in response.get("data", []):
        writer.writerow({
            "job_title": job.get("job_title", ""),
            "employer_name": job.get("employer_name", ""),
            "job_apply_link": job.get("job_apply_link", ""),
            "job_location": job.get("job_location", ""),
            "job_description": job.get("job_description", ""),
            "job_posted_at_datetime_utc": job.get("job_posted_at_datetime_utc", ""),
        })

print(f"Wrote {len(response.get('data', []))} jobs to {output_file}")