from typing import List


console_scripts: List[str] = [
    "pytubekit=pytubekit.main:main",
]
dev_requires: List[str] = [
    "pypitools",
    "black",
]
config_requires: List[str] = [
    "pyclassifiers",
]
install_requires: List[str] = [
    "google-api-python-client",
    "pygooglehelper",
    "pytconf",
    "pylogconf",
    "pyvardump",
    "youtube-dl",
    "browsercookie",
]
build_requires: List[str] = [
    "pydmt",
    "pymakehelper",
]
test_requires: List[str] = [
    "pytest",
    "pytest-cov",
    "pylint",
    "flake8",
    "mypy",
]
requires = config_requires + install_requires + build_requires + test_requires
