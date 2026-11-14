# Accessibility execution matrix

## Manual matrix

| Area | Procedure | Pass evidence |
|---|---|---|
| Keyboard | Start at browser chrome; Tab/Shift+Tab, arrows, Enter/Space, Escape and documented shortcuts, no pointer. | Every required outcome reachable without timing-dependent keys; focus order follows task order. [AX2] |
| Focus visibility | Tab through sticky headers, rails, panes, dialogs, toasts and overlays at normal and 200% zoom. | Indicator visible; focused component never fully obscured. [AX3] |
| Modal dialog | Open from keyboard; traverse both ways; try background interaction; Escape/cancel/confirm. | Focus enters, stays contained, background inert, Escape works when appropriate, close returns focus to the invoker. [AX4] |
| Names/roles/states | Inspect the accessibility tree and use a screen reader. | Useful names, correct roles; expanded/selected/checked/disabled/current states match the UI. |
| Dynamic status | Trigger save, error, progress, completion, stale, retry and count changes. | Important changes announced once without unwanted focus movement; error associated with its control. |
| Contrast/colour | Measure text, icons, controls, charts, focus and disabled reasons; view in greyscale/high contrast. | Information not colour-only; applicable contrast thresholds pass. [AX1] |
| Zoom/reflow | 200% zoom and a narrow viewport; enlarge text where supported. | No loss of action, data, focus, labels or error text; no destructive two-dimensional scroll unless content requires it. [AX1] |
| Pointer | Measure targets; test click/tap, hover/focus content, cancellation, drag alternatives. | 24×24 CSS px minimum or valid exception; non-drag alternative unless essential. [AX1] |
| Motion/time | Enable reduced motion; exercise timeouts, auto-advance, animated scrolling, progress. | No essential information depends on motion; user can pause/stop/extend where required. [AX1] |
| Audio/media | Mute audio; test visible transport state, captions/transcript, errors, keyboard control. | Non-audio information path where required; transport operable; status perceivable. [AX1] |

## WCAG 2.2 additions that bite most apps

Source: W3C, "What's New in WCAG 2.2" (w3.org/WAI/standards-guidelines/wcag/new-in-22).

| SC | Level | Rule | Typical places |
|---|---|---|---|
| 2.4.11 Focus Not Obscured (Minimum) | AA | focused component not *entirely* hidden by author content | docked timelines, sticky toolbars, toasts, side panels |
| 2.4.12 Focus Not Obscured (Enhanced) | AAA | no part hidden | nice-to-have |
| 2.4.13 Focus Appearance | AAA | strong focus indicator | headless libraries leave focus styling to you |
| 2.5.7 Dragging Movements | AA | single-pointer alternative to every drag | reorderable outlines, timeline cue drag, graphs |
| 2.5.8 Target Size (Minimum) | AA | ≥24×24 CSS px or non-overlapping 24 px circles; exceptions inline/equivalent/UA/essential | dense rows, waveform markers, icon buttons |
| 3.2.6 Consistent Help | A | help in the same relative place | |
| 3.3.7 Redundant Entry | A | don't make users re-enter information in one process | multi-step wizards |
| 3.3.8 Accessible Authentication (Minimum) | AA | no cognitive tests to log in | any login |

Carry-overs always checked: 1.4.3 contrast 4.5:1 text, 1.4.11 3:1 non-text, 2.1.1 keyboard, 2.4.7
focus visible, 4.1.2 name/role/value, 4.1.3 status messages.

## Library responsibilities (examples)

- **Base UI** (headless, under shadcn): ARIA attributes, roles, keyboard (arrows, Home/End, Enter,
  Esc, typeahead), focus management (`initialFocus`, `finalFocus`). Developer: visible focus
  (`:focus-visible`), contrast, names for custom controls; Select needs `<Select.Label>` or
  `aria-label`; prefer Combobox over Select for long filterable lists
  (base-ui.com/react/overview/accessibility, /components/select).
- **dnd-kit**: the activator must be focusable (button or `tabindex=0`); keyboard sensor uses
  Space/Enter to pick up and drop, arrows to move, Esc to cancel; off-screen instructions via
  `aria-describedby`; customise live-region announcements to use positions, not indices
  (github.com/dnd-kit/docs guides/accessibility.md — written for `@dnd-kit/core`; confirm names in
  newer React APIs). Still add move up/down buttons for SC 2.5.7.
- **Plate/Slate** (contenteditable): verify editor commands are keyboard-reachable and announced.
- **wavesurfer** and other canvas widgets: provide named buttons for play/pause/seek and a text time
  readout.
- **Toast libraries** (e.g. sonner): check the announced text is meaningful.
- **Theme switchers** (e.g. next-themes): check contrast in every theme.
- **oxlint / eslint**: the `jsx-a11y` plugin catches machine-detectable issues; check it is enabled.

## Automation boundary

Automated checks catch machine-testable failures. Manually verify keyboard, focus order and return,
meaningful announcements, contrast edge cases, zoom/reflow, cognitive clarity, audio and usability.
W3C states that tools cannot check all aspects and cannot determine accessibility by themselves.
[AX5] Playwright's documentation likewise says automated accessibility testing cannot detect every
violation (playwright.dev/docs/accessibility-testing).

## Sources

- **[AX1]** W3C Accessibility Guidelines Working Group, *Web Content Accessibility Guidelines (WCAG) 2.2*, W3C Recommendation (2024). https://www.w3.org/TR/WCAG22/ — quick reference: https://www.w3.org/WAI/WCAG22/quickref
- **[AX2]** W3C WAI, *Understanding Success Criterion 2.1.1: Keyboard*. https://www.w3.org/WAI/WCAG22/Understanding/keyboard
- **[AX3]** W3C WAI, *Understanding Success Criterion 2.4.11: Focus Not Obscured (Minimum)*. https://www.w3.org/WAI/WCAG22/Understanding/focus-not-obscured-minimum.html
- **[AX4]** W3C WAI-ARIA Authoring Practices, *Dialog (Modal) Pattern*. https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/
- **[AX5]** W3C WAI, *Selecting Web Accessibility Evaluation Tools*. https://www.w3.org/WAI/test-evaluate/tools/selecting
- W3C WAI, *What's New in WCAG 2.2*. https://www.w3.org/WAI/standards-guidelines/wcag/new-in-22/
- W3C WAI, *ARIA Authoring Practices Guide*. https://www.w3.org/WAI/ARIA/apg/
- Base UI, *Accessibility*, *Select*. https://base-ui.com/react/overview/accessibility ; https://base-ui.com/react/components/select
- dnd-kit docs, *Accessibility*. https://github.com/dnd-kit/docs/blob/master/guides/accessibility.md
- Testing Library, *About Queries* (priority: role, label, placeholder, text, display value, alt, title, test id last). https://testing-library.com/docs/queries/about/
- Microsoft Playwright, *Accessibility testing*. https://playwright.dev/docs/accessibility-testing
