# ---------------------------------------
# File: sqlite_check.ps1
# Usage: Run in PowerShell from project root
# ---------------------------------------

Write-Host " Checking your SQLite database..." -ForegroundColor Cyan

# Path to sqlite3.exe and DB file
$sqliteExe = ".\data\sqlite3.exe"
$dbPath = ".\data\translations.db"

# Check files exist
if (!(Test-Path $sqliteExe)) {
    Write-Host " sqlite3.exe not found at $sqliteExe" -ForegroundColor Red
    exit
}
if (!(Test-Path $dbPath)) {
    Write-Host " translations.db not found at $dbPath" -ForegroundColor Red
    exit
}

# Show table count
Write-Host "`n Row count:" -ForegroundColor Yellow
& $sqliteExe $dbPath "SELECT COUNT(*) FROM translations;"

# Show unique pairs
Write-Host "`n Unique (source_bn, reference_en) pairs:" -ForegroundColor Yellow
& $sqliteExe $dbPath "SELECT DISTINCT TRIM(source_bn), TRIM(reference_en) FROM translations;"

# Show top rows for quick review
Write-Host "`n Top 5 rows:" -ForegroundColor Yellow
& $sqliteExe $dbPath "SELECT id, TRIM(source_bn), TRIM(reference_en), translation, score, rank FROM translations ORDER BY id ASC LIMIT 5;"

# Prompt: Wipe data? (optional)
$wipe = Read-Host "`n Do you want to wipe ALL translations? (yes/no)"
if ($wipe -eq "yes") {
    & $sqliteExe $dbPath "DELETE FROM translations;"
    Write-Host " All rows deleted!" -ForegroundColor Green
} else {
    Write-Host "  No data deleted." -ForegroundColor DarkGray
}

Write-Host "`n Done!" -ForegroundColor Cyan
