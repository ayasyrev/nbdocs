from setuptools import setup


VERSION_FILENAME = 'src/nbdocs/version.py'
REQUIREMENTS_FILENAME = 'requirements.txt'
REQUIREMENTS_TEST_FILENAME = 'requirements_test.txt'


# Requirements
try:
    with open(REQUIREMENTS_FILENAME, encoding="utf-8") as f:
        REQUIRED = f.read().split("\n")
except FileNotFoundError:
    REQUIRED = []

try:
    with open(REQUIREMENTS_TEST_FILENAME, encoding="utf-8") as f:
        TEST_REQUIRED = f.read().split("\n")
except FileNotFoundError:
    TEST_REQUIRED = []

# What packages are optional?
EXTRAS = {"test": TEST_REQUIRED}

# Load the package's __version__ from version.py
version = {}
with open(VERSION_FILENAME, 'r') as f:
    exec(f.read(), version)
VERSION = version['__version__']


setup(
    version=VERSION,
    install_requires=REQUIRED,
    extras_require=EXTRAS,
)
