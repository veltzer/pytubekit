import config.project

package_name = config.project.project_name

console_scripts = [
    "pytubekit=pytubekit.main:main",
]

setup_requires = []

run_requires = [
    "google-api-python-client",  # for google API
    "google-auth-httplib2",  # for google API
    "google-auth-oauthlib",  # for google API
    "pytconf",  # for command line parsing
    "pylogconf",  # for logging configuration
    "pyvardump",  # for dumping data
]

test_requires = [
    "pytest",  # for testing
    "pytest-cov",  # for testing
    "pylint",  # for linting
    "flake8",  # for linting
    "pymakehelper",  # for make
]

dev_requires = [
    "pyclassifiers",  # for programmatic classifiers
    "pypitools",  # for upload etc
    "pydmt",  # for building
    "Sphinx",  # for the sphinx builder
    "black",  # for code style
]

install_requires = list(setup_requires)
install_requires.extend(run_requires)

python_requires = ">=3.6"

extras_require = {
    # ':python_version == "2.7"': ['futures'],  # for python2.7 backport of concurrent.futures
}
