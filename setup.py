from setuptools import setup, find_packages

setup(
    name="colormaestro",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click",
        "pillow",
        "jinja2",
    ],
    entry_points={
        "console_scripts": [
            "colormaestro=colormaestro.cli:cli",
        ],
    },
    package_data={
        "colormaestro": ["templates/*.html"],
    },
)
