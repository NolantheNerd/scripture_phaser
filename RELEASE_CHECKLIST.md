# Release Checklist

For the sake of consistency, this is how a release of scripture_phaser should be done.

1. Increment the VERSION and RELEASE DATE in variables in `src/enums.py`.

2. Update the version in `pyproject.toml`

3. Successfully merge your PR from your feature branch into `master`.

4. If the release constitutes a patch release, merge `master` into the existing `MAJOR.MINOR.x` branch. Otherwise, branch off of `master` into a new branch with the name `MAJOR.MINOR.x`.

5. Make sure that you don't have a preexisting dist folder in the root of the scripture_phaser repository. On the `MAJOR.MINOR.x` branch, run: `python -m build`.

6. From the root of the scripture_phaser repository, run: `python -m twine upload --repository pypi dist/*`.

7. Tag the commit on the `MAJOR.MINOR.x` branch with the MAJOR.MINOR.PATCH version number. `git tag MAJOR.MINOR.PATCH COMMIT`

8. Push the tag to GitHub. `git push tag MAJOR.MINOR.PATCH`.

9. Create a release on GitHub by clicking the tags button to the right of the branch selection dropdown. Provide a detailed description of the release and select the tag that was just pushed to mark the release. Upload the contents of the dist folder in the scripture_phaser directory to the release.
