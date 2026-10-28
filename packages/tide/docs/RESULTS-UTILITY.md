# Results utility variant · Tide 1.11.0

`tide-results--utility` is an additive presentation option for compact result headings and adjacent utility labels. It does not change the default Results recipe or supply behavior. The user authorized this narrow kit extension for the selected Lineup design and accepted the reviewed implementation on 2026-10-27.

```html
<div class="tide-results tide-results--utility">
  <h1 class="tide-results__count">54 events</h1>
  <span class="tide-results__order">Soonest first</span>
</div>
```

The count/label uses Manrope 20px/28px, heading weight 580 and primary text, with normal tracking. Order stays 14px/24px regular in secondary text. Existing named type/spacing/color inputs own these values. The row retains 16px block padding and 12px wrapping gap; 24px inline margins inset the lower hairline. Its inline padding is zero. The default top hairline is removed only for this variant.

Use a native heading at the level appropriate to the document, or a paragraph for a utility label that does not introduce a new section. A left-column Search & filters label can use the same count slot with no order text. The host owns region names, IDs, contextual count wording, actual counts and placement. Long count/order text wraps; hidden headers remain native hidden content. Plain order text does not become a sort control, and no live-region announcement is implied.

The default `.tide-results` remains 14px/24px with its existing top separator and 16px/24px insets. Filter panel titles and all existing field/control/card recipes are unchanged. Palette inputs, primitive tokens and assets are unchanged.

Canonical package sources are `css/layout.css`, `css/patterns.css` and `templates/listings.html`. The registered listing-state fixture includes utility-label, zero/one/many, long, hidden and context-isolation cases in every theme/mode. Regression checks protect registration, unchanged defaults, named utility inputs and native state markup.

Current browser evidence is in-app Chromium on Windows at 390 and 1440 CSS pixels across all ten theme/mode combinations. Utility counts/context-isolated counts compute to 20px/28px, default counts and order remain 14px, the lower hairline matches the default hairline thickness, hidden cases have no box, and no horizontal overflow or scripts were found. Border widths may snap to the current device-pixel density. Firefox/Safari, physical devices and screen readers remain unverified.
