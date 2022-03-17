import io
import os
import sys
from shutil import rmtree

from setuptools import Command, find_packages, setup


# Requirements
try:
    with open("requirements.txt", encoding="utf-8") as f:
        REQUIRED = f.read().split("\n")
except FileNotFoundError:
    REQUIRED = []

try:
    with open("requirements_test.txt", encoding="utf-8") as f:
        TEST_REQUIRED = f.read().split("\n")
except FileNotFoundError:
    TEST_REQUIRED = []

# What packages are optional?
EXTRAS = {"test": TEST_REQUIRED}

# Load the package's __version__ from version.py
version = {}
with open('nbdocs/version.py', 'r') as f:
    exec(f.read(), version)
VERSION = version['__version__']


class UploadCommand(Command):
    """Support setup.py upload."""

    description = "Build and publish the package."
    user_options = []

    @staticmethod
    def status(s):
        """Print things in bold."""
        print(s)

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status("Removing previous builds...")
            rmtree("dist")
        except OSError:
            pass

        self.status("Building Source and Wheel (universal) distribution...")
        os.system(f"{sys.executable} setup.py sdist bdist_wheel --universal")

        self.status("Uploading the package to PyPI via Twine...")
        os.system("twine upload dist/*")

        self.status("Pushing git tags...")
        os.system(f"git tag v{VERSION}")
        os.system("git push --tags")

        sys.exit()


setup(
    version=VERSION,
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    cmdclass={"upload": UploadCommand},
    entry_points={'console_scripts': [
        'nbdocs=nbdocs.app:app']},
)
