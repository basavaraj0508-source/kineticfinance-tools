import requests
import csv

API_KEY = "YOUR_RAPIDAPI_KEY"   # ← replace with your key
API_URL = "https://jsearch.p.rapidapi.com/search"

# Roles to search
job_roles = [
    "DevOps Manager",
    "Director",
    "Product Owner",
    "Project Leader",
    "IT Project Manager"
]

# Connecticut filter keywords
CT_KEYWORDS = ["Connecticut", "CT", "Hartford", "Stamford", "Norwalk", "Waterbury", 
               "Bridgeport", "New Haven", "Danbury", "Middletown", "Farmington", 
               "New Britain", "West Hartford", "Windsor"]

headers = {
    "x-rapidapi-key": API_KEY,
    "x-rapidapi-host": "jsearch.p.rapidapi.com"
}

all_results = []

for role in job_roles:
    query_params = {
        "query": f"{role} in Connecticut",   # ← helps API focus on CT jobs
        "num_pages": 2                       # increase for more results
    }

    response = requests.get(API_URL, headers=headers, params=query_params)
    data = response.json().get("data", [])

    for job in data:
        job_location = job.get("job_city", "") or ""
        full_location = job.get("job_location", "") or ""
        employer_location = job.get("employer_country", "") or ""

        # Check if job is CT-based (city or state's abbreviation)
        if any(keyword.lower() in full_location.lower() for keyword in CT_KEYWORDS):
            all_results.append({
                "Role Searched": role,
                "Job Title": job.get("job_title"),
                "Company": job.get("employer_name"),
                "Location": full_location,
                "Employment Type": job.get("job_employment_type"),
                "Posted At": job.get("job_posted_at_datetime_utc"),
                "Apply Link": job.get("job_apply_link")
            })

# Save only CT jobs to a CSV
with open("CT_job_results.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=all_results[0].keys())
    writer.writeheader()
    writer.writerows(all_results)

print("CT job search complete. Saved to CT_job_results.csv")
