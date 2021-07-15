git add .
if [ "$1" ]; then
 echo  
  git commit -m \""$@"\"
else
  git commit -m "autopush"
fi
git push
