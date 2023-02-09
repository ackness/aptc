from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='aptc',
    packages=find_packages(),
    version='0.0.3',
    license='MIT',
    description='A simple web3py like client for APTOS chain.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Yong',
    author_email='ackness8@gmail.com',
    url='https://github.com/ackness/aptc',
    python_requires=">=3.7",
    keywords=['apt', 'aptos', 'block chain', 'web3'],
    install_requires=[
        'httpx', 'PyNaCl'
    ]
)
