from setuptools import setup, find_packages

setup(
    name='aptc',
    packages=find_packages(),
    version='0.0.1',
    license='MIT',
    description='A simple web3py like client for APTOS chain.',
    author='Yong',
    author_email='ackness8@gmail.com',
    url='https://github.com/ackness/aptc',
    python_requires=">=3.7",
    keywords=['apt', 'aptos', 'block chain', 'web3'],
    install_requires=[
        'httpx', 'PyNaCl'
    ]
)
