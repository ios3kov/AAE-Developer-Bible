param(
  [Parameter(Mandatory=$true)][string]$SdkHeaders
)
$ErrorActionPreference = "Stop"
$Here = Split-Path -Parent $MyInvocation.MyCommand.Path
$Out = Join-Path $Here "generated\local-sdk"
New-Item -ItemType Directory -Force -Path $Out | Out-Null
$Inventory = Join-Path $Out "ae-sdk-inventory.json"
$Markdown = Join-Path $Out "ae-sdk-inventory.md"
py (Join-Path $Here "tools\ae_sdk_inventory.py") $SdkHeaders --json $Inventory --markdown $Markdown
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
py (Join-Path $Here "tools\verify_recipe_symbols.py") $Inventory (Join-Path $Here "..\17-NATIVE-SUITE-COOKBOOK\code")
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host "native SDK validation: PASS"
