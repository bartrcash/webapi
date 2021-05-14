set -e

# image name
IMAGE_NAME="bartrcash/webapi"

# stop container
echo "Stoping container..."

CONTAINER_ID=$(docker ps -q --filter ancestor=$IMAGE_NAME )

if [ $CONTAINER_ID ]
then
    set -x
    docker stop $CONTAINER_ID
    set +x

    echo "Containter stopped."
else
    echo "Containter not found."
fi


# delete container
echo "Deleting container...."

CONTAINER_ID=$(docker ps --all -q --filter ancestor=$IMAGE_NAME )  

if [ $CONTAINER_ID ]
then
    set -x
    docker rm $CONTAINER_ID
    set +x
    echo "Containter deleted."
else
    echo "Containter not found."
fi

# delete image
echo "Deleting image...."
IMAGE_ID=$(docker images  --filter reference=$IMAGE_NAME  --format "{{.ID}}" )

if [ $IMAGE_ID ]
then
    set -x
    docker rmi $IMAGE_ID
    set +x
    echo "Image deleted."
else
    echo "Image not found."
fi

# get lastest image
echo "Getting the last version...."
set -x
docker pull $IMAGE_NAME
set +x

# run image
echo "Running image...."
set -x
docker run -p 5000:80 -d $IMAGE_NAME
set +x

# End
echo "Docker tasks completed :)"