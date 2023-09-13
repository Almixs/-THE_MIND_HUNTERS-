from setuptools import setup, find_packages

setup(
    name='assistant',
    version='1.1',
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'assistant': [
            'assistant = assistant.__main__:run_main_menu'
        ]
    }
)