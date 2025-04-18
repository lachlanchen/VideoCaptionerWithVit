# Uploading to PyPI

This guide explains how to upload your package to PyPI.

## Prerequisites

1. Create a PyPI account at https://pypi.org/account/register/
2. Install the required tools:
   ```bash
   pip install build twine
   ```

## Manual Upload Process

### 1. Update version information (optional)

If you want to set a specific version instead of using the date-based versioning:

- Open `setup.py`
- Change the version from `f"0.1.{current_date}"` to a specific version like `"0.1.0"`

### 2. Build the package

```bash
python -m build
```

This will create two files in the `dist/` directory:
- A source distribution (`.tar.gz`)
- A wheel distribution (`.whl`)

### 3. Check the built package

```bash
twine check dist/*
```

This checks for any issues with your package files.

### 4. Upload to TestPyPI (recommended testing step)

```bash
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```

You'll be prompted for your TestPyPI username and password.

Then test the installation from TestPyPI:

```bash
pip install --index-url https://test.pypi.org/simple/ vit-captioner
```

### 5. Upload to PyPI

```bash
twine upload dist/*
```

You'll be prompted for your PyPI username and password.

## Automated Upload with GitHub Actions

You can also use GitHub Actions to automate the upload process:

1. Store your PyPI API token as a GitHub secret:
   - Go to your GitHub repository
   - Click on "Settings" > "Secrets" > "New repository secret"
   - Name it `PYPI_API_TOKEN`
   - Get the token from your PyPI account settings

2. Create a new GitHub release:
   - Go to your repository on GitHub
   - Click on "Releases" > "Create a new release"
   - Tag version: `v0.1.0` (or whatever version you're releasing)
   - Release title: `Version 0.1.0`
   - Description: Add release notes
   - Click "Publish release"

3. The GitHub Actions workflow will automatically:
   - Run tests
   - Build the package
   - Upload to PyPI

## Updating Your Package

To update your package on PyPI:

1. Make your changes to the code
2. Update the version number in `setup.py`
3. Rebuild and reupload the package using the steps above

## Common Issues

### Package name already exists

If the name `vit-captioner` is already taken on PyPI, you can:
- Choose a different name like `vit-video-captioner`
- Update your package name in `setup.py`

### Missing dependencies

Make sure all dependencies are listed in `setup.py`. If users report missing dependencies, add them to the `install_requires` list.

### Package is not installing correctly

Test your package installation in a clean virtual environment before uploading to PyPI.