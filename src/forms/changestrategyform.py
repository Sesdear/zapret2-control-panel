import curses
from src.forms.manualstrategy import manual_strategy_screen

def change_strategy_screen(stdscr):
    curses.curs_set(0)
    stdscr.timeout(-1)

    current_option = 0
    options = [
        "Выбрать стратегию вручную",
        "Автоматический подбор стратегии",
        "Назад в настройки"
    ]

    message = None
    msg_color = 0
    message_timer = 0

    def refresh_screen():
        nonlocal message, message_timer

        stdscr.erase()
        h, w = stdscr.getmaxyx()

        title = " Выбор способа смены стратегии "
        stdscr.attron(curses.A_BOLD | curses.color_pair(1))
        safe_addstr(stdscr, 2, max(0, (w - len(title)) // 2), title)
        stdscr.attroff(curses.A_BOLD | curses.color_pair(1))

        stdscr.hline(4, 4, curses.ACS_HLINE, w - 8, curses.color_pair(4))

        safe_addstr(stdscr, 6, 6,
                    "Выберите способ установки новой стратегии:",
                    curses.color_pair(4))

        for i, text in enumerate(options):
            y = 9 + i * 2
            x = 8
            item_text = f"  {text}  "

            if i == current_option:
                stdscr.attron(curses.color_pair(1) | curses.A_REVERSE)
                safe_addstr(stdscr, y, x, item_text.ljust(w - x - 4))
                stdscr.attroff(curses.color_pair(1) | curses.A_REVERSE)
            else:
                safe_addstr(stdscr, y, x, item_text, curses.color_pair(4))

        stdscr.hline(h - 7 if h > 20 else h - 6, 4,
                        curses.ACS_HLINE, w - 8, curses.color_pair(4))

        hint = " ↑↓ / j k — выбор   Enter — действие   q / ESC — назад "
        safe_addstr(stdscr, h - 3, max(4, (w - len(hint)) // 2),
                    hint, curses.color_pair(4))

        if message and message_timer > 0:
            safe_addstr(stdscr, h - 5, 6, message, msg_color)
            message_timer -= 1
        else:
            message = None
            message_timer = 0
        stdscr.refresh()

    refresh_screen()

    while True:
        key = stdscr.getch()
        h, w = stdscr.getmaxyx()

        if key == curses.KEY_RESIZE:
            refresh_screen()
            continue

        if key in (curses.KEY_UP, ord('k')):
            current_option = (current_option - 1) % len(options)
            refresh_screen()

        elif key in (curses.KEY_DOWN, ord('j')):
            current_option = (current_option + 1) % len(options)
            refresh_screen()

        elif key in (10, 13, curses.KEY_ENTER):
            if current_option == 0:
                try:
                    manual_strategy_screen(stdscr)
                    refresh_screen()
                except NameError:
                    message = "Экран ручного выбора пока не подключён"
                    msg_color = curses.color_pair(4)
                    message_timer = 20
                    refresh_screen()

            elif current_option == 1:
                message = "Автоматический подбор пока не реализован"
                msg_color = curses.color_pair(4)
                message_timer = 20
                refresh_screen()

            elif current_option == 2:
                return

        elif key in (ord('q'), ord('Q'), 27):
            return


def safe_addstr(win, y, x, text, attr=0):
    if y < 0 or y >= win.getmaxyx()[0]:
        return
    maxw = win.getmaxyx()[1] - x
    if maxw <= 0:
        return
    win.addnstr(y, x, text, maxw, attr)