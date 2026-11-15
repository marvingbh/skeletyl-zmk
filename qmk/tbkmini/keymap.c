// TBK Mini (LAYOUT_split_3x6_3) with the same keymap as the Skeletyl ZMK
// config in ../../config/skeletyl.keymap. The outer columns are left empty
// so both keyboards feel the same. Keep the two files in step.
#include QMK_KEYBOARD_H

enum layers { BASE, FN, NAV, PTR, NUM, SYM };

// home-row mods (Mac: GUI = Cmd)
#define HM_A LGUI_T(KC_A)
#define HM_S LALT_T(KC_S)
#define HM_D LCTL_T(KC_D)
#define HM_F LSFT_T(KC_F)
#define HM_J RSFT_T(KC_J)
#define HM_K RCTL_T(KC_K)
#define HM_L LALT_T(KC_L)
#define HM_Q RGUI_T(KC_QUOT)

const uint16_t PROGMEM keymaps[][MATRIX_ROWS][MATRIX_COLS] = {
    [BASE] = LAYOUT_split_3x6_3(
        KC_NO, KC_Q,         KC_W,  KC_E,    KC_R,  KC_T,          KC_Y, KC_U, KC_I,    KC_O,   KC_P,          KC_NO,
        KC_NO, HM_A,         HM_S,  HM_D,    HM_F,  KC_G,          KC_H, HM_J, HM_K,    HM_L,   HM_Q,          KC_NO,
        KC_NO, LT(PTR,KC_Z), KC_X,  KC_C,    KC_V,  KC_B,          KC_N, KC_M, KC_COMM, KC_DOT, LT(PTR,KC_SLSH), KC_NO,
                        LT(FN,KC_ESC), LT(NUM,KC_SPC), LT(SYM,KC_TAB),     LT(SYM,KC_BSPC), LT(NAV,KC_ENT), LT(NUM,KC_DEL)
    ),
    [FN] = LAYOUT_split_3x6_3(
        KC_NO, KC_NO,   KC_NO,   KC_NO,   KC_NO,   KC_NO,          KC_PSCR, KC_F7, KC_F8, KC_F9, KC_F12, KC_NO,
        KC_NO, KC_LGUI, KC_LALT, KC_LCTL, KC_LSFT, KC_NO,          KC_SCRL, KC_F4, KC_F5, KC_F6, KC_F11, KC_NO,
        KC_NO, KC_NO,   KC_NO,   KC_NO,   KC_NO,   KC_NO,          KC_PAUS, KC_F1, KC_F2, KC_F3, KC_F10, KC_NO,
                                 _______, KC_NO,   _______,        _______, KC_NO, KC_NO
    ),
    [NAV] = LAYOUT_split_3x6_3(
        KC_NO, KC_NO,   KC_NO,   KC_UP,   KC_NO,   KC_NO,          KC_NO, KC_NO, KC_NO, KC_NO, KC_NO, KC_NO,
        KC_NO, KC_LGUI, KC_LEFT, KC_DOWN, KC_RGHT, KC_CAPS,        KC_NO, KC_NO, KC_NO, KC_NO, KC_NO, KC_NO,
        KC_NO, KC_END,  KC_PGUP, KC_PGDN, KC_HOME, KC_INS,         KC_NO, KC_NO, KC_NO, KC_NO, KC_NO, KC_NO,
                                 KC_NO,   _______, _______,        _______, KC_ENT, KC_BSPC
    ),
    // Skeletyl's BT/USB keys have no meaning on a wired board: left empty.
    [PTR] = LAYOUT_split_3x6_3(
        KC_NO, QK_BOOT, KC_NO,   KC_NO,   KC_NO,   KC_NO,          KC_NO, KC_NO,   KC_NO,   KC_NO,   QK_BOOT, KC_NO,
        KC_NO, KC_LGUI, KC_LALT, KC_LCTL, KC_LSFT, KC_NO,          KC_NO, KC_LSFT, KC_LCTL, KC_LALT, KC_LGUI, KC_NO,
        KC_NO, _______, KC_NO,   KC_NO,   MS_BTN3, KC_NO,          KC_NO, MS_BTN3, KC_NO,   KC_NO,   _______, KC_NO,
                                 MS_BTN2, MS_BTN1, _______,        _______, MS_BTN1, MS_BTN2
    ),
    [NUM] = LAYOUT_split_3x6_3(
        KC_NO, KC_NO,   KC_NO,   KC_NO,   KC_NO,   KC_NO,          KC_LBRC, KC_7, KC_8, KC_9, KC_RBRC, KC_NO,
        KC_NO, KC_LGUI, KC_LALT, KC_LCTL, KC_LSFT, KC_NO,          KC_EQL,  KC_4, KC_5, KC_6, KC_LGUI, KC_NO,
        KC_NO, KC_NO,   KC_NO,   KC_NO,   KC_NO,   KC_NO,          KC_BSLS, KC_1, KC_2, KC_3, KC_DOT,  KC_NO,
                                 _______, _______, _______,        _______, KC_0, KC_MINS
    ),
    // right side = NUM with Shift (8 -> *, 2 -> @); ( ) on the right thumbs
    [SYM] = LAYOUT_split_3x6_3(
        KC_NO, KC_LCBR, KC_AMPR, KC_ASTR, KC_LPRN, KC_RCBR,        KC_LCBR, KC_AMPR, KC_ASTR, KC_LPRN, KC_RCBR, KC_NO,
        KC_NO, KC_COLN, KC_DLR,  KC_PERC, KC_CIRC, KC_PLUS,        KC_PLUS, KC_DLR,  KC_PERC, KC_CIRC, KC_SCLN, KC_NO,
        KC_NO, KC_TILD, KC_EXLM, KC_AT,   KC_HASH, KC_PIPE,        KC_PIPE, KC_EXLM, KC_AT,   KC_HASH, KC_TILD, KC_NO,
                                 KC_GRV,  KC_UNDS, _______,        KC_LPRN, _______, KC_RPRN
    ),
};

