import\
    setuptools,\
    sys

NAME = "assetmgr"
VERSION = (0, 1, 0)
DESCRIPTION = "Asset and inventory management app for everyday people."
LICENSE = "GPL-3.0-only"
KEYWORDS = [
    "asset",
    "management",
    "inventory",
    "manager"
]
INSTALL_REQUIRES = [
    "datakick"
]
LATEST_PYTHON_VERSION = (3, 7)
REQUIRED_PYTHON_VERSION = (3, 6) # for f strings
CURRENT_PYTHON_VERSION = sys.version_info[:2]
if CURRENT_PYTHON_VERSION < REQUIRED_PYTHON_VERSION:
    sys.stderr.write("""
==========================
Unsupported Python version
==========================
This version of {0} requires Python {1}.{2}, but you're trying to
install it on Python {3}.{4}.
This may be because you are using a version of pip that doesn't
understand the python_requires classifier. Make sure you
have pip >= 9.0 and setuptools >= 24.2, then try again:
    $ python -m pip install --upgrade pip setuptools
    $ python -m pip install django
This will install the latest version of {0} which works on your
version of Python. If you can't upgrade your pip (or Python), request
an older version of {0}:
    $ python -m pip install "{0}<{5}"
""".format(NAME,
    *(REQUIRED_PYTHON_VERSION
    + CURRENT_PYTHON_VERSION
    + VERSION)))
    sys.exit(1)


with open("README.md", "r") as readme_file, open("LICENSE", "r") as licence_file:
    LONG_DESCRIPTION = readme_file.read() + licence_file.read()

CLASSIFIERS = [
    "License :: OSI Approved :: GNU General Public License version 3",
    f"Programming Language :: Python :: {REQUIRED_PYTHON_VERSION[0]}"
]
for version in range(REQUIRED_PYTHON_VERSION[0], LATEST_PYTHON_VERSION[0] + 1):
    for subversion in range(REQUIRED_PYTHON_VERSION[1], LATEST_PYTHON_VERSION[1] + 1):
        CLASSIFIERS.append(f"Programming Language :: Python :: {version}.{subversion}")

setuptools.setup(
    name=NAME,
    version="{}.{}.{}".format(*VERSION),
    author="Jones Murphy III",
    author_email="jones.murphy@outlook.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    keywords=f"{NAME} {' '.join(KEYWORDS)}",
    url=f"https://github.com/jmurphy61/{NAME}",
    packages=setuptools.find_packages(),
    license=LICENSE,
    classifiers=CLASSIFIERS,
    python_requires=">={}.{}".format(*REQUIRED_PYTHON_VERSION),
    install_requires=INSTALL_REQUIRES,
    entry_points={
        "console_scripts": [
            f"{NAME}={NAME}.__main__:main"
        ]
    },
    include_package_data=True
)