# Contribution Process

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

### Testing with Mocks for External Services
Much of Foundry's functionality involves interacting with external services like Globus (for authentication, search, and transfer) and the Materials Data Facility (MDF Connect for publishing). To ensure our tests are reliable, fast, and can run in offline environments (like CI), we extensively use mocking.

*   **Core Idea:** Instead of making real network calls in tests, we replace parts of our code (or the external libraries Foundry uses) with "mock" objects. These mocks simulate the behavior of the real services.
*   **Tools:** We primarily use Python's built-in `unittest.mock` library, often through the `pytest-mock` plugin which provides convenient fixtures (e.g., the `mocker` fixture).
*   **Where to Find Mocks:**
    *   Shared, reusable mocks for core components (like a mocked `Foundry` client instance or mock authorizers) are often defined as fixtures in `tests/conftest.py`. For example, `mock_foundry` provides a `Foundry` instance where authentication and other clients are already mocked.
    *   For specific tests, you might apply mocks directly using `mocker.patch(...)` or `@patch(...)` decorators.
*   **How It Works:**
    *   When testing a function that, for example, searches for datasets, we would mock the method on the `ForgeClient` that actually performs the search (e.g., `foundry_instance.forge_client.search`).
    *   We configure this mock to return a predefined, sample response (like a list of dataset metadata dictionaries).
    *   This allows us to test the logic of our function (how it processes the search results, how it handles errors, etc.) without relying on a live search backend or specific data existing there.
*   **Contributing Tests:** If you're adding a feature that interacts with an external service:
    *   Please include unit tests that use mocks to cover its behavior.
    *   Check `tests/conftest.py` and existing tests in `tests/` for examples of how to set up and use mocks for the services your feature touches.
    *   The goal is to make your tests deterministic and independent of external factors.

## Pull Request Process

1. Ensure any install or build dependencies are removed before the end of the layer when doing a

   build.

2. Update the README.md with details of changes to the interface, this includes new environment

   variables, exposed ports, useful file locations and container parameters.

3. Increase the version numbers in any examples files and the README.md to the new version that this

   Pull Request would represent. The versioning scheme we use is [SemVer](http://semver.org/).

4. You may merge the Pull Request in once you have the sign-off of two other developers, or if you

   do not have permission to do that, you may request the second reviewer to merge it for you.

