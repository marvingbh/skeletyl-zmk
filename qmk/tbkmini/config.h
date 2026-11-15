// TBK Mini (QMK) settings that copy the Skeletyl ZMK hold-tap behaviour.
#pragma once

#define TAPPING_TERM 200            // layer-taps, like ZMK &lt
#define TAPPING_TERM_PER_KEY        // home-row mods use 280
#define QUICK_TAP_TERM_PER_KEY      // tap then hold repeats: 300 mods, 200 layer-taps
#define PERMISSIVE_HOLD_PER_KEY     // "balanced" flavour, home-row mods only
#define CHORDAL_HOLD                // opposite-hand rule = ZMK hold-trigger-key-positions
#define FLOW_TAP_TERM 150           // = ZMK require-prior-idle-ms, home-row mods only

// The RIGHT half has the USB cable (and talks to the left over TRRS).
#define MASTER_RIGHT
