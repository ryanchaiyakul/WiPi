import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="WiPi",
    version="0.0.5",
    author="Ryan Chaiyakul",
    description="A general use class based WPA network manager",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ryanchaiyakul/WiPi",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'netifaces>=0.10.9',
        'psutil>=5.6.7',
        'PyAccessPoint>=0.2.5',
        'wireless>=0.3.3'
    ],
    python_requires='>=3.6',
    include_package_data=True,
)
