import os
import subprocess
from pathlib import Path
from dotenv import load_dotenv

# Load .env file where your PYPI_API_TOKEN is stored
load_dotenv()
pypi_token = os.getenv('PYPI_API_TOKEN')

# Set a default base directory
default_base_dir = os.getenv('BASE_URL')

# Step 1: Set up directories and files for a minimal package
def create_package_structure(base_dir, package_name, package_description):
    base_path = Path(base_dir)
    root = base_path / package_name
    root.mkdir(parents=True, exist_ok=True)

    # Create subdirectory for package
    (root / package_name).mkdir(exist_ok=True)

    # Create __init__.py for the package
    (root / package_name / '__init__.py').touch()

    # Create a minimal setup.py
    setup_content = f"""
from setuptools import setup, find_packages

setup(
    name='{package_name}',
    version='0.0.1',
    packages=find_packages(),
    description='{package_description}',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://example.com/{package_name}',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
"""
    (root / 'setup.py').write_text(setup_content.strip())

    # Create README.md
    (root / 'README.md').write_text(f"# {package_name}\n{package_description}")

    # Create LICENSE file (MIT license as an example)
    license_text = """
MIT License

Copyright (c) 2024 Your Name

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
... (truncated for brevity)
"""
    (root / 'LICENSE').write_text(license_text.strip())

# Step 2: Build the package
def build_package(base_dir, package_name):
    root = Path(base_dir) / package_name
    subprocess.run([f"{Path().resolve()}/venv/bin/python", 'setup.py', 'sdist', 'bdist_wheel'], cwd=root)

# Step 3: Upload only the .whl file to PyPI
def upload_package(base_dir, package_name):
    root = Path(base_dir) / package_name
    token_cmd = f"--repository-url https://upload.pypi.org/legacy/ -u __token__ -p {pypi_token}"

    # Install twine if not installed
    subprocess.run(["pip", "install", "twine"])

    # Upload only the .whl file
    subprocess.run(f"twine upload dist/*.whl {token_cmd}", cwd=root, shell=True)

if __name__ == "__main__":
    package_name = input("Enter the package name you want to reserve: ")
    package_description = input("Enter the description for your package: ")

    # Ask if user wants to use the default base directory
    use_default_base = input(f"Do you want to use the default base directory ({default_base_dir})? (y/n): ")

    if use_default_base.lower() == 'y':
        base_dir = default_base_dir
    else:
        base_dir = input("Enter the base directory where you want to create the package (e.g., D:/MyPackages): ")

    print("Creating package structure...")
    create_package_structure(base_dir, package_name, package_description)

    print("Building the package...")
    build_package(base_dir, package_name)

    print("Uploading the .whl package to PyPI...")
    upload_package(base_dir, package_name)

    print(f"Package {package_name} (.whl) with description '{package_description}' has been uploaded to PyPI!")
