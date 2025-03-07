from setuptools import setup, find_packages

setup(
    name="ticket-analytics-jupyterlite",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "jupyterlite-core",
        "jupyterlite-xeus-python",
        "jupyterlab",
        "jupyterlab-fasta",
        "jupyterlab-geojson",
        "jupyterlab-tour",
        "plotly",
        "numpy",
        "pandas",
        "matplotlib",
        "scikit-learn",
        "scipy",
        "seaborn",
        "ipywidgets",
        "theme-darcula",
    ],
)
