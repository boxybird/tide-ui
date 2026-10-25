import unittest
from contracts import markup_issues


class ContractTests(unittest.TestCase):
    def test_icon_path_is_not_a_button_name(self):
        html='<main><h1>Events</h1><button><svg aria-hidden="true"><path d="fake"></path></svg></button></main>'
        self.assertIn('Link/button missing an authored accessible name',markup_issues(html))

    def test_labelled_icon_and_semantic_state_pass(self):
        html='<main><h1>Events</h1><button class="tide-icon-button" type="button" aria-label="Save event" aria-pressed="true"><svg aria-hidden="true"></svg></button></main>'
        self.assertEqual(markup_issues(html),[])

    def test_missing_bem_base_and_positive_tab_order_are_rejected(self):
        issues=markup_issues('<main><h1>Events</h1><a class="tide-button--secondary" tabindex="3" href="event.html">Event</a></main>')
        self.assertIn('Modifier without its base class: tide-button--secondary',issues)
        self.assertIn('Positive tabindex changes natural focus order',issues)

    def test_hidden_copy_does_not_name_a_control(self):
        issues=markup_issues('<main><h1>Events</h1><button><span aria-hidden="true">Save</span></button></main>')
        self.assertIn('Link/button missing an authored accessible name',issues)
