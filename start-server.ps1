param(
    [string]$BindAddress = "0.0.0.0",
    [int]$Port = 8000
)

$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$python = Join-Path $projectRoot "venv\Scripts\python.exe"
$manage = Join-Path $projectRoot "manage.py"
$pidFile = Join-Path $projectRoot ".server.pid"
$stdoutLog = Join-Path $projectRoot "server.out.log"
$stderrLog = Join-Path $projectRoot "server.err.log"

if (-not (Test-Path $python)) {
    throw "Python do virtualenv nao encontrado em '$python'."
}

if (Test-Path $pidFile) {
    $existingPid = Get-Content $pidFile -ErrorAction SilentlyContinue
    if ($existingPid) {
        $existingProcess = Get-Process -Id $existingPid -ErrorAction SilentlyContinue
        if ($existingProcess) {
            Write-Host "Servidor ja esta rodando no PID $existingPid."
            Write-Host "Log: $stdoutLog"
            return
        }
    }
}

$arguments = @(
    $manage,
    "runserver",
    "$BindAddress`:$Port",
    "--noreload"
)

$process = Start-Process `
    -FilePath $python `
    -ArgumentList $arguments `
    -WorkingDirectory $projectRoot `
    -WindowStyle Hidden `
    -RedirectStandardOutput $stdoutLog `
    -RedirectStandardError $stderrLog `
    -PassThru

$process.Id | Set-Content $pidFile

Write-Host "Servidor iniciado em http://$BindAddress`:$Port/"
Write-Host "PID: $($process.Id)"
Write-Host "Logs: $stdoutLog , $stderrLog"
