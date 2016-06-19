proc=$(docker stats --no-stream $1  | tail -n 1 | awk '{print $2}' | cut -d '.' -f1)
if [ $proc -le "60" ];
then
   exit 0
else
   exit 1
fi
