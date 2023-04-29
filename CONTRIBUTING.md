# Contributing Guidelines

Contributions are welcome via GitHub Pull Requests. This document outlines the process to help get your contribution accepted.

Any type of contribution is welcome; from new features, bug fixes, [tests](#testing), documentation improvements.

## How to Contribute

1. Fork this repository, develop, and test your changes.
2. Submit a pull request.


### Technical Requirements

When submitting a pull request, please make sure your changes meet the following requirements:

- Must pass CI jobs.
- Must be formatted with [Black](https://github.com/psf/black)
- Must follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) guidelines.
- Must be documented with [Google Style Docstrings](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings).

#### Sign Your Work

The sign-off is a simple line at the end of the explanation for a commit. All commits needs to be signed. Your signature certifies that you wrote the patch or otherwise have the right to contribute the material. The rules are pretty simple, you only need to certify the guidelines from [developercertificate.org](https://developercertificate.org/).

Then you just add a line to every git commit message:

    Signed-off-by: Ricardo Domenzain <rdomenzain@example.com>

Use your real name (sorry, no pseudonyms or anonymous contributions.)

If you set your `user.name` and `user.email` git configs, you can sign your commit automatically with `git commit -s`.

Note: If your git config information is set properly then viewing the `git log` information for your commit will look something like this:

```
Author: Ricardo Domenzain <rdomenzain@example.com>
Date:   Thu Dic 2 11:41:15 2022 -0800
    Update README
    Signed-off-by: Ricardo Domenzain <rdomenzain@example.com>
```

Notice the `Author` and `Signed-off-by` lines match. If they don't your PR will be rejected by the automated DCO check.


### Documentation Requirements

- Update Gitlab Pages documentation if needed.
- Update README.md if needed.

### PR Approval and Release Process

1. Changes are manually reviewed by team members.
2. When the PR passes all tests, the PR is merged by the reviewer(s) in the GitHub `master` branch.
3. Then our CI/CD pipeline will automatically publish a new version to PyPI.