# log_input_interactive.ps1
# Run this AFTER starting your log_inputs_api.py on port 8001

# Prompt user
$source_bn = Read-Host "Enter Bengali"
$reference_en = Read-Host "Enter English"

# Build JSON
$body = @{
    source_bn = $source_bn
    reference_en = $reference_en
} | ConvertTo-Json

# Send POST request
$response = Invoke-RestMethod -Uri "http://127.0.0.1:8001/log_input" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"

# Show server result
Write-Host "`nServer response:" $response.message -ForegroundColor Cyan
