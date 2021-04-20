import setuptools

setuptools.setup(
    name="random_graph",
    version="0.0.0a1",
    author="James Ross",
    author_email="jamespatross@gmail.com",
    description="Fast, approximately uniform, random sampling for graphs.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    package_dir={"": "src"},
    packages=setuptools.find_packages("src"),
    install_requires=["tqdm"],
    tests_require=["pytest", "pytest-cov", "coverage"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7" "Programming Language :: Python :: 3.8",
    ],
)
