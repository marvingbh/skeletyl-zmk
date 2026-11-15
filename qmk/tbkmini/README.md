# TBK Mini (QMK)

Same keymap as the Skeletyl (`config/skeletyl.keymap`), for the wired TBK Mini with Elite-C controllers. The outer columns are empty. The RIGHT half has the USB cable (`MASTER_RIGHT`).

Build (Docker, QMK checkout in `$QMK`):

    cp -r qmk/tbkmini $QMK/keyboards/bastardkb/tbkmini/keymaps/marcus
    docker run --rm -v $QMK:/qmk_firmware -w /qmk_firmware qmkfm/qmk_cli qmk compile -kb bastardkb/tbkmini/promicro -km marcus

Flash each half (Elite-C, atmel-dfu): put it in bootloader (reset button, or hold Z + tap Q), then

    dfu-programmer atmega32u4 erase --force
    dfu-programmer atmega32u4 flash bastardkb_tbkmini_promicro_marcus.hex
    dfu-programmer atmega32u4 launch

Flash both halves with the same file, so the split link uses the same QMK version.
