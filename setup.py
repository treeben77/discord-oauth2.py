from setuptools import setup

with open("README.md", "r") as file:
    long_description = file.read()

setup(
    name='discord-oauth2.py',
    description='Use Discord\'s OAuth2 effortlessly! Turns the auth code to a access token and the access token into scope infomation. ',
    version="1.0.0",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    python_requires='>=3.8',
    author="TreeBen77",
    packages=[
        'discordoauth2'
    ],
    url='https://github.com/TreeBen77/discordoauth2',
    keywords='flask, oauth2, discord, discord-api',
    install_requires=[
        'requests'
    ]
)
