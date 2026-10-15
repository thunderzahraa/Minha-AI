"""Rule-based career analysis engine for the MIHNA AI prototype.

This module intentionally uses transparent, manually defined starter frameworks.
It does not claim to measure proficiency or predict hiring outcomes.
"""
from __future__ import annotations
import re
from typing import Any

CAREER_SKILLS: dict[str, list[str]] = {
    "AI / Machine Learning Engineer": ["Python", "Statistics", "Linear Algebra", "Machine Learning", "Data Preprocessing", "Model Evaluation", "Git"],
    "Software Developer": ["Programming Fundamentals", "Python", "Data Structures", "Algorithms", "Git", "Debugging", "Testing"],
    "Data Analyst": ["Excel", "SQL", "Python", "Statistics", "Data Cleaning", "Data Visualization", "Communication"],
    "Cybersecurity Analyst": ["Networking", "Linux", "Security Fundamentals", "Log Analysis", "Risk Assessment", "Python", "Incident Response"],
    "Web Developer": ["HTML", "CSS", "JavaScript", "Responsive Design", "Git", "APIs", "Debugging"],
}

# Common ways people describe the same skill. Keep this deliberately explicit.
ALIASES = {
    "ml": "machine learning", "machine learning models": "machine learning",
    "js": "javascript", "html5": "html", "css3": "css",
    "github": "git", "git and github": "git", "version control": "git",
    "data visualisation": "data visualization", "data viz": "data visualization",
    "data visualization tools": "data visualization", "power bi": "data visualization",
    "cyber security": "security fundamentals", "cybersecurity basics": "security fundamentals",
    "networking fundamentals": "networking", "computer networks": "networking",
    "communication skills": "communication", "dsa": "data structures",
    "data structures and algorithms": "data structures", "problem solving": "algorithms",
    "problem-solving": "algorithms", "unit testing": "testing", "software testing": "testing",
    "data cleaning and preprocessing": "data cleaning", "data wrangling": "data cleaning",
    "linear algebra basics": "linear algebra", "statistics and probability": "statistics",
    "rest api": "apis", "rest apis": "apis", "api integration": "apis",
    "incident handling": "incident response", "security logs": "log analysis",
    "linux basics": "linux", "spreadsheets": "excel", "microsoft excel": "excel",
    "python programming": "python", "debugging skills": "debugging",
}

SKILL_DETAILS: dict[str, dict[str, str]] = {
    "Python": {"why": "It is widely used for automation, scripting, data work, and many technical workflows.", "evidence": "A small, readable program with input validation and a README."},
    "Statistics": {"why": "It helps you interpret data and judge whether a result is meaningful.", "evidence": "A short analysis explaining averages, variation, and uncertainty."},
    "Linear Algebra": {"why": "Vectors and matrices are foundational concepts behind many machine-learning methods.", "evidence": "A notebook demonstrating vector and matrix operations."},
    "Machine Learning": {"why": "You need to understand how models learn patterns and where they can fail.", "evidence": "A baseline model compared with a simple alternative."},
    "Data Preprocessing": {"why": "Real datasets often contain missing, duplicated, or inconsistent values.", "evidence": "A reproducible cleaning notebook with before-and-after checks."},
    "Model Evaluation": {"why": "Evaluation helps reveal errors and prevents relying on accuracy alone when it is unsuitable.", "evidence": "A test-set report with appropriate metrics and limitations."},
    "Programming Fundamentals": {"why": "Control flow, functions, and modular code make programs easier to build and maintain.", "evidence": "A small application split into clear functions."},
    "Data Structures": {"why": "Choosing suitable structures can make code clearer and more efficient.", "evidence": "A simple implementation and explanation of a list, stack, or queue."},
    "Algorithms": {"why": "Algorithmic thinking helps you solve problems systematically and reason about efficiency.", "evidence": "A searching or sorting solution with a brief complexity explanation."},
    "Git": {"why": "Version control records changes and makes collaboration and recovery easier.", "evidence": "A repository with meaningful commits and a useful README."},
    "Debugging": {"why": "Systematic debugging helps isolate causes rather than guessing at fixes.", "evidence": "A documented bug report showing reproduction, cause, and fix."},
    "Testing": {"why": "Tests check expected behaviour and reduce regressions when code changes.", "evidence": "Unit tests for normal, boundary, and invalid inputs."},
    "Excel": {"why": "Spreadsheet analysis remains useful for quick exploration, summaries, and reporting.", "evidence": "A workbook using formulas, filters, and a pivot table."},
    "SQL": {"why": "SQL is used to retrieve, combine, and summarize structured data.", "evidence": "Queries demonstrating filtering, grouping, and joins."},
    "Data Cleaning": {"why": "Data quality problems can distort the conclusions drawn from an analysis.", "evidence": "A cleaning log showing how missing values and duplicates were handled."},
    "Data Visualization": {"why": "Clear charts help people understand patterns and make decisions from data.", "evidence": "A dashboard with a clear question, labelled charts, and concise findings."},
    "Communication": {"why": "Technical findings are more useful when you can explain them to other people.", "evidence": "A one-page summary written for a non-technical audience."},
    "Networking": {"why": "Understanding protocols, ports, DNS, and traffic supports security analysis.", "evidence": "A diagram explaining a basic request flow and common ports."},
    "Linux": {"why": "Linux command-line skills are useful for inspecting systems, processes, permissions, and logs.", "evidence": "A short command reference and safe lab notes."},
    "Security Fundamentals": {"why": "Core security concepts help you reason about confidentiality, integrity, availability, and access.", "evidence": "A short threat model using a simple example system."},
    "Log Analysis": {"why": "Logs provide evidence for understanding system events and investigating anomalies.", "evidence": "A script or worksheet summarising a clearly labelled sample log."},
    "Risk Assessment": {"why": "A structured risk assessment makes assumptions, likelihood, and impact visible.", "evidence": "A small risk register with justified likelihood and impact ratings."},
    "Incident Response": {"why": "A consistent response process helps document, contain, and learn from security incidents.", "evidence": "A tabletop incident timeline with decisions and lessons learned."},
    "HTML": {"why": "Semantic HTML provides the structure and meaning of a web page.", "evidence": "An accessible page using headings, landmarks, links, and forms."},
    "CSS": {"why": "CSS controls layout, visual hierarchy, and presentation across screen sizes.", "evidence": "A styled page with consistent spacing and reusable styles."},
    "JavaScript": {"why": "JavaScript adds interaction and behaviour to web interfaces.", "evidence": "A small interaction with sensible handling of user input."},
    "Responsive Design": {"why": "Responsive layouts make interfaces usable across mobile, tablet, and desktop screens.", "evidence": "Screenshots or checks at narrow and wide viewport sizes."},
    "APIs": {"why": "APIs let applications exchange data with other services.", "evidence": "A small client that handles success, empty responses, and errors."},
}

ROADMAP_ACTIONS = {
    "AI / Machine Learning Engineer": {
        "Python": "Build a small Python utility using functions, loops, collections, and input validation.",
        "Statistics": "Explore a small dataset and explain averages, spread, and basic probability in plain language.",
        "Linear Algebra": "Practise vectors, matrices, and matrix multiplication in a short notebook.",
        "Machine Learning": "Train a beginner scikit-learn model and compare it with a simple baseline.",
        "Data Preprocessing": "Clean missing values and duplicates, documenting each decision.",
        "Model Evaluation": "Evaluate on held-out data and explain why you chose each metric.",
        "Git": "Publish a project repository with meaningful commits and a setup guide.",
    },
    "Software Developer": {
        "Programming Fundamentals": "Practise functions, conditions, loops, modules, and input validation.",
        "Python": "Build a command-line application that solves one small everyday problem.",
        "Data Structures": "Implement a list-based stack or queue and test its operations.",
        "Algorithms": "Solve a beginner searching or sorting problem and explain its time complexity.",
        "Git": "Track your project with meaningful commits and a README.",
        "Debugging": "Reproduce a bug, isolate its cause, fix it, and document the result.",
        "Testing": "Write tests for normal cases, edge cases, and invalid input.",
    },
    "Data Analyst": {
        "Excel": "Explore a spreadsheet using formulas, filters, and a pivot table.",
        "SQL": "Practise SELECT, WHERE, GROUP BY, JOIN, and aggregate queries on sample data.",
        "Python": "Use pandas to inspect and analyse a small CSV dataset.",
        "Statistics": "Calculate summary statistics and explain what they do and do not show.",
        "Data Cleaning": "Handle missing values, duplicates, and inconsistent formats, recording your choices.",
        "Data Visualization": "Build charts that answer specific questions and label them clearly.",
        "Communication": "Write a one-page insight report with findings, caveats, and next questions.",
    },
    "Cybersecurity Analyst": {
        "Networking": "Learn IP addresses, ports, DNS, HTTP, and TCP using diagrams or a safe lab.",
        "Linux": "Practise commands, permissions, processes, and log inspection in a local environment.",
        "Security Fundamentals": "Study the CIA triad, authentication, authorization, and least privilege.",
        "Log Analysis": "Inspect clearly labelled sample logs and explain any patterns you notice.",
        "Risk Assessment": "Create a small likelihood-and-impact risk matrix for a fictional system.",
        "Python": "Write a script that summarises a provided sample log file.",
        "Incident Response": "Document a simulated incident timeline, decisions, and lessons learned.",
    },
    "Web Developer": {
        "HTML": "Build a semantic page with headings, navigation, links, and an accessible form.",
        "CSS": "Create a polished layout with spacing, grid or flexbox, and responsive rules.",
        "JavaScript": "Add one useful interactive feature and validate user input.",
        "Responsive Design": "Test your page at mobile, tablet, and desktop widths and fix overflow.",
        "Git": "Track the website in a repository and document how to run it.",
        "APIs": "Fetch and display data from a suitable public API, including error handling.",
        "Debugging": "Use browser developer tools to diagnose and fix a user-interface issue.",
    },
}

