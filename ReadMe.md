The goal of this agent is to monitor Lockheed Martin’s careers page and relevant job boards for QA roles that match my experience, and notify me with tailored summaries and application suggestions.
# Running this agent
1. Install playwright:  
    python -m playwright install
1. Install Chromium browser:  
    python -m playwright install chromium
1. Run the agent:  
    python playwright_scraper.py

# Next Steps You Can Take:
1. Customize Keywords: Modify the is_relevant() function to match your specific interests
1. Add More Companies: Create similar scrapers for other aerospace companies  
1. Schedule Regular Runs: Set up the script to run daily/weekly  
1. Export Results: Add functionality to save results to CSV/Excel  
1. Add Notifications: Get email/SMS alerts for new relevant jobs  
1. Scan other sites for QA Leadership roles

# Credits
    This code has been written by Github Copilot.