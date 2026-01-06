PY-RECORDER — RECORD & REPLAY WEB VERIFICATION FRAMEWORK

OVERVIEW

Py-Recorder is a Playwright + Pytest based record-and-replay framework designed to verify real user navigation flows by validating meaningful page content rather than fragile UI selectors.

It allows you to:

Automatically log in to a web application

Record real manual navigation (user clicks)

Capture content snapshots per navigation step

Replay the same journey automatically

Verify recorded content against live content

Generate a self-contained HTML verification report

Embed screenshots directly into the report on failure

Run fully headless in a CI/CD pipeline

This framework focuses on CONTENT VALIDATION, not UI automation.

WHY THIS PROJECT

Traditional UI automation:

Breaks on minor layout changes

Depends heavily on selectors

Produces noisy, unhelpful failures

Py-Recorder solves this by:

Tracking real user navigation

Validating meaningful content (text users actually read)

Producing audit-ready HTML evidence

Running deterministically in CI pipelines

Ideal use cases:

Regression verification

Content drift detection

Post-deployment validation

Manual to automated test migration

CI gatekeeping

CORE CONCEPTS

RECORD PHASE

Browser opens after successful login

User manually clicks links

Each navigation records:

current_url

target_url

page title

h1 heading

first meaningful paragraph (firstP)

Saved to steps.json

REPLAY PHASE

Login happens automatically

Recorded navigation is replayed

Live content is extracted at each step

Recorded vs live content is compared

VERIFICATION

PASS: logged in report

FAIL:

Screenshot captured

Screenshot embedded in report (Base64)

Recorded vs Live text displayed

CI pipeline fails with proof

TECH STACK

Automation: Playwright (Python)
Test Runner: Pytest
Reporting: pytest-html
CI/CD: GitHub Actions
Browser: Chromium
Language: Python 3.11+

FOLDER STRUCTURE

py-recorder/
├── recorder/
│ ├── login.py
│ ├── record.py
│ ├── replay.py
│ ├── content.py
│ ├── steps_store.py
│ ├── report_context.py
│ └── init.py
│
├── tests/
│ ├── test_record.py
│ └── test_replay.py
│
├── data/
│ └── steps.json
│
├── reports/
│ └── replay-report.html
│
├── .github/workflows/
│ └── pytest-replay.yml
│
├── conftest.py
├── pytest.ini
├── requirements.txt
└── README.md

HOW TO EXECUTE

CREATE VIRTUAL ENVIRONMENT
python -m venv .venv
source .venv/bin/activate (Windows: .venv\Scripts\activate)

INSTALL DEPENDENCIES
pip install -r requirements.txt
python -m playwright install

RECORD A USER JOURNEY (LOCAL ONLY)

pytest tests/test_record.py -s

Browser opens

Login happens automatically

You manually navigate the site

Close browser to stop recording

steps.json is created

REPLAY AND VERIFY

pytest tests/test_replay.py
--html=reports/replay-report.html
--self-contained-html
-v

SAMPLE TEST REPORT

Each step includes:

Step number

URL

Status (PASSED / FAILED)

Recorded content

Live content

Embedded screenshot on failure

No stack traces. No noise. Just evidence.

CI/CD READY

Headless execution

Self-contained HTML report

Screenshot embedding

Artifacts uploaded on every run

Recorder excluded from CI

Replay only in pipeline

EXPECTED OUTPUT

SUCCESS:

All steps PASSED

Report shows verified content

FAILURE:

Step marked FAILED

Screenshot embedded

Recorded vs Live content shown

CI job fails intentionally

BRANCHING STRATEGY

main
├── staging
└── development

Rules:

No direct commits to main

All work happens in development

PR to staging

Final merge to main

DEPENDENCIES

playwright
pytest
pytest-html
typing-extensions

Browsers installed via:
python -m playwright install

CI PIPELINE

Triggered on push to development

Triggered on PR to development

Generates replay-report.html

Uploads report as artifact

CREATED BY

Rajeev S
Automation & AI Engineer
Bengaluru, India                            