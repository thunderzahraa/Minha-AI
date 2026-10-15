
"""Public job-search adapters for MIHNA AI."""

import json
from html import unescape
import re
from urllib.parse import urlencode
from urllib.request import Request, urlopen

HIMALAYAS_API = "https://himalayas.app/jobs/api/search"
HIMALAYAS_SOURCE = "https://himalayas.app"
JOBSFORCE_API = "https://jobsforceindia.com/api/public/v1/jobs"
JOBSFORCE_SOURCE = "https://jobsforceindia.com"


def _get_json(url: str, timeout: int = 20) -> dict:
    request = Request(
        url,
        headers={
            "User-Agent": "MIHNA-AI-Student-Project/1.0",
            "Accept": "application/json",
        },
    )

    with urlopen(request, timeout=timeout) as response:
        data = json.loads(response.read().decode("utf-8"))

    if not isinstance(data, dict):
        raise ValueError("The job API returned an unexpected response format.")

    return data


def _text(value, fallback=""):
    """Convert API values, including nested objects, into readable text."""
    if isinstance(value, dict):
        for key in ("display", "name", "city", "label", "title", "value"):
            if value.get(key):
                return str(value[key])
        return fallback

    if isinstance(value, list):
        return ", ".join(str(item) for item in value if item)

    return str(value) if value is not None else fallback


def search_jobs(
    query: str,
    page: int = 1,
    timeout: int = 20,
    source: str = "India jobs",
) -> dict:
    """Search a supported public job feed and normalize its results."""

    page = max(1, int(page))

    params = urlencode({"q": query})

    data = _get_json(f"{JOBSFORCE_API}?{params}", timeout)

    raw_jobs = data.get(
            "results",
            data.get("jobs", data.get("data", [])),
        )

    if isinstance(raw_jobs, dict):
            raw_jobs = raw_jobs.get(
                "results",
                raw_jobs.get("jobs", []),
            )

    if not isinstance(raw_jobs, list):
            raise ValueError(
                "India job API did not return a valid results list."
            )

    jobs = []

    for item in raw_jobs:
            if not isinstance(item, dict):
                continue

            employer = item.get("employer")
            company = (
                item.get("company_name")
                or item.get("company")
                or _text(employer, "Employer details on source page")
            )

            location_data = item.get("location")
            location = (
                _text(location_data)
                or _text(item.get("city"))
                or _text(item.get("work_mode"))
                or "India"
            )

            description = (
                item.get("description")
                or item.get("job_description")
                or item.get("summary")
                or item.get("excerpt")
                or ""
            )

            link = (
                item.get("url")
                or item.get("job_url")
                or item.get("apply_url")
                or item.get("application_url")
                or item.get("link")
                or JOBSFORCE_SOURCE
            )

            jobs.append({
                "title": _text(
                    item.get("title")
                    or item.get("job_title")
                    or item.get("role"),
                    "Untitled role",
                ),
                "companyName": _text(company, "Employer details on source page"),
                "description": _text(description),
                "excerpt": _text(item.get("summary") or item.get("excerpt") or description),
                "employmentType": _text(item.get("job_type") or item.get("employment_type")),
                "locationRestrictions": [location],
                "pubDate": (
                    item.get("posted_date")
                    or item.get("posted_at")
                    or item.get("published_at")
                    or item.get("created_at")
                    or item.get("date_posted")
                ),
                "applicationLink": str(link),
                "guid": str(item.get("id") or link),
                "_source": "JobsForce India",
                "_source_url": JOBSFORCE_SOURCE,
                "_raw": item,
            })

    return {
            "jobs": jobs,
            "totalCount": data.get(
                "total",
                data.get("total_count", data.get("count", len(jobs))),
            ),
            "source": "JobsForce India",
            "source_url": JOBSFORCE_SOURCE,
            "updatedAt": data.get("updated_at"),
        }

    params = {
        "q": query,
        "sort": "recent",
        "page": page,
    }

    if source == "India-eligible remote jobs":
        params["country"] = "IN"

    data = _get_json(
        f"{HIMALAYAS_API}?{urlencode(params)}",
        timeout,
    )

    raw_jobs = data.get("jobs", [])

    if not isinstance(raw_jobs, list):
        raise ValueError("Remote job API did not return a valid jobs list.")

    jobs = []

    for item in raw_jobs:
        if isinstance(item, dict):
            item["_source"] = "Himalayas"
            item["_source_url"] = HIMALAYAS_SOURCE
            jobs.append(item)

    data["jobs"] = jobs
    data["source"] = "Himalayas"
    data["source_url"] = HIMALAYAS_SOURCE

    return data


def clean_description(value: str) -> str:
    value = re.sub(
        r"(?i)<br\s*/?>|</p>|</li>|</div>",
        "\n",
        value or "",
    )
    value = re.sub(r"<[^>]+>", " ", value)
    value = re.sub(r"[ \t]+", " ", unescape(value))
    return value.strip()
