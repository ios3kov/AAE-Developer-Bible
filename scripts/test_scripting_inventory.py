import unittest
from audit_scripting_inventory import members


class ScriptingInventoryTests(unittest.TestCase):
    def test_member_headings_and_duplicates(self):
        self.assertEqual(members("### Item.setGuide()\n### Item.setGuide()\n"
                                 "### Property.valueText\n## Other.x\n"
                                 "### Not a member\n"),
                         ["Item.setGuide", "Property.valueText"])

    def test_enum_namespace_preserved(self):
        self.assertEqual(members("### Property.LayerInputStageType\n"),
                         ["Property.LayerInputStageType"])


if __name__ == "__main__":
    unittest.main()
