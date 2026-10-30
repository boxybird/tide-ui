# Venue page width review · 2026-10-30

Status: user review, based on the committed and pushed Lineup 2.4.2 checkpoint. The current source shows the middle option; no new release is assigned until the width is accepted.

The quoted disclosure belongs to the five standalone venue pages (Sister, Dry Heat, Barelas Print Studio, The Paper Table and Warehouse Room). It has been removed from their shared partial. Sunshine Theater retains its distinct factual profile/workspace; individual event details are unchanged. Authored fixture provenance remains in project documentation rather than customer-facing disclosure text.

The private `tide-venue__page` wrapper constrains the existing Tide Content page. It caps the image and event collection at `--tide-app-venue-width`, adding the existing two page insets outside that content width. Heading, image and list start at the same edge. The wrapper centers on wide screens and fits available width on smaller screens. Tide controls, card padding, type, colors and content-page internals remain unchanged.

Three alternatives were rendered sequentially from the same canonical template and stylesheet at 1440×1100: 40rem/640px, 48rem/768px and 56rem/896px. These are image/list widths, excluding the shared page insets. Screenshots are review evidence in ignored `build/qa/venue-profile-width/`; they are not separate application sources. The current live page uses 48rem/768px.

## Verification

- `npm run build` and `npm run check` pass: 138 tests and 1,107 generated documents. CSS rule/declaration parity checks cover both the native app and map stylesheets after dropping optional trailing declaration semicolons. The app stylesheet is 21,955 bytes, below its unchanged 22,000-byte budget.
- Chromium on Windows: all five affected venue routes have aligned 768px images and event lists at 1440×1100, preserve their 9/13/10/8/8 event counts and omit the disclosure. The Barelas page also preserves alignment without horizontal overflow at 320×700, 390×844, 768×900 and 960×800.
- All ten theme/mode versions of Barelas preserve the same 768px column at 1440×1100. Ink After Dark opens its existing event route; browser Back returns to the venue page.
- Tide, shared tooling, map code and fixtures are unchanged. Firefox, Safari, physical touch devices and screen readers have not been verified.

The screenshot comparison at `/qa/venue-profile-width/index.html` uses native radio controls and links back to the live page. The current draft remains on `main` awaiting the user's width choice; no release tag or push is part of this review.
