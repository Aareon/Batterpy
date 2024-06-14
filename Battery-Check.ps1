param (
    [string]$ReportPath = "C:\battery-report.html",
    [switch]$HideConsole = $false
)

# Function to check if the script is running with admin privileges
function Test-Administrator {
    $currentUser = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
    return $currentUser.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

# Function to restart the script with elevated privileges
function Restart-Elevated {
    param (
        [string]$ScriptPath,
        [string]$ReportPath,
        [switch]$HideConsole
    )
    
    $arguments = "-ReportPath `"$ReportPath`""
    if ($HideConsole) {
        $arguments += " -HideConsole"
    }
    $startInfo = New-Object System.Diagnostics.ProcessStartInfo
    $startInfo.FileName = "powershell"
    $startInfo.Arguments = "-NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File `"$ScriptPath`" $arguments"
    $startInfo.Verb = "runas"
    $process = [System.Diagnostics.Process]::Start($startInfo)
    $process.WaitForExit()
}

# Main script logic
if (-not (Test-Administrator)) {
    if ($HideConsole) {
        Write-Output "Script is not running with administrative privileges. Restarting with elevated privileges..."
    }
    Restart-Elevated -ScriptPath $MyInvocation.MyCommand.Path -ReportPath $ReportPath -HideConsole:$HideConsole
    exit
}

# Run the powercfg command to generate the battery report
powercfg /BATTERYREPORT /OUTPUT $ReportPath /XML /DURATION 45

# Notify the user of the report location
Write-Output "Battery report generated and saved to $ReportPath"

# Pause to prevent the prompt from closing automatically
if (-not $HideConsole) {
    Write-Output "Press any key to exit..."
    [System.Console]::ReadKey() | Out-Null
}
