paddle() {
  version=${2:-latest}
  docker buildx build --load -t aihub-paddle:$version ./paddle
  docker rm -f aihub-paddle
  docker run -dp 8000:8000 --name aihub-paddle aihub-paddle:$version
}

openai() {
  version=${2:-latest}
  docker buildx build --load -t aihub-openai:$version ./openai
  docker rm -f aihub-openai
  docker run -dp 8001:8000 --name aihub-openai aihub-openai:$version
}

case $1 in
   # 飞浆平台
   paddle)
    echo "build aihub paddle"
    paddle ;;
    # openai
   openai)
    echo "build openai"
    openai ;;
  

   *) echo "Invalid argument '$1'. Please use start, stop, or restart." ;;
esac