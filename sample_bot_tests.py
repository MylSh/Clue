import unittest
from sample_bot import SampleBot
from clue_game import Accusation, Location, Suggestion, Suspect, Weapon


class TestNameMethod(unittest.TestCase):
    def test_name(self):
        sample_bot = SampleBot()
        self.assertEqual(sample_bot.name(), 'sample_bot')


class TestRespondToSuggestionMethod(unittest.TestCase):
    sample_bot = SampleBot()
    sample_bot.initialize(0, 6, [Location.BALLROOM], [Suspect.COLONEL_MUSTARD,
                                                      Suspect.REVEREND_GREEN])

    def test_respond_to_suggestion(self):
        # A suggestion that sample_bot can refute
        self.assertEqual(
            self.sample_bot.
            respond_to_suggestion(1, Suggestion(Suspect.COLONEL_MUSTARD,
                                                Location.BALLROOM,
                                                Weapon.CANDLESTICK)),
            Suspect.COLONEL_MUSTARD)

        # A card that sample_bot can't refute
        self.assertEqual(
            self.sample_bot.
            respond_to_suggestion(1, Suggestion(Suspect.MISS_SCARLETT,
                                                Location.CONSERVATORY,
                                                Weapon.CANDLESTICK)),
            None)

        # A card that sample_bot can't refute, even though a card in the
        # suggestion exists in the face up cards
        self.assertEqual(
            self.sample_bot.
            respond_to_suggestion(1, Suggestion(Suspect.MISS_SCARLETT,
                                                Location.BALLROOM,
                                                Weapon.CANDLESTICK)),
            None)


@unittest.skip("SampleBot is not smart enough... yet.")
class TestObserveSuggestionResult(unittest.TestCase):
    def test_observe_suggestion_result(self):
        sample_bot = SampleBot()
        sample_bot.initialize(0, 6, [], [])
        sample_bot.receive_suggestion_result(Suggestion(Suspect.MISS_SCARLETT,
                                                        Location.BALLROOM,
                                                        Weapon.CANDLESTICK),
                                             None)
        expected_turn = Accusation(Suspect.MISS_SCARLETT,
                                   Location.BALLROOM,
                                   Weapon.CANDLESTICK)
        self.assertEqual(sample_bot.take_turn(), expected_turn)


if __name__ == '__main__':
    unittest.main()
