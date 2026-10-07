#!/usr/bin/env bash
# Optional local runner: move non-CI phase/p0 process configs into docs/archive/phases/.
# Does NOT move CI-held paths (batch01 semantic/overlap/snapshots, p0_materialization,
# p0_service_identity). Review ARCHIVE_INVENTORY.md before running.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
DEST_CFG="docs/archive/phases/config"
DEST_SNAP="docs/archive/phases/snapshots"
mkdir -p "$DEST_CFG" "$DEST_SNAP"

move_if_exists() {
  local src="$1" dest_dir="$2"
  if [ -e "$src" ]; then
    echo "MOVE $src -> $dest_dir/"
    git mv "$src" "$dest_dir/" || mv "$src" "$dest_dir/"
  fi
}

# Phase planning YAML
for f in config/phase_*.yaml config/v1_final_migration_gate.yaml config/canonical_root_migration.yaml; do
  move_if_exists "$f" "$DEST_CFG"
done

# Batch 02–04 (not batch01)
for f in config/p0_batch02_*.yaml config/p0_batch03_*.yaml config/p0_batch04_*.yaml; do
  move_if_exists "$f" "$DEST_CFG"
done
move_if_exists config/p0_batch04_snapshots "$DEST_SNAP"

# Geosite / source bridge process artifacts
for f in config/p0_geosite_*.yaml config/p0_source_bridge_*.yaml config/p0_source_bridge_evidence.yaml; do
  move_if_exists "$f" "$DEST_CFG"
done
move_if_exists config/p0_geosite_snapshots "$DEST_SNAP"
move_if_exists config/p0_source_snapshots "$DEST_SNAP"

echo "Done. Review git status; run CI build/publish dry paths before push."
echo "KEEP untouched: p0_batch01_*, p0_materialization.yaml, p0_service_identity.yaml"
