from setuptools import setup, find_packages

setup(
    name="freshservice_scraper",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "freshpy",
        "python-dateutil",
    ],
    extras_require={
        "dev": [
            "pytest",
            "pytest-cov",
            "flake8",
        ],
    },
    entry_points={
        "console_scripts": [
            "get-tickets=freshservice_scraper.lib.cli:main",
        ],
    },
    description="Library for retrieving and analyzing Freshservice tickets",
    author="Freshservice API Team",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
