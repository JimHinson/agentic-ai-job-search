# The goal of this agent is to continuously monitor Lockheed Martin’s careers page and relevant job boards for QA roles that match my experience, and notify me with tailored summaries and application suggestions.
import requests
from bs4 import BeautifulSoup

def get_job_listings(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    job_listings = []
    for job in soup.find_all('div', class_='job-listing'):
        title = job.find('h2').text
        location = job.find('span', class_='location').text
        job_listings.append({'title': title, 'location': location})
    return job_listings

def is_relevant(job_title, job_description):
    keywords = ['QA', 'Quality Engineer', 'CI/CD', 'Cypress', 'Leadership']
    return any(keyword.lower() in job_title.lower() or keyword.lower() in job_description.lower() for keyword in keywords)

from openai import OpenAI

def summarize_job(description):
    prompt = f"Summarize this job description and explain how it matches Jim's skills: {description}"
    response = openai.ChatCompletion.create(model="gpt-4", messages=[{"role": "user", "content": prompt}])
    return response['choices'][0]['message']['content']

import smtplib
def send_email(subject, body, to_email):
    from_email = "jim@hinson.com"
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(from_email, "your_password")
        message = f"Subject: {subject}\n\n{body}"
        server.sendmail(from_email, to_email, message)
        server.quit()

def generate_cover_letter(job_title, company, description):
    prompt = f"Write a cover letter for a QA Manager role at {company} based on this job description: {description}. Highlight Jim's experience in CI/CD, Cypress, and leadership."
    response = openai.ChatCompletion.create(model="gpt-4", messages=[{"role": "user", "content": prompt}])
    return response['choices'][0]['message']['content']