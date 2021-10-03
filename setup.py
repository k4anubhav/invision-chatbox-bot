from setuptools import setup, find_packages

setup(
    name="invisionChatboxBot",
    version="0.3.1",
    description='Allows to make bots for invison community chatbox',
    packages=find_packages(),
    python_requires='>=3.8',
    install_requires=[
        'requests',
    ],
    package_data={},
    include_package_data=True
)
