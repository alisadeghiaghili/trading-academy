from setuptools import setup, find_packages

setup(
    name="trading_academy",
    version="1.0.0",
    description="Trading Academy - Comprehensive trading education platform",
    author="Ali Sadeghi Aghili",
    author_email="ali@example.com",
    url="https://github.com/alisadeghiaghili/trading-academy",
    license="Apache-2.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pandas>=2.0",
        "numpy>=1.24",
        "matplotlib>=3.7",
        "plotly>=5.15",
        "requests>=2.31",
        "ta-lib>=0.4.24",
        "scikit-learn>=1.3",
        "nltk>=3.8",
        "textblob>=0.17",
        "yfinance>=0.2",
        "python-binance>=1.0",
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
    python_requires=">=3.11",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Topic :: Office/Business :: Financial :: Investment",
        "Intended Audience :: Education",
        "Intended Audience :: Financial and Insurance Industry",
    ],
)