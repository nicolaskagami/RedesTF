docker cp $2 mn.$1:/$2
docker exec -d mn.$1 sudo /root/Click -j4 /$2 DEV=$1 &
