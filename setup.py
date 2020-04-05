from setuptools import setup, find_packages
import pathlib

setup(
    name='random_graph',
    version='0.0.0a0',
    author='James Ross',
    author_email='jamespatross@gmail.com',
    description='Sample random bipartite graphs to test for simple-ness',
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    package_dir={'': 'src'},
    # packages=["src"],
    packages=find_packages("src"),
    install_requires=['numpy >= 1.11.1', "networkx", "tqdm"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
        'Programming Language :: Python :: 3.8'
    ],
)