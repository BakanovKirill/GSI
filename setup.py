from setuptools import setup, find_packages

setup(
    name="gsi",
    version="1.0",
    url='https://github.com/BakanovKirill/GSI',
    license='BSD',
    description="GSI application.",
    author='Kirill Bakanov',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=['setuptools'],
)
