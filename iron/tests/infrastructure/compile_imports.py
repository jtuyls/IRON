# SPDX-FileCopyrightText: Copyright (C) 2026 Advanced Micro Devices, Inc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""Compile-time MHA imports must not require torch."""

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def test_mha_imports_without_torch():
    env = os.environ.copy()
    env["PYTHONPATH"] = os.pathsep.join([str(ROOT), env.get("PYTHONPATH", "")])
    script = r"""
import sys

class _BlockTorch:
    def find_spec(self, name, path=None, target=None):
        if name == "torch" or name.startswith("torch."):
            raise ModuleNotFoundError(name)
        return None

sys.meta_path.insert(0, _BlockTorch())
import iron.operators.mha.op
"""
    completed = subprocess.run(
        [sys.executable, "-c", script],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr
