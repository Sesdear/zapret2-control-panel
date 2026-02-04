import curses
import sys
from pysysctllib import Systemctl

from src.forms.serviceform import service_form_screen
from src.forms.configform import config_form_screen

SERVICE = Systemctl("zapret2")


def get_service_status():
    try:
        if SERVICE.is_active():
            return "active", "работает", "Выключить"
        else:
            return "inactive", "остановлен", "Включить"
    except Exception as e:
        return "error", f"ошибка: {str(e)}", "Ошибка"


def safe_addstr(win, y, x, text, attr=0):
    """Безопасный вывод строки — не выходит за пределы окна"""
    if y < 0 or y >= win.getmaxyx()[0]:
        return
    maxw = win.getmaxyx()[1] - x
    if maxw <= 0:
        return
    win.addnstr(y, x, text, maxw, attr)


def main(stdscr):
    curses.curs_set(0)
    stdscr.timeout(100)
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_CYAN, -1)
    curses.init_pair(2, curses.COLOR_GREEN, -1)
    curses.init_pair(3, curses.COLOR_RED, -1)
    curses.init_pair(4, curses.COLOR_YELLOW, -1)

    height, width = stdscr.getmaxyx()

    if height < 20 or width < 70:
        stdscr.clear()
        msg = f"Терминал слишком маленький ({width}x{height}). Нужно минимум 70×20"
        safe_addstr(stdscr, height//2, (width - len(msg))//2, msg, curses.color_pair(3))
        stdscr.refresh()
        stdscr.getch()
        return

    current_row = 0
    menu = [
        "Включить / Выключить сервис",
        "Настройка конфигурации",
        "Настройка сервиса",
        "Проверить на наличие обновлений",
        "Выход"
    ]

    while True:
        stdscr.erase()

        title = " Управление сервисом zapret2 "
        stdscr.attron(curses.color_pair(1) | curses.A_BOLD)
        safe_addstr(stdscr, 1, (width - len(title)) // 2, title)
        stdscr.attroff(curses.color_pair(1) | curses.A_BOLD)

        stdscr.hline(3, 4, curses.ACS_HLINE, width - 8, curses.color_pair(4))

        status_code, status_text, button_text = get_service_status()
        status_line = f"Статус сервиса: {status_text}"
        color = 2 if status_code == "active" else 3 if status_code == "inactive" else 4
        stdscr.attron(curses.color_pair(color))
        safe_addstr(stdscr, 5, 4, status_line)
        stdscr.attroff(curses.color_pair(color))

        safe_addstr(stdscr, 7, 4, f"Действие: {button_text}", curses.A_BOLD | curses.color_pair(1))

        stdscr.hline(9, 4, curses.ACS_HLINE, width - 8, curses.color_pair(4))

        for idx, item in enumerate(menu):
            y = 11 + idx
            x = 6
            text = f"  {item}  "
            if idx == current_row:
                stdscr.attron(curses.color_pair(1) | curses.A_REVERSE)
                safe_addstr(stdscr, y, x, text.ljust(width - x - 4))
                stdscr.attroff(curses.color_pair(1) | curses.A_REVERSE)
            else:
                safe_addstr(stdscr, y, x, text, curses.color_pair(4))

        hint = " ↑↓ / j k — перемещение   Enter — выбрать   q / ESC — выход "
        safe_addstr(stdscr, height - 3, max(4, (width - len(hint)) // 2), hint, curses.color_pair(4))

        author = "Created by sesdear.github.io"
        safe_addstr(stdscr, height - 2, width - len(author) - 4, author, curses.color_pair(4))

        stdscr.refresh()

        key = stdscr.getch()

        if key in (curses.KEY_UP, ord('k')):
            current_row = (current_row - 1) % len(menu)
        elif key in (curses.KEY_DOWN, ord('j')):
            current_row = (current_row + 1) % len(menu)
        elif key in (10, 13, curses.KEY_ENTER):
            if current_row == 0:
                try:
                    if SERVICE.is_active():
                        SERVICE.stop()
                        msg = "Сервис остановлен          "
                        color = curses.color_pair(3)
                    else:
                        SERVICE.start()
                        msg = "Сервис запущен             "
                        color = curses.color_pair(2)
                    safe_addstr(stdscr, height - 5, 4, msg, color)
                    stdscr.refresh()
                    curses.napms(1400)
                except Exception as e:
                    safe_addstr(stdscr, height - 5, 4, f"Ошибка: {str(e)[:60]}", curses.color_pair(3))
                    stdscr.refresh()
                    curses.napms(2000)
            elif current_row == 1:
                config_form_screen(stdscr)
            elif current_row == 2:
                service_form_screen(stdscr)
            elif current_row == 3:
                safe_addstr(stdscr, height - 5, 4, "Проверка обновлений — пока не реализовано", curses.color_pair(4))
                stdscr.refresh()
                curses.napms(1800)
            elif current_row == 4:
                break
        elif key in (ord('q'), ord('Q'), 27):
            break


if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        print("Ошибка:", e, file=sys.stderr)
        sys.exit(1)