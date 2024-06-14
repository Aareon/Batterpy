# Ensure Python and PyInstaller are installed
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
    $pyinstallerVersion = & pyinstaller --version
    if ($LASTEXITCODE -ne 0) {
        Write-Host "PyInstaller is not installed. Installing PyInstaller..."
        pip install pyinstaller
    }
} catch {
    Write-Host "PyInstaller is not installed or not found in the system PATH. Installing PyInstaller..."
    pip install pyinstaller
}

# Define the paths
$mainScript = "__main__.py"
$batteryCheckScript = "Battery-Check.ps1"
$outputDir = "dist"

# Create the output directory if it doesn't exist
if (-Not (Test-Path $outputDir)) {
    New-Item -ItemType Directory -Path $outputDir
}

# Ensure the PowerShell script exists
if (-Not (Test-Path $batteryCheckScript)) {
    Write-Host "The PowerShell script '$batteryCheckScript' does not exist. Ensure it is in the current directory."
    exit 1
}

# Create a spec file for PyInstaller to include the PowerShell script
$specFileContent = @"
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(['$mainScript'],
             pathex=['.'],
             binaries=[],
             datas=[('$batteryCheckScript', '.')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='$($mainScript -replace ".py", "")',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='$($mainScript -replace ".py", "")')
"@

$specFilePath = "$mainScript.spec"
$specFileContent | Out-File -FilePath $specFilePath -Encoding UTF8

# Compile the Python script using PyInstaller with the spec file
try {
    & pyinstaller $specFilePath
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Compilation successful. The executable has been created in the 'dist' directory."
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
