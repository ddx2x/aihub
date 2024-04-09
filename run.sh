build_paddle() {
  version=${2:-latest}
  docker buildx build --load -t aihub-paddle:$version ./paddle
  docker rm -f aihub-paddle
  docker run -dp 8000:8000 --name aihub-paddle aihub-paddle:$version
}

build_openai() {
  version=${2:-latest}
  docker buildx build --load -t harbor-pro.iauto360.cn/dengxiaopengtest/aihub-openai:$version ./openai
  docker push harbor-pro.iauto360.cn/dengxiaopengtest/aihub-openai:$version
}

version=$2
if [ -z "$version" ]; then
  version="latest"
fi

case $1 in
   # 飞浆平台
   b_paddle)
    echo "build aihub paddle"
    build_paddle ;;
    # openai
   b_openai)
    echo "build openai"
    build_openai ;;
  

   *) echo "Invalid argument '$1'. Please use start, stop, or restart." ;;
esac