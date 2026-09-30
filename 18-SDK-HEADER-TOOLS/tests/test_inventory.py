#!/usr/bin/env python3
import importlib.util, json, tempfile, unittest
from pathlib import Path

HERE=Path(__file__).resolve().parent
TOOL=HERE.parent/'tools'/'ae_sdk_inventory.py'
spec=importlib.util.spec_from_file_location('ae_sdk_inventory',TOOL)
mod=importlib.util.module_from_spec(spec)
import sys
sys.modules[spec.name]=mod
spec.loader.exec_module(mod)

class InventoryTest(unittest.TestCase):
    def test_fixture(self):
        data=mod.inventory([str(HERE/'fixture_header.h')])
        names={t['name'] for t in data['tables']}
        self.assertIn('AEGP_ExampleSuite2',names)
        self.assertIn('PF_TestSuite1',names)
        self.assertIn('AEIO_FunctionBlock4',names)
        funcs={f['name'] for t in data['tables'] for f in t['functions']}
        self.assertEqual({'AEGP_DoThing','AEGP_GetThing','PF_TestCallback','AEIO_InitInSpecFromFile'},funcs)
        self.assertEqual(4,data['function_count'])

if __name__=='__main__':
    unittest.main()
