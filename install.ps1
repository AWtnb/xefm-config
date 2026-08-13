$d = ".xefm"
$dataPath = $env:USERPROFILE | Join-Path -ChildPath $d
$srcPath = $PSScriptRoot | Join-Path -ChildPath $d
New-Item -Path $dataPath -Value $srcPath -ItemType Junction -Force