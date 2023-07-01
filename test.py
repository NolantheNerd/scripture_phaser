import unittest
from colour_runner.runner import ColourTextTestRunner
from scripture_phaser.test.test_agents import AgentsTests
from scripture_phaser.test.test_passage import PassageTests
from scripture_phaser.test.test_verse import VerseTests

suite = unittest.TestSuite()

suite.addTest(AgentsTests("test_esvapi_agent"))
suite.addTest(AgentsTests("test_kjvapi_agent"))
suite.addTest(AgentsTests("test_webapi_agent"))
suite.addTest(AgentsTests("test_bbeapi_agent"))

suite.addTest(VerseTests("test_validate"))
suite.addTest(VerseTests("test_show"))

suite.addTest(PassageTests("test_validate_verse_pair"))
suite.addTest(PassageTests("test_clean_reference"))
suite.addTest(PassageTests("test_interpret_reference"))
suite.addTest(PassageTests("test_reference_to_verses"))
suite.addTest(PassageTests("test_populate"))
suite.addTest(PassageTests("test_show"))

if __name__ == "__main__":
    ColourTextTestRunner(verbosity=2).run(suite)
