# Keymap

36 keys: 3×5 per half plus 3 thumbs. Source: [`config/skeletyl.keymap`](../config/skeletyl.keymap).

- Small text after a key is what it does when **held** (home-row mods ⌘ ⌥ ⌃ ⇧, or a layer).
- Home-row mods only fire when combined with a key on the **other** half or a thumb, which avoids misfires while typing.
- **S** (⌥) is stricter: it becomes ⌥ only when held alone for about 0.3 s before the other key. Any key pressed sooner types **s**.
- **F** and **J** (⇧) work like the old QMK board: Shift after 0.2 s of hold, even right after fast typing, so **?** (F + /) and capitals after a space come out.
- `·` = nothing, `▽` = transparent (falls through to the layer below).

## Base

Default layer.

| | | | | | ‖ | | | | | |
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| Q | W | E | R | T | ‖ | Y | U | I | O | P |
| A <sub>⌘</sub> | S <sub>⌥</sub> | D <sub>⌃</sub> | F <sub>⇧</sub> | G | ‖ | H | J <sub>⇧</sub> | K <sub>⌃</sub> | L <sub>⌥</sub> | ' <sub>⌘</sub> |
| Z <sub>Mouse</sub> | X | C | V | B | ‖ | N | M | , | . | / <sub>Mouse</sub> |
| | | Esc <sub>FN</sub> | Space <sub>NUM</sub> | Tab <sub>SYM</sub> | ‖ | ⌫ <sub>SYM</sub> | Enter <sub>NAV</sub> | Del <sub>NUM</sub> | | |

## FN

Hold **Esc** (left inner thumb).

| | | | | | ‖ | | | | | |
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| · | · | · | · | · | ‖ | PrtSc | F7 | F8 | F9 | F12 |
| ⌘ | ⌥ | ⌃ | ⇧ | · | ‖ | ScrLk | F4 | F5 | F6 | F11 |
| · | · | · | · | · | ‖ | Pause | F1 | F2 | F3 | F10 |
| | | ▽ | · | ▽ | ‖ | ▽ | · | · | | |

## NAV

Hold **Enter** (right middle thumb).

| | | | | | ‖ | | | | | |
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| · | · | ↑ | · | · | ‖ | · | · | · | · | · |
| ⌘ | ← | ↓ | → | Caps | ‖ | · | · | · | · | · |
| End | PgUp | PgDn | Home | Ins | ‖ | · | · | · | · | · |
| | | · | ▽ | ▽ | ‖ | ▽ | Enter | ⌫ | | |

## Mouse

Hold **Z** or **/**.

| | | | | | ‖ | | | | | |
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| Boot | · | · | USB/BT | BT clear | ‖ | BT 0 | BT 1 | BT 2 | BT 3 | Boot |
| ⌘ | ⌥ | ⌃ | ⇧ | · | ‖ | · | ⇧ | ⌃ | ⌥ | ⌘ |
| ▽ | · | · | Mid click | · | ‖ | · | Mid click | · | · | ▽ |
| | | R click | L click | ▽ | ‖ | ▽ | L click | R click | | |

## NUM

Hold **Space** (left middle thumb) or **Delete** (right outer thumb).

| | | | | | ‖ | | | | | |
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| · | · | · | · | · | ‖ | [ | 7 | 8 | 9 | ] |
| ⌘ | ⌥ | ⌃ | ⇧ | · | ‖ | = | 4 | 5 | 6 | ⌘ |
| · | · | · | · | · | ‖ | \ | 1 | 2 | 3 | . |
| | | ▽ | ▽ | ▽ | ‖ | - | 0 | ▽ | | |

## SYM

Hold **Tab** (left outer thumb) or **Backspace** (right inner thumb). With **Tab** held, the right thumbs type **(** (Backspace thumb) and **)** (Delete thumb). The right side is NUM with Shift: each key gives the symbol printed above that NUM key's number on a normal keyboard (8 → *, 2 → @). The ⌘ slot of NUM holds **:** here (Shift of the key right of L on a normal keyboard); the plain **;** is on the left pinky.

| | | | | | ‖ | | | | | |
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| { | & | * | ( | } | ‖ | { | & | * | ( | } |
| ; | $ | % | ^ | + | ‖ | + | $ | % | ^ | : |
| ~ | ! | @ | # | \| | ‖ | \| | ! | @ | # | ~ |
| | | ` | _ | ▽ | ‖ | ▽ | ▽ | · | | |
