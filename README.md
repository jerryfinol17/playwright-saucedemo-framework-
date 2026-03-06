# Playwright Sauce Demo Framework

[![Python](https://img.shields.io/badge/python-3.9+-blue)](https://www.python.org/)
[![Playwright](https://img.shields.io/badge/Playwright-1.40+-45ba75?logo=playwright)](https://playwright.dev/python/)
[![pytest](https://img.shields.io/badge/pytest-9.0+-blueviolet)](https://docs.pytest.org/)
[![Coverage](https://img.shields.io/badge/coverage-70%25-success?logo=Coverage.py&logoColor=white)](https://coverage.readthedocs.io/) 

End-to-End (E2E) automation framework for the [Sauce Demo](https://www.saucedemo.com/) demo e-commerce application, built with **Playwright** (synchronous API), **pytest**, and **Page Object Model (POM)**.

This project demonstrates production-grade test automation practices: clean modular structure, reusable fixtures, parameterized tests, handling of flaky behavior, meaningful code coverage, and CI/CD readiness.

## Features

- Cross-browser testing support (Chromium, Firefox, WebKit) via pytest fixtures
- Complete Page Object Model (BasePage + dedicated pages for Login, Inventory, Cart, Checkout)
- Full coverage of Sauce Demo test users: standard_user, locked_out_user, problem_user, performance_glitch_user, visual_user, error_user, plus invalid credentials
- Comprehensive scenarios:
  - Login (positive/negative, locked out, performance glitch, visual issues, logout)
  - Inventory (add/remove items, cart badge sync, 4 sorting options, reset app state, item descriptions, known bugs with @xfail)
  - Cart (add/remove consistency, quantity checks, empty cart validation)
  - Checkout (happy path with 8% tax calculation, required fields validation (parametrized), cancel at each step, subtotal/tax/total assertions, checkout without items – noted as known site bug)
  - Full E2E journeys (add items → cart → checkout → order complete → back home → logout)

## Project Structure

```text
playwright-saucedemo-framework/
├── pages/                          # Page Object Model implementation
│   ├── __init__.py                 # Makes pages importable as module
│   ├── base_page.py                # Common methods & utilities
│   ├── cart_page.py
│   ├── checkout_page.py
│   ├── config.py                   # Constants: BASE_URL, users credentials, checkout test data
│   ├── inventory_page.py
│   └── login_page.py
├── tests/                          # All test files & fixtures
│   ├── conftest.py                 # Global fixtures: multi-browser/page, logged-in state
│   ├── test_dummy.py               # Basic smoke / dummy tests (title, simple login/inventory/cart)
│   ├── test_login.py               # Login scenarios (all users + negatives)
│   ├── test_inventory.py           # Add/remove, sorting, reset, descriptions, xfail for problem/visual users
│   ├── test_cart.py                # Cart consistency & empty checks
│   ├── test_e2e_cart.py            # (optional) Focused E2E cart flows
│   ├── test_checkout.py            # Checkout happy path, validations, parametrized fields, cancels
│   └── test_e2e.py                 # Complete end-to-end purchase + logout flow
├── screenshots/                    # Auto-generated on failures (configurable)
├── videos/                         # Auto-recorded videos on failures
├── .coveragerc                     # Coverage configuration (optional: omit lines/files)
├── pytest.ini                      # Pytest settings (pythonpath, addopts, markers, etc.)
├── requirements.txt                # Dependencies: playwright, pytest, pytest-cov, etc.
└── .github/                        # (Upcoming)
    └── workflows/
        └── ci.yml                  # GitHub Actions CI pipeline (multi-python, install, tests, coverage upload)
```
## Installation

1. Clone the repository

```bash

git clone https://github.com/YOUR_USERNAME/playwright-saucedemo-framework.git
cd playwright-saucedemo-framework
```

2. Install dependencies

```bash

pip install -r requirements.txt
playwright install --with-deps
```
## Running Tests
Run the full suite:

```bash

pytest
# Verbose + show summary
pytest -v
```
Quick feedback on pages logic:

```bash

pytest tests/ --cov=pages
```
Generate HTML coverage report:
```bash
pytest --cov=pages --cov-report=html
# Open htmlcov/index.html in your browser
```
Cross-browser run:
```bash

pytest --browser chromium --browser firefox --browser webkit
```
Useful dev flags:
```bash--headed, --slowmo 500, --screenshot only-on-failure, --video retain-on-failure
```
##Current Coverage (March 2026)
pages/ (core business logic): 70%  

Overall project: ~65%

Coverage prioritizes the pages/ module (interactions & assertions). Tests & fixtures naturally lower the global %.

## About & Contact

Hi! I'm **Jerry Finol** (@GordoRelig3d), a QA Junior from Venezuela currently based in the US.

I'm passionate about building reliable, maintainable automation frameworks using Python. This Sauce Demo project started as a way to level up my skills in **Playwright**, **Page Object Model**, **pytest best practices**, and **CI/CD readiness** — while having fun breaking (and fixing) a classic demo site.

From manual testing roots to writing battle-tested E2E suites, I enjoy clean code, good coverage, and proving that automation doesn't have to be boring or flaky.

If this repo saves you time, inspires an idea, or you want to chat about:
- Playwright tips & tricks
- Improving test stability (timeouts, flakiness, retries)
- QA career paths
- Collaborations / code reviews
- Or just say hi...

Feel free to **DM me on X** → [@GordoRelig3d](https://x.com/GordoRelig3d)

¡Gracias por pasar por acá y que los tests siempre pasen en verde! 💚

[e2e.webm](videos/e2e.webm)
