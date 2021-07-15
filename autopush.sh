git add .
if [[ $2 ]]; then
  git commit -m "$2"
else
  git commit -m "autopush"
fi
git push
