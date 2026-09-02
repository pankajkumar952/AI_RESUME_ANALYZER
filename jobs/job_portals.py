"""Module for handling job portal integrations"""
import urllib.parse
from typing import Dict, List
from .suggestions import LOCATION_SUGGESTIONS, get_cities_by_state

class JobPortal:
    """Class for searching jobs across multiple job portals"""
    
    def __init__(self):
        """Initialize job portal URLs and parameters"""
        self.portals = [
            {
                "name": "LinkedIn",
                "icon": "fab fa-linkedin",
                "color": "#0A66C2",
                "url": "https://www.linkedin.com/jobs/search/?keywords={}&location={}&f_E={}",
                "experience_param": ""
            },
            {
                "name": "Naukri",
                "icon": "fas fa-building",
                "color": "#FF7555",
                "url": "https://www.naukri.com/{}-jobs-in-{}?experience={}",
                "experience_param": ""
            },
            {
                "name": "Foundit (Monster)",
                "icon": "fas fa-globe",
                "color": "#5D3FD3",
                "url": "https://www.foundit.in/srp/results?query={}&locations={}",
                "experience_param": ""
            },
            {
                "name": "FreshersWorld",
                "icon": "fas fa-graduation-cap",
                "color": "#003A9B",
                "url": "https://www.freshersworld.com/jobs/jobsearch/{}-jobs-in-{}",
                "experience_param": ""
            },
            {
                "name": "TimesJobs",
                "icon": "fas fa-briefcase",
                "color": "#003A9B",
                "url": "https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords={}&txtLocation={}",
                "experience_param": ""
            },
            {
                "name": "Instahyre",
                "icon": "fas fa-user-tie",
                "color": "#003A9B",
                "url": "https://www.instahyre.com/{}-jobs-in-{}",
                "experience_param": ""
            },
            {
                "name": "Indeed",
                "icon": "fas fa-search-dollar",
                "color": "#003A9B",
                "url": "https://in.indeed.com/jobs?q={}&l={}&explvl={}",
                "experience_param": ""
            }
        ]

    def get_portal_list(self) -> List[Dict]:
        """Get list of available job portals"""
        return self.portals

    def format_query(self, query: str) -> str:
        """Format query string for URLs"""
        # Replace spaces with appropriate characters based on portal
        return query.replace(" ", "+")

    def format_location(self, location: str) -> str:
        """Format location string for URLs"""
        if not location:
            return ""
            
        # Check if location is a state
        location = location.strip()
        is_state = False
        
        # Check if the location is a state
        for loc in LOCATION_SUGGESTIONS:
            if loc.get("type") == "state" and loc.get("text").lower() == location.lower():
                is_state = True
                break
        
        # If it's a state, get the major city in that state for better job results
        if is_state:
            cities = get_cities_by_state(location)
            if cities:
                # Use the first city in the state (usually the capital or major city)
                location = cities[0]["text"]
        
        # Convert to lowercase and replace spaces with hyphens
        return location.lower().replace(" ", "-")

    def format_job_title(self, title: str) -> str:
        """Format job title for URLs"""
        # Remove common words and special characters
        title = title.lower()
        title = title.replace("developer", "").replace("engineer", "").strip()
        title = title.replace(" ", "-")
        return title.strip("-")

    def format_experience(self, experience: str) -> tuple:
        """Format experience for different job portals"""
        if not experience or experience == "all":
            return "", "0", "0", "entry"
        
        try:
            # Handle dictionary input
            if isinstance(experience, dict):
                exp_id = experience.get('id', 'all')
                if exp_id == 'all':
                    return "", "0", "0", "entry"
                
                # Split experience range (e.g., "1-3" -> ["1", "3"])
                if "-" in exp_id:
                    exp_min, exp_max = exp_id.split('-')
                    if exp_max == "+":
                        exp_max = "15"  # Set a reasonable maximum for 10+ years
                else:
                    # Handle "fresher" or other non-range values
                    exp_min = "0"
                    exp_max = "1"
                
                # Map to portal-specific format
                exp_level = {
                    "fresher": "0",
                    "0-1": "0",
                    "1-3": "1",
                    "3-5": "2",
                    "5-7": "3",
                    "7-10": "4",
                    "10+": "5"
                }.get(exp_id, "0")
                
                return exp_level, exp_min, exp_max, "entry" if exp_min == "0" else "experienced"
            
            return "", "0", "0", "entry"
            
        except Exception as e:
            print(f"Error formatting experience: {str(e)}")
            return "", "0", "0", "entry"

    def get_experience_param(self, portal_name, experience):
        """Get experience parameter for specific portal"""
        experience_id = experience.get("id", "all")
        
        if experience_id == "all":
            if portal_name == "Foundit (Monster)":
                return ""
            elif portal_name == "Naukri":
                return ""
            elif portal_name == "LinkedIn":
                return ""
            elif portal_name == "Indeed":
                return "entry_level"
        
        if portal_name == "Foundit (Monster)":
            if experience_id == "fresher":
                return "&experienceRanges=0~0"
            elif experience_id == "0-1":
                return "&experienceRanges=0~1"
            elif experience_id == "1-3":
                return "&experienceRanges=1~3"
            elif experience_id == "3-5":
                return "&experienceRanges=3~5"
            elif experience_id == "5-7":
                return "&experienceRanges=5~7"
            elif experience_id == "7-10":
                return "&experienceRanges=7~10"
            elif experience_id == "10+":
                return "&experienceRanges=10~50"
        
        elif portal_name == "Naukri":
            if experience_id == "fresher":
                return "0"
            elif experience_id == "0-1":
                return "0-1"
            elif experience_id == "1-3":
                return "1-3"
            elif experience_id == "3-5":
                return "3-5"
            elif experience_id == "5-7":
                return "5-7"
            elif experience_id == "7-10":
                return "7-10"
            elif experience_id == "10+":
                return "10-50"
        
        elif portal_name == "LinkedIn":
            if experience_id == "fresher" or experience_id == "0-1":
                return "1"  # Entry level
            elif experience_id == "1-3" or experience_id == "3-5":
                return "2"  # Associate
            elif experience_id == "5-7" or experience_id == "7-10":
                return "3"  # Mid-Senior level
            elif experience_id == "10+":
                return "4"  # Director
        
        elif portal_name == "Indeed":
            if experience_id == "fresher" or experience_id == "0-1":
                return "entry_level"
            elif experience_id == "1-3" or experience_id == "3-5":
                return "mid_level"
            elif experience_id == "5-7" or experience_id == "7-10" or experience_id == "10+":
                return "senior_level"
        
        return ""

    def search_jobs(self, job_title, location, experience=None):
        """Search jobs across multiple portals"""
        if not experience:
            experience = {"id": "all", "text": "All Levels"}
        
        results = []
        
        for portal in self.portals:
            portal_name = portal["name"]
            
            # Format job title based on portal
            if portal_name == "Foundit (Monster)":
                formatted_job = job_title.replace(' ', '+')
            elif portal_name == "Naukri":
                formatted_job = self.format_job_title(job_title)
            elif portal_name == "Glassdoor":
                # For Glassdoor, format job title with + signs
                formatted_job = job_title.replace(' ', '+')
            elif portal_name in ["LinkedIn", "Indeed", "TimesJobs"]:
                formatted_job = job_title.replace(' ', '%20')
            elif portal_name in ["FreshersWorld", "Instahyre"]:
                formatted_job = job_title.lower().replace(' ', '-')
            else:
                formatted_job = job_title
            
            # Format location based on portal
            if portal_name == "Foundit (Monster)":
                formatted_location = location.replace(' ', '+') if location else "India"
            elif portal_name == "Naukri":
                formatted_location = self.format_location(location) if location else "india"
            elif portal_name == "Glassdoor":
                # For Glassdoor, keep spaces in location name
                formatted_location = location if location else "India"
            elif portal_name in ["LinkedIn", "Indeed", "TimesJobs"]:
                formatted_location = location.replace(' ', '%20') if location else "India"
            elif portal_name in ["FreshersWorld", "Instahyre"]:
                formatted_location = location.lower().replace(' ', '-') if location else "india"
            else:
                formatted_location = location if location else "India"
            
            # Get experience parameter
            exp_param = self.get_experience_param(portal_name, experience)
            
            # Build URL based on portal
            try:
                if portal_name == "Foundit (Monster)":
                    url = portal["url"].format(formatted_job, formatted_location)
                    if exp_param:
                        url += exp_param
                elif portal_name == "Naukri":
                    url = portal["url"].format(formatted_job, formatted_location, exp_param)
                elif portal_name == "LinkedIn":
                    url = portal["url"].format(formatted_job, formatted_location, exp_param)
                elif portal_name == "Indeed":
                    url = portal["url"].format(formatted_job, formatted_location, exp_param)
                elif portal_name == "Glassdoor":
                    # For Glassdoor, location comes first, then job title (occ parameter)
                    url = portal["url"].format(formatted_location, formatted_job)
                elif portal_name in ["TimesJobs"]:
                    url = portal["url"].format(formatted_job, formatted_location)
                elif portal_name in ["FreshersWorld", "Instahyre"]:
                    url = portal["url"].format(formatted_job, formatted_location)
                else:
                    url = portal["url"]
                
                results.append({
                    "portal": portal_name,
                    "icon": portal["icon"],
                    "color": portal["color"],
                    "title": f"{job_title} jobs in {location if location else 'India'}",
                    "url": url
                })
            except Exception as e:
                print(f"Error creating URL for {portal_name}: {str(e)}")
                continue
        
        return results