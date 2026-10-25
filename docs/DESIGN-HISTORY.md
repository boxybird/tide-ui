# Preserved design history

The complete pre-migration repository is preserved at annotated tag **`design-history/2026-10-25`**, commit `60864d0`. It includes all earlier studies, frozen originals, QA, ZIP archives, selected-design notes and App1.1.0. Cleanup does not rewrite that history.

The original selected Date Line, Tide theme studies, approved Shared Filters baseline, sticky-heading study and venue study remain in that tagged tree. Important paths there:

| Milestone | Tagged path |
| --- | --- |
| Selected Date Line | `quiet-assembly/01-date-line.html` |
| Original kit foundation | `tide-ui-kit/` |
| Approved Shared Filters baseline / kit1.3.0 | `tide-desktop-studies/shared-filter-release/` |
| Accepted sticky correction | `tide-desktop-studies/event-pressure-test/` |
| Accepted venue study | `tide-desktop-studies/venue-discovery/` |
| Combined app1.1.0 | `tide-desktop-studies/app-release-1.1.0/` |
| Preference/research history | `research/` |

Run `npm run verify:history` to verify the tag's committed-file inventory. Normal builds/tests deliberately do not read this history. A shallow clone may need `git fetch origin tag design-history/2026-10-25` before this optional command.

To inspect an older file without changing the checkout:

```sh
git show design-history/2026-10-25:tide-desktop-studies/shared-filter-release/kit/README.md
```

To export the complete tagged tree into a tar archive:

```sh
git archive --format=tar --output=design-history.tar design-history/2026-10-25
```

The migration also created a standalone recovery bundle at `.git/design-history-2026-10-25.bundle` on the original machine. Verify it with `git bundle verify .git/design-history-2026-10-25.bundle`; clone that bundle into a separate folder if the remote is unavailable. New clones recover the same history through the remote tag.

Forty-one ignored historical build/log files were additionally preserved and checksum-verified in `.git/design-history-local-artifacts-2026-10-25.zip` on this machine. Remaining dependency caches and temporary local files were relocated intact to ignored `.cache/legacy-before-migration/`; no broad recursive cache deletion was performed. These local-only files are not library sources or normal build inputs. The tag holds the complete 5,300-file tracked source/evidence inventory.

Historical binaries remain part of Git history, so this cleanup reduces the active checkout and browsing clutter rather than rewriting old clone storage. Keep `main` as the only branch; tags are the archive references.
