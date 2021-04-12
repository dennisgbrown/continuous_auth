#!bin/env python3
import sys
from datetime import datetime
from keystrokes import Keystrokes

def elapsed_ms(start):
    dt = datetime.now()
    return int((dt - start).total_seconds() * 1000)

if __name__ == '__main__':

    start = datetime.now()
    pressed_keys = {}
    keystrokes = []
    if len(sys.argv) != 2:
        print("usage: python3 ./keylogger.py <filename>")
        exit(0)
        
    filename = sys.argv[1]
    
    while True:
        try:
            line = input()
            if not line.startswith('keycode'):
                # disregard initial and closing lines
                continue
            code, action = line.split()[1:]
            code = int(code)
            
            if action == "press" and code not in pressed_keys:
                pressed_keys[code] = elapsed_ms(start)
            elif action == "release" and code in pressed_keys:
                keystrokes.append([code, pressed_keys.pop(code), elapsed_ms(start)])
            # else disregard "press" with previously pressed keys
            # or "release" with unpressed keys

        # I think python might get the CTRL-C signal instead of showkey, or both
        except EOFError:
            break
        except KeyboardInterrupt:
            break
        
    Keystrokes.write_to_txt(keystrokes, filename)

    
