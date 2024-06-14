# Ensure Python and Nuitka are installed
try {
    $pythonVersion = & python --version
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Python is not installed. Please install Python before proceeding."
        exit 1
    }
} catch {
    Write-Host "Python is not installed or not found in the system PATH. Please install Python before proceeding."
    exit 1
}

try {
    $nuitkaVersion = & nuitka --version
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Nuitka is not installed. Installing Nuitka..."
        pip install nuitka
    }
} catch {
    Write-Host "Nuitka is not installed or not found in the system PATH. Installing Nuitka..."
    pip install nuitka
}

# Define the paths
$mainScript = "__main__.py"
$batteryCheckScript = "Battery-Check.ps1"
$outputDir = "dist"

# Create the output directory if it doesn't exist
if (-Not (Test-Path $outputDir)) {
    New-Item -ItemType Directory -Path $outputDir
}

# Copy the PowerShell script to the output directory
if (-Not (Test-Path $batteryCheckScript)) {
    Write-Host "The PowerShell script '$batteryCheckScript' does not exist. Ensure it is in the current directory."
    exit 1
}

Copy-Item $batteryCheckScript -Destination $outputDir

# Compile the Python script using Nuitka
$nuitkaCommand = @(
    "--standalone",
    "--onefile",
    "--include-data-file=$batteryCheckScript=$outputDir\$batteryCheckScript",
    "--output-dir=$outputDir",
    $mainScript,
    "--enable-plugin=tk-inter"
)

try {
    & nuitka $nuitkaCommand
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Compilation successful. The executable has been created in the '$outputDir' directory."
    } else {
        Write-Host "Compilation failed. Please check the output for errors."
        exit 1
    }
} catch {
    Write-Host "Compilation failed. Please check the output for errors."
    exit 1
}

# Check if the executable was created successfully
$exeName = [System.IO.Path]::GetFileNameWithoutExtension($mainScript) + ".exe"
if (Test-Path "$outputDir\$exeName") {
    Write-Host "Executable created successfully: $outputDir\$exeName"
} else {
    Write-Host "Executable not found in the output directory. Something went wrong."
    exit 1
}
