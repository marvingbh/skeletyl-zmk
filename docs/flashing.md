# Flashing

Each half needs its own file:

| Half | File | Role |
|---|---|---|
| Left | `skeletyl_left.uf2` | Central: talks to the computer over USB and Bluetooth |
| Right | `skeletyl_right.uf2` | Peripheral: talks only to the left half |

Get the files from the latest GitHub Actions run (`firmware.zip`) or build them with `scripts/build.sh`.

## UF2 (normal way)

1. Put the controller in bootloader mode (see below). A drive called **NICENANO** appears.
2. Copy the matching `.uf2` onto it.
3. The drive disappears on its own. The controller has restarted with the new firmware.

### Entering the bootloader

| Method | When |
|---|---|
| Hold **Z** (Mouse layer) and tap **Q** (or hold **/** and tap **P**) | Firmware is running and keys work |
| Touch **RST** to **GND** twice within half a second | Bare controller, or keys don't work |

Some clones ignore the double tap. Use serial DFU for those.

## Serial DFU (fallback)

Some clones restart into a bootloader that exposes only a serial port, with no drive. Convert the UF2 and flash it with [`adafruit-nrfutil`](https://github.com/adafruit/Adafruit_nRF52_nrfutil):

```sh
# 1. UF2 → raw binary (the app starts at 0x26000 on nice!nano v2)
python3 - <<'EOF'
import struct
d = open("skeletyl_left.uf2", "rb").read()
blocks = {}
for i in range(0, len(d), 512):
    _, _, _, addr, size, *_ = struct.unpack("<8I", d[i:i+32])
    blocks[addr] = d[i+32:i+32+size]
lo = min(blocks); hi = max(a + len(v) for a, v in blocks.items())
img = bytearray(b"\xff" * (hi - lo))
for a, v in blocks.items():
    img[a-lo:a-lo+len(v)] = v
open("left.bin", "wb").write(img)
EOF

# 2. binary → hex → DFU package
uvx --from intelhex python -c "from intelhex import IntelHex as I; h=I(); h.loadbin('left.bin', offset=0x26000); h.tofile('left.hex', format='hex')"
uvx adafruit-nrfutil dfu genpkg --dev-type 0x0052 --sd-req 0xFFFE --application left.hex left_dfu.zip

# 3. flash over the serial port
uvx adafruit-nrfutil dfu serial --package left_dfu.zip -p /dev/cu.usbmodem1101 -b 115200 --singlebank
```

The port name varies: on macOS, run `ls /dev/cu.usbmodem*` to find it.

## Checking which firmware is on a controller

On macOS, run `ioreg -p IOUSB -l -w0 | grep -E '"USB Product Name"|"USB Serial Number"'`:

- Left half: listed as **Skeletyl**.
- Right half: listed as a **ZMK Project** device with no product name.
- Bootloader: listed as **nice_nano**.
