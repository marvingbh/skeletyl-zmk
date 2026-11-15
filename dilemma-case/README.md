# Dilemma 3mod case

3D-printable case for the [Dilemma-3mod](https://github.com/dixls/Dilemma-3mod) PCB with Choc switches, an external nice!nano-style controller and a 38×20×9 mm battery. Flat, no tenting. A tray holds the PCB, and a cover closes the controller and the battery pod. The cover top is level with the Choc keycaps.

- `out/`: print files (STL) and CAD files (STEP) for the tray and the cover, left and right.
- `preview/`: renders and `.glb` models of the assembled keyboard.
- `dilemma_case.py`: the parametric model (build123d). Run `python dilemma_case.py <dilemma.kicad_pcb> out [controller_gap_mm]`. The gap is the space between the keyboard PCB and the controller board (default 1.0). The cover is flush with the keycaps up to about 1.9 mm, and grows taller above that.
- `assembly.py`: builds the preview models. `check.py`: top view and cross-section plots.

Screws: 5× M3×6 (tray), 4× M3×12 (cover), 9 M3 nuts. Current files in `out/` are for a 1.0 mm controller gap.
