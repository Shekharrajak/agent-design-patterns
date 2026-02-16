# Agent Design Patterns

A visual guide to agentic systems in modern software architecture.
Served as a static site via [MkDocs Material](https://squidfunk.github.io/mkdocs-material/) on GitHub Pages.

## Local Development

```bash
pip install -r requirements.txt
mkdocs serve
```

Open `http://127.0.0.1:8000` in your browser.

## Deploy

Push to `main`. The GitHub Actions workflow builds and deploys to GitHub Pages automatically.

After the first push, enable GitHub Pages in the repo settings:
**Settings > Pages > Source > GitHub Actions**.

## Project Structure

```
docs/
  index.md                  Landing page
  posts/
    01-the-agentic-spectrum.md
    02-the-six-patterns.md
    03-agents-in-distributed-systems.md
    04-agents-in-microservices.md
    05-agents-in-web-applications.md
    06-multi-agent-system-architecture.md
    07-production-playbook.md
    08-the-future-of-software-systems.md
    09-deep-challenges.md
  stylesheets/
    extra.css
mkdocs.yml                  Site configuration
.github/workflows/deploy.yml  CI/CD pipeline
```
