"""Setup script for KCM Framework."""
from pathlib import Path
from setuptools import setup, find_packages

# Read README
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

# Read requirements
requirements_file = Path(__file__).parent / "requirements.txt"
requirements = []
if requirements_file.exists():
    requirements = [
        line.strip()
        for line in requirements_file.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.startswith("#")
    ]

setup(
    name="kascmpy",
    version="0.1.0",
    author="kasperenok",
    author_email="kasperstudioshelp@gmail.com",
    description="Modern Console User Interface (CUI) Framework for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kasper-studios/kascmenu-engine",
    project_urls={
        "Bug Tracker": "https://github.com/kasper-studios/kascmenu-engine/issues",
        "Documentation": "https://github.com/kasper-studios/kascmenu-engine#readme",
        "Source Code": "https://github.com/kasper-studios/kascmenu-engine",
    },
    packages=find_packages(include=["kcmpy", "kcmpy.*"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: User Interfaces",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
    ],
    python_requires=">=3.7",
    install_requires=[
        # Core dependencies (none for basic framework)
    ],
    extras_require={
        "chat": [
            "flask>=3.0.0",
            "flask-socketio>=5.3.0",
            "python-socketio>=5.11.0",
        ],
        "notifications": [
            "win10toast>=0.9; sys_platform == 'win32'",
        ],
        "build": [
            "nuitka>=1.0",
            "cython>=3.0.0; python_version >= '3.12'",
        ],
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=4.0",
            "black>=23.0",
            "flake8>=6.0",
            "mypy>=1.0",
        ],
        "all": [
            "flask>=3.0.0",
            "flask-socketio>=5.3.0",
            "python-socketio>=5.11.0",
            "win10toast>=0.9; sys_platform == 'win32'",
            "nuitka>=1.0",
            "cython>=3.0.0; python_version >= '3.12'",
        ],
    },
    entry_points={
        "console_scripts": [
            "kcm=kcmpy.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "kcmpy": ["py.typed"],
    },
    keywords=[
        "cui",
        "tui",
        "console",
        "terminal",
        "ui",
        "framework",
        "menu",
        "widgets",
        "screen",
        "layout",
    ],
    license="MIT",
    zip_safe=False,
)
