for dir in $(ls $1); do
#  echo $dir
  if [ -d $1/$dir ]; then
    cd $1/$dir && rename 's/_.*\)/_1/' *
    cd ../../
  fi
done
