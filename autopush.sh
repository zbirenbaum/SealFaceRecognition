git add .
if [ "$1" ]; then
  git commit -m '$@'
else
  git commit -m "autopush"
fi
git push
