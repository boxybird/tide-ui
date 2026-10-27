# Application kits

Application kits are named, independently versioned starting points composed from the Tide UI kit. Tide at `packages/tide/` owns component appearance, tokens, recipes and contracts. Each application kit owns its page composition, responsive layout, native journeys, sample content, assets, build-time templates and application tests.

| Kit | Layout family | Application version | UI dependency | Canonical home |
| --- | --- | --- | --- | --- |
| [Lineup](lineup/README.md) | Option 1: responsive event discovery with a list/detail workspace | 2.0.4 | Tide 1.10.0 | `application-kits/lineup/` |

“Option 1” identifies this layout family, not a semantic version. The existing application history continues at 2.0.4. Future alternatives get their own meaningful sibling names, independent application versions and ownership contracts; they consume the same canonical UI kit. Release snapshots belong in Git tags/artifacts, not copied version folders. No second kit is created by this move.

Work on an application kit must not modify Tide's component sources, recipes, tokens, palettes or registry. Adopt documented UI-kit options in application markup; record missing options as application audit findings. Extending the source of truth requires a separately authorized UI-kit task. Shared integration checks may follow a source relocation without changing the UI-kit API or distribution.

From the repository root, run `npm run build`, `npm run check` and `npm run dev`. Lineup retains `/events/app/`, `/events/themes/` and `/events/index.html` as its local preview routes. Build output remains in ignored `build/events/`; it is not a second source home. The [Lineup audit](lineup/docs/AUDIT.md) records the initial responsive/component baseline and application-only follow-up work.
