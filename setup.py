from setuptools import setup

setup(
    name="invisionChatboxBot",
    version="0.1",
    description='Convert Chegg url to complete html',
    packages=['invisionChatbox'],
    python_requires='>=3.8',
    install_requires=[
        'requests',
    ],
    package_data={},
    include_package_data=True
)