import streamlit as st
from typing import List, Dict
from .job_portals import JobPortal
from .suggestions import (
    JOB_SUGGESTIONS, 
    LOCATION_SUGGESTIONS, 
    EXPERIENCE_RANGES,
    SALARY_RANGES,
    JOB_TYPES,
    get_cities_by_state,
    get_all_states
)
from .companies import get_featured_companies, get_market_insights
from .linkedin_scraper import render_linkedin_scraper
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_option_menu import option_menu

def filter_suggestions(query: str, suggestions: List[Dict]) -> List[Dict]:
    """Filter suggestions based on user input"""
    if not query:
        return []
    return [
        s for s in suggestions 
        if query.lower() in s["text"].lower()
    ][:5]

def filter_location_suggestions(query: str, suggestions: List[Dict]) -> List[Dict]:
    """Filter location suggestions based on user input with smart categorization"""
    if not query or len(query) < 2:
        return []
        
    # First check if query matches any state
    matching_states = [s for s in suggestions if s.get("type") == "state" and query.lower() in s["text"].lower()]
    
    # Then check cities
    matching_cities = [s for s in suggestions if s.get("type") == "city" and query.lower() in s["text"].lower()]
    
    # Then check work modes
    matching_work_modes = [s for s in suggestions if s.get("type") == "work_mode" and query.lower() in s["text"].lower()]
    
    # Combine results with states first, then major cities, then other matches
    results = matching_states + matching_cities + matching_work_modes
    return results[:7]  # Return top 7 matches

def get_filter_options():
    """Get filter options for job search"""
    return {
        "experience_levels": [
            {"id": "all", "text": "All Levels"},
            {"id": "fresher", "text": "Fresher"},
            {"id": "0-1", "text": "0-1 years"},
            {"id": "1-3", "text": "1-3 years"},
            {"id": "3-5", "text": "3-5 years"},
            {"id": "5-7", "text": "5-7 years"},
            {"id": "7-10", "text": "7-10 years"},
            {"id": "10+", "text": "10+ years"}
        ],
        "salary_ranges": [
            {"id": "all", "text": "All Ranges"},
            {"id": "0-3", "text": "0-3 LPA"},
            {"id": "3-6", "text": "3-6 LPA"},
            {"id": "6-10", "text": "6-10 LPA"},
            {"id": "10-15", "text": "10-15 LPA"},
            {"id": "15+", "text": "15+ LPA"}
        ],
        "job_types": [
            {"id": "all", "text": "All Types"},
            {"id": "full-time", "text": "Full Time"},
            {"id": "part-time", "text": "Part Time"},
            {"id": "contract", "text": "Contract"},
            {"id": "remote", "text": "Remote"}
        ]
    }

def render_company_section():
    """Render the featured companies section"""
    st.markdown("""
        <style>
        .company-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
            gap: 1rem;
            padding: 1rem 0;
        }
        .company-card {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 10px;
            padding: 1rem;
            transition: transform 0.2s;
            cursor: pointer;
        }
        .company-card:hover {
            transform: translateY(-5px);
            background: rgba(255, 255, 255, 0.08);
        }
        .company-header {
            display: flex;
            align-items: center;
            margin-bottom: 0.5rem;
        }
        .company-icon {
            font-size: 1.5rem;
            margin-right: 0.5rem;
        }
        .company-categories {
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
            margin-top: 0.5rem;
        }
        .company-category {
            background: rgba(255, 255, 255, 0.1);
            padding: 0.2rem 0.5rem;
            border-radius: 15px;
            font-size: 0.8rem;
        }
        </style>
    """, unsafe_allow_html=True)

    # Featured Companies
    st.markdown("### 🏢 Featured Companies")
    
    tabs = st.tabs(["All Companies", "Tech Giants", "Indian Tech", "Global Corps"])
    
    categories = [None, "tech", "indian_tech", "global_corps"]
    for tab, category in zip(tabs, categories):
        with tab:
            companies = get_featured_companies(category)
            st.markdown('<div class="company-grid">', unsafe_allow_html=True)
            
            for company in companies:
                st.markdown(f"""
                    <a href="{company['careers_url']}" target="_blank" style="text-decoration: none; color: inherit;">
                        <div class="company-card">
                            <div class="company-header">
                                <i class="{company['icon']} company-icon" style="color: {company['color']}"></i>
                                <h3 style="margin: 0;">{company['name']}</h3>
                            </div>
                            <p style="margin: 0.5rem 0; color: #888;">{company['description']}</p>
                            <div class="company-categories">
                                {' '.join(f'<span class="company-category">{cat}</span>' for cat in company['categories'])}
                            </div>
                        </div>
                    </a>
                """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)

