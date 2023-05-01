from setuptools import find_packages, setup

version = "0.0.1"

setup(
    name="picklr",
    version=version,
    description="Rate my ratings.",
    packages=find_packages(),
    test_suite="tests",
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "flask==2.3.2",
        "scrython",
        "flask-sqlalchemy",
        "flask-migrate",
        "uwsgi",
    ],
)
