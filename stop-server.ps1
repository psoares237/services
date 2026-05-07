$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$pidFile = Join-Path $projectRoot ".server.pid"

if (-not (Test-Path $pidFile)) {
    Write-Host "Nenhum PID salvo em '$pidFile'."
    return
}

$pidText = Get-Content $pidFile -ErrorAction SilentlyContinue
if (-not $pidText) {
    Remove-Item $pidFile -Force
    Write-Host "Arquivo de PID vazio removido."
    return
}

$pid = [int]$pidText
$process = Get-Process -Id $pid -ErrorAction SilentlyContinue

if ($process) {
    Stop-Process -Id $pid -Force
    Write-Host "Servidor parado. PID: $pid"
} else {
    Write-Host "PID $pid nao esta mais ativo."
}

Remove-Item $pidFile -Force -ErrorAction SilentlyContinue
