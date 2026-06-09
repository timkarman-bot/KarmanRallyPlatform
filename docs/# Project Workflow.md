# Project Workflow

Karman Kar Shows Platform

---

## Development Process

1. Create feature branch or work on main.
2. Implement change.
3. Update documentation.
4. Run validation.
5. Commit.
6. Push.
7. Verify Railway deployment.
8. Verify production operation.

---

## Required Validation

Before every deployment:

python -m py_compile app.py database.py utils/print_cards.py

Verify:

- Registration
- Admin login
- Car search
- Placeholder page
- Show page
- Voting page

---

## Version Management

Update:

APP_VERSION

Example:

APP_VERSION = "0.8.4-beta"

---

## Documentation Requirements

Every deployment requires:

### CHANGELOG.md

Update release notes.

### RELEASE_HISTORY.md

Update historical record.

### SCALING_ROADMAP.md

Update if architecture changes.

---

## Railway Deployment Procedure

1. Commit changes.
2. Push to GitHub.
3. Verify Railway deployment.
4. Check logs.
5. Validate production.

Commands:

git add .
git commit -m "Description"
git push origin main

---

## Production Verification

Verify:

/admin
/admin/car-search
/admin/placeholders
/admin/version

---

## Rollback Procedure

Identify last stable commit:

git log --oneline

Rollback:

git checkout COMMIT_ID

or

git revert COMMIT_ID

---

## Documentation Rule

No release is complete until:

- Code deployed
- Version updated
- Documentation updated
- Production validated