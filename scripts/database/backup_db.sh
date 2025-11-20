#!/usr/bin/env bash
set -euo pipefail

# 默认连接信息，可通过环境变量覆盖
PGHOST=${PGHOST:-localhost}
PGPORT=${PGPORT:-5432}
PGUSER=${PGUSER:-replay_user}
PGDATABASE=${PGDATABASE:-replay_db}
PGPASSWORD=${PGPASSWORD:-replay_password}

BACKUP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)/backups"
mkdir -p "$BACKUP_DIR"

STAMP=$(date +"%Y%m%d_%H%M%S")
OUTPUT_FILE="${BACKUP_DIR}/replay_db_${STAMP}.dump"

echo "Backing up ${PGDATABASE} to ${OUTPUT_FILE}"
PGPASSWORD=$PGPASSWORD pg_dump \
  -h "$PGHOST" \
  -p "$PGPORT" \
  -U "$PGUSER" \
  -F c \
  -b \
  -v \
  -f "$OUTPUT_FILE" \
  "$PGDATABASE"

echo "Backup complete."

