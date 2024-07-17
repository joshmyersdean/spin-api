from setuptools import setup, find_packages

setup(
    name="spin-dataset-api",
    version="1.0.0",
    author="Josh Myers-Dean",
    author_email="josh.myers-dean@colorado.edu",
    description="A description of your package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/joshmyersdean/spin-api",
    packages=find_packages(),
    package_data={
        "spin.object_mapping": ["object_mapping.json"],
    },
    install_requires=[
        "numpy",
        "requests",
        "pillow",
        "matplotlib",
        "pycocotools",
        "opencv-python",
        "tqdm",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
