# Troubleshooting

Problems hit during this build, and what fixed them.

## Controller does not appear on USB after soldering

**Symptom:** it worked loose, and after soldering it to the adapter it shows no drive and no keyboard. An LED may still light.

**Cause:** the controller was mounted chip-up on the *"Install Elite-C upside down"* side. That mirrors the two pin rows, which puts:

| Controller pin | Lands on adapter hole | Effect |
|---|---|---|
| VCC (3.3 V) | GND | 3.3 V rail shorted, chip unpowered |
| RST | GND | Chip held in reset |
| RAW | RGB data | Harmless |
| GND | RST and 5V nets | Harmless |

**Check:** with USB unplugged, beep VCC ↔ GND. A beep means it's mounted backwards.

**Prevention:** solder only 2 pins, beep VCC ↔ GND and RST ↔ GND, then solder the rest. Desoldering a full header later is hard enough that it may cost you the controller.

## Battery reaches the adapter but not the controller

**Symptom:** the battery voltage shows on the adapter's B+ pad, but the board doesn't run on battery and doesn't advertise over Bluetooth.

**Cause:** the adapter routes B+ through the footprint for an SMD power switch, plus a solder jumper (JP1) that bypasses it. Both sit between the controller's pin rows, so with the controller mounted they are covered and can't be bridged.

**Fix:** wire the battery's red wire, through your own switch, to the controller's own **B+** hole (the empty corner hole at the USB end). Black can stay on the adapter's B−.

## Shorting R1 + C1 on the adapter does nothing

That's expected. The adapter supports 6 columns and 5 rows. The Skeletyl uses **R2–R5** and **C2–C6**: `q` is R2 + C2.

## Double-tap reset doesn't open the NICENANO drive

Some clones don't detect the double tap, or restart into a serial-only bootloader. Use the bootloader key in the keymap, or [serial DFU](flashing.md#serial-dfu-fallback).

## Right half doesn't type when plugged in alone

That's expected: the right half is a Bluetooth peripheral and doesn't act as a keyboard over USB. Power the left half too; the right one connects to it by itself.

## Matrix reference

Pin labels are the nRF52840 port numbers printed on the controller.

| | Pins |
|---|---|
| Rows (top → thumbs) | 115, 024, 022, 106 |
| Columns (left half, outer → inner) | 029, 009, 100, 011, 104 |
| Columns (right half, inner → outer) | 104, 011, 100, 009, 029 |
| Diodes | ROW2COL |
