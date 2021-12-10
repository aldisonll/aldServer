from setuptools import setup, find_packages
from aldServer import __version__

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name = 'aldServer',
    author='Aldison Lluka', 
    author_email='aldison.lluka.al@gmail.com',
    description='aldServer - a template server',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages = find_packages(),
    python_requires='>=3',
    version = __version__
)