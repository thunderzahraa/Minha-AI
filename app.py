import streamlit as st
from html import escape
from career_engine import analyse_skills, build_roadmap, get_project

st.set_page_config(page_title="MIHNA AI — Career Intelligence", page_icon="✳", layout="wide", initial_sidebar_state="collapsed")

st.markdown(r'''<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');
:root{--bg:#101014;--panel:#19191f;--panel2:#202027;--line:#34343d;--ink:#f5f3f8;--muted:#aaa7b5;--lilac:#c2a7ff;--coral:#ff927c;--lime:#c9f27a}
html,body,[class*="css"],[data-testid="stAppViewContainer"]{font-family:'DM Sans',sans-serif}.stApp{background:var(--bg);color:var(--ink)}
[data-testid="stHeader"]{background:rgba(16,16,20,.92)}[data-testid="stMainBlockContainer"]{max-width:1540px;width:100%;padding:2rem clamp(1.25rem,4vw,4rem) 5rem}
h1,h2,h3,h4{font-family:'Manrope',sans-serif!important;color:var(--ink)!important;letter-spacing:-.04em}p,label,li{color:var(--muted)}a{color:var(--lilac)!important}
.topbar{display:flex;justify-content:space-between;align-items:center;gap:1.5rem;min-height:88px;padding:1.15rem 0 1.45rem;border-bottom:1px solid var(--line);margin-bottom:2.5rem}.wordmark{font-family:'Manrope',sans-serif;font-size:clamp(1.45rem,2.2vw,2rem);font-weight:800;letter-spacing:-.05em;color:var(--ink);white-space:nowrap}.wordmark span{color:var(--lilac)}.topnote{color:var(--muted);font-size:.9rem;letter-spacing:.08em;text-align:right}
.hero{border:1px solid var(--line);border-radius:30px;padding:clamp(2rem,5vw,5rem);background:radial-gradient(circle at 88% 12%,rgba(194,167,255,.18),transparent 28%),radial-gradient(circle at 10% 100%,rgba(255,146,124,.10),transparent 34%),linear-gradient(135deg,#1b1a22,#141419 72%);margin-bottom:1.5rem;overflow:hidden}
.eyebrow,.section-kicker{color:var(--lilac);font-size:.75rem;font-weight:700;letter-spacing:.15em;text-transform:uppercase}.hero h1{font-size:clamp(3rem,7.2vw,6.5rem);line-height:1.02;max-width:1120px;margin:.9rem 0 1.1rem}.hero h1 em{color:var(--lilac);font-style:normal}.hero-copy{font-size:1.12rem;line-height:1.9;max-width:760px;color:#c2bfcb}.hero-bottom{display:flex;gap:.65rem;flex-wrap:wrap;margin-top:1.6rem}.pill{border:1px solid #494451;border-radius:999px;padding:.45rem .8rem;color:#ded8e9;font-size:.8rem}
.section-title{font-size:clamp(1.8rem,4vw,2.8rem);margin:.3rem 0 .4rem}.section-copy{color:var(--muted);margin-bottom:1.2rem}.feature-card,.metric-card,.roadmap-card,.project-card{background:var(--panel);border:1px solid var(--line);border-radius:22px;padding:1.65rem}.feature-number,.step{color:var(--coral);font-size:.75rem;font-weight:800;letter-spacing:.12em;text-transform:uppercase}.feature-card h3{font-size:1.12rem;margin:.65rem 0 .4rem}.feature-card p{font-size:.9rem;line-height:1.65;margin-bottom:0}.metric-card{min-height:130px}.metric-label{color:var(--muted);font-size:.83rem}.metric-value{font-family:'Manrope',sans-serif;color:var(--lilac);font-size:2.2rem;font-weight:800;letter-spacing:-.05em;margin-top:.35rem}.skill-chip,.gap-chip{display:inline-block;padding:.4rem .7rem;border-radius:999px;margin:.2rem .25rem .2rem 0;font-size:.82rem}.skill-chip{border:1px solid #514768;background:#292433;color:#e8ddff}.gap-chip{border:1px solid #63433d;background:#2c211f;color:#ffc0b2}.roadmap-card{margin:.75rem 0;padding:1.8rem}.roadmap-card p{line-height:1.7}.stForm label{color:var(--ink)!important}.stMarkdown p{line-height:1.7}.roadmap-card h4{font-size:1.15rem;margin:.45rem 0}.project-card{background:linear-gradient(135deg,#24202e,#19191f)}.project-card h3{margin:.5rem 0}.tag{display:inline-block;border-radius:8px;padding:.25rem .5rem;color:#16131b;background:var(--lime);font-size:.72rem;font-weight:800}.footer{border-top:1px solid var(--line);margin-top:3rem;padding-top:1.2rem;display:flex;justify-content:space-between;gap:1rem;flex-wrap:wrap;color:#817d8b;font-size:.78rem}
.stTextInput input,.stTextArea textarea,.stSelectbox div[data-baseweb="select"]{background:var(--panel2)!important;color:var(--ink)!important;border-radius:12px!important;border-color:var(--line)!important}.stButton>button,.stFormSubmitButton>button{background:var(--lilac);color:#17131e;border:1px solid var(--lilac);border-radius:12px;font-weight:800;min-height:48px;padding:.65rem 1.2rem;transition:all .2s ease}.stButton>button:hover,.stFormSubmitButton>button:hover{background:var(--coral);border-color:var(--coral);color:#17131e}[data-testid="stProgressBar"]>div>div{background:var(--lilac)}[data-testid="stAlert"]{border-radius:14px}hr{border-color:var(--line)}
@media(min-width:1500px){.hero{min-height:440px}.feature-card{min-height:220px}}
@media(max-width:700px){[data-testid="stMainBlockContainer"]{padding:1rem 1rem 3rem}.topbar{align-items:flex-start;flex-direction:column;gap:.5rem;min-height:auto;padding:1rem 0 1.2rem;margin-bottom:1.5rem}.topnote{text-align:left;font-size:.72rem}.hero{border-radius:20px;padding:1.5rem}.hero h1{font-size:clamp(2.6rem,12vw,4rem)}.feature-card{min-height:0}}
</style>''', unsafe_allow_html=True)

st.markdown('<div class="topbar"><div class="wordmark">✳ MIHNA<span> AI</span></div><div class="topnote">CAREER INTELLIGENCE · BUILT AROUND YOUR NEXT MOVE</div></div>', unsafe_allow_html=True)
st.markdown('''<section class="hero"><div class="eyebrow">Your skills. Your direction. Your next chapter.</div><h1>Make your next move<br>with <em>more clarity.</em></h1><div class="hero-copy">A practical career companion that helps you map your current skills, uncover what to learn next, and turn your ambitions into a plan you can act on.</div><div class="hero-bottom"><span class="pill">01 · Analyse</span><span class="pill">02 · Find the gaps</span><span class="pill">03 · Build your roadmap</span></div></section>''', unsafe_allow_html=True)

st.markdown('<div class="section-kicker">A clearer way forward</div><h2 class="section-title">From unsure to actionable.</h2><p class="section-copy">Start with what you know. Leave with a practical next step.</p>', unsafe_allow_html=True)
cols = st.columns(3)
for col, num, title, desc in zip(cols, ["01", "02", "03"], ["Know your starting point", "See what is missing", "Turn gaps into action"], ["Compare your listed skills with a starter checklist for your target role.", "Understand which skills to explore next without treating a checklist as a hiring verdict.", "Get learning actions and a portfolio project idea tailored to your chosen career."]):
    with col:
        st.markdown(f'<div class="feature-card"><div class="feature-number">{num} / MIHNA</div><h3>{title}</h3><p>{desc}</p></div>', unsafe_allow_html=True)

