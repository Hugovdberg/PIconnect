"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# To use a consistent encoding
from codecs import open
from os import path
# Always prefer setuptools over distutils
from setuptools import setup, find_packages

HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(HERE, 'README.rst'), encoding='utf-8') as readme_file:
    README = readme_file.read()

with open(path.join(HERE, 'HISTORY.rst'), encoding='utf-8') as history_file:
    HISTORY = history_file.read()


REQUIREMENTS = [
    'pythonnet',
    'future'
    # 'Click>=6.0',
    # TODO: put package requirements here
]

SETUP_REQUIREMENTS = [
    'pytest-runner',
    # TODO(Hugovdberg): put setup requirements (distutils extensions, etc.) here
]

TEST_REQUIREMENTS = [
    'pytest',
    # TODO: put package test requirements here
]

setup(
    name='PIconnect',
    version='0.6.0',
    description="Python connector to OSIsoft PI SDK",
    long_description=README + '\n\n' + HISTORY,

    # Author details
    author='Hugo van den Berg',
    author_email='hugo.van.den.berg@brabantwater.nl',
    url='https://github.com/Hugovdberg/PIconnect',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(include=['PIconnect']),
    include_package_data=True,
    install_requires=REQUIREMENTS,
    license="MIT license",
    zip_safe=False,
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Database',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        # 'Programming Language :: Python :: 3',
        # 'Programming Language :: Python :: 3.3',
        # 'Programming Language :: Python :: 3.4',
        # 'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=TEST_REQUIREMENTS,
    setup_requires=SETUP_REQUIREMENTS,

    # What does your project relate to?
    keywords='OSIsoft PI ProcessInformation PIconnect',

    # Alternatively, if you want to distribute just a my_module.py, uncomment
    # this:
    #   py_modules=["my_module"],

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    # install_requires=['peppercorn'],

    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    extras_require={
        'dev': ['check-manifest'],
        'test': ['coverage', 'nose'],
    },

    # If there are data files included in your packages that need to be
    # installed, specify them here.  If using Python 2.6 or less, then these
    # have to be included in MANIFEST.in as well.
    package_data={
        # 'sample': ['package_data.dat'],
    },

    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages. See:
    # http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files # noqa
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    # data_files=[('my_data', ['data/data_file'])],

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    # entry_points={
    #     'console_scripts': [
    #         'piconnect=PIconnect.cli:main'
    #     ]
    # },
)
