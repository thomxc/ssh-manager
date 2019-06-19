from setuptools import setup

setup(
    name='sshmanager',
    version='0.0.1',
    packages=['sshmanager'],
    url='https://github.com/thomxc/ssh-manager',
    license='MIT',
    author='Thomas Wiersema',
    author_email='thomas.wiersema@gmail.com',
    description='Easy SSH Manager with autocompletion',
    install_requires=[
        'prompt_toolkit',
        'fuzzyfinder'
    ],
    scripts=['bin/sshman']
)
