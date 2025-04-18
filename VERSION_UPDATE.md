# Version Update Guide

When you're ready to release a new version of the package, follow these steps:

## 1. Update version numbers

Update the version number in **two places**:

1. In `setup.py`:
   ```python
   setup(
       name="vit-captioner",
       version="0.1.0",  # Change this to the new version
       ...
   )
   ```

2. In `vit_captioner/__init__.py`:
   ```python
   __version__ = "0.1.0"  # Change this to the new version
   ```

## 2. Create a GitHub release

1. Go to your GitHub repository
2. Click on "Releases" in the right sidebar
3. Click "Create a new release" or "Draft a new release"
4. Tag version: `v0.1.0` (replace with your new version number)
5. Release title: `Version 0.1.0` (replace with your new version number)
6. Description: Add release notes, changes, etc.
7. Click "Publish release"

## 3. Wait for automatic publishing

The GitHub Action will automatically:
1. Build the package
2. Publish it to PyPI

You can check the progress by going to the "Actions" tab in your GitHub repository.

## 4. Verify PyPI publication

Visit https://pypi.org/project/vit-captioner/ to verify that your new version has been published.

## Semantic Versioning Guide

For version numbering, follow [Semantic Versioning](https://semver.org/):

- **MAJOR.MINOR.PATCH** (e.g., 1.2.3)
- Increment PATCH for backwards-compatible bug fixes
- Increment MINOR for new backwards-compatible functionality
- Increment MAJOR for incompatible API changes

Examples:
- 0.1.0 → 0.1.1 (bug fixes)
- 0.1.1 → 0.2.0 (new features, no breaking changes)
- 0.2.0 → 1.0.0 (stable release or breaking changes)