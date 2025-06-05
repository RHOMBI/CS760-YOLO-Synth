#!/usr/bin/env bash
set -euo pipefail

echo "→ PWD: $(pwd)"
mkdir -p logs
echo "→ logs/ created at $(pwd)/logs"

LOGFILE="logs/inference_$(date +'%Y%m%d_%H%M%S').log"

run_model(){
  local LABEL=$1
  local DIR=$2

  echo -e "\n\n=== $LABEL ===" | tee -a "$LOGFILE"

  python predict.py --model-path "$DIR/train/weights/best.pt" \
    2>&1 | tee -a "$LOGFILE"

  pushd mAP-master >/dev/null
    python main.py "$@" 2>&1 | tee -a "$LOGFILE"
  popd >/dev/null
}

run_model BASELINE   runs_baseline
run_model DIFFUSION  runs_diffusion
run_model ENGINE     runs_engine
run_model PERTURBED  runs_perturbed
run_model PSEUDO     runs_pseudo
run_model YARDS      runs_yards

echo "✔️  All done; full log at $LOGFILE"
