# Kit normalization status · 2026-10-27

The four requested normalization passes are complete in Tide 1.9.0. Each family has canonical HTML/CSS, explicit type/spacing/state contracts, all-ten-mode specimens and portable regression checks. Chromium measurements cover 1280px, 430px and 320px widths. These completed passes do not close every finding from the broader component audit.

| Completed family | Contract | Evidence and limits |
| --- | --- | --- |
| Buttons, icon buttons and photo controls | [Buttons](BUTTONS.md) | [Button verification](BUTTON-VERIFICATION.md) |
| Fields, choices, chips, disclosures, upload and errors, including select/summary alignment | [Forms](FORMS.md) | [Form verification](FORM-VERIFICATION.md) |
| Badges, notices, toast specimens and empty states | [Feedback](FEEDBACK.md) | [Feedback verification](FEEDBACK-VERIFICATION.md) |
| Event cards, dates, calendar groups and result summaries | [Listings](LISTINGS.md) | [Listing verification](LISTING-VERIFICATION.md) |

The original audit's button geometry/type, implicit density, incomplete control states, disabled precedence, missing disclosure indicator, upload error treatment and obsolete demonstration claims (F01–F09) are addressed by these contracts. The display-only focus alias (F11) is explicitly deprecated and retained for compatibility; new specimens use actual keyboard focus. Equivalent forced-colors state rules are present (F12), with actual operating-system verification still outstanding.

## Remaining kit work

Ownership enforcement (F10) is improved for the normalized families but is not complete across the registry. Organizer, Sponsored placement, Missing photo, Photographic event opening, Event details and Additive panel still lack the full CSS/HTML/contract/ownership metadata. Supporting blocks also need their canonical HTML homes recorded where applicable. Requiring these fields for every public component should follow that inventory cleanup, with checks that catch missing ownership rather than silently skipping entries.

A final typography/spacing review remains for those components and page patterns. The original audit noted unnamed brand/admission type values and event-detail leading, plus nested venue-profile padding that can double an inset in a composed page. These are review items, not evidence that every occurrence should be flattened to one size or inset. Review canonical recipes and name intentional exceptions before changing them. Application viewport and layout sources remain separate.

## Verification boundary

The current root build/check passes 57 kit tests, 28 application tests and seven local HTTP tests. It validates generated HTML, ownership rules already registered, references, zero browser JavaScript, ten-mode parity, 600 contrast pairs and existing byte budgets. Each family document records rendered/native checks and their limits. Passing these checks does not cover components without registered contracts.

Firefox, Safari, physical devices, screen readers, enlarged root fonts and an actual OS forced-colors session remain untested. Current engine observations are Chromium on Windows; feature compatibility data is not a passed browser test. Some pointer-held active states and nonzero consumer sticky offsets have source checks rather than exhaustive rendered verification. These limits remain visible in the family verification documents.

The next kit closeout should finish the remaining ownership inventory and review its component/page-pattern typography and insets before calling the whole kit normalized. Cross-engine and assistive-technology verification remains a separate recorded check. Application composition can then build on the documented kit contracts; service operations are outside repository scope.
