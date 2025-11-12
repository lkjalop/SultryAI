import os
import subprocess
from pathlib import Path


def test_check_max_lines_detects_long_file(tmp_path, monkeypatch):
    # create a small repo structure
    repo = tmp_path / "repo"
    repo.mkdir()
    long_file = repo / "long.json"
    # write 20 lines
    long_file.write_text('\n'.join([str(i) for i in range(20)]))

    # run the script with MAX_LINES=10 so 20 > 10 triggers
    env = os.environ.copy()
    env['MAX_LINES'] = '10'

    script = Path(__file__).resolve().parent.parent / 'scripts' / 'check_max_lines.py'
    res = subprocess.run(['python', str(script)], cwd=repo, env=env, capture_output=True, text=True)
    assert res.returncode == 2
    assert 'FILE_TOO_LONG' in res.stdout or 'Found' in res.stdout