st.markdown('<div class="section-kicker">Build your profile</div><h2 class="section-title">Let’s map your next move.</h2><p class="section-copy">A few details are enough to create your first career snapshot.</p>', unsafe_allow_html=True)
with st.form("mihna_profile"):
    left, right = st.columns(2)
    with left:
        name = st.text_input("What should we call you?", placeholder="Name or nickname")
        career = st.selectbox("Which career are you working towards?", ["Select a career", "AI / Machine Learning Engineer", "Software Developer", "Data Analyst", "Cybersecurity Analyst", "Web Developer", "Other"])
        education = st.selectbox("Current learning stage", ["Choose your current stage", "School student", "Undergraduate student", "Graduate student", "Recent graduate", "Working professional", "Self-taught learner"])
    with right:
        experience = st.selectbox("Relevant experience", ["Choose your experience level", "Just starting", "Personal projects or coursework", "Internship experience", "Professional experience"])
        weekly_time = st.selectbox("Time you can dedicate each week", ["Choose weekly time", "1–3 hours", "4–6 hours", "7–10 hours", "10+ hours"])
        skills = st.text_area("Skills you already have", placeholder="Example: Python, Excel, communication, Git", height=124)
    submitted = st.form_submit_button("Create my career snapshot  →", use_container_width=True)

if submitted:
    if not name.strip():
        st.warning("Please enter your name or a nickname.")
    elif career == "Select a career":
        st.warning("Please select a career goal.")
    elif education == "Choose your current stage":
        st.warning("Please select your learning stage.")
    elif experience == "Choose your experience level":
        st.warning("Please select your experience level.")
    elif weekly_time == "Choose weekly time":
        st.warning("Please select how much time you can dedicate each week.")
    elif career == "Other":
        st.info("A custom skill framework is not configured for this career yet. Choose one of the listed roles to generate a roadmap.")
    else:
        result = analyse_skills(career, skills)
        matched, missing, score = result["matched"], result["missing"], result["checklist_match"]
        roadmap = build_roadmap(career, missing, weekly_time)
        project = get_project(career)
        st.divider()
        st.markdown('<div class="section-kicker">Your snapshot</div>', unsafe_allow_html=True)
        st.markdown(f'<h2 class="section-title">A starting point for {escape(name.strip())}.</h2><p class="section-copy">Target role: <strong>{escape(career)}</strong> · {escape(education)} · {escape(experience)} · {escape(weekly_time)} weekly</p>', unsafe_allow_html=True)
        metrics = st.columns(3)
        for col, label, value in zip(metrics, ["Checklist match", "Skills matched", "Skills to explore"], [f"{score}%", str(len(matched)), str(len(missing))]):
            with col:
                st.markdown(f'<div class="metric-card"><div class="metric-label">{label}</div><div class="metric-value">{value}</div></div>', unsafe_allow_html=True)
        st.progress(score / 100)
        st.info(result["interpretation"])
        st.caption("This transparent, rule-based checklist compares skills you listed with a starter framework. It does not test proficiency or predict employability or hiring outcomes.")
        a, b = st.columns(2)
        with a:
            st.markdown('<div class="section-kicker">What already matches</div>', unsafe_allow_html=True)
            st.subheader("Skills in your toolkit")
            if matched:
                st.markdown(" ".join(f'<span class="skill-chip">{escape(s)}</span>' for s in matched), unsafe_allow_html=True)
                st.caption("Next, collect evidence for these skills through projects, coursework, or practical exercises.")
            else:
                st.write("No skills matched this starter checklist yet. That is a useful place to begin.")
        with b:
            st.markdown('<div class="section-kicker">Your growth areas</div>', unsafe_allow_html=True)
            st.subheader("Skills to explore")
            if missing:
                st.markdown(" ".join(f'<span class="gap-chip">{escape(s)}</span>' for s in missing), unsafe_allow_html=True)
                with st.expander("Why these skills matter"):
                    for gap in result["gaps"]:
                        st.markdown(f"**{escape(gap['skill'])}** — {escape(gap['why'])}")
                        st.caption(f"Evidence idea: {gap['evidence']}")
            else:
                st.success("You matched every skill in this starter checklist. Next, gather evidence through projects and practical assessments.")
        st.divider()
        st.markdown('<div class="section-kicker">Your next steps</div><h2 class="section-title">A roadmap you can actually use.</h2><p class="section-copy">Work through the skills at a pace that fits your week. Start small and document what you learn.</p>', unsafe_allow_html=True)
        if roadmap:
            for i, item in enumerate(roadmap, 1):
                st.markdown(f'<div class="roadmap-card"><div class="step">WEEK {i:02d} · PRIORITY SKILL</div><h4>{escape(item["skill"])}</h4><p>{escape(item["action"])}</p><p><strong>Evidence to aim for:</strong> {escape(item["outcome"])}</p></div>', unsafe_allow_html=True)
        else:
            st.success("No checklist gaps were detected. Focus on building evidence and testing your skills in a practical project.")
        st.markdown('<div class="section-kicker">Build proof, not just knowledge</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="project-card"><span class="tag">PORTFOLIO PROJECT</span><h3>{escape(project["title"])}</h3><p>{escape(project["description"])}</p><strong>Suggested deliverables</strong></div>', unsafe_allow_html=True)
        for item in project["deliverables"]:
            st.markdown(f"- {item}")
        st.info("Prototype note: this version uses a transparent, manually defined starter checklist—not an external AI model or live job data. Frameworks are illustrative, may not cover every employer, and should be checked against current job descriptions.")

        st.divider()
        st.markdown('<div class="section-kicker">Career market explorer · Step 3</div><h2 class="section-title">Connect your plan to the job market.</h2><p class="section-copy">Use this starter market view to compare your listed skills with a role checklist, then open current job-search pages to inspect real employer requirements.</p>', unsafe_allow_html=True)
        from market_intel import get_market_profile, build_job_search_links
        market = get_market_profile(career)
        market_matched = [skill for skill in market["skills"] if skill.lower() in {x.lower() for x in matched}]
        market_missing = [skill for skill in market["skills"] if skill.lower() not in {x.lower() for x in matched}]
        m1, m2, m3 = st.columns(3)
        with m1:
            st.markdown(f'<div class="metric-card"><div class="metric-label">Starter role skills</div><div class="metric-value">{len(market["skills"])}</div></div>', unsafe_allow_html=True)
        with m2:
            st.markdown(f'<div class="metric-card"><div class="metric-label">Matched in your profile</div><div class="metric-value">{len(market_matched)}</div></div>', unsafe_allow_html=True)
        with m3:
            st.markdown(f'<div class="metric-card"><div class="metric-label">To investigate</div><div class="metric-value">{len(market_missing)}</div></div>', unsafe_allow_html=True)
        st.markdown('**Common skills to look for in job descriptions**')
        st.markdown(" ".join(f'<span class="skill-chip">{escape(skill)}</span>' for skill in market["skills"]), unsafe_allow_html=True)
        if market_missing:
            st.markdown('**Potential gaps to verify against real listings**')
            st.markdown(" ".join(f'<span class="gap-chip">{escape(skill)}</span>' for skill in market_missing), unsafe_allow_html=True)
        st.markdown('**Open current job searches**')
        st.caption('These links open external search pages. Listings, locations, and requirements are controlled by those sites; MIHNA AI does not scrape or verify individual vacancies in this version.')
        job_links = build_job_search_links(career)
        link_cols = st.columns(len(job_links))
        for col, (label, url) in zip(link_cols, job_links.items()):
            with col:
                st.link_button(label, url, use_container_width=True)
        st.caption('Data transparency: the skill list above is a manually defined starter profile for exploration, not a statistical survey of vacancies or a claim about live market demand. Compare several recent listings in your preferred location before deciding what to learn.')



