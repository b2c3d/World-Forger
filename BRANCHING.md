# World Forger — Branch Strategy

Both the **code repo** (private) and this **docs repo** (public) follow the same branch conventions so it's always clear which documentation state matches which code state.

## Branch Map

```
main        ← RELEASED. Tagged at every Asset Store release.
develop     ← Next release staging. Default working branch.
feature/*   ← Individual features. Branch off develop, merge back to develop.
hotfix/*    ← Urgent fixes. Branch off main, merge into BOTH main AND develop.
```

## ⚠️ Docs-Specific Rule

**Never push to `main` in this repo unless intentionally publishing.**
Every push to `main` triggers GitHub Actions and deploys immediately to the live public site at `https://b2c3d.github.io/World-Forger/`.

All work-in-progress documentation goes on `develop` or a `feature/*` branch.

## Common Workflows

### Day-to-day doc writing
```bash
git checkout develop
# edit docs...
git add docs/
git commit -m "docs: describe what changed"
# DO NOT push to main
```

### Start a feature doc branch (mirrors a code feature branch)
```bash
git checkout develop
git checkout -b feature/feature-name
```

### Finish a feature (merge into develop)
```bash
git checkout develop
git merge --no-ff feature/feature-name
git branch -d feature/feature-name
```

### Publish (only when explicitly requested)
```bash
git checkout main
git merge develop
git push origin main        # deploys to live site
git checkout develop        # return to develop immediately
```

### Hotfix a live doc error
```bash
git checkout main
git checkout -b hotfix/description
# fix...
git checkout main && git merge --no-ff hotfix/description
git push origin main        # deploys fix immediately
git checkout develop && git merge --no-ff hotfix/description
git branch -d hotfix/description
```

## Branch Naming Conventions

| Prefix | Purpose | Example |
|--------|---------|---------|
| `feature/` | New content for an upcoming feature | `feature/runtime-api` |
| `hotfix/` | Urgent fix to live docs | `hotfix/broken-link` |
| `develop` | Next release staging | — |
| `main` | Live / released | — |
