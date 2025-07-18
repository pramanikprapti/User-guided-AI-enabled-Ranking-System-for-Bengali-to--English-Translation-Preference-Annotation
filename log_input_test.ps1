# --------------------------------------------
# log_input_test.ps1
# --------------------------------------------

#  This script tests the /log_input endpoint via cURL
# and hits your FastAPI server running on localhost:8001

$bengali = Read-Host "Enter Bengali"
$english = Read-Host "Enter English"

$jsonBody = @{
    source_bn = $bengali
    reference_en = $english
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "http://127.0.0.1:8001/log_input" `
    -Method POST `
    -Body $jsonBody `
    -ContentType "application/json"

Write-Host "`nServer response:" $response.message
