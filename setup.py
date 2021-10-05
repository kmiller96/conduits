import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="conduits",
    version="0.1.1",
    author="Kale Miller",
    url="https://github.com/kmiller96/conduits",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    install_requires=[
        "pandas",
        "networkx[default]",
        "joblib",
    ],
)
