from setuptools import setup, find_namespace_packages


setup(
    name='auto-pangolin',
    version='0.1.0-alpha-1',
    packages=find_namespace_packages(),
    entry_points={
        "console_scripts": [
            "auto-pangolin = auto_pangolin.__main__:main",
        ]
    },
    scripts=[],
    package_data={
    },
    install_requires=[
    ],
    description=' Automated lineage assignment of SARS-CoV-2 sequence data using Pangolin',
    url='https://github.com/BCCDC-PHL/auto-pangolin',
    author='Dan Fornika',
    author_email='dan.fornika@bccdc.ca',
    include_package_data=True,
    keywords=[],
    zip_safe=False
)
