"""Transparent starter career-market explorer. Does not scrape job sites."""
from urllib.parse import quote_plus

MARKET_SKILLS = {
    "AI / Machine Learning Engineer": ["Python", "Statistics", "Linear Algebra", "Machine Learning", "Data Preprocessing", "Model Evaluation", "Git", "SQL"],
    "Software Developer": ["Programming Fundamentals", "Data Structures", "Algorithms", "Git", "Debugging", "Testing", "APIs"],
    "Data Analyst": ["Excel", "SQL", "Python", "Statistics", "Data Cleaning", "Data Visualization", "Communication", "Power BI"],
    "Cybersecurity Analyst": ["Networking", "Linux", "Security Fundamentals", "Log Analysis", "Risk Assessment", "Incident Response", "SIEM"],
    "Web Developer": ["HTML", "CSS", "JavaScript", "Responsive Design", "Git", "APIs", "Debugging", "Accessibility"],
}

def get_market_profile(career: str) -> dict:
    """Return illustrative role skills; these are not live vacancy statistics."""
    return {"career": career, "skills": MARKET_SKILLS.get(career, [])}

def build_job_search_links(career: str) -> dict[str, str]:
    query = quote_plus(career)
    return {
        "LinkedIn Jobs ↗": f"https://www.linkedin.com/jobs/search/?keywords={query}",
        "Indeed ↗": f"https://www.indeed.com/jobs?q={query}",
        "Google Jobs search ↗": f"https://www.google.com/search?q={query}+jobs&ibp=htl;jobs",
    }
