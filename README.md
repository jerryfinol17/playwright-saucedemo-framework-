# Python Playwright Async POM Framework  
**Production-Ready | High Coverage | Modern E2E Automation**

![Python](https://img.shields.io/badge/Python-3.12%20|%203.13-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Playwright](https://img.shields.io/badge/Playwright-Async-2CA5E0?style=for-the-badge&logo=playwright&logoColor=white)
![pytest](https://img.shields.io/badge/pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)
![Coverage](https://img.shields.io/badge/Coverage-88.5%25-success?style=for-the-badge)
![CI](https://github.com/jerryfinol17/Python-Playwright-Saucedemo-Pom-Framework/actions/workflows/main.yml/badge.svg)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

A clean, scalable, and fully **asynchronous** Page Object Model framework built with **Playwright** and **pytest** for robust End-to-End testing.

Designed with real-world QA Automation best practices in mind — fast, reliable, maintainable, and production-ready from day one.

---

### ✨ Highlights

- **Full Async** implementation using `playwright.async_api` + `pytest-asyncio`
- Professional **Page Object Model** with reusable `BasePage` class
- Complete coverage of all SauceDemo user scenarios (including glitch users)
- Full business flows: Login → Inventory → Cart → Checkout → Order Confirmation
- Smart flakiness handling with `@pytest.mark.xfail` for known issues
- Automatic screenshots + video recording on test failure
- **88.5% code coverage** on the `pages/` layer (strategic, not inflated)
- Parallel test execution with `pytest-xdist`
- Professional CI/CD pipeline with GitHub Actions (Python 3.12 & 3.13)
- Cross-browser support (Chromium, Firefox, WebKit) ready

### Project Structure

```bash
├── pages/                  # Core Page Objects (BasePage + Login, Inventory, Cart, etc.)
├── tests/                  # Test cases + async fixtures
├── .github/workflows/      # CI/CD pipeline
├── screenshots/            # Auto-generated on failure
├── videos/                 # Auto-recorded on failure
├── pytest.ini
├── requirements.txt
└── coverage.xml
```
###  Quick Start


```bash 
git clone https://github.com/jerryfinol17/Python-Playwright-Saucedemo-Pom-Framework.git
cd Python-Playwright-Saucedemo-Pom-Framework

# Install dependencies
pip install -r requirements.txt

# Install browsers
playwright install --with-deps
```
### Running the Tests

 ```bash 
 # Run full test suite in parallel
pytest -n auto

# Debug mode (headed + slow motion)
pytest --browser chromium --headed --slowmo 300

# Generate beautiful HTML coverage report
pytest --cov=pages --cov-report=html
```
Open htmlcov/index.html to explore the detailed coverage.


### Live DemoWatch Full E2E Flow
(Async Version)![E2E-gif.gif](videos/E2E-gif.gif)
Complete checkout flow in under 20 seconds

### Why This Framework Stands Out:
Modern **Async-first** architecture (2026 best practice)
Production-grade code quality and maintainability
Strategic test coverage focused on the most critical layer (pages/)
Excellent balance between speed, reliability, and readability
Built to be easily extended for real client projects

### About the Author
**Jerry Finol** — QA Automation Engineer
Specialized in building high-quality automation frameworks with Python + Playwright (Async) and Selenium.Passionate about writing clean, scalable, and maintainable test code that teams actually love to work with.Currently open to freelance and full-time remote opportunities.Twitter / X: @GordoRelig3d

Email: jerrytareas17@gmail.com

Green tests. Happy teams. Reliable delivery.






