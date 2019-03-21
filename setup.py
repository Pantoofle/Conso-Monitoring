import setuptools

with open("README.md", "r") as file_handle:
    long_description = file_handle.read()

setuptools.setup(
    name='wirelessconso',
    version='1.0',
    author="Simon Fernandez",
    description="A toolbox for modelizing wireless interfaces and measuring the power consumption of each interface",
    long_description=long_description,
    packages=setuptools.find_packages()
)
