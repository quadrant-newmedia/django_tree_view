import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('VERSION', 'r') as fh:
    version = fh.read()

setuptools.setup(
    name="django_tree_view",
    version=version,
    author="Alex Fischer",
    author_email="alex@quadrant.net",
    description="Organize your code and templates in a natural directory structure",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/quadrant-newmedia/django_tree_view",
    packages=['django_tree_view'],
    package_dir={'': 'src'},
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=["Django>=2.2,<4.3", "django-dynamic-path<1", "django_referer_csrf<1", "django_early_return<1", "backports-datetime-fromisoformat>=1.0.0"],
)