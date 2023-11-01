$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Definition

$pythonSrriptName = "login.py"

$pythonSrriptPath = Join-Path -Path $scriptPath -ChildPath $pythonSrriptName

if (Test-Path $pythonSrriptPath -PathType Leaf){
  python $pythonSrriptPath
}else{
  Write-Host "file not exit"
}