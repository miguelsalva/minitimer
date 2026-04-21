# Phase 1: Full Pomodoro Cycles & Session Tracking

## Tasks

- [ ] Define the Pomodoro cycle sequence: 25 min work → 5 min short break → repeat × 4 → 15 min long break
- [ ] Add a state machine to track the current phase (work, short break, long break) and cycle count
- [ ] Auto-advance to the next phase when the timer completes (with a confirmation prompt or auto-start option)
- [ ] Update the UI labels and ring color to reflect the current phase (e.g., green for work, blue for break)
- [ ] Add a session counter showing how many Pomodoros have been completed today
- [ ] Persist the session count to a local file (e.g., `~/.minitimer_sessions`) so it survives app restarts
- [ ] Reset the daily counter automatically when the date changes
- [ ] Expose cycle configuration (work/short break/long break durations) as constants for easy customization

## Notes

- The preset buttons (5m, 15m, 25m, 45m) should still work for manual overrides outside the cycle flow
- The session counter only increments on completion of a work phase, not breaks
- Keep CLI behavior unchanged or add equivalent cycle support as a follow-up

---

# Phase 2: Tomato-Shaped Window

## Tasks

- [ ] Apply `FramelessWindowHint` + `WA_TranslucentBackground` to the main window
- [ ] Draw the tomato body silhouette using `QPainterPath` (ellipse, slightly wider than tall)
- [ ] Fill body with a radial gradient (bright red at center → deep red at edges)
- [ ] Draw green leaves at the top (two curved lobes + a stem using `QPainterPath`)
- [ ] Add kawaii face as decoration (eyes, optional blush marks using `QPainter`)
- [ ] Overlay the countdown ring and controls on top of the tomato canvas
- [ ] Enable window dragging via `mousePressEvent` / `mouseMoveEvent`
- [ ] Add right-click context menu (Quit, Reset, About)

## Notes

- Window shape mask must match the painted tomato silhouette (`setMask`)
- The ring widget should sit centered on the tomato body
- Leaves should extend above the main bounding rect; account for this in the window size
- Context menu should use a dark-themed `QMenu` consistent with the palette
