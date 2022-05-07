import config.project

package_name = config.project.project_name

console_scripts = [
    "pytubekit=pytubekit.main:main",
]
dev_requires = [
    "pyclassifiers",
    "pypitools",
    "pydmt",
    "Sphinx",
    "black",
]
install_requires = [
    "google-api-python-client",
    "google-auth-httplib2",
    "google-auth-oauthlib",
    "pygooglehelper",
    "pytconf",
    "pylogconf",
    "pyvardump",
    "youtube-dl",
    "browsercookie",
]
test_requires = [
    "pytest",
    "pytest-cov",
    "pylint",
    "flake8",
    "pymakehelper",
]

python_requires = ">=3.10"

test_os = ["ubuntu-22.04"]
test_python = ["3.10"]
