"""Transparent, heuristic job requirement classification and tailored next steps."""
import re

# Terms are intentionally explicit; this is a lightweight heuristic, not an NLP model.
REQUIRED = re.compile(r"\b(required|required qualification|required skill|must[- ]have|must|required to|minimum qualifications|you need to|essential|mandatory)\b", re.I)
PREFERRED = re.compile(r"\b(preferred|preferably|nice[- ]to[- ]have|bonus|a plus|desirable|ideally|not required)\b", re.I)
SECTION_REQUIRED = re.compile(r"\b(requirements|what you need|what we're looking for|what we are looking for|qualifications|must have|essential skills)\b", re.I)
SECTION_PREFERRED = re.compile(r"\b(preferred qualifications|preferred skills|nice to have|bonus points|additional skills)\b", re.I)

ACTIONS = {
    "HTML": ("Build a semantic page with headings, navigation, links and an accessible form.", "A small page with clear structure and working links."),
    "CSS": ("Style a page with consistent spacing, flexbox or grid, and responsive rules.", "A screenshot set showing the layout at mobile and desktop widths."),
    "JavaScript": ("Add one interactive feature and validate user input.", "A working interaction with a short explanation of edge cases."),
    "React": ("Build a small component-based interface with props, state and a form or list.", "A running demo with reusable components and a README."),
    "Python": ("Write a small script or app using functions, collections, input validation and clear errors.", "A runnable project with examples and a setup guide."),
    "SQL": ("Practise SELECT, filtering, grouping and JOIN queries on a sample database.", "A query file with comments and sample outputs."),
    "Git": ("Track a small project with meaningful commits and practise branches and merges.", "A repository with useful commit history and a README."),
    "APIs": ("Call a public API and handle success, empty responses and errors.", "A demo that displays API data and explains its error handling."),
    "Responsive Design": ("Test a page at narrow and wide viewport sizes and fix overflow.", "Screenshots or notes showing mobile, tablet and desktop checks."),
    "Testing": ("Write tests for normal inputs, boundary cases and invalid input.", "A test suite with a short note on what each test protects."),
    "Debugging": ("Reproduce a bug, isolate its cause, apply a fix and record the result.", "A concise bug report showing reproduction steps and resolution."),
    "Data Analysis": ("Analyse a small dataset and explain three findings plus limitations.", "A notebook or report with reproducible steps and clear caveats."),
    "Excel": ("Use formulas, filters and a pivot table to answer a practical question.", "A workbook with formulas and a brief findings summary."),
    "Data Visualization": ("Create labelled charts that answer specific questions from a dataset.", "A small dashboard with a clear title and takeaways."),
    "Machine Learning": ("Train a beginner model and compare it with a simple baseline.", "A notebook documenting data split, metrics and limitations."),
    "Communication": ("Explain a technical result in plain language for a non-technical reader.", "A one-page summary with findings and next steps."),
    "Linux": ("Practise file, process, permission and log commands in a safe local environment.", "A command log with explanations and example output."),
    "Networking": ("Learn IP addresses, DNS, ports and HTTP/TCP request flow.", "A diagram explaining one request from client to server."),
    "Cybersecurity": ("Study core security principles and write a simple threat model for a fictional app.", "A short threat model with assets, threats and mitigations."),
}

def _context(text, skill):
    """Return short contexts around mentions, avoiding a claim based on the whole document."""
    patterns = []
    # Reuse the supported skill vocabulary's common spellings where possible.
    aliases = {"JavaScript": r"javascript|\bjs\b", "CSS": r"\bcss3?\b|cascading style sheets", "HTML": r"\bhtml5?\b", "APIs": r"\bapis?\b|application programming interface", "Git": r"\bgit\b|github|gitlab", "Node.js": r"node(?:\.js)?"}
    pat = aliases.get(skill, re.escape(skill))
    for match in re.finditer(pat, text, flags=re.I):
        patterns.append(text[max(0, match.start()-220):min(len(text), match.end()+220)])
    return patterns

def classify_job_skills(description, skills):
    """Classify recognized skills as required/preferred/unclear using nearby wording and headings."""
    text = re.sub(r"\s+", " ", description or "")
    result = {"required": [], "preferred": [], "unclear": []}
    for skill in skills:
        contexts = _context(text, skill)
        classes = []
        for ctx in contexts:
            if PREFERRED.search(ctx) or SECTION_PREFERRED.search(ctx):
                classes.append("preferred")
            elif REQUIRED.search(ctx) or SECTION_REQUIRED.search(ctx):
                classes.append("required")
        # A skill can appear in multiple contexts; keep the strongest explicit signal.
        chosen = "required" if "required" in classes else ("preferred" if "preferred" in classes else "unclear")
        result[chosen].append(skill)
    return result

def build_priority_roadmap(missing_skills, job_title=""):
    """Create practical first steps and portfolio evidence for each missing skill."""
    roadmap = []
    for skill in missing_skills:
        action, evidence = ACTIONS.get(skill, (
            f"Learn the fundamentals of {skill}, complete a small guided exercise, then apply it in a mini-project related to {job_title or 'your target role'}.",
            f"A small working example, notes explaining your decisions, and a README describing what you learned about {skill}."
        ))
        roadmap.append({"skill": skill, "priority": "Start here" if len(roadmap) < 2 else "Next", "action": action, "evidence": evidence})
    return roadmap
