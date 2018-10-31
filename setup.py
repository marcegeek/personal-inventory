import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="personal_inventory",
    version="0.0.1",
    author="Marcelo Castellano",
    author_email="marce.geek22@gmail.com",
    description="Web application for managing an inventory of personal items",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/marcegeek/personal-inventory",
    packages=['personal_inventory', 'personal_inventory.data',
              'personal_inventory.logic', 'personal_inventory.presentation'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'sqlalchemy',
        'flask',
        'email_validator',
        'gunicorn',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
