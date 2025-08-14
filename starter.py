import requests
from bs4 import BeautifulSoup

# Lockheed Martin job search URL (example for QA roles)
url = "https://www.lockheedmartinjobs.com/search-jobs/quality%20assurance"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)
print(f"Response status code: {response.status_code}")
soup = BeautifulSoup(response.text, 'html.parser')

# This selector may need adjustment based on actual HTML structure
job_cards = soup.find_all('div', class_='job-result-card')
print(f"Found {len(job_cards)} job cards")

for job in job_cards:
    title = job.find('h2').text.strip()
    location = job.find('span', class_='job-location').text.strip()
    link = job.find('a', href=True)['href']
    
    print(f"🔹 {title} — {location}")
    print(f"🔗 Apply here: https://www.lockheedmartinjobs.com{link}\n")
def is_relevant(title):
    keywords = ['QA', 'Quality Assurance', 'Quality Engineer', 'CI/CD', 'Cypress', 'Manager']
    return any(keyword.lower() in title.lower() for keyword in keywords)

for job in job_cards:
    title = job.find('h2').text.strip()
    location = job.find('span', class_='job-location').text.strip()
    link = job.find('a', href=True)['href']
    
    if is_relevant(title):
        print(f"✅ {title} — {location}")
        print(f"🔗 Apply here: https://www.lockheedmartinjobs.com{link}\n")