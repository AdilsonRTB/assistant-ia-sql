from setuptools import setup, find_packages

setup(
    name='assistent-n6',
    version='0.1.0',
    packages=find_packages(),
    package_dir={"": "src"},
    install_requires=[
        'requests',
        'pandas',
        'pyodbc',
        'setuptools', 
        'flask',   
    ],
    entry_points={
        'console_scripts': [
            'assistent-n6=assistent-n6.main:main',
        ],
    },
)
