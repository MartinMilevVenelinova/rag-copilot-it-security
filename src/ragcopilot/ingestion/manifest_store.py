from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from ragcopilot.ingestion.models import Manifest


def write_manifest(path: Path, manifest: Manifest) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    data = manifest.to_dict()
    content = json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True)

    path.write_text(content + "\n", encoding="utf-8")


def read_manifest(path: Path) -> Optional[Manifest]:
    if not path.exists():
        return None

    data = json.loads(path.read_text(encoding="utf-8"))
    return Manifest.from_dict(data)