# Step 4 — Compare against a real job description supplied by the user.
from job_compare import extract_skills, compare_skills
st.divider()
st.markdown('<div class="section-kicker">Job requirement comparison · Step 4</div><h2 class="section-title">Compare your skills with a real vacancy.</h2><p class="section-copy">Open a current job listing, copy its description, and paste it here. MIHNA AI will identify skills it recognizes and compare them with the skills you enter.</p>', unsafe_allow_html=True)
st.caption("This version analyzes text you provide; it does not scrape job boards. Skill extraction is keyword-based, so it can miss skills or interpret context imperfectly. Verify the original listing.")
with st.form("job_requirement_comparison"):
    job_title = st.text_input("Job title", placeholder="Example: Junior Web Developer")
    company_name = st.text_input("Company (optional)", placeholder="Company name")
    job_url = st.text_input("Original job listing URL (optional)", placeholder="https://...")
    listing_date = st.text_input("Listing date (optional)", placeholder="Example: 14 October 2026")
    user_skills_for_job = st.text_area("Your skills for this comparison", placeholder="Example: HTML, CSS, JavaScript, Git, Python", height=100)
    job_description = st.text_area("Paste the job description", placeholder="Paste the responsibilities and requirements from the actual vacancy here...", height=240)
    compare_clicked = st.form_submit_button("Compare skills with this job", use_container_width=True)
if compare_clicked:
    if not user_skills_for_job.strip() or not job_description.strip():
        st.warning("Please enter your skills and paste the job description before comparing.")
    else:
        extracted = extract_skills(job_description)
        comparison = compare_skills(user_skills_for_job, extracted)
        st.markdown(f"### {escape(job_title.strip() or 'Job listing comparison')}")
        meta = " · ".join(x for x in [company_name.strip(), listing_date.strip()] if x)
        if meta:
            st.caption(meta)
        if job_url.strip().startswith(("https://", "http://")):
            st.markdown(f"**Source listing:** [{escape(job_url.strip())}]({job_url.strip()})")
        elif job_url.strip():
            st.caption("Source URL was entered, but it does not begin with http:// or https://. Check the URL before relying on it.")
        total = len(extracted)
        matched_count = len(comparison["matched"])
        score = round(matched_count / total * 100) if total else 0
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f'<div class="metric-card"><div class="metric-label">Recognized skills in listing</div><div class="metric-value">{total}</div></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="metric-card"><div class="metric-label">You listed as having</div><div class="metric-value">{matched_count}</div></div>', unsafe_allow_html=True)
        with c3:
            st.markdown(f'<div class="metric-card"><div class="metric-label">Not listed in your skills</div><div class="metric-value">{len(comparison["missing"])}</div></div>', unsafe_allow_html=True)
        if total:
            st.progress(score / 100)
            st.caption(f"Checklist coverage: {score}% of the skills MIHNA AI recognized in the pasted description also appear in your self-reported skills. This is not a hiring probability or proficiency score.")
            left, right = st.columns(2)
            with left:
                st.markdown("**Skills you listed that also appear in the job text**")
                if comparison["matched"]:
                    st.markdown(" ".join(f'<span class="skill-chip">{escape(x)}</span>' for x in comparison["matched"]), unsafe_allow_html=True)
                else:
                    st.write("No recognized overlap found. Check spelling and the pasted text.")
            with right:
                st.markdown("**Recognized job skills not in your list**")
                if comparison["missing"]:
                    st.markdown(" ".join(f'<span class="gap-chip">{escape(x)}</span>' for x in comparison["missing"]), unsafe_allow_html=True)
                else:
                    st.write("Every recognized skill was included in your list. Review the original description for requirements the detector may not recognize.")
            with st.expander("All skills recognized in the job description"):
                st.write(", ".join(extracted))
            st.info("Interpretation note: the detector recognizes a defined set of common technical and workplace skills. It does not reliably distinguish mandatory requirements from preferred qualifications, measure your actual ability, or validate whether the vacancy is still open.")
        else:
            st.warning("MIHNA AI did not recognize any skills in that text. Try pasting the requirements section, or check whether the listing mentions skills from the supported vocabulary.")




