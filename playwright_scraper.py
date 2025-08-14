import asyncio
from playwright.async_api import async_playwright
import time

async def scrape_lockheed_martin_jobs():
    """
    Scrape Lockheed Martin jobs using Playwright to handle dynamic content
    """
    
    async with async_playwright() as p:
        # Launch browser (set headless=False to see the browser in action)
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # Set a realistic user agent
        await page.set_extra_http_headers({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        })
        
        try:
            print("🚀 Loading Lockheed Martin jobs page...")
            
            # Navigate to the jobs page
            url = "https://www.lockheedmartinjobs.com/search-jobs/quality%20assurance"
            await page.goto(url, wait_until="networkidle")
            
            print("⏳ Waiting for job listings to load...")
            
            # Wait for the search results section to load
            try:
                await page.wait_for_selector('#search-results-list', timeout=15000)
                print("✅ Found search results section")
                
                # Wait a bit more for the job list to populate
                await page.wait_for_selector('#search-results-list ul li', timeout=10000)
                print("✅ Found job listings")
                jobs_found = True
                
            except Exception as e:
                print(f"❌ Could not find job listings: {e}")
                jobs_found = False
            
            if not jobs_found:
                print("⚠️ No job listings found with standard selectors. Let's inspect the page...")
                
                # Take a screenshot for debugging
                await page.screenshot(path="debug_screenshot.png")
                print("📸 Screenshot saved as debug_screenshot.png")
                
                # Get page content and look for patterns
                content = await page.content()
                
                # Look for common job-related patterns in the HTML
                if "job" in content.lower():
                    print("🔍 Found 'job' text in page content")
                
                # Try to find any clickable job elements
                job_elements = await page.query_selector_all('a[href*="job"], div[class*="job"], li[class*="job"]')
                print(f"🔍 Found {len(job_elements)} potential job elements")
                
                # Show page title and some content for debugging
                title = await page.title()
                print(f"📄 Page title: {title}")
                
                await browser.close()
                return
            
            # If we found jobs, extract them
            print("📝 Extracting job information...")
            
            # Extract job data from the list structure
            jobs = []
            
            # Get all job list items
            job_list_items = await page.query_selector_all('#search-results-list ul li')
            
            if job_list_items:
                print(f"Found {len(job_list_items)} job listings")
                
                for job_item in job_list_items:
                    try:
                        # Extract job details from each list item
                        job_link = await job_item.query_selector('a[data-job-id]')
                        
                        if job_link:
                            # Get job title
                            title_element = await job_link.query_selector('.job-title')
                            title = await title_element.inner_text() if title_element else "Title not found"
                            
                            # Get location
                            location_element = await job_link.query_selector('.job-location')
                            location = await location_element.inner_text() if location_element else "Location not found"
                            
                            # Get job link
                            href = await job_link.get_attribute('href')
                            full_link = f"https://www.lockheedmartinjobs.com{href}" if href else "Link not found"
                            
                            # Get job ID
                            job_id_element = await job_link.query_selector('.job-id')
                            job_id = await job_id_element.inner_text() if job_id_element else "ID not found"
                            
                            # Get date posted
                            date_element = await job_link.query_selector('.job-date-posted')
                            date_posted = await date_element.inner_text() if date_element else "Date not found"
                            
                            jobs.append({
                                'title': title.strip(),
                                'location': location.strip(),
                                'link': full_link,
                                'job_id': job_id.strip(),
                                'date_posted': date_posted.strip()
                            })
                            
                    except Exception as e:
                        print(f"Error extracting job details: {e}")
                        continue
            
            # Display results
            if jobs:
                print(f"\n🎯 Found {len(jobs)} relevant jobs:")
                print("=" * 80)
                
                relevant_jobs = []
                for i, job in enumerate(jobs, 1):
                    print(f"\n{i}. 🔹 {job['title']}")
                    print(f"   📍 {job['location']}")
                    print(f"   🆔 {job['job_id']}")
                    print(f"   � {job['date_posted']}")
                    print(f"   �🔗 {job['link']}")
                    
                    # Check if job is relevant
                    if is_relevant(job['title']):
                        print("   ✅ RELEVANT JOB!")
                        relevant_jobs.append(job)
                    
                print(f"\n🎉 Summary: Found {len(relevant_jobs)} relevant jobs out of {len(jobs)} total jobs!")
                
                if relevant_jobs:
                    print("\n🏆 RELEVANT JOBS SUMMARY:")
                    print("=" * 50)
                    for i, job in enumerate(relevant_jobs, 1):
                        print(f"{i}. {job['title']} - {job['location']}")
                        print(f"   {job['link']}")
                        
            else:
                print("❌ No jobs extracted. The page structure might be different than expected.")
                
                # Let's save the page content for manual inspection
                content = await page.content()
                with open("debug_page_content.html", "w", encoding="utf-8") as f:
                    f.write(content)
                print("💾 Page content saved to debug_page_content.html for inspection")
        
        except Exception as e:
            print(f"❌ Error occurred: {e}")
        
        finally:
            await browser.close()

def is_relevant(title):
    """Check if job title contains relevant keywords"""
    keywords = ['QA', 'Quality Assurance', 'Quality Engineer', 'CI/CD', 'Cypress', 'Manager', 'Test', 'Testing']
    return any(keyword.lower() in title.lower() for keyword in keywords)

async def main():
    print("🔍 Starting Lockheed Martin Job Scraper with Playwright...")
    await scrape_lockheed_martin_jobs()
    print("\n✅ Scraping completed!")

if __name__ == "__main__":
    # Run the async function
    asyncio.run(main())
