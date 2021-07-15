git add .
if $1; then
  git commit -m "$1"
else
  git commit -m "autopush"
fi
git push