# Step 5 — Search real remote listings from the public Himalayas API.
from job_discovery import search_jobs, clean_description
from job_compare import extract_skills, compare_skills
from job_fit import classify_job_skills, build_priority_roadmap
st.divider()
st.markdown('<div class="section-kicker">Live job discovery · India + remote</div><h2 class="section-title">Find opportunities and compare requirements.</h2><p class="section-copy">Search an India-focused public job API or remote listings that may accept applicants from India. Listings are external; verify availability, location, and requirements on the original page.</p>', unsafe_allow_html=True)
with st.form("automatic_job_discovery"):
    discovery_source = st.selectbox("Job source", ["India jobs", "India-eligible remote jobs", "Worldwide remote jobs"], help="India jobs uses JobsForce India's public API. Remote sources do not represent the full Indian job market.")
    discovery_query = st.text_input("Search job titles or skills", value="junior web developer", placeholder="e.g. Python developer, data analyst internship")
    discovery_skills = st.text_area("Your skills", placeholder="HTML, CSS, JavaScript, Git", height=80)
    discovery_submit = st.form_submit_button("Search jobs", use_container_width=True)
if discovery_submit:
    if not discovery_query.strip():
        st.warning("Enter a role or skill to search for.")
    else:
        with st.spinner("Searching the public job feed..."):
            try:
                payload = search_jobs(discovery_query.strip(), source=discovery_source)
                jobs = payload.get("jobs", [])
                source_name = payload.get("source", discovery_source)
                source_url = payload.get("source_url", "https://jobsforceindia.com")
                st.caption(f"Source: {source_name} · {payload.get('totalCount', len(jobs))} matching listings reported where available. This is not the entire job market.")
                st.markdown(f"Job data provided by [{escape(source_name)}]({source_url}); open the original listing to verify it is still active.")
                if not jobs:
                    st.info("No results returned. Try a broader keyword, check your internet connection, or try another source.")
                else:
                    choices = []
                    for idx, job in enumerate(jobs):
                        title = str(job.get("title") or "Untitled role")
                        company = str(job.get("companyName") or "Company not specified")
                        choices.append(f"{title} — {company}")
                    selected_idx = st.selectbox("Choose a listing to compare", range(len(choices)), format_func=lambda i: choices[i])
                    selected_job = jobs[selected_idx]
                    desc = clean_description(str(selected_job.get("description") or selected_job.get("excerpt") or ""))
                    title = str(selected_job.get("title") or "Job listing")
                    company = str(selected_job.get("companyName") or "Company not specified")
                    link = str(selected_job.get("applicationLink") or selected_job.get("url") or selected_job.get("apply_url") or selected_job.get("guid") or "")
                    st.markdown(f"### {escape(title)}")
                    st.write(f"**Company:** {escape(company)}")
                    if selected_job.get("employmentType"):
                        st.write(f"**Employment:** {escape(str(selected_job.get('employmentType')))}")
                    restrictions = selected_job.get("locationRestrictions") or []
                    if restrictions:
                        st.write("**Location restrictions:** " + escape(", ".join(str(x) for x in restrictions)))
                    if selected_job.get("pubDate"):
                        from datetime import datetime, timezone
                        try:
                            raw_date = selected_job["pubDate"]
                            if isinstance(raw_date, (int, float)) or str(raw_date).isdigit():
                                stamp = float(raw_date)
                                if stamp > 100000000000:
                                    stamp /= 1000
                                pubdate = datetime.fromtimestamp(stamp, timezone.utc).strftime("%d %b %Y")
                            else:
                                pubdate = str(raw_date)[:10]
                            st.write(f"**Published / posted:** {pubdate}")
                        except (ValueError, TypeError, OSError, OverflowError):
                            pass
                    if link.startswith(("https://", "http://")):
                        st.link_button("Open original listing / application", link, use_container_width=True)
                    st.markdown("**Recognized skills in this listing**")
                    job_skills = extract_skills(desc)
                    if job_skills:
                        st.write(", ".join(job_skills))
                    else:
                        st.info("The listing text did not include skills recognized by the current vocabulary. Open the source and review it manually.")
                    if discovery_skills.strip() and job_skills:
                        comparison = compare_skills(discovery_skills, job_skills)
                        total = len(job_skills)
                        matched_count = len(comparison["matched"])
                        score = round(matched_count / total * 100) if total else 0
                        a, b, c = st.columns(3)
                        a.metric("Recognized job skills", total)
                        b.metric("Skills you listed", matched_count)
                        c.metric("Not in your list", len(comparison["missing"]))
                        st.progress(score / 100)
                        st.caption(f"Checklist coverage: {score}% of recognized skills also appear in your self-reported list. Not a proficiency or hiring score.")
                        left, right = st.columns(2)
                        with left:
                            st.markdown("**Matched skills**")
                            st.write(", ".join(comparison["matched"]) or "No recognized overlap")
                        with right:
                            st.markdown("**Potential gaps**")
                            st.write(", ".join(comparison["missing"]) or "No gaps detected by the current vocabulary")

                        # Step 6: classify requirement language and tailor next steps.
                        st.markdown("### Step 6 · Understand which gaps to tackle first")
                        st.caption("MIHNA looks for wording such as ‘required’, ‘must have’, ‘preferred’ and ‘nice to have’ near each recognized skill. If the listing is ambiguous, it labels the requirement unclear instead of guessing.")
                        classified = classify_job_skills(desc, job_skills)
                        groups = [
                            ("Likely required", "required", "These skills appeared near explicit must-have wording or in a requirements section."),
                            ("Preferred / nice to have", "preferred", "These skills appeared near preference wording; confirm the original listing."),
                            ("Requirement unclear", "unclear", "The listing mentions these skills but its wording did not clearly establish priority."),
                        ]
                        for heading, key, explanation in groups:
                            vals = classified[key]
                            if vals:
                                st.markdown(f"**{heading}**")
                                st.write(", ".join(vals))
                                st.caption(explanation)
                        missing_priority = [s for s in classified["required"] if s in comparison["missing"]]
                        missing_priority += [s for s in classified["unclear"] if s in comparison["missing"] and s not in missing_priority]
                        missing_priority += [s for s in classified["preferred"] if s in comparison["missing"] and s not in missing_priority]
                        if missing_priority:
                            st.markdown("### Your job-specific learning order")
                            st.write("Start with likely required gaps, then unclear ones, then preferred skills. This is a suggested study order—not a claim that the employer will reject or accept you.")
                            roadmap = build_priority_roadmap(missing_priority, title)
                            for number, item in enumerate(roadmap, 1):
                                st.markdown(f"**{number}. {escape(item['skill'])}** · {escape(item['priority'])}")
                                st.write(item['action'])
                                st.caption("Portfolio evidence: " + item['evidence'])
                        else:
                            st.success("No missing skills were identified by this vocabulary. Review the original listing and build evidence for the skills you already listed.")
                    elif not discovery_skills.strip():
                        st.caption("Add your skills above and search again to see the comparison.")
                    with st.expander("Preview description text used for matching"):
                        st.text(desc[:12000] if desc else "No description text was supplied by the API.")
                    st.markdown('Job data provided by [Himalayas](https://himalayas.app). Use the original listing link to confirm details and apply.')
            except Exception as exc:
                st.error("Could not retrieve job listings right now. Check your internet connection and try again later.")
                st.caption(f"Technical detail: {type(exc).__name__}: {exc}")


st.markdown('<div class="footer"><span>✳ MIHNA AI — Know your skills. Close the gap. Build your career.</span><span>SDG 8: Decent Work and Economic Growth</span></div>', unsafe_allow_html=True)
