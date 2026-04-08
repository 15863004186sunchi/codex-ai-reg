param (
    [string]$action = "deploy",
    [string]$msg = "Update deploy script"
)

switch ($action) {
    "deploy" {
        Write-Host "Building Docker image and deploying container..."
        docker build -t wenfxl/wenfxl-codex-manager:latest . ; docker-compose down ; docker-compose up -d
    }
    "start" {
        Write-Host "Starting container..."
        docker-compose up -d
    }
    "stop" {
        Write-Host "Stopping container..."
        docker-compose down
    }
    "restart" {
        Write-Host "Restarting container..."
        docker-compose restart
    }
    "logs" {
        Write-Host "Viewing logs..."
        docker-compose logs -f
    }
    "push" {
        Write-Host "Pushing to remote repository..."
        git add . ; git commit -m $msg ; git push
    }
    default {
        Write-Host "Usage: .\deploy.ps1 [deploy|start|stop|restart|logs|push] [-msg 'commit message']"
        Write-Host "Examples:"
        Write-Host "  .\deploy.ps1 deploy  - Build image and start project"
        Write-Host "  .\deploy.ps1 start   - Start project"
        Write-Host "  .\deploy.ps1 stop    - Stop project"
        Write-Host "  .\deploy.ps1 restart - Restart project"
        Write-Host "  .\deploy.ps1 logs    - View project logs"
        Write-Host "  .\deploy.ps1 push    - Commit and push changes to github"
    }
}
