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
