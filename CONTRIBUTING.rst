.. highlight:: shell

============
Contributing
============

Contributions are welcome, and they are greatly appreciated! Every
little bit helps, and credit will always be given.

You can contribute in many ways:

Types of Contributions
----------------------

Report Bugs
~~~~~~~~~~~

Report bugs at https://github.com/Hugovdberg/PIconnect/issues.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

Fix Bugs
~~~~~~~~

Look through the GitHub issues for bugs. Anything tagged with "bug"
and "help wanted" is open to whoever wants to implement it.

Implement Features
~~~~~~~~~~~~~~~~~~

Look through the GitHub issues for features. Anything tagged with
"enhancement" and "help wanted" is open to whoever wants to implement it.

Write Documentation
~~~~~~~~~~~~~~~~~~~

PIconnect could always use more documentation, whether as part of the
official PIconnect docs, in docstrings, or even on the web in blog posts,
articles, and such.

Submit Feedback
~~~~~~~~~~~~~~~

The best way to send feedback is to file an issue at https://github.com/Hugovdberg/PIconnect/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

Get Started!
------------

Ready to contribute? Here's how to set up `PIconnect` for local development.

1. Fork the `PIconnect` repo on GitHub.
2. Clone your fork locally::

    $ git clone git@github.com:your_name_here/PIconnect.git

3. Install your local copy into a virtualenv. Assuming you have pipenv
installed, this is how you set up your fork for local development::

    $ cd PIconnect/
    $ pipenv sync -d
    $ pipenv install -e .

4. Create a branch for local development::

    $ git checkout -b name-of-your-bugfix-or-feature

   Now you can make your changes locally.

5. When you're done making changes, format the code with black, check that your changes
pass pylint and the tests, including testing other Python versions with tox::

    $ black PIconnect
    $ pylint PIconnect tests
    $ python setup.py test or py.test
    $ tox

   Pylint and tox will be installed automatically by pipenv.

6. Commit your changes and push your branch to GitHub::

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

7. Submit a pull request through the GitHub website.

Pull Request Guidelines
-----------------------

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs should be updated. Put
   your new functionality into a function with a docstring, and add the
   feature to the list in README.rst.
3. The pull request should work for Python 3.6, 3.7, 3.8 and 3.9. Testing is automated
   through GitHub Actions, so you get feedback on your pull request where things are not
   up to standards.

Tips
----

To run a subset of tests::

$ py.test tests.test_piconnect
