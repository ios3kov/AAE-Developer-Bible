param(
  [Parameter(Mandatory=$true)][string]$SdkExamples,
  [string]$Compiler = "cl.exe"
)

$ErrorActionPreference = "Stop"
$Here = Split-Path -Parent $MyInvocation.MyCommand.Path
$Root = Resolve-Path (Join-Path $Here "..")
$SdkExamples = (Resolve-Path $SdkExamples).Path
$SdkHeaders = Join-Path $SdkExamples "Headers"
$AeEffect = Join-Path $SdkHeaders "AE_Effect.h"
$Out = Join-Path $Here "generated\local-sdk"

if (-not (Test-Path $AeEffect -PathType Leaf)) {
  throw "Expected SDK Examples\Headers\AE_Effect.h"
}

if (-not (Get-Command $Compiler -ErrorAction SilentlyContinue)) {
  throw "MSVC compiler '$Compiler' not found. Run from a Visual Studio Developer Command Prompt / VsDevCmd environment."
}

New-Item -ItemType Directory -Force -Path $Out | Out-Null
$Inventory = Join-Path $Out "ae-sdk-inventory.json"
$Markdown = Join-Path $Out "ae-sdk-inventory.md"
$CompileReport = Join-Path $Out "native-compile-report.json"

py (Join-Path $Here "tools\ae_sdk_inventory.py") `
  $SdkHeaders `
  --json $Inventory `
  --markdown $Markdown
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

py (Join-Path $Here "tools\verify_required_contracts.py") `
  $Inventory `
  (Join-Path $Here "sdk25.6-required-contracts.json")
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

py (Join-Path $Here "tools\verify_recipe_symbols.py") `
  $Inventory `
  (Join-Path $Here "..\17-NATIVE-SUITE-COOKBOOK\code")
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

py (Join-Path $Root "scripts\check_native.py") `
  $SdkExamples `
  --compiler $Compiler `
  --compiler-style msvc `
  --report $CompileReport `
  --require-clean
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "Gate-4 local SDK lane: inventory + symbol-name + MSVC syntax/type checks PASS"
Write-Host "No link, PiPL load, AE host execution or runtime semantics were tested."
