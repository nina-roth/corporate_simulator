from setuptools import setup, find_packages

setup(
    name="corporate_simulator",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'PyQt5',
        'pillow'
    ],
    entry_points={
        'console_scripts': [
            'corporate-simulator=src.app:main',
        ],
    }
)