def render_market_insights():
    """Render job market insights section"""
    insights = get_market_insights()
    
    st.markdown("""
        <style>
        .insights-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 1rem;
            padding: 1rem 0;
        }
        .insight-card {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 10px;
            padding: 1rem;
            text-align: center;
            transition: transform 0.3s ease, background 0.3s ease;
        }
        .insight-card:hover {
            transform: translateY(-5px);
            background: rgba(255, 255, 255, 0.08);
        }
        .insight-icon {
            font-size: 2rem;
            margin-bottom: 0.5rem;
            color: #00bfa5;
        }
        .growth-text {
            color: #00c853;
            font-weight: bold;
        }
        .salary-card {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 15px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            transition: all 0.3s ease;
            border-left: 4px solid #00bfa5;
        }
        .salary-card:hover {
            transform: translateX(10px);
            background: rgba(255, 255, 255, 0.08);
        }
        .salary-header {
            display: flex;
            align-items: center;
            margin-bottom: 1rem;
        }
        .role-icon {
            font-size: 1.5rem;
            margin-right: 1rem;
            color: #00bfa5;
        }
        .salary-details {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 0.5rem;
        }
        .salary-tag {
            background: rgba(0, 191, 165, 0.1);
            color: #00bfa5;
            padding: 0.3rem 0.8rem;
            border-radius: 20px;
            font-size: 0.9rem;
        }
        .experience-tag {
            background: rgba(255, 255, 255, 0.1);
            padding: 0.3rem 0.8rem;
            border-radius: 20px;
            font-size: 0.9rem;
        }
        .role-title {
            font-size: 1.2rem;
            font-weight: bold;
            margin: 0;
        }
        .salary-range {
            font-size: 1.1rem;
            color: #00bfa5;
            font-weight: bold;
        }
        .role-icons {
            font-family: "Font Awesome 5 Free";
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("### 📊 Job Market Insights")
    
    tabs = st.tabs(["Trending Skills", "Top Locations", "Salary Insights"])
    
    with tabs[0]:
        st.markdown('<div class="insights-grid">', unsafe_allow_html=True)
        for skill in insights["trending_skills"]:
            st.markdown(f"""
                <div class="insight-card">
                    <i class="{skill['icon']} insight-icon"></i>
                    <h4>{skill['name']}</h4>
                    <p class="growth-text">Growth: {skill['growth']}</p>
                </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tabs[1]:
        st.markdown('<div class="insights-grid">', unsafe_allow_html=True)
        for location in insights["top_locations"]:
            st.markdown(f"""
                <div class="insight-card">
                    <i class="{location['icon']} insight-icon"></i>
                    <h4>{location['name']}</h4>
                    <p>Available Jobs: {location['jobs']}</p>
                </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tabs[2]:
        # Role-specific icons
        role_icons = {
            "Software Engineer": "fas fa-code",
            "Data Scientist": "fas fa-brain",
            "Product Manager": "fas fa-tasks",
            "DevOps Engineer": "fas fa-server",
            "UI/UX Designer": "fas fa-paint-brush"
        }
        
        for insight in insights["salary_insights"]:
            role = insight['role']
            icon = role_icons.get(role, "fas fa-briefcase")
            
            st.markdown(f"""
                <div class="salary-card">
                    <div class="salary-header">
                        <i class="{icon} role-icon"></i>
                        <div>
                            <h3 class="role-title">{role}</h3>
                            <div class="salary-details">
                                <span class="salary-tag">₹ {insight['range']}</span>
                                <span class="experience-tag">
                                    <i class="fas fa-history"></i> {insight['experience']}
                                </span>
                            </div>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

def render_job_search():
    """Render job search page with enhanced features"""
    st.title("🔍 Smart Job Search")
    st.markdown("Find Your Dream Job Across Multiple Platforms")
    
    # Market Insights Section (Above Search)
    render_market_insights()
    
    # Job Search Section
    with st.container():
        st.markdown("""
            <style>
            .search-container {
                background: rgba(255, 255, 255, 0.05);
                border-radius: 10px;
                padding: 20px;
                margin-bottom: 20px;
            }
            .search-title {
                color: #00bfa5;
                font-weight: bold;
                margin-bottom: 5px;
            }
            .search-description {
                color: #888;
                font-size: 0.9rem;
                margin-bottom: 20px;
            }
            </style>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="search-container">', unsafe_allow_html=True)
        
        # Create tabs with icons
        tabs = option_menu(
            menu_title=None,
            options=["Job Portal", "LinkedIn"],
            icons=["search", "linkedin"],
            menu_icon="cast",
            default_index=0,
            orientation="horizontal",
            styles={
                "container": {"padding": "0px", "margin-bottom": "20px"},
                "icon": {"font-size": "18px"},
                "nav-link": {"font-size": "16px", "text-align": "center", "padding": "10px", "border-radius": "5px"},
                "nav-link-selected": {"background-color": "#00bfa5", "font-weight": "bold"},
            }
        )
        
        # Display content based on selected tab
        if tabs == "Job Portal":
            st.markdown('<h3 class="search-title"><i class="fas fa-search-dollar" style="color: #00bfa5;"></i> Search Jobs Across Multiple Platforms</h3>', unsafe_allow_html=True)
            st.markdown('<p class="search-description">Find job opportunities from top job portals like LinkedIn, Indeed, Naukri, and Foundit</p>', unsafe_allow_html=True)
            
            # Search inputs
            col1, col2 = st.columns([2, 1])
            
            with col1:
                job_query = st.text_input("Job Title / Skills", 
                                        value="", 
                                        placeholder="e.g. Software Engineer, Data Scientist")
                
                if job_query and len(job_query) >= 2:
                    filtered_jobs = [s["text"] for s in JOB_SUGGESTIONS if job_query.lower() in s["text"].lower()]
                    if filtered_jobs:
                        job_query = st.selectbox("Select Job Title", filtered_jobs)
            
            with col2:
                location = st.text_input("Location", 
                                       value="",
                                       placeholder="e.g. Bangalore, Karnataka")
                
                if location and len(location) >= 2:
                    # Use enhanced location filtering
                    filtered_locations = filter_location_suggestions(location, LOCATION_SUGGESTIONS)
                    
                    if filtered_locations:
                        # Format the display text to show location type
                        location_options = []
                        location_display = {}
                        
                        for loc in filtered_locations:
                            display_text = loc["text"]
                            if loc.get("type") == "state":
                                display_text = f"{loc['text']} (State)"
                            elif loc.get("type") == "city":
                                display_text = f"{loc['text']}, {loc.get('state', '')}"
                            elif loc.get("type") == "work_mode":
                                display_text = f"{loc['text']} (Work Mode)"
                                
                            location_options.append(loc["text"])
                            location_display[loc["text"]] = display_text
                        
                        # Create a selectbox with formatted display
                        selected_location = st.selectbox(
                            "Select Location",
                            options=location_options,
                            format_func=lambda x: location_display.get(x, x)
                        )
                        
                        location = selected_location
                        
                        # If a state is selected, show cities in that state
                        selected_loc_type = next((loc.get("type") for loc in filtered_locations if loc["text"] == selected_location), None)
                        
                        if selected_loc_type == "state":
                            st.markdown(f"**Cities in {selected_location}:**")
                            cities = get_cities_by_state(selected_location)
                            
                            # Display cities as clickable buttons
                            city_cols = st.columns(3)
                            for i, city in enumerate(cities):
                                with city_cols[i % 3]:
                                    if st.button(f"{city['icon']} {city['text']}", key=f"city_{i}"):
                                        location = city['text']

            # Advanced Filters
            with st.expander("🎯 Advanced Filters"):
                st.markdown('<div class="filter-section">', unsafe_allow_html=True)
                filter_cols = st.columns(3)
                
                with filter_cols[0]:
                    experience = st.selectbox("Experience Level",
                                            options=get_filter_options()["experience_levels"],
                                            format_func=lambda x: x["text"])
                
                with filter_cols[1]:
                    salary_range = st.selectbox("Salary Range",
                                              options=get_filter_options()["salary_ranges"],
                                              format_func=lambda x: x["text"])
                
                with filter_cols[2]:
                    job_type = st.selectbox("Job Type",
                                          options=get_filter_options()["job_types"],
                                          format_func=lambda x: x["text"])
                
                st.markdown('</div>', unsafe_allow_html=True)

            # Search button
            if st.button("SEARCH JOBS", type="primary", use_container_width=True):
                if job_query:
                    job_portal = JobPortal()
                    results = job_portal.search_jobs(job_query, location, experience)
                    
                    if results:
                        st.markdown("""
                            <style>
                            .result-card {
                                background: rgba(255, 255, 255, 0.05);
                                border-radius: 10px;
                                padding: 15px;
                                margin-bottom: 10px;
                                border-left: 4px solid #00bfa5;
                                transition: transform 0.2s;
                            }
                            .result-card:hover {
                                transform: translateX(5px);
                                background: rgba(255, 255, 255, 0.08);
                            }
                            .portal-name {
                                color: #00bfa5;
                                font-weight: bold;
                                font-size: 1.2rem;
                            }
                            .portal-link {
                                display: inline-block;
                                background: #00bfa5;
                                color: white !important;
                                padding: 5px 15px;
                                border-radius: 5px;
                                text-decoration: none;
                                margin-top: 10px;
                                font-weight: bold;
                            }
                            .portal-link:hover {
                                background: #00a589;
                            }
                            </style>
                        """, unsafe_allow_html=True)
                        
                        st.markdown("### 🎯 Job Search Results")
                        for result in results:
                            with st.container():
                                st.markdown(f"""
                                <div class="result-card">
                                    <div class="portal-name">
                                        <i class="{result["icon"]}" style="color: {result["color"]}"></i>
                                        {result["portal"]}
                                    </div>
                                    <p>{result["title"]}</p>
                                    <a href="{result["url"]}" target="_blank" class="portal-link">
                                        View Jobs on {result["portal"]} →
                                    </a>
                                </div>
                                """, unsafe_allow_html=True)
                    else:
                        st.warning("No results found. Try different search terms or filters.")
                else:
                    st.warning("Please enter a job title or skills to search.")
        
        else:
            # LinkedIn Job Scraper - only show the title once
            st.markdown('<h3 class="search-title"><i class="fab fa-linkedin" style="color: #0A66C2;"></i> LinkedIn Job Scraper</h3>', unsafe_allow_html=True)
            st.markdown('<p class="search-description">Find real-time job listings directly from LinkedIn</p>', unsafe_allow_html=True)
            
            # Render LinkedIn scraper without showing the title again
            render_linkedin_scraper()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Featured Companies Section (Below Search)
    render_company_section()

# Removed render_job_search() call to prevent automatic rendering