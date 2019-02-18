from setuptools import setup, find_packages

version = {}
with open('./dequindre/__init__.py', 'r') as ifile:
    exec(ifile.read(), version)

setup(
    name='dequindre',
    version=version['__version__'],
    description="Dequindre: a lightweight scheduler.",
    long_description=open('readme.md').read(),
    long_description_content_type="text/markdown",
    url='https://github.com/vogt4nick/dequindre',
    author='Nick Vogt',
    author_email='vogt4nick@gmail.com',
    packages=["dequindre"],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent"
    ],
    include_package_data=True,
    # install_requires='',
    test_suite='nose.collector',
    tests_require=['nose']
)
