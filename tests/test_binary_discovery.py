import shutil
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

sys.argv = ["penelope"]
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import penelope


class EchoingShell:
    OS = "Unix"

    def __init__(self):
        self._bin = defaultdict(str)

    def exec(self, command):
        result = subprocess.run(
            ["/bin/bash", "-c", command],
            capture_output=True,
            check=True,
        )
        # The interactive shell echoes the probe and drops empty output lines.
        lines = [line for line in result.stdout.splitlines() if line]
        return command.encode() + b"\n" + b"\n".join(lines) + b"\n"


session = EchoingShell()
paths = penelope.Session.bin.fget(session)
for name in ("sh", "bash", "python3", "uname", "stat", "df"):
    expected = shutil.which(name)
    actual = paths[name]
    assert actual == expected, f"{name}: expected {expected!r}, got {actual!r}"
print("binary discovery handles echoed probes and missing blank lines")
