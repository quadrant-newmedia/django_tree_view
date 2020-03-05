import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="django_tree_view",
    version="0.0.0",
    author="Alex Fischer",
    author_email="alex@quadrant.net",
    description="TODO",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # url="TODO - github repo",
    packages=['django_tree_view', 'django_tree_view.tests'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    # TODO - this doesn't work -> I guess you can't use "editable" requirements in here
    # We'll need to put these up on pypi, or create our own
    install_requires=["Django>=2.2,<3.1", "-e git+ssh://localhost:/Users/alex/projects/pip_packages/django_dynamic_path@0eb32fee4197d2aa6565813b1885c77eedb65880#egg=django_dynamic_path", "-e git+ssh://localhost:/Users/alex/projects/pip_packages/django_referer_csrf@e94fef25db9c8c0dcbf17792563adb30f1040447#egg=django_referer_csrf"],
)