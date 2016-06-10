bash ~/containernet/bin/clear_crash.sh
docker rm $(docker ps -q -f status=exited)
