import time
import numpy as np
import pandas as pd
import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import warnings
warnings.filterwarnings('ignore')

# Import our custom webdriver utility
from .webdriver_utils import setup_webdriver

class LinkedInScraper:
    """Class for scraping job listings from LinkedIn"""

    @staticmethod
    def webdriver_setup():
        """Set up and configure the Chrome webdriver"""
        # Use our custom webdriver setup utility with multiple fallback options
        return setup_webdriver()

    @staticmethod
    def get_user_input(show_title=True):
        """Get user input for job search parameters"""
        add_vertical_space(1)
        
        # Apply custom styling for the form
        if show_title:
            st.markdown("""
                <style>
                .linkedin-form {
                    background: rgba(10, 102, 194, 0.05);
                    border-radius: 10px;
                    padding: 20px;
                    border-left: 4px solid #0A66C2;
                    margin-bottom: 20px;
                }
                .linkedin-title {
                    color: #0A66C2;
                    font-weight: bold;
                }
                .linkedin-subtitle {
                    color: #666;
                    font-size: 0.9rem;
                    margin-bottom: 15px;
                }
                </style>
            """, unsafe_allow_html=True)
            
            st.markdown('<div class="linkedin-form">', unsafe_allow_html=True)
            st.markdown('<h3 class="linkedin-title"><i class="fab fa-linkedin"></i> LinkedIn Job Scraper</h3>', unsafe_allow_html=True)
            st.markdown('<p class="linkedin-subtitle">Find real-time job listings directly from LinkedIn</p>', unsafe_allow_html=True)
            
        with st.form(key='linkedin_scrape'):
            col1, col2, col3 = st.columns([0.5, 0.3, 0.2], gap='medium')
            
            with col1:
                job_title_input = st.text_input(
                    label='Job Title',
                    placeholder='e.g. Data Scientist, Software Engineer',
                    help="Enter job titles separated by commas"
                )
                job_title_input = job_title_input.split(',')
            
            with col2:
                job_location = st.text_input(
                    label='Job Location', 
                    value='India',
                    placeholder='e.g. Bangalore, Mumbai, Remote',
                    help="Enter a location or 'India' for nationwide search"
                )
            
            with col3:
                job_count = st.number_input(
                    label='Number of Jobs', 
                    min_value=1, 
                    max_value=10,
                    value=3, 
                    step=1,
                    help="Number of job listings to scrape (max 10)"
                )

            # Submit Button
            add_vertical_space(1)
            submit = st.form_submit_button(
                label='Search LinkedIn Jobs',
                type='primary',
                use_container_width=True
            )
            add_vertical_space(1)
        
        if show_title:
            st.markdown('</div>', unsafe_allow_html=True)
        
        return job_title_input, job_location, job_count, submit

    @staticmethod
    def build_url(job_title, job_location):
        """Build LinkedIn search URL from job title and location"""
        # Format job titles
        formatted_titles = []
        for title in job_title:
            if title.strip():  # Skip empty titles
                words = title.strip().split()
                formatted_title = '%20'.join(words)
                formatted_titles.append(formatted_title)
        
        # If no valid titles, use a default
        if not formatted_titles:
            formatted_titles = ["jobs"]
        
        # Join multiple job titles
        job_title_param = '%2C%20'.join(formatted_titles)
        
        # Format location
        location_param = job_location.replace(' ', '%20')
        
        # Build the LinkedIn search URL
        link = f"https://in.linkedin.com/jobs/search?keywords={job_title_param}&location={location_param}&geoId=102713980&f_TPR=r604800&position=1&pageNum=0"
        
        return link

    @staticmethod
    def open_link(driver, link):
        """Open LinkedIn link and wait for page to load"""
        max_attempts = 3
        attempts = 0
        
        while attempts < max_attempts:
            try:
                driver.get(link)
                driver.implicitly_wait(5)
                time.sleep(3)
                
                # Check if page loaded correctly
                if "LinkedIn" in driver.title:
                    return True
                    
                # Alternative check for elements
                try:
                    driver.find_element(by=By.CSS_SELECTOR, value='.jobs-search-results')
                    return True
                except:
                    pass
                    
                try:
                    driver.find_element(by=By.CSS_SELECTOR, value='.jobs-search-results-list')
                    return True
                except:
                    pass
                
                # One more attempt with a different selector
                try:
                    driver.find_element(by=By.CSS_SELECTOR, value='.base-search-card')
                    return True
                except:
                    pass
                
                attempts += 1
                if attempts >= max_attempts:
                    st.warning("Could not load LinkedIn jobs page. Please try again.")
                    return False
                    
                time.sleep(2)
                
            except Exception as e:
                attempts += 1
                if attempts >= max_attempts:
                    st.warning(f"Error loading LinkedIn page: {str(e)}")
                    return False
                time.sleep(2)
                
        return False

    @staticmethod
    def link_open_scrolldown(driver, link, job_count):
        """Open LinkedIn link and scroll down to load more jobs"""
        # Open the link
        if not LinkedInScraper.open_link(driver, link):
            return False
        
        # Scroll down to load more jobs
        scroll_attempts = min(job_count + 5, 15)  # Add extra scrolls to ensure we get enough jobs
        
        for i in range(scroll_attempts):
            try:
                # Handle sign-in modal if it appears
                try:
                    dismiss_buttons = driver.find_elements(
                        by=By.CSS_SELECTOR, 
                        value="button[data-tracking-control-name='public_jobs_contextual-sign-in-modal_modal_dismiss']"
                    )
                    if dismiss_buttons:
                        dismiss_buttons[0].click()
                except:
                    pass
                
                # Scroll down to load more content
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1.5)
                
                # Try to click "See more jobs" button if present
                try:
                    see_more_buttons = driver.find_elements(
                        by=By.CSS_SELECTOR, 
                        value="button[aria-label='See more jobs']"
                    )
                    if see_more_buttons:
                        see_more_buttons[0].click()
                        time.sleep(2)
                except:
                    pass
                
            except Exception as e:
                continue
        
        return True

    @staticmethod
    def job_title_filter(scrap_job_title, user_job_title_input):
        """Filter job titles based on user input"""
        # Skip filtering if job title input is empty or contains only empty strings
        if not user_job_title_input or all(not title.strip() for title in user_job_title_input):
            return scrap_job_title
        
        # User job titles converted to lowercase
        user_input = [title.lower().strip() for title in user_job_title_input if title.strip()]
        
        # If no valid user input after cleaning, return the original title
        if not user_input:
            return scrap_job_title
        
        # Scraped job title converted to lowercase
        scrap_title = scrap_job_title.lower().strip()
        
        # Check if any user job title matches the scraped job title
        for user_title in user_input:
            # Check if all words in user title are in scraped title
            if all(word in scrap_title for word in user_title.split()):
                return scrap_job_title
        
        # No match found
        return np.nan

    @staticmethod
    def scrap_company_data(driver, job_title_input, job_location):
        """Scrape company data from LinkedIn job listings"""
        try:
            # Scrape company names
            company_elements = driver.find_elements(
                by=By.CSS_SELECTOR, 
                value='h4.base-search-card__subtitle'
            )
            company_names = [element.text for element in company_elements if element.text.strip()]
            
            # Scrape job locations
            location_elements = driver.find_elements(
                by=By.CSS_SELECTOR, 
                value='span.job-search-card__location'
            )
            company_locations = [element.text for element in location_elements if element.text.strip()]
            
            # Scrape job titles
            title_elements = driver.find_elements(
                by=By.CSS_SELECTOR, 
                value='h3.base-search-card__title'
            )
            job_titles = [element.text for element in title_elements if element.text.strip()]
            
            # Scrape job URLs
            url_elements = driver.find_elements(
                by=By.XPATH, 
                value='//a[contains(@href, "/jobs/view/")]'
            )
            job_urls = [element.get_attribute('href') for element in url_elements if element.get_attribute('href')]
            
            # Check if we have any data
            if not company_names or not job_titles or not company_locations or not job_urls:
                st.warning("No job listings found on LinkedIn. Try different search terms.")
                return pd.DataFrame()
            
            # Ensure all arrays have the same length by truncating to the shortest length
            min_length = min(len(company_names), len(job_titles), len(company_locations), len(job_urls))
            
            if min_length == 0:
                st.warning("No job listings found on LinkedIn. Try different search terms.")
                return pd.DataFrame()
                
            company_names = company_names[:min_length]
            job_titles = job_titles[:min_length]
            company_locations = company_locations[:min_length]
            job_urls = job_urls[:min_length]
            
            # Create DataFrame
            df = pd.DataFrame({
                'Company Name': company_names,
                'Job Title': job_titles,
                'Location': company_locations,
                'Website URL': job_urls
            })
            
            # Filter job titles based on user input if provided
            if job_title_input and job_title_input != ['']:
                filtered_titles = []
                for title in df['Job Title']:
                    if any(user_title.lower().strip() in title.lower() for user_title in job_title_input if user_title.strip()):
                        filtered_titles.append(title)
                    else:
                        filtered_titles.append(np.nan)
                df['Job Title'] = filtered_titles
            
            # Filter locations based on user input if provided and not "India"
            if job_location and job_location.lower() != "india":
                filtered_locations = []
                for loc in df['Location']:
                    if job_location.lower() in loc.lower():
                        filtered_locations.append(loc)
                    else:
                        filtered_locations.append(np.nan)
                df['Location'] = filtered_locations
            
            # Drop rows with NaN values and reset index
            df = df.dropna()
            df = df.reset_index(drop=True)
            
            return df
            
        except Exception as e:
            st.error(f"Error scraping company data: {str(e)}")
            st.info("Try refreshing the page or using different search terms.")
            return pd.DataFrame()

    @staticmethod
    def scrap_job_description(driver, df, job_count):
        """Scrape job descriptions for each job listing"""
        if df.empty:
            return df
        
        # Get job URLs
        job_urls = df['Website URL'].tolist()
        
        # Limit to requested job count
        job_urls = job_urls[:min(len(job_urls), job_count)]
        
        # Initialize list for job descriptions
        job_descriptions = []
        
        # Progress bar for scraping job descriptions
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i, url in enumerate(job_urls):
            try:
                # Update progress
                progress = int((i + 1) / len(job_urls) * 100)
                progress_bar.progress(progress)
                status_text.text(f"Scraping job {i+1} of {len(job_urls)}...")
                
                # Open job listing page
                driver.get(url)
                driver.implicitly_wait(5)
                time.sleep(2)
                
                # Try to click "Show more" button to expand job description
                try:
                    show_more_buttons = driver.find_elements(
                        by=By.CSS_SELECTOR, 
                        value='button[data-tracking-control-name="public_jobs_show-more-html-btn"]'
                    )
                    if show_more_buttons:
                        show_more_buttons[0].click()
                        time.sleep(1)
                except:
                    pass
                
                # Get job description
                description_elements = driver.find_elements(
                    by=By.CSS_SELECTOR, 
                    value='div.show-more-less-html__markup'
                )
                
                if description_elements and description_elements[0].text.strip():
                    description_text = description_elements[0].text
                    
                    # Process and structure the job description
                    processed_description = LinkedInScraper.process_job_description(description_text)
                    job_descriptions.append(processed_description)
                else:
                    # Try alternative selectors
                    alt_description = driver.find_elements(
                        by=By.CSS_SELECTOR, 
                        value='div.description__text'
                    )
                    if alt_description and alt_description[0].text.strip():
                        description_text = alt_description[0].text
                        processed_description = LinkedInScraper.process_job_description(description_text)
                        job_descriptions.append(processed_description)
                    else:
                        job_descriptions.append("Description not available")
                    
            except Exception as e:
                job_descriptions.append("Description not available")
                st.warning(f"Error scraping job description {i+1}: {str(e)}")
            
        # Clear progress indicators
        progress_bar.empty()
        status_text.empty()
        
        # Filter DataFrame to include only rows with descriptions
        df = df.iloc[:len(job_descriptions), :]
        
        # Add job descriptions to DataFrame
        df['Job Description'] = job_descriptions
        
        # Filter out rows with unavailable descriptions
        df['Job Description'] = df['Job Description'].apply(
            lambda x: np.nan if x == "Description not available" else x
        )
        df = df.dropna()
        df = df.reset_index(drop=True)
        
        return df

    @staticmethod
    def process_job_description(text):
        """Process and structure job description text"""
        if not text or text == "Description not available":
            return text
            
        # Split into sections
        sections = text.split('\n\n')
        processed_sections = []
        
        # Common section headers to identify
        section_headers = [
            "responsibilities", "requirements", "qualifications", "skills", 
            "about the job", "about the role", "what you'll do", "what you'll need",
            "about us", "about the company", "who we are", "benefits", "perks",
            "job description", "role description", "experience", "education", 
            "job summary", "job overview", "job requirements", "job responsibilities",
            "job qualifications", "job skills", "job benefits", "job perks",
            "job description", "role description", "experience", "education",
            "job summary", "job overview", "job requirements", "job responsibilities",
            "job qualifications", "job skills", "job benefits", "job perks",
            "Education Qualification and Experience", "Required Skills", "Preferred Qualifications", "Key Responsibilities",
            "About Us", "About the Company", "About the Role", "About the Job",
            "About the Team", "About the Organization", "About the Industry", "About the Location",
            "Position", "Job Description", "Job Summary", "Job Overview"
        ]
        
        # Process each section
        current_section = ""
        for section in sections:
            if not section.strip():
                continue
                
            # Check if this is a new section header
            is_header = False
            section_lower = section.lower().strip()
            
            # Check if section starts with a header
            for header in section_headers:
                if section_lower.startswith(header) or section_lower.startswith("• " + header) or section_lower.startswith("- " + header):
                    # Format as a header
                    current_section = section.strip()
                    is_header = True
                    processed_sections.append(f"\n**{current_section}**\n")
                    break
            
            if not is_header:
                # Check if it's a bullet point list
                if section.strip().startswith('•') or section.strip().startswith('-') or section.strip().startswith('*'):
                    lines = section.split('\n')
                    formatted_lines = []
                    
                    for line in lines:
                        line = line.strip()
                        if line:
                            if line.startswith('•') or line.startswith('-') or line.startswith('*'):
                                # Format as bullet point
                                formatted_lines.append(f"• {line.lstrip('•').lstrip('-').lstrip('*').strip()}")
                            else:
                                formatted_lines.append(line)
                    
                    processed_sections.append('\n'.join(formatted_lines))
                else:
                    # Regular paragraph
                    processed_sections.append(section.strip())
        
        # Join all processed sections
        return '\n\n'.join(processed_sections)

    @staticmethod
    def display_data_userinterface(df_final):
        """Display scraped job data in the user interface"""
        if df_final.empty:
            st.warning("No matching jobs found. Try different search terms or location.")
            return
            
        # Apply custom styling for job cards
        st.markdown("""
            <style>
            .job-card {
                background: rgba(255, 255, 255, 0.05);
                border-radius: 10px;
                padding: 1.5rem;
                margin-bottom: 1rem;
                border-left: 4px solid #0A66C2;
                transition: transform 0.2s;
            }
            .job-card:hover {
                background: rgba(255, 255, 255, 0.08);
            }
            .job-title {
                color: #0A66C2;
                font-size: 1.3rem;
                margin-bottom: 0.5rem;
            }
            .company-name {
                font-weight: bold;
                font-size: 1.1rem;
            }
            .job-location {
                color: #888;
                margin-bottom: 1rem;
            }
            .job-url-button {
                display: inline-block;
                background: #0A66C2;
                color: white;
                padding: 0.5rem 1rem;
                border-radius: 5px;
                text-decoration: none;
                margin-top: 1rem;
                font-weight: bold;
            }
            .job-url-button:hover {
                background: #084d8e;
            }
            .job-count {
                background: rgba(10, 102, 194, 0.1);
                color: #0A66C2;
                padding: 0.5rem 1rem;
                border-radius: 5px;
                margin-bottom: 1rem;
                font-weight: bold;
            }
            .job-section {
                margin-top: 1rem;
                padding-top: 0.5rem;
                border-top: 1px solid rgba(255, 255, 255, 0.1);
            }
            .job-section-title {
                font-weight: bold;
                color: #0A66C2;
                margin-bottom: 0.5rem;
            }
            </style>
        """, unsafe_allow_html=True)
        
        # Display job count
        st.markdown(f'<div class="job-count">🎯 Found {len(df_final)} matching jobs on LinkedIn</div>', unsafe_allow_html=True)
        
        # Display each job
        for i in range(len(df_final)):
            company_name = df_final.iloc[i, 0]
            job_title = df_final.iloc[i, 1]
            location = df_final.iloc[i, 2]
            url = df_final.iloc[i, 3]
            description = df_final.iloc[i, 4]
            
            # Create job card
            st.markdown(f"""
                <div class="job-card">
                    <div class="job-title">{job_title}</div>
                    <div class="company-name">{company_name}</div>
                    <div class="job-location">📍 {location}</div>
                </div>
            """, unsafe_allow_html=True)
            
            # Job description in expander with better formatting
            with st.expander("View Job Description"):
                st.markdown(description)
                st.markdown(f"<a href='{url}' target='_blank' class='job-url-button'>Apply on LinkedIn</a>", unsafe_allow_html=True)
            
            st.markdown("<hr>", unsafe_allow_html=True)

    @staticmethod
    def main(show_title=True):
        """Main function to run the LinkedIn job scraper"""
        # Initialize driver to None
        driver = None
        
        try:
            # Get user input
            job_title_input, job_location, job_count, submit = LinkedInScraper.get_user_input(show_title)
            
            if submit:
                if job_title_input != [''] and job_location:
                    try:
                        # Set up Chrome webdriver
                        with st.spinner('Setting up Chrome webdriver...'):
                            driver = LinkedInScraper.webdriver_setup()
                            
                            if not driver:
                                st.error("Failed to initialize Chrome webdriver. Please make sure Chrome is installed.")
                                return
                        
                        # Build URL and open LinkedIn
                        with st.spinner('Loading LinkedIn jobs page...'):
                            link = LinkedInScraper.build_url(job_title_input, job_location)
                            st.info(f"Searching for: {', '.join([t for t in job_title_input if t.strip()])} in {job_location}")
                            success = LinkedInScraper.link_open_scrolldown(driver, link, job_count)
                            
                            if not success:
                                st.error("Failed to load LinkedIn jobs page. Please try again.")
                                return
                        
                        # Scrape job data
                        with st.spinner('Scraping job listings...'):
                            df = LinkedInScraper.scrap_company_data(driver, job_title_input, job_location)
                            
                            if df.empty:
                                st.warning("No jobs found matching your criteria. Try different search terms.")
                                return
                        
                        # Scrape job descriptions
                        with st.spinner('Fetching job descriptions...'):
                            df_final = LinkedInScraper.scrap_job_description(driver, df, job_count)
                            
                            if df_final.empty:
                                st.warning("Could not retrieve job descriptions. Try different search terms.")
                                return
                        
                        # Display results
                        LinkedInScraper.display_data_userinterface(df_final)
                        
                    except Exception as e:
                        st.error(f"An error occurred: {str(e)}")
                        st.info("Try refreshing the page or using different search terms.")
                        
                elif job_title_input == ['']:
                    st.warning("Please enter a job title to search.")
                    
                elif not job_location:
                    st.warning("Please enter a job location to search.")
                    
        except Exception as e:
            st.error(f"An unexpected error occurred: {str(e)}")
            
        finally:
            # Close the webdriver
            if driver:
                driver.quit()

def render_linkedin_scraper():
    """Render the LinkedIn job scraper interface"""
    # Don't show the title again, as it's already shown in the job_search.py file
    LinkedInScraper.main(show_title=False)