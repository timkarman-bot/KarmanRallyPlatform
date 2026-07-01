# Karman Kar Shows Guide for Codex

This project is the public web platform for Karman Kar Shows & Events.

## Local project path

```text
C:\Karman_Kar\karman-kar-shows
```

## Current purpose

The platform supports car shows and event operations, including:

- Public show pages.
- Participant registration.
- Attendee information capture.
- Sponsor interest and sponsor information.
- Charity/community follow-up.
- Admin tools.
- Voting, including participant-only or judge-only restrictions when configured.
- Contact exports and consent-aware lead handling.

## Repository

Current GitHub repository:

```text
git@github.com:timkarman-bot/KarmanRallyPlatform.git
```

Use SSH remotes rather than HTTPS.

## Important release context

Recent release work included:

- Participant and attendee opt-ins for event, sponsor, and charity follow-up.
- Admin contact exports.
- Participant/judge restricted voting.
- CSRF and role protection improvements.
- Mobile/navigation improvements.
- No-active-show and expired-upcoming-show messaging.
- Documentation and release history updates.

When changing this project:

- Increment the version number for release-worthy changes.
- Update `docs/CHANGELOG.md` and `docs/RELEASE_HISTORY.md` when applicable.
- Preserve consent language and privacy-conscious contact handling.
- Keep voting restrictions configurable by show.
- Test date/status logic carefully, especially stale upcoming shows.
- Keep the public experience simple and clear for participants, attendees, sponsors, and charities.

## Deployment workflow

Typical PowerShell flow:

```powershell
cd C:\Karman_Kar\karman-kar-shows
git status -sb
git add .
git commit -m "Release x.y.z-beta: short accurate description"
git push origin main
```

Railway should redeploy from GitHub after the push.

If `git push` says `Everything up-to-date`, check whether a commit was actually created:

```powershell
git status -sb
git log --oneline -5
```

Common typo to avoid:

```powershell
git commit
```

not:

```powershell
it commit
```

