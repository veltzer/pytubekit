""" python deps for this project """

console_scripts: list[str] = [
    "pytubekit=pytubekit.main:main",
]

config_requires: list[str] = [
    "pyclassifiers",
]
install_requires: list[str] = [
    "google-api-python-client",
    "pygooglehelper",
    "pytconf",
    "pylogconf",
    "pyvardump",
    "youtube-dl",
    "browsercookie",
]
build_requires: list[str] = [
    "pydmt",
    "pymakehelper",
]
test_requires: list[str] = [
    "pytest",
    "pytest-cov",
    "pylint",
    "mypy",
]
requires = config_requires + install_requires + build_requires + test_requires
