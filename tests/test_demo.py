"""Testy bez pytest - wystarcza biblioteka standardowa Python."""

import contextlib
import io
import json
import runpy
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from pw_databricks_demo.job import calculate_sales, main  # noqa: E402


EXPECTED = {"days": 7, "orders": 112, "revenue_pln": 2744, "best_day": 7}


class DemoTests(unittest.TestCase):
    def test_wheel_module(self):
        self.assertEqual(calculate_sales(), EXPECTED)

    def test_script_output(self):
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            runpy.run_path(str(ROOT / "scripts" / "sales_job.py"), run_name="__main__")
        self.assertEqual(json.loads(buffer.getvalue()), EXPECTED)

    def test_notebook_output(self):
        notebook = json.loads((ROOT / "notebooks" / "sales_job.ipynb").read_text())
        namespace = {"__name__": "__main__"}
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            for cell in notebook["cells"]:
                if cell["cell_type"] == "code":
                    exec(compile("".join(cell["source"]), "sales_job.ipynb", "exec"), namespace)
        self.assertEqual(json.loads(buffer.getvalue()), EXPECTED)

    def test_wheel_entrypoint_output(self):
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            main()
        self.assertEqual(json.loads(buffer.getvalue()), EXPECTED)


if __name__ == "__main__":
    unittest.main()
