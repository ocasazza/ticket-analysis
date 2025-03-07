# JupyterLite for Ticket Analytics

This directory contains all the necessary files to build and deploy a JupyterLite instance for analyzing ticket data.

## Directory Structure

- `requirements.txt` - Python dependencies required for building JupyterLite
- `jupyter_lite_config.json` - Configuration for the JupyterLite build
- `index.html` - Custom landing page for the JupyterLite deployment
- `content/` - Directory containing notebooks and data
  - `ticket_analysis.ipynb` - Sample notebook for analyzing ticket data
  - `data/` - Directory where ticket data is copied during build

## Local Development

1. Run the test script to build the JupyterLite environment:
   ```bash
   ./test_local_build.sh
   ```

2. If the build is successful, serve the site locally:
   ```bash
   python -m http.server 8765 -d _output
   ```

3. Open your browser to http://localhost:8765

## Troubleshooting

If you encounter issues with the build:

1. Ensure you have Python 3.8+ installed
2. Try installing the dependencies manually:
   ```bash
   python -m pip install --upgrade pip wheel
   python -m pip install jupyterlite-core
   python -m pip install -e .
   ```
3. Run the build command directly:
   ```bash
   python -m jupyterlite build --output-dir _output
   ```
4. If you get dependency errors, check that:
   - You have a recent version of pip and wheel
   - All dependencies in setup.py are available
   - The output directory has been specified correctly

## Deployment

This JupyterLite site is automatically deployed to GitHub Pages via GitHub Actions when changes are pushed to the main branch. The workflow defined in `.github/workflows/deploy.yml` handles:

1. Installing dependencies
2. Copying ticket data
3. Building the JupyterLite site
4. Deploying to the gh-pages branch
