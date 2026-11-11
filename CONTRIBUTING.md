# Contributing to SUAMS

## Team workflow

For a team of up to 12 developers, coordinate ownership of a task before coding and use one feature branch per task. Start branches from the team's agreed integration point (`main` unless the project lead has announced a temporary integration branch).

Use descriptive branch names, such as:

- `feature/student-registration`
- `feature/course-enrollment`
- `feature/result-processing`
- `feature/exam-routine`
- `feature/role-based-access`
- `fix/registration-capacity`
- `docs/scm-workflow`

Keep commits small and meaningful. Push the branch regularly, especially before requesting review. Do not commit credentials, real student records, generated environments, or unrelated changes.

## Pull requests and reviews

1. Rebase or merge the current integration branch into your feature branch and resolve conflicts before opening a PR.
2. Open a PR into `main` and use the repository PR template. Summarize the change, link the task or issue, and state what was tested.
3. Request review from at least one other developer. The author should address review comments and not approve their own PR.
4. Wait for the required GitHub Actions checks to pass and the review approval before merging.
5. Use the repository's configured merge strategy. Delete the feature branch after merge when it is no longer needed.
6. Verify the integrated application and tests after merging. Report failures and fix them in a follow-up PR.

Do not push directly to `main`. Repository administrators must enable a `main` branch ruleset or branch protection rule that requires a pull request and at least one approval, and require every matrix check from the `Tests` workflow (`Python 3.10` through `Python 3.14`). They should also block force pushes and deletion. These controls are configured in GitHub repository settings and cannot be enforced by files committed in this repository.

## Local checks

Run the same core checks as CI before requesting review:

```bash
python -m compileall -q .
python -m unittest discover -v
```

The GitHub Actions workflow runs these checks for pull requests targeting `main` and pushes to `main` on Python 3.10 through 3.14.

## Releases

Only the project lead should create release tags, after the merged code passes integration, system, and acceptance testing. Use semantic version tags (`vMAJOR.MINOR.PATCH`), for example `v1.0.0` for an initial release and `v1.1.0` for a backward-compatible feature release.

Create and push an annotated tag from the verified `main` commit:

```bash
git switch main
git pull --ff-only origin main
git tag -a v1.0.0 -m "SUAMS v1.0.0"
git push origin v1.0.0
```

Pushing the tag starts the `Release` workflow. It reruns compilation and the complete test suite on Python 3.10 through 3.14; only if every matrix job succeeds does it publish a GitHub Release with generated notes. The notes include the current known limitations and migration status. Review the release after publication and ensure the notes cover:

- Included features and fixes.
- Known limitations and any migration or configuration steps.
- The test and acceptance checks completed for the release.

SUAMS currently stores demo data in memory and has no database migrations.
