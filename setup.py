import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="django_tree_view",
    version="0.1.0",
    author="Alex Fischer",
    author_email="alex@quadrant.net",
    description="Organize your code and templates in a natural directory structure",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/quadrant-newmedia/django_tree_view",
    packages=['django_tree_view', 'django_tree_view.tests'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=["Django>=2.2,<3.1", "django-dynamic-path>=0.0.4<1", "django_referer_csrf<1", "django_early_return<1"],
)