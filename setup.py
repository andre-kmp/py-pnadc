from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="py-pnadc", 
    version="0.1.2",
    author="André Klaic",
    author_email="andreklaic@gmail.com",
    description="Unofficial package for PNADC microdata (IBGE)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/andre-kmp/py-pnadc",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    install_requires=[
        "pandas",
        "fastparquet",
        "requests",
        "bs4",
        "urljoin",
        "chardet",
        "io",
        "zipfile",
        "os",
        "re"
    ],
)
