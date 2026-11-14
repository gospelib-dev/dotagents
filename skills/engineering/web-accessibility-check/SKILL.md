---
name: web-accessibility-check
description: Use when building, reviewing or accepting UI. WCAG 2.2 AA checks and tools.
metadata:
  version: "0.1.0"
  status: draft
  owner: Lance
---

# Web accessibility check (WCAG 2.2 AA)

One method for engineers building UI, reviewers judging UI diffs, and QA accepting UI behaviour.
Target WCAG 2.2 Level AA unless the task requires more; follow the WAI-ARIA Authoring Practices
Guide (APG) for custom widgets. Conformance applies to full pages and their responsive variations,
not selected components. [AX1]

## When to use

Any change a user can see or operate: new components, layout changes, drag interactions, dialogs,
status messages, media players, themes.

## Principles

- **Automation finds some failures; it cannot declare a pass.** Run an automated scan (axe, a lint
  plugin such as `jsx-a11y`), then do the manual checks. Never convert "zero automated violations"
  into "accessible". [AX5]
- **Headless libraries split the work.** Primitives such as Base UI or Radix handle ARIA roles,
  keyboard patterns and focus management; *you* still own visible focus, contrast, and accessible
  names for custom or icon-only controls.
- **Cite the success criterion** (SC number) in every finding.
- **Tests query by role and accessible name first**, test ids last; that tests the same thing a
  screen reader sees.

## Checklist (apply to every UI change)

1. Every control reachable and operable by keyboard without timing-dependent keystrokes; custom
   widgets follow their APG pattern keys (arrows, Home/End, Enter/Space, Esc). (2.1.1) [AX2]
2. Visible focus on everything focusable (`:focus-visible`), and the focused item never *entirely*
   hidden by sticky headers, docked panels or toasts. (2.4.7, 2.4.11) [AX3]
3. Modal dialogs: focus moves in, stays contained, background inert, Esc closes when appropriate,
   focus returns to the invoker, and global shortcuts resume after close. [AX4]
4. Pointer targets at least 24×24 CSS px, or spaced so 24 px circles don't overlap, or a listed
   exception (inline, equivalent, user-agent, essential). (2.5.8)
5. Every drag has a single-pointer, non-drag alternative unless dragging is essential: keyboard
   sensor plus move up/down buttons for reorder lists. Drag announcements use positions
   ("position 2 of 5"), not ids or indices. (2.5.7)
6. Accessible name, role and state on every control, including icon buttons and canvas-based
   widgets (give canvas players named play/pause/seek buttons and a text time readout). Expanded,
   selected, checked, disabled and current states match the UI. Focusable disabled controls expose
   *why* they are unavailable. (4.1.2)
7. Status changes (progress, save, error, completion) announced through a live region without
   stealing focus; errors associated with their control; toast text meaningful when read alone.
   (4.1.3)
8. Contrast: text 4.5:1 (3:1 for large text), UI components, graphics and focus indicators 3:1, in
   every theme. Information never conveyed by colour alone: add labels or shapes to state badges.
   (1.4.3, 1.4.11, 1.4.1)
9. 200% zoom and narrow reflow keep every action, label, focus indicator and error available without
   destructive overlap or two-dimensional scrolling. (1.4.10)
10. Reduced motion respected; no essential information depends on animation; pause/stop/extend where
    WCAG requires. Tooltips work on focus as well as hover and don't obscure the next focused item.
11. Media: visible transport state, keyboard control, and a non-audio path (captions/transcript)
    where information is conveyed by sound.
12. Pointer-only interactions (right-click-only menus, hover-only actions) have an equivalent
    keyboard/menu route.

Manual execution steps and pass evidence for each area are in
[references/execution-matrix.md](references/execution-matrix.md), with the WCAG 2.2 additions and
library responsibilities.

## How to verify, in order

1. Keyboard-only pass of the changed flow in a real browser (Tab, Shift+Tab, Enter, Space, Esc,
   arrows, documented shortcuts), starting from browser chrome.
2. Accessibility tree: every interactive node has role and name (e.g. CDP
   `Accessibility.getFullAXTree`, or the browser devtools tree).
3. Measure target sizes of icon buttons, rows and markers (box model).
4. Contrast in light and dark themes.
5. Automated scan and lint on changed flows: zero serious/critical violations, then the manual steps
   above. [AX5]
6. Screen-reader spot check of announcements for the changed flow.
7. Component tests use role + name queries.

## Pitfalls

- Disabling a control with `disabled` removes it from the tab order and hides the reason; prefer a
  focusable `aria-disabled` control that explains itself when the reason matters.
- Select-like widgets need a visible label or `aria-label`; for long filterable lists prefer a
  combobox.
- Contenteditable editors: verify that suggestion/accept/reject and similar commands are reachable by
  keyboard and announced.
- Prototype test suites in a node environment have no rendered DOM, so they say nothing about
  accessibility; that stays a manual gate until browser-mode tests exist.

## Verification

Findings cite SC numbers; the keyboard pass, AX-tree check, target measurement and both-theme
contrast were done on the changed flow; the automated scan result is reported separately from the
manual result.

## Project specifics

The project's UI or QA skill supplies which components, panels and gestures carry the most risk,
which lint plugins are enabled, the theme switcher, and how to reach the running app.

Sources: [AX1]–[AX5] and library docs in references/execution-matrix.md.
