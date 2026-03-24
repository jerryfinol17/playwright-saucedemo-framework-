# 🛡️ Python Playwright + POM Framework | SauceDemo E2E

**Production-ready End-to-End Automation Framework** built with **Playwright (Sync)** + **pytest** + **clean Page Object Model**.

A scalable, maintainable, and production-ready framework designed to demonstrate real-world QA Automation skills that companies and clients are actively looking for.

![Playwright](https://img.shields.io/badge/Playwright-2CA5E0?style=for-the-badge&logo=playwright&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![pytest](https://img.shields.io/badge/pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)
![Coverage](https://img.shields.io/badge/Coverage-88.5%25-brightgreen)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

---

### ✨ Key Features

- Clean **Page Object Model** with reusable `BasePage` class
- Full **cross-browser** support (Chromium, Firefox, WebKit)
- Complete business flows: Login → Inventory → Cart → Checkout → Order Success → Logout
- Coverage of all **7 SauceDemo users** + invalid credentials + real edge cases
- Smart handling of known bugs using `@xfail`
- **Automatic** screenshots + video recording on failure
- **70% coverage** focused on the `pages/` folder (where it matters most)
- Ready-to-use **GitHub Actions** CI/CD pipeline
- Professional reporting (Allure & HTML)

### 📁 Project Structure

```bash
Python-Playwright-Saucedemo-Pom-Framework/
├── pages/              # Page Objects (core of the framework)
├── tests/              # Organized tests + fixtures
├── videos/             # Automatic video recordings (demo included)
├── screenshots/        # Automatic failure screenshots
├── .github/workflows/  # CI/CD pipeline
├── LICENSE
├── pytest.ini
├── .coveragerc
├── requirements.txt
└── coverage.xml
```
 Quick Start

```bash
git clone https://github.com/jerryfinol17/Python-Playwright-Saucedemo-Pom-Framework.git
cd Python-Playwright-Saucedemo-Pom-Framework

pip install -r requirements.txt
playwright install --with-deps
```

 How to Run the Tests

```bash
# Run full test suite
pytest

# Run in headed mode with slow motion (great for debugging)
pytest --browser firefox --headed --slowmo 300

# Generate coverage report (focused on pages)
pytest --cov=pages --cov-report=html
```
 ### Live Demo 
 [Full E2E Flow](https://github.com/jerryfinol17/Python-Playwright-Saucedemo-Pom-Framework/raw/main/videos/e2e.webm)
 (Watch the complete flow running in under 40 seconds)

 ### Why Hire Me With This Framework?

This is **not** just another bootcamp project.It’s a real demonstration of how I deliver professional, production-ready automation frameworks from day one:Clean, maintainable, and scalable code  
Strong focus on stability and real QA experience  
CI/CD ready for production  
Business understanding, not just “clicking buttons”

Perfect for startups, agencies, or teams that need **reliable and fast automation**.

## About MeJerry Finol – QA Automation Engineer

Specialized in **Python + Playwright + Selenium.**
Currently **open to freelance and remote opportunities** (available in NJ/NY area as well).Need a solid automation framework for your project?
I’d love to help you deliver quality and speed.
### Contact me
X / Twitter: @GordoRelig3d

Email: jerrytareas17@gmail.com


Green tests. Happy clients. 




