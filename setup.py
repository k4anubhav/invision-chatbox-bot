from setuptools import setup, find_packages

setup(
    name="invisionChatboxBot",
    version="0.1.9",
    description='Convert Chegg url to complete html',
    packages=find_packages(),
    python_requires='>=3.8',
    install_requires=[
        'requests',
    ],
    package_data={},
    include_package_data=True
)