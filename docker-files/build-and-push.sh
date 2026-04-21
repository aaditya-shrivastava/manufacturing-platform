#!/bin/bash
# ============================================================
#  build-and-push.sh
#  Builds 3 Docker images and pushes them to Docker Hub.
#
#  Usage:
#    chmod +x build-and-push.sh
#    ./build-and-push.sh
#
#  Prerequisites:
#    - docker login   (run once before this script)
# ============================================================

set -e  # Exit immediately on any error

# ------- CONFIGURE THESE -------
DOCKERHUB_USERNAME="dockeruser2004"   # <-- replace with your Docker Hub username
VERSION="1.0.0"                                 # <-- bump this on every release
# --------------------------------

IMAGE_1="$DOCKERHUB_USERNAME/manufacturing-creator:$VERSION"
IMAGE_2="$DOCKERHUB_USERNAME/multi-agent-manufacturing:$VERSION"
IMAGE_3="$DOCKERHUB_USERNAME/main-app:$VERSION"

echo "========================================"
echo " Building & Pushing 3 Docker Images"
echo " Version : $VERSION"
echo " User    : $DOCKERHUB_USERNAME"
echo "========================================"

# ── Image 1: manufacturing-creator ──
echo ""
echo "[1/3] Building $IMAGE_1 ..."
docker build -f docker-files/Dockerfile.manufacturing-creator -t "$IMAGE_1" .
echo "[1/3] Pushing $IMAGE_1 ..."
docker push "$IMAGE_1"

# ── Image 2: multi-agent-manufacturing ──
echo ""
echo "[2/3] Building $IMAGE_2 ..."
docker build -f docker-files/Dockerfile.multi-agent-manufacturing -t "$IMAGE_2" .
echo "[2/3] Pushing $IMAGE_2 ..."
docker push "$IMAGE_2"

# ── Image 3: main-app ──
echo ""
echo "[3/3] Building $IMAGE_3 ..."
docker build -f docker-files/Dockerfile.main-app -t "$IMAGE_3" .
echo "[3/3] Pushing $IMAGE_3 ..."
docker push "$IMAGE_3"

echo ""
echo "========================================"
echo " All images pushed successfully!"
echo ""
echo " Images available on Docker Hub:"
echo "   $IMAGE_1"
echo "   $IMAGE_2"
echo "   $IMAGE_3"
echo ""
echo " Next step: Deploy to EC2 with Kubernetes"
echo "========================================"
