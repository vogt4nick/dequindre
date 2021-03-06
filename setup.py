from setuptools import setup, find_packages


version = {}
with open('./dequindre/__init__.py', 'r') as ifile:
    exec(ifile.read(), version)

setup(
    name='dequindre',
    version=version['__version__'],
    description="Dequindre /de-KWIN-der/ (n.): A minimalist scheduler.",
    long_description=open('readme.rst').read(),
    long_description_content_type="text/x-rst",
    url='https://github.com/vogt4nick/dequindre',
    author='Nick Vogt',
    author_email='vogt4nick@gmail.com',
    packages=["dequindre"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
    ],
    include_package_data=True
)
