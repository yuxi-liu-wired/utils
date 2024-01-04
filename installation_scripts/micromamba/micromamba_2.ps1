# Setting up the MAMBA_ROOT_PREFIX environment variable
$Env:MAMBA_ROOT_PREFIX="$HOME\micromambaenv"

# Displaying micromamba help
micromamba --help

# Invoking the shell hook
micromamba shell hook -s powershell | Out-String | Invoke-Expression

# Initializing the shell
micromamba shell init -s powershell -p $Env:MAMBA_ROOT_PREFIX

echo "Try `micromamba create -f mamba_math.yml` to see it working."
echo "Also, try adding to `~/.mambarc` "
echo "channels:"
echo " - conda-forge"
echo "always_yes: false "