// Thumbs ('*') count as either hand, like ZMK hold-trigger-key-positions.
const char chordal_hold_layout[MATRIX_ROWS][MATRIX_COLS] PROGMEM = LAYOUT_split_3x6_3(
    'L', 'L', 'L', 'L', 'L', 'L',     'R', 'R', 'R', 'R', 'R', 'R',
    'L', 'L', 'L', 'L', 'L', 'L',     'R', 'R', 'R', 'R', 'R', 'R',
    'L', 'L', 'L', 'L', 'L', 'L',     'R', 'R', 'R', 'R', 'R', 'R',
                   '*', '*', '*',     '*', '*', '*'
);

// Only home-row mods (mod-taps) get the opposite-hand rule; layer-taps
// behave like ZMK's plain &lt.
bool get_chordal_hold(uint16_t tap_hold_keycode, keyrecord_t *tap_hold_record,
                      uint16_t other_keycode, keyrecord_t *other_record) {
    if (!IS_QK_MOD_TAP(tap_hold_keycode)) return true;
    return get_chordal_hold_default(tap_hold_record, other_record);
}

uint16_t get_tapping_term(uint16_t keycode, keyrecord_t *record) {
    return IS_QK_MOD_TAP(keycode) ? 280 : TAPPING_TERM;
}

uint16_t get_quick_tap_term(uint16_t keycode, keyrecord_t *record) {
    return IS_QK_MOD_TAP(keycode) ? 300 : 200;
}

bool get_permissive_hold(uint16_t keycode, keyrecord_t *record) {
    return IS_QK_MOD_TAP(keycode);
}

uint16_t get_flow_tap_term(uint16_t keycode, keyrecord_t *record, uint16_t prev_keycode) {
    return IS_QK_MOD_TAP(keycode) ? FLOW_TAP_TERM : 0;
}
