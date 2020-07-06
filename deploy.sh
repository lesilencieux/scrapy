docker stop app_scripy
docker rm app_scripy
docker rmi app_scripy_img
docker build -t app_scripy_img .
docker run -p 8585:8585 --name app_scripy --restart always -d app_scripy_img
