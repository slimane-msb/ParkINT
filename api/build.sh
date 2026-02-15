cp env-exemple .env
sudo docker-compose up


docker rm -vf $(docker ps -aq)
docker rmi -f $(docker images -aq)
sudo docker-compose up

docker system prune -y
docker volume prune -y
docker volume rm -f $(docker volume ls)
sudo docker-compose up