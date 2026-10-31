# Garden Shop Dashboard: GitHub Storage & Publishing Guide

This guide explains how to store, test locally, and publish the interactive Garden Shop Inventory Dashboard directly through GitHub.

---

## Architecture Overview

The dashboard is delivered in two complementary forms:
1. **Option 1 (Zero-Server GitHub Pages Web App):** An ultra-fast, responsive single-page application (`index.html`) using Tailwind CSS and Chart.js that executes 100% in the user's browser with sub-50ms dynamic filtering over `dashboard_data.json`.
2. **Option 2 (Python Streamlit Community Cloud App):** A full Python dashboard (`app.py`) using Pandas, Plotly, and SQLite for data science teams and Streamlit Cloud deployment.

---

## 1. Local Testing

### A. Testing the GitHub Pages Web App (`index.html`)

You can test the web app immediately without any web server:
- Simply double-click [`./exercise/Task_01/index.html`](index.html) or open it in your browser (Chrome, Edge, Firefox, Safari).
- Or run a local Python HTTP server from the project root:
  ```powershell
  python -m http.server 8000
  ```
  Then navigate to: `http://localhost:8000/exercise/Task_01/index.html`

### B. Testing the Streamlit App (`app.py`)

Run the Streamlit app directly from your terminal:
```powershell
streamlit run exercise/Task_01/app.py
```
This opens the Python dashboard at `http://localhost:8501`.

---

## 2. Publishing to GitHub Pages (Recommended)

GitHub Pages provides free static web hosting directly from your repository with zero server setup.

### Step 1: Place Files in GitHub Pages Directory
You can configure GitHub Pages to deploy from:
- A `/docs` directory on the `main` branch, OR
- A dedicated `gh-pages` branch, OR
- The root of the repository.

To deploy via `/docs`:
1. Copy `exercise/Task_01/index.html` and `exercise/Task_01/dashboard_data.json` into a top-level `docs/` folder in your repository.
2. Commit and push to GitHub:
   ```bash
   git add docs/
   git commit -m "Deploy Garden Shop dashboard to GitHub Pages"
   git push origin main
   ```

### Step 2: Enable GitHub Pages in Repository Settings
1. Navigate to your repository on **GitHub.com**.
2. Click **Settings** > **Pages** (under "Code and automation" in the left sidebar).
3. Under **Build and deployment**:
   - **Source:** Select `Deploy from a branch`.
   - **Branch:** Select `main` and set the folder to `/docs` (or `/ (root)` if deployed from root).
4. Click **Save**.
5. Within 60 seconds, your dashboard will be live at:
   ```
   https://<your-github-username>.github.io/<repository-name>/
   ```

### (Optional) Automated CI/CD via GitHub Actions
To automate updating the dashboard whenever `data/garden_shop.db` is updated, add a `.github/workflows/deploy-pages.yml` file:
```yaml
name: Deploy Dashboard to GitHub Pages

on:
  push:
    branches: [ main ]
    paths:
      - 'data/garden_shop.db'
      - 'exercise/Task_01/**'

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: 'pages'
  cancel-in-progress: true

jobs:
  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Extract Fresh Dashboard Data
        run: |
          python exercise/Task_01/export_dashboard_data.py

      - name: Prepare Artifacts
        run: |
          mkdir -p _site
          cp exercise/Task_01/index.html _site/
          cp exercise/Task_01/dashboard_data.json _site/

      - name: Upload GitHub Pages Artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: '_site'

      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

---

## 3. Publishing to Streamlit Community Cloud

If you prefer the pure Python application:
1. Push your repository to GitHub.
2. Visit [share.streamlit.io](https://share.streamlit.io/) and log in with your GitHub account.
3. Click **"New app"**.
4. Select your repository, branch (`main`), and set the main file path to:
   ```
   exercise/Task_01/app.py
   ```
5. Click **"Deploy!"**.
6. Streamlit Cloud automatically installs dependencies, runs the app, and assigns a public URL. Every `git push` will automatically trigger a re-deployment!

---

## 4. How to Update Data

Whenever orders, products, or suppliers are added or modified in `data/garden_shop.db`:
1. Run the data extractor:
   ```powershell
   python exercise/Task_01/export_dashboard_data.py
   ```
2. Commit and push the updated `dashboard_data.json`:
   ```bash
   git add exercise/Task_01/dashboard_data.json
   git commit -m "Update inventory snapshot and sales metrics"
   git push
   ```
The web dashboard will automatically display the updated inventory numbers and reorder recommendations!
