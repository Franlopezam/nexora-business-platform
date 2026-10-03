from pathlib import Path
from datetime import datetime
import shutil

source = Path("nexora.db")
if not source.exists():
    raise SystemExit("nexora.db was not found.")

backup_dir = Path("backups")
backup_dir.mkdir(exist_ok=True)
target = backup_dir / f"nexora-{datetime.now():%Y%m%d-%H%M%S}.db"
shutil.copy2(source, target)
print(f"Backup created: {target}")
