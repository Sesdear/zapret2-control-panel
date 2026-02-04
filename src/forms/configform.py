import curses
import os
import json
from src.forms.changestrategyform import change_strategy_screen
from src.forms.changeipsetform import change_ipset_screen

CONFIG_PATH = "/opt/zapret2-installer/data/config.json"


def config_form_screen(stdscr):
    curses.curs_set(0)
    stdscr.timeout(-1)
    stdscr.clear()

    height, width = stdscr.getmaxyx()

    if height < 14 or width < 60:
        msg = "Окно слишком маленькое (рекомендуется минимум 60×14)"
        stdscr.addstr(height // 2, max(0, (width - len(msg)) // 2), msg)
        stdscr.refresh()
        stdscr.getch()
        return

    options = [
        "Сменить стратегию",
        "Сменить лист обхода (ipset)",
        "Назад в меню"
    ]

    current_option = 0

    def get_current_strategy():
        if not os.path.exists(CONFIG_PATH) or os.path.getsize(CONFIG_PATH) == 0:
            return "Unknown"
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data.get("strategy", "Unknown")
        except Exception:
            return "Ошибка чтения конфига"

    def refresh_screen(message=None, msg_color=0):
        stdscr.erase()

        title = " Настройка конфигурации zapret2 "
        stdscr.attron(curses.A_BOLD | curses.color_pair(1))
        stdscr.addstr(2, max(0, (width - len(title)) // 2), title)
        stdscr.attroff(curses.A_BOLD | curses.color_pair(1))

        stdscr.hline(4, 4, curses.ACS_HLINE, width - 8, curses.color_pair(4))

        strategy = get_current_strategy()
        strat_color = curses.color_pair(2) if strategy not in ("Unknown", "Ошибка чтения конфига") else curses.color_pair(3)
        stdscr.addstr(6, 6, f"Текущая стратегия: {strategy}", strat_color)

        stdscr.hline(8, 4, curses.ACS_HLINE, width - 8, curses.color_pair(4))

        for i, text in enumerate(options):
            y = 10 + i * 2
            x = 8
            item_text = f"  {text}  "

            if i == current_option:
                stdscr.attron(curses.color_pair(1) | curses.A_REVERSE)
                safe_addstr(stdscr, y, x, item_text.ljust(width - x - 4))
                stdscr.attroff(curses.color_pair(1) | curses.A_REVERSE)
            else:
                safe_addstr(stdscr, y, x, item_text, curses.color_pair(4))

        hint = " ↑↓ / j k — выбор   Enter — действие   q / ESC — назад "
        safe_addstr(stdscr, height - 3, max(6, (width - len(hint)) // 2), hint, curses.color_pair(4))

        if message:
            safe_addstr(stdscr, height - 6, 6, message, msg_color)
            stdscr.refresh()
            curses.napms(1400)
            stdscr.erase()

        stdscr.refresh()

    refresh_screen()

    while True:
        key = stdscr.getch()

        if key in (curses.KEY_UP, ord('k')):
            current_option = (current_option - 1) % len(options)
            refresh_screen()

        elif key in (curses.KEY_DOWN, ord('j')):
            current_option = (current_option + 1) % len(options)
            refresh_screen()

        elif key in (10, 13, curses.KEY_ENTER):
            if current_option == 0:
                change_strategy_screen(stdscr)
                refresh_screen()

            elif current_option == 1:
                change_ipset_screen(stdscr)
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