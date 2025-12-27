# Release Workflow

This project uses automated semantic versioning and releases.

## How It Works

### 1. Development Workflow
- Create a feature branch from `master`
- Make changes with conventional commits:
  - `feat:` - New feature (minor version bump)
  - `fix:` - Bug fix (patch version bump)
  - `docs:`, `chore:`, etc. - No version bump
- Create PR to `master`
- Tests run automatically
- Merge PR after approval

### 2. Automated Release Process

When code is merged to `master`:

1. **Release workflow triggers** (`.github/workflows/release.yml`)
   - Analyzes commits since last release
   - Determines next version using semantic-release
   - Creates a release PR with version bump

2. **Release PR created** (`release-v{version}`)
   - Updates `pyproject.toml` version
   - Updates `src/csv2iif/__init__.py` version
   - Generates changelog in `RELEASE_NOTES.md`
   - Tests run automatically

3. **Manual approval required**
   - Review and approve the release PR
   - Merge the PR

4. **Create release workflow triggers** (`.github/workflows/create-release.yml`)
   - Creates git tag `v{version}`
   - Builds distribution packages
   - Creates GitHub release with artifacts

## Version Bumping Rules

- `feat:` commits → Minor version (1.0.0 → 1.1.0)
- `fix:` commits → Patch version (1.0.0 → 1.0.1)
- `BREAKING CHANGE:` in commit body → Major version (1.0.0 → 2.0.0)
- Other commits (`docs:`, `chore:`, etc.) → No release

## Manual Release

To manually trigger a release:

```bash
gh workflow run release.yml
```

## Requirements

- Branch protection enabled on `master`
- Required status check: `test`
- Required approvals: 1
- `RELEASE_TOKEN` secret configured (Personal Access Token with repo permissions)

## Testing the Workflow

1. Make a change with a conventional commit
2. Push to master or merge a PR
3. Wait for release PR to be created
4. Approve and merge the release PR
5. Verify tag and release are created automatically
