<#
.SYNOPSIS
    Batch-run inference + mAP eval for MINOVERLAP=0.1→0.9, logging per-run files.
#>

param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$ScriptArgs
)

# 1) Where this script lives
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition

# 2) Ensure logs folder exists
$LogDir = Join-Path $ScriptDir 'logs'
if (-not (Test-Path $LogDir)) {
    New-Item -ItemType Directory -Path $LogDir | Out-Null
}

# 3) Absolute paths to your scripts
$PredictPy = Join-Path $ScriptDir 'predict.py'
$MainPy    = Join-Path $ScriptDir 'mAP-master' 'main.py'

# 4) Models to process
$models = @(
    @{ Label='BASELINE';  Dir='runs_baseline'  },
    @{ Label='DIFFUSION'; Dir='runs_diffusion2' },
    @{ Label='ENGINE';    Dir='runs_engine'    },
    @{ Label='PERTURBED'; Dir='runs_perturbed' },
    @{ Label='PSEUDO';    Dir='runs_pseudo'    },
    @{ Label='YARDS';     Dir='runs_yards'     },
    @{ Label='ORIGINAL';     Dir='runs_original'     },
    @{ Label='YARDS_ORIGINAL';     Dir='runs_yards_original'     }
)

# 5) Loop 0.1 → 0.9
#for ($i = 1; $i -le 9; $i++) {
for ($i = 1; $i -le 1; $i++) {
    #$min    = [math]::Round($i/10, 1)
    $min = 0.5
    $minStr = $min.ToString('0.0')
    $ignoreClasses = @(2)
    $LogFile = Join-Path $LogDir "inference_minOverlap_$minStr.log"

    # Header
    "`n`n=== MINOVERLAP = $minStr ===" |
      Tee-Object -FilePath $LogFile -Append |
      Write-Host

    foreach ($m in $models) {
        $label = $m.Label
        $dir   = Join-Path $ScriptDir $m.Dir

        # Section marker
        "`n--- $label ---" | Tee-Object -FilePath $LogFile -Append | Write-Host

        # 1) inference (no --min-overlap here)
        python predict.py --model-path "$dir\train\weights\best.pt" 2>&1 | Tee-Object -FilePath $LogFile -Append

        # 2) mAP evaluation: script path *first*, then --min-overlap as two args
        python mAP-master/main.py --min-overlap $minStr --ignore $ignoreClasses 2>&1 | Tee-Object -FilePath $LogFile -Append
    }

    Write-Host "Completed MINOVERLAP=$minStr; log at $LogFile"
}

Write-Host "`nAll experiments done."
