# Create temporary directory
New-Item -ItemType Directory -Force -Path MicroMambaTemp
cd MicroMambaTemp

# Downloading micromamba latest version
Invoke-WebRequest -URI https://micro.mamba.pm/api/micromamba/win-64/latest -OutFile micromamba.tar.bz2

# Extracting the downloaded file
tar xf micromamba.tar.bz2

# Moving the micromamba executable
$targetDir = "C:\Program Files\micromamba"
New-Item -ItemType Directory -Force -Path $targetDir
Move-Item -Force Library\bin\micromamba.exe $targetDir\micromamba.exe

# Adding micromamba to system PATH
$path = [System.Environment]::GetEnvironmentVariable("Path", "Machine")
$newPath = "$path;$targetDir"
[System.Environment]::SetEnvironmentVariable("Path", $newPath, "Machine")

# Setting up the MAMBA_ROOT_PREFIX environment variable
$Env:MAMBA_ROOT_PREFIX="$HOME\micromambaenv"

# Remove temporary files
cd ..
Remove-Item -Force -Recurse -Path MicroMambaTemp

# Setting alias for micromamba
# The alias doesn't FUCKING WORK
# If (-Not (Test-Path $PROFILE)) { 
#     New-Item -Type File -Force $PROFILE 
# }
# Add-Content -Path $PROFILE -Value "Set-Alias -Name mamba -Value `$(Join-Path '$targetDir' 'micromamba.exe')"

echo "Restart PowerShell and run micromamba_2.ps1 to complete the installation."
