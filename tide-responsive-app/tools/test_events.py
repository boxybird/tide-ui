from pathlib import Path
from collections import Counter
from datetime import datetime
import unittest
from events import load_events,month_groups

ROOT=Path(__file__).resolve().parents[1]


class LongFeedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.events=load_events(ROOT/'data/events.json')

    def test_fixture_has_enough_distinct_events_across_months(self):
        self.assertEqual(len(self.events),48)
        self.assertEqual(Counter(x['date'][:7] for x in self.events),{'2026-10':16,'2026-11':32})
        self.assertEqual(len({x['slug'] for x in self.events}),48)

    def test_month_boundary_and_day_labels_are_consistent(self):
        groups=month_groups(self.events)
        self.assertEqual([key for key,_ in groups],['2026-10','2026-11'])
        self.assertEqual(groups[0][1][-1]['date'],'2026-10-31')
        self.assertEqual(groups[1][1][0]['date'],'2026-11-01')
        for event in self.events:
            stamp=datetime.fromisoformat(event['datetime'])
            self.assertEqual(event['weekday'],stamp.strftime('%a'))
            self.assertEqual(event['month'],stamp.strftime('%b'))
            self.assertEqual(event['day'],str(stamp.day))

    def test_albuquerque_offset_changes_at_november_boundary(self):
        for event in self.events:
            self.assertTrue(event['datetime'].endswith('-06:00' if event['date']<'2026-11-01' else '-07:00'))

    def test_three_original_favorites_remain_with_their_details(self):
        import json
        originals=json.loads((ROOT/'data/events-core.json').read_text(encoding='utf-8'))
        for original in originals:
            current=next(x for x in self.events if x['slug']==original['slug'])
            for field,value in original.items():self.assertEqual(current[field],value)

    def test_content_varies_enough_to_exercise_card_wrapping_and_admission(self):
        self.assertTrue(any(len(x['title'])>70 for x in self.events))
        self.assertTrue(all(len(x['title'])<=80 for x in self.events))
        self.assertTrue(any(x['price']=='Free' for x in self.events))
        self.assertTrue(any(x['age']=='All ages' for x in self.events))
        self.assertGreater(len({x['lead'] for x in self.events}),40)


if __name__=='__main__':unittest.main()
