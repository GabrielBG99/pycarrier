from setuptools import setup, find_packages


def requirements() -> list[str]:
    with open('requirements.txt', mode='r') as f:
        data = f.read()

    return data.split('\n')


setup(
    name='pycarrier',
    version='0.1.0',
    python_requires='>=3.9.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements(),
    entry_points="""
        [console_scripts]
        pycarrier=pycarrier.main:main
    """
)
