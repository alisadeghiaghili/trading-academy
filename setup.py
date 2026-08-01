from setuptools import setup, find_packages

setup(
    name="trading_academy",
    version="0.1.0",
    description="A comprehensive Python-based trading education application",
    author="Your Name",
    author_email="you@example.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pandas>=2.0",
        "numpy>=1.24",
        "matplotlib>=3.7",
        "plotly>=5.15",
        "requests>=2.31",
        "ta-lib>=0.4.24",  # Note: may require system installation
        "scikit-learn>=1.3",
        "nltk>=3.8",
        "textblob>=0.17",
        "transformers>=4.30",
        "torch>=2.0",
        "yfinance>=0.2",
        "python-binance>=1.0",
        "streamlit>=1.28",
        "streamlit-aggrid>=0.3.4",
        "plotly-express",
        "openpyxl>=3.1",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "black>=23.0",
            "flake8>=6.0",
            "mypy>=1.0",
            "jupyterlab>=4.0",
            "notebook>=6.5",
        ]
    },
    entry_points={
        "console_scripts": [
            "trading-academy=trading_academy.ui.app:main",
        ],
    },
    python_requires=">=3.9",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Office/Business :: Financial :: Investment",
    ],
)