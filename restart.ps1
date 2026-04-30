# InstaGuard Restart Script
# ─────────────────────────────────────────────────────────────────
# Use this to restart all containers WITHOUT deleting the database.
# Your user accounts and scan history will be preserved.
#
# NEVER use: docker-compose down -v
# That flag deletes the pg_data volume (all your data).
# ─────────────────────────────────────────────────────────────────

Write-Host "InstaGuard: Restarting containers (data preserved)..." -ForegroundColor Cyan

Set-Location "$PSScriptRoot"

# Stop containers — NO -v flag so pg_data volume is kept
docker-compose down

# Rebuild images and start
docker-compose up --build -d

Write-Host ""
Write-Host "Done! InstaGuard running at http://localhost:3000" -ForegroundColor Green
Write-Host "Your login credentials and scan history are preserved." -ForegroundColor Green
