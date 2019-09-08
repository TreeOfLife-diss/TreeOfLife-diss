# How to contribute

## Bugs and suggestions

Use the in the [issues tab](https://github.com/TreeOfLife-diss/TreeOfLife-diss/issues) to report bugs, give suggestions and rise discussions.

## Projects

The developing route of Tree-of-Life is registered and organized in the [Projects tab](https://github.com/TreeOfLife-diss/TreeOfLife-diss/projects). Browse it freely to see to where the project is heading and if you wish to conbribute to a given topic, just let us now by raising an issue.

## Code Style

Style your code following PEP8 rules, some necessary exceptions are allowed for the Tree-of-Life project. The following `flake8` options enforce the coding style: `flake8 --hang-closing --ignore=W293,W503,E402`. Please follow these rules when submitting Pull Requests.

```
W293 blank line contains whitespaces
W503 line break before binary operator, actually favoured by PEP8
E402 module level import not at top of file, in Tree-of-Life sometimes is necessary to import later on
-hang-closing, allows:
my_func(
    var1,
    var2,
    )
```

## Pull Request

- **Always** submit a Pull Request from a forked repository.
- Pull Requests title should start with a proposal of version change and, if helpful, followed by a short title: `v1.3.12 - corrected bug in updater`
  - follow versioning according to [Semantic Versioning 2.0](https://semver.org/#semantic-versioning-200): MAJOR.MINOR.PATCH
  - new version number should be updated in the [README.md](https://github.com/TreeOfLife-diss/TreeOfLife-diss/blob/master/README.md) file.
- Pull Request description should state the added improvements and corrections.
- Pull Request should close issues whenever applicable.

_Thanks!_
