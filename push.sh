#!/usr/bin/env bash
# Commit and push everything new in the workspace to github.com/ahmed-berrais/study.
#
#   ./push.sh                  # commit message is generated from what changed
#   ./push.sh "lab 3 notes"    # your own commit message
#
# .gitignore decides what is left out. Files over 95 MB are refused by GitHub,
# so they are added to .gitignore automatically instead of breaking the push.
set -euo pipefail
cd "$(dirname "$0")"

LIMIT=$((95 * 1024 * 1024))

git add -A

# Move any file too large for GitHub out of the commit and into .gitignore.
while IFS= read -r -d '' f; do
  [ -f "$f" ] || continue
  if [ "$(stat -c %s "$f")" -gt "$LIMIT" ]; then
    echo "⚠  too big for GitHub, ignoring: $f ($(du -h "$f" | cut -f1))"
    git rm -q --cached -- "$f"
    printf '%s\n' "$f" >> .gitignore
    git add .gitignore
  fi
done < <(git diff --cached --name-only -z --diff-filter=AM)

# Never let a secret through, even if .gitignore gets edited by mistake.
if git diff --cached --name-only | grep -qE '(^|/)\.env|(^|/)secrets/'; then
  echo "✗ a .env or secrets/ file is staged — refusing to push. Check .gitignore."
  git reset -q
  exit 1
fi

if git diff --cached --quiet; then
  echo "Nothing new to push."
  exit 0
fi

echo "Changes:"
git diff --cached --name-status | sed 's/^/  /'

if [ $# -gt 0 ]; then
  msg="$*"
else
  added=$(git diff --cached --name-only --diff-filter=A | wc -l)
  changed=$(git diff --cached --name-only --diff-filter=MR | wc -l)
  removed=$(git diff --cached --name-only --diff-filter=D | wc -l)
  msg="Update $(date '+%d-%m-%Y %H:%M'): $added added, $changed changed, $removed removed"
fi

git commit -q -m "$msg" -m "$(git diff --cached --name-status)"
git push -q origin main
echo "✓ pushed: $msg"
