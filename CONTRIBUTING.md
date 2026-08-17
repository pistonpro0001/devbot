# Contributing

First, thank you for wanting to spend your time helping make this project better! It's very appreciated <3

## Requirements

1. By making PR, you agree that your code will be published under the [MIT License](https://opensource.org/license/MIT).
2. You agree to our [No LLM](#no-llm) rule.
3. You agree to follow the [style guidelines](#style-guidelines) when making changes to the code.

### No LLM

Due to the current [black-box nature of LLMs](https://archive.ph/2026.03.06-144058/https://alexeyondata.substack.com/p/how-i-dropped-our-production-database), a bad [impact on the environment](https://en.wikipedia.org/wiki/Environmental_impact_of_AI), legal issues (such as [no copyright mentions in the generated codes from GitHub Copilot](https://githubcopilotinvestigation.com/)) and many other problems, any commits, issues or PRs must not contain LLM responses and/or a help from LLM. Even if it was reviewed by a human, it will be rejected.

## Guidelines

Create an issue, if you...

- Noticed a bug or a typo.
- Want to propose a new feature.

Create a PR, if you...

- Want to improve the documentation.

Create an issue and PR, if you...

- Know how to realize the feature or fix the bug you found.

If none of these cases are yours, then create an issue about your case and we'll discuss it.

### Style Guidelines

The project follows [PEP 8](https://peps.python.org/pep-0008/). The only change is a maximum line length: limit all lines to a maximum of 120 symbols.

## Developing

### Setting up the developing environment

Before making any changes, you must to set up the developing environment.

First of all, you need to install the [project's tooling](#tooling). If you don't have some of the tools, follow the instructions on the corresponding pages.

When all tools are installed, clone the repo, `cd` into the folder and sync all dependencies by `uv`:

```bash
uv sync --all-groups
```

Then we need to install the `prek`'s `pre-commit`. The `pre-commit` hook will help to mitigate the typical mistakes like forgetting to use the formatter or run the unit tests. To do this, run this command:

```bash
prek install
```

Done!

To test the bot, run this:

```bash
pytest
```

If you want to measure a code coverage, run the test command with a `--cov` flag. For example, here's a command to run the unit tests and measure a code coverage of the `main` module:

```bash
pytest --cov='./main.py'
```

### Tooling

The project uses the following tools:

- Package manager: [uv](https://docs.astral.sh/uv/)
- Linter and formatter: [Ruff](https://docs.astral.sh/ruff/)
- Type checker: [mypy](https://mypy-lang.org/)
- Test runner: [pytest](https://docs.pytest.org/)
- Coverage: [Coverage.py](https://coverage.readthedocs.io/)
- `pre-commit` framework: [`prek`](https://prek.j178.dev/)

## Security

Send security issues to one of the authors' emails: [piston.pro0001@gmail.com](mailto:piston.pro0001@gmail.com) or [romanmashevskyi@proton.me](mailto:romanmashevskyi@proton.me).
