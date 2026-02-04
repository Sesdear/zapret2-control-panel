import curses
from src.utils.ipset_list import IpsetList
from src.utils.apply_ipset import ApplyIpset


def change_ipset_screen(stdscr):
    curses.curs_set(0)
    stdscr.timeout(-1)

    try:
        ipsets = IpsetList.fetch_ipsets()
    except Exception as e:
        return

    if not ipsets:
        return

    current_idx = 0
    scroll_offset = 0
    max_visible = 0

    def refresh():
        nonlocal max_visible
        stdscr.erase()
        h, w = stdscr.getmaxyx()

        title = " Смена  "
        safe_addstr(stdscr, 1, (w - len(title)) // 2, title, curses.A_BOLD | curses.color_pair(1))

        stdscr.hline(3, 2, curses.ACS_HLINE, w - 4, curses.color_pair(4))

        max_visible = h - 12

        for screen_row in range(max_visible):
            real_idx = scroll_offset + screen_row
            if real_idx >= len(ipsets):
                break

            y = 5 + screen_row
            num = real_idx + 1
            text = f"{num:3d}. {ipsets[real_idx]}"

            if real_idx == current_idx:
                stdscr.attron(curses.color_pair(1) | curses.A_REVERSE)
                safe_addstr(stdscr, y, 4, text.ljust(w - 8))
                stdscr.attroff(curses.color_pair(1) | curses.A_REVERSE)
            else:
                safe_addstr(stdscr, y, 4, text[:w - 8], curses.color_pair(5))

        if scroll_offset > 0:
            safe_addstr(stdscr, 4, w - 10, "▲ Вверх", curses.color_pair(4))
        if scroll_offset + max_visible < len(ipsets):
            safe_addstr(stdscr, 5 + max_visible, w - 10, "▼ Вниз", curses.color_pair(4))

        hint = " ↑↓ — выбор   Enter — применить   q / ESC — назад "
        safe_addstr(stdscr, h - 3, max(4, (w - len(hint)) // 2), hint, curses.color_pair(4))

        stdscr.refresh()

    refresh()

    while True:
        key = stdscr.getch()
        h, w = stdscr.getmaxyx()
        max_visible = h - 12

        if key in (curses.KEY_UP, ord('k')):
            if current_idx > 0:
                current_idx -= 1
                if current_idx < scroll_offset:
                    scroll_offset = current_idx
            refresh()

        elif key in (curses.KEY_DOWN, ord('j')):
            if current_idx < len(ipsets) - 1:
                current_idx += 1
                if current_idx >= scroll_offset + max_visible:
                    scroll_offset = current_idx - max_visible + 1
            refresh()

        elif key in (10, 13, curses.KEY_ENTER):
            selected_strategy = ipsets[current_idx]

            if ApplyIpset.requires_root():
                safe_addstr(stdscr, h - 6, 6, "Требуются права root (sudo)", curses.color_pair(3))
                stdscr.refresh()
                curses.napms(2200)
                refresh()
                continue

            try:
                ApplyIpset.apply_ipset(selected_strategy)
                msg = f"Применен ipset: {selected_strategy}"
                safe_addstr(stdscr, h - 6, 6, msg, curses.color_pair(2))
                stdscr.refresh()
                curses.napms(1800)
                return
            except Exception as e:
                safe_addstr(stdscr, h - 6, 6, f"Ошибка: {str(e)[:60]}", curses.color_pair(3))
                stdscr.refresh()
                curses.napms(3000)
                refresh()

        elif key in (ord('q'), ord('Q'), 27):
            return

        elif key == curses.KEY_RESIZE:
            refresh()
            
def safe_addstr(win, y, x, text, attr=0):
    if y < 0 or y >= win.getmaxyx()[0]:
        return
    maxw = win.getmaxyx()[1] - x
    if maxw <= 0:
        return
    win.addnstr(y, x, text, maxw, attr)