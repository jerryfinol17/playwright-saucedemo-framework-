# 🛡️ Python Playwright SauceDemo POM Framework

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Playwright](https://img.shields.io/badge/Playwright-1.45+-45ba75?style=for-the-badge&logo=playwright&logoColor=white)](https://playwright.dev/python/)
[![pytest](https://img.shields.io/badge/pytest-8.0+-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)](https://pytest.org/)
[![Coverage](https://img.shields.io/badge/Coverage-70%25_pages-success?style=for-the-badge&logo=coverage.py)](https://coverage.readthedocs.io/)
[![CI](https://img.shields.io/badge/CI-GitHub_Actions-2088FF?style=for-the-badge&logo=github)](https://github.com/jerryfinol17/Python-Playwright-Saucedemo-Pom-Framework/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](https://opensource.org/licenses/MIT)

**Production-grade End-to-End automation framework** built with **Playwright (Sync)** + **pytest** + **clean Page Object Model**.  

Designed and implemented to demonstrate the exact skills companies and clients look for in a QA Automation Engineer: maintainable architecture, rock-solid stability, real coverage focus, and immediate CI/CD readiness.

### ✨ Key Highlights (what makes this repo stand out)
- ✅ Full **Page Object Model** with `BasePage` inheritance – 100% reusable and scalable  
- ✅ Cross-browser out-of-the-box (Chromium, Firefox, WebKit)  
- ✅ All 7 SauceDemo users covered + invalid credentials + edge cases  
- ✅ Complete business flows: Login ↔ Inventory ↔ Cart ↔ Checkout ↔ Order success + Logout  
- ✅ Smart handling of known site bugs with `@xfail` (shows I understand real-world testing)  
- ✅ Automatic screenshots + video recording on failure  
- ✅ Prioritized coverage **70% in pages/** (the part that actually matters)  
- ✅ GitHub Actions CI pipeline already configured and ready  

### 📁 Project Structure
```bash
Python-Playwright-Saucedemo-Pom-Framework/
├── pages/                  # Core business logic (POM)
├── tests/                  # 8 well-organized test modules + fixtures
├── videos/                 # ✅ e2e.webm demo included
├── screenshots/            # Auto-generated on failure
├── .github/workflows/ci.yml # CI pipeline (active)
├── pytest.ini, .coveragerc, requirements.txt, coverage.xml
└── Full E2E + parametrized + smoke tests

```
### Quick Start

```bash
git clone https://github.com/jerryfinol17/Python-Playwright-Saucedemo-Pom-Framework.git
cd Python-Playwright-Saucedemo-Pom-Framework
pip install -r requirements.txt
playwright install --with-deps
```


### Run Tests
```bash
pytest                          # Full suite
pytest --browser firefox --headed --slowmo 300   # Debug mode
pytest --cov=pages --cov-report=html             # 70% coverage report
```
### Live Demo
[e2e.webm](videos/e2e.webm)

### Why you should  love this framework?

This is not just another bootcamp project — **it’s a ready-to-extend, production-oriented automation framework**
that proves I can:Build clean, maintainable code from day one  
Think like a senior QA (flakiness handling, coverage strategy, known-bug documentation)  
Deliver immediate value in any e-commerce or web project

**Perfect for your team.**

### About me:
Jerry Finol (@GordoRelig3d)! — QA Automation Engineer specialized in Python + Playwright.
From manual testing roots to building robust E2E frameworks, I focus on delivering clean, reliable, and fast automation that saves companies time and money.Currently open for freelance and contract opportunities (remote or NJ/NY area).Need a QA Automation Engineer who can ship frameworks like this for your project?
→ DM me on X (@GordoRelig3d)!

→ Email: jerrytareas17@gmail.com (or update to your pro one)¡Tests always green, clients always happy!