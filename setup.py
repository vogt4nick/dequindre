from setuptools import setup, find_packages

setup(
    name='dequindre',
    version='0.2.0',
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