PROJECTS = {
    "AI / Machine Learning Engineer": {"title": "Student Performance Predictor", "description": "Train and evaluate a simple model on a public or synthetic dataset. Avoid using it to make real decisions about students.", "deliverables": ["Documented dataset and cleaning steps", "Baseline and evaluation metrics", "README explaining limitations and responsible use"]},
    "Software Developer": {"title": "Personal Task Manager", "description": "Build an application that creates, edits, completes, and filters tasks.", "deliverables": ["Working create/read/update/delete flow", "Input validation and useful error messages", "Unit tests and a clear README"]},
    "Data Analyst": {"title": "Insight Dashboard", "description": "Analyse a public or synthetic CSV dataset and communicate three useful findings.", "deliverables": ["Documented cleaning steps", "Charts or an interactive dashboard", "One-page insight report with limitations"]},
    "Cybersecurity Analyst": {"title": "Security Log Explorer", "description": "Use safe sample logs to summarise event types and flag unusual patterns.", "deliverables": ["Parser or analysis script", "Transparent detection rules", "Report discussing false positives and scope"]},
    "Web Developer": {"title": "Responsive Portfolio", "description": "Create a responsive portfolio with projects, an about section, and contact links.", "deliverables": ["Mobile-friendly and accessible layout", "Project pages with clear evidence", "Deployment instructions"]},
}


def normalize_skill(skill: str) -> str:
    value = re.sub(r"[^a-z0-9+#. ]+", " ", (skill or "").lower())
    value = re.sub(r"\s+", " ", value).strip()
    return ALIASES.get(value, value)


def parse_skills(skills_text: str | list[str] | None) -> list[str]:
    if isinstance(skills_text, list):
        raw = skills_text
    else:
        raw = re.split(r"[,;\n|]", skills_text or "")
    found: list[str] = []
    seen: set[str] = set()
    for item in raw:
        original = re.sub(r"\s+", " ", str(item).strip())
        if not original:
            continue
        key = normalize_skill(original)
        if key and key not in seen:
            seen.add(key)
            found.append(original)
    return found


def analyse_skills(career: str, skills_text: str | list[str] | None) -> dict[str, Any]:
    required = CAREER_SKILLS.get(career)
    if required is None:
        raise ValueError(f"No skill framework configured for: {career}")
    entered = parse_skills(skills_text)
    normalized_entered = {normalize_skill(s) for s in entered}
    matched = [s for s in required if normalize_skill(s) in normalized_entered]
    missing = [s for s in required if normalize_skill(s) not in normalized_entered]
    score = round(len(matched) / len(required) * 100) if required else 0
    strengths = [{"skill": s, "why": SKILL_DETAILS.get(s, {}).get("why", "This is included in the starter framework for your selected role."), "evidence": SKILL_DETAILS.get(s, {}).get("evidence", "Create a small practical example and document what you learned.")} for s in matched]
    gaps = [{"skill": s, "why": SKILL_DETAILS.get(s, {}).get("why", "This is included in the starter framework for your selected role."), "evidence": SKILL_DETAILS.get(s, {}).get("evidence", "Create a small practical example and document what you learned.")} for s in missing]
    return {"career": career, "entered": entered, "matched": matched, "missing": missing,
            "strengths": strengths, "gaps": gaps, "required_count": len(required),
            "matched_count": len(matched), "gap_count": len(missing),
            "checklist_match": score,
            "interpretation": _interpret_score(score),
            "disclaimer": "Checklist coverage only. It does not assess skill depth, employability, or hiring probability."}


def _interpret_score(score: int) -> str:
    if score == 100:
        return "You listed every skill in this starter checklist. Your next step is to demonstrate them with practical evidence."
    if score >= 70:
        return "Your listed skills cover much of this starter checklist. Prioritise the remaining gaps and build evidence for your strongest skills."
    if score >= 40:
        return "You have a starting foundation in this checklist. Choose one or two gaps to work on first instead of trying to learn everything at once."
    return "Treat this as an initial map, not a verdict. Start with foundational skills and build confidence through small, practical exercises."


def build_roadmap(career: str, missing_skills: list[str], weekly_time: str = "4–6 hours") -> list[dict[str, str]]:
    actions = ROADMAP_ACTIONS.get(career, {})
    # Limit the initial plan so it is actionable rather than overwhelming.
    count = {"1–3 hours": 2, "4–6 hours": 3, "7–10 hours": 4, "10+ hours": 5}.get(weekly_time, 3)
    result = []
    for index, skill in enumerate(missing_skills[:count], start=1):
        result.append({"skill": skill, "action": actions.get(skill, f"Learn the fundamentals of {skill} and practise with a small exercise."),
                       "duration": "1 week", "outcome": SKILL_DETAILS.get(skill, {}).get("evidence", "Create a small practical example and document what you learned.")})
    return result


def get_project(career: str) -> dict[str, Any]:
    project = PROJECTS.get(career)
    if project:
        return {"title": project["title"], "description": project["description"], "deliverables": list(project["deliverables"])}
    return {"title": "Career Starter Project", "description": "Create a small practical project related to your target role.", "deliverables": ["Working prototype", "Documentation", "Reflection on limitations"]}
