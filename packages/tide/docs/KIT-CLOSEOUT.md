# Remaining components and page rhythm · Tide 1.10.0

This pass finishes the source/contract inventory and normalizes the remaining component typography and spacing. Canonical comparison HTML is `templates/closeout-components.html`, rendered in all ten modes by `frames/kit-closeout.html`. Panel loads its existing additive extension CSS. Native links, semantic headings and static authored content remain the behavior boundary.

## Type and spacing

Values below assume a 16px root; the named inputs use rem and grow with font preferences. Component roots declare Manrope, upright regular 14px/24px, normal tracking and natural case. Explicit slots override that base. Surrounding bold, italic, serif or uppercase reading contexts do not change them.

| Component | Type | Spacing |
| --- | --- | --- |
| Organizer | Body 14/24 regular; title 14/24, weight 550 | 24px insets, 12px gaps; neutral 1px boundary |
| Sponsored placement | Title 16/24, weight 550; body 12/20; sponsorship 12/20, weight 550, tracked uppercase | 24px block/inline insets, 8px gaps; persistent explicit sponsorship wording |
| Missing photo | Title 28/36, weight 580; label 12/20 | 32px block/24px inline padding, named 220px minimum; copy grows rather than clipping |
| Event opening | Title 36/40, weight 580; subtitle 16/24; facts 14/24; admission 22/28, weight 500; notes 12/20 | Existing viewport/photo reserve retained, 24px inline inset, 12px fact-row gap and 8px inline fact gap at every width |
| Event details | Title 28/36, weight 580; section title 16/24, weight 550; body 14/24 | Existing 40px/24px insets, 32px section margin, 24px section top padding; named reading rhythm |
| Additive panel | Title 20/28, weight 580; description 14/24 | Existing 24px insets, 12px gaps and neutral boundary |
| Venue profile/card and Site header | Explicit body 14/24; venue card title 20/28, weight 580 | Existing 24px inset/rhythm; native navigation targets retain 44px minimum and wrap |

Organizer and partner now share the kit's 24px regular inset rather than mixing 20px and 24px. Sponsorship uses the readable caption role instead of a 10px label. Details use the common page-heading line box instead of an unnamed 1.2 multiplier. Legacy heading selectors remain compatible; named title slots work independently of heading level. No viewport changes type density or the fact text gap. Long admission labels can wrap without changing type size.

Brand's 19px type, weight 450 and .22em tracking are intentional optical identity values, now named inputs. Admission's 22px role, 17px fact glyph, 2px optical offset and 14px cue glyph are also named. These are not additional button or body sizes. Summary/Schedule label columns and Appbar minimum height now have named inputs without changing their accepted dimensions.

## Nested venue insets

Default `tide-venue-profile` still supplies 24px on every edge. Its new `--flush-inline` variant removes inline padding when a containing page already supplies the inset. Canonical populated/empty venue recipes use it so profile facts and the following schedule align. There is no descendant selector that silently strips all profiles' padding. The application keeps its default profile, viewport geometry and source files.

## States and ownership

Organizer, sponsorship, fallback and panel are static content. They do not gain hover shells, live-region roles or fake disabled states. Native links retain keyboard focus and destinations; hero actions use the existing [button contract](BUTTONS.md). Hidden ancestors remove entire examples from layout. The photo context retains the existing scrim and semantic palette roles. Theme values, including Bumble Dark, are unchanged.

Every public block now has a required [ownership contract](OWNERSHIP.md). Consumers own content, native destinations, viewport composition and their documented property/value exceptions. The kit owns internal type, rhythm and state presentation. See [verification and limits](KIT-CLOSEOUT-VERIFICATION.md); this is not a cross-browser or assistive-technology certification.
