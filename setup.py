from setuptools import setup, find_packages

version = {}
with open('./dequindre/version.py', 'r') as ifile:
    exec(ifile.read(), version)


setup(
    name='dequindre',
    version=version['__version__'],
    description="Dequindre: a lightweight scheduler.",
    long_description=open('readme.md').read(),
    url='https://github.com/vogt4nick/dequindre',
    author='Nick Vogt',
    author_email='vogt4nick@gmail.com',
    license='MIT',
    packages=["dequindre"],
    # install_requires='',
    test_suite='nose.collector',
    tests_require=['nose']
)
