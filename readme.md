# PY-create_testER — CREATE_TEST & RUN_TEST WEB VERIFICATION FRAMEWORK

## OVERVIEW

**Py-create_tester** is a Playwright + Pytest based **create_test and run_test verification framework** designed to validate **real user navigation flows** by comparing **meaningful page content**, not fragile UI selectors.

It allows you to:

- Automatically log in to a web application
- Create tests by capturing real manual navigation (user clicks)
- Store content snapshots per navigation step
- Execute the same journey automatically
- Verify stored content against live content
- Generate a self-contained HTML verification report
- Embed screenshots directly into the report on failure
- Run fully headless in a CI/CD pipeline

This framework focuses on **CONTENT VALIDATION**, not traditional UI automation.

---

## WHY THIS PROJECT

Traditional UI automation:

- Breaks on minor layout changes  
- Depends heavily on brittle selectors  
- Produces noisy, low-signal failures  

**Py-create_tester** solves this by:

- Tracking **real user navigation**
- Validating **meaningful content users actually read**
- Producing **audit-ready HTML evidence**
- Running deterministically in **CI pipelines**

---

## CORE CONCEPTS

### CREATE_TEST PHASE

- Browser opens after successful login
- User manually navigates through the application
- Each navigation step captures:
  - `current_url`
  - `target_url`
  - page title
  - `h1` heading
  - first meaningful paragraph (`firstP`)
- All steps are stored in `steps.json`

---

### RUN_TEST PHASE

- Login happens automatically
- Stored navigation steps are executed sequentially
- Live page content is extracted at each step
- Stored content is compared against live content
- All steps are executed even if mismatches occur

---

### VERIFICATION

- **PASS**
  - Step marked as verified in the report
- **FAIL**
  - Screenshot captured
  - Screenshot embedded directly in the HTML report (Base64)
  - Stored vs Live `firstP` displayed
  - CI pipeline fails **after all steps complete**

---

## TECH STACK

- **Automation:** Playwright (Python)
- **Test Runner:** Pytest
- **Reporting:** pytest-html
- **CI/CD:** GitHub Actions
- **Browser:** Chromium
- **Language:** Python 3.11+

---

## FOLDER STRUCTURE

```text
py-create_tester/
├── create_tester/
│   ├── login.py
│   ├── create_test.py
│   ├── run_test.py
│   ├── content.py
│   ├── steps_store.py
│   ├── report_context.py
│   └── __init__.py
│
├── tests/
│   ├── test_create_test.py
│   └── test_run_test.py
│
├── data/
│   └── steps.json
│
├── reports/
│   └── run_test-report.html
│
├── .github/workflows/
│   └── pytest-run_test.yml
│
├── conftest.py
├── pytest.ini
├── requirements.txt
└── README.md
```

## HOW TO EXECUTE
CREATE VIRTUAL ENVIRONMENT

```bash
python -m venv .venv
source .venv/bin/activate
Windows:

powershell

.venv\Scripts\activate
INSTALL DEPENDENCIES

pip install -r requirements.txt
python -m playwright install
CREATE_TEST (LOCAL ONLY)

pytest tests/test_create_test.py -s
Generates data/steps.json
This phase is intentionally excluded from CI

RUN_TEST AND VERIFY

pytest tests/test_run_test.py \
  --html=reports/run_test-report.html \
  --self-contained-html \
  -v

```

## CI/CD READY
Fully headless execution

Self-contained HTML report

Screenshots embedded on failure

Artifacts uploaded on every run

Create_test excluded from CI

Run_test enforced in pipeline
```

## EXPECTED OUTPUT

SUCCESS
All steps verified successfully

HTML report shows validated content

CI pipeline passes

FAILURE
One or more steps marked as failed

Screenshot embedded in report

Stored vs Live content displayed

CI job fails intentionally with evidence
```

## BRANCHING STRATEGY

```bash
main
├── staging
└── development

```
## CREATED BY
Rajeev S