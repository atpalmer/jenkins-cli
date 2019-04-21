from setuptools import setup, find_packages


setup(
    name='jenkins-cli',
    packages=find_packages(),
    version='2019.4.9',
    install_requires=[
        'click',
        'python-dotenv',
        'requests',
    ],
    entry_points={
        'console_scripts': 'jenkins=jenkins.cli:main'
    },
)
