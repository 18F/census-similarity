from setuptools import setup, find_packages

setup(
    name="census_similarity",
    version="master",
    packages=find_packages(),
    classifiers=[
        'License :: Public Domain',
        'License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication'
    ],
    install_requires=[
        "click",
        "distance",
        "numpy",
        "scipy",    # must be before scikit-learn
        "scikit-learn"
    ],
    entry_points={"console_scripts": [
        'cluster_by_field = census_similarity.commands:cluster_by_field',
        'group_by = census_similarity.commands:group_by',
        'lookup = census_similarity.commands:lookup',
    ]}
)
