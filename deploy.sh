#!/bin/bash

# deploy.sh
ACTION=${1:-"deploy"}
MSG=${2:-"Update deploy script"}

case "$ACTION" in
    "deploy")
        echo "Building Docker image and deploying container..."
        docker build -t wenfxl/wenfxl-codex-manager:latest . && \
        docker-compose down && \
        docker-compose up -d
        ;;
    "start")
        echo "Starting container..."
        docker-compose up -d
        ;;
    "stop")
        echo "Stopping container..."
        docker-compose down
        ;;
    "restart")
        echo "Restarting container..."
        docker-compose restart
        ;;
    "logs")
        echo "Viewing logs..."
        docker-compose logs -f
        ;;
    "push")
        echo "Pushing to remote repository..."
        git add . && \
        git commit -m "$MSG" && \
        git push
        ;;
    *)
        echo "Usage: ./deploy.sh [deploy|start|stop|restart|logs|push] ['commit message']"
        echo "Examples:"
        echo "  ./deploy.sh deploy  - Build image and start project"
        echo "  ./deploy.sh start   - Start project"
        echo "  ./deploy.sh stop    - Stop project"
        echo "  ./deploy.sh restart - Restart project"
        echo "  ./deploy.sh logs    - View project logs"
        echo "  ./deploy.sh push    - Commit and push changes to github"
        ;;
esac
