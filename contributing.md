# Contributing

When contributing to this repository, please first discuss the change you wish to make via issue, email, or any other method with the owners of this repository before making a change.

Please note we have a code of conduct, please follow it in all your interactions with the project.

## Contributing code

If you have improvements to Foundry, send us your pull requests! For those just getting started, Github has a [how to](https://help.github.com/articles/using-pull-requests/).

If you want to contribute, start working through the Foundry codebase, navigate to the [Github "issues" tab](https://github.com/MLMI2-CSSI/foundry/issues) and start looking through interesting issues. If you are not sure of where to start, then start by trying one of the smaller/easier issues here i.e. [issues with the "good first issue" label](https://github.com/MLMI2-CSSI/foundry/labels/good%20first%20issue). These are issues that we believe are particularly well suited for outside contributions. If you want to help out, but not alone, use the issue comment thread to coordinate.

### General guidelines and philosophy for contribution

* Include unit tests when you contribute new features, as they help to a\)

  prove that your code works correctly, and b\) guard against future breaking

  changes to lower the maintenance cost.

* Bug fixes also generally require unit tests, because the presence of bugs

  usually indicates insufficient test coverage.

* Keep API compatibility in mind when you change code in Foundry,
* When you contribute a new feature to Foundry, the maintenance burden is

  \(by default\) transferred to the Foundry team. This means that the benefit

  of the contribution must be compared against the cost of maintaining the

  feature.

* Tests should follow [testing best practices](https://www..org/community/contribute/tests)

  guide.

## Pull Request Process

1. Ensure any install or build dependencies are removed before the end of the layer when doing a 

   build.

2. Update the README.md with details of changes to the interface, this includes new environment 

   variables, exposed ports, useful file locations and container parameters.

3. Increase the version numbers in any examples files and the README.md to the new version that this

   Pull Request would represent. The versioning scheme we use is [SemVer](http://semver.org/).

4. You may merge the Pull Request in once you have the sign-off of two other developers, or if you 

   do not have permission to do that, you may request the second reviewer to merge it for you.

