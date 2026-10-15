"""Keyword-based skill extraction and comparison for MIHNA AI Step 4."""
import re

# Explicit vocabulary for transparent prototype matching. Add terms as needed.
SKILL_PATTERNS = {
    "HTML": [r"\bhtml5?\b"],
    "CSS": [r"\bcss3?\b", r"cascading style sheets"],
    "JavaScript": [r"\bjavascript\b", r"\bjs\b"],
    "TypeScript": [r"\btypescript\b"],
    "React": [r"\breact(?:\.js)?\b"],
    "Node.js": [r"\bnode(?:\.js)?\b"],
    "Python": [r"\bpython\b"],
    "Java": [r"\bjava\b"],
    "C++": [r"\bc\+\+\b"],
    "C#": [r"\bc#\b", r"\bc-sharp\b"],
    "SQL": [r"\bsql\b", r"structured query language"],
    "Excel": [r"\bexcel\b", r"microsoft excel"],
    "Power BI": [r"\bpower\s?bi\b"],
    "Tableau": [r"\btableau\b"],
    "Git": [r"\bgit\b", r"\bgithub\b", r"\bgitlab\b"],
    "APIs": [r"\bapis?\b", r"application programming interface"],
    "REST": [r"\brest(?:ful)?\b"],
    "Debugging": [r"\bdebug(?:ging|ger)?\b"],
    "Testing": [r"\btesting\b", r"unit tests?", r"automated tests?"],
    "Responsive Design": [r"responsive design", r"mobile[- ]first"],
    "Accessibility": [r"accessibility", r"\bwcag\b", r"accessible web"],
    "Data Analysis": [r"data analysis", r"analy[sz]e data", r"data analytics"],
    "Data Visualization": [r"data visuali[sz]ation", r"visuali[sz]ation tools"],
    "Statistics": [r"\bstatistics\b", r"statistical analysis"],
    "Machine Learning": [r"machine learning", r"\bml models?\b"],
    "Deep Learning": [r"deep learning"],
    "Data Cleaning": [r"data cleaning", r"data cleansing", r"cleaning data"],
    "Linux": [r"\blinux\b"],
    "Networking": [r"\bnetworking\b", r"tcp/ip", r"network protocols"],
    "Cybersecurity": [r"cybersecurity", r"cyber security", r"information security"],
    "Incident Response": [r"incident response"],
    "SIEM": [r"\bsiem\b", r"security information and event management"],
    "Cloud Computing": [r"cloud computing", r"\baws\b", r"\bazure\b", r"\bgcp\b"],
    "Docker": [r"\bdocker\b", r"containeri[sz]ation"],
    "Kubernetes": [r"\bkubernetes\b", r"\bk8s\b"],
    "Communication": [r"communication skills", r"communicate effectively"],
    "Problem Solving": [r"problem[- ]solving", r"analytical thinking"],
    "Project Management": [r"project management", r"manage projects"],
    "Agile": [r"\bagile\b", r"\bscrum\b"],
    "Documentation": [r"documentation", r"technical writing"],
    "Data Structures": [r"data structures"],
    "Algorithms": [r"\balgorithms?\b"],
    "Figma": [r"\bfigma\b"],
    "UI/UX Design": [r"ui/ux", r"user experience", r"user interface design"],
}

def extract_skills(text: str) -> list[str]:
    """Return vocabulary terms found in text, preserving dictionary order."""
    content = text.lower()
    found = []
    for skill, patterns in SKILL_PATTERNS.items():
        if any(re.search(pattern, content, flags=re.IGNORECASE) for pattern in patterns):
            found.append(skill)
    return found

def compare_skills(user_skills: str, job_skills: list[str]) -> dict[str, list[str]]:
    """Compare recognized terms in the user's self-reported skill text."""
    owned = set(extract_skills(user_skills))
    matched = [skill for skill in job_skills if skill in owned]
    missing = [skill for skill in job_skills if skill not in owned]
    return {"matched": matched, "missing": missing}
