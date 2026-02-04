import curses
from pysysctllib import Systemctl

SERVICE_NAME = "zapret2"
SERVICE = Systemctl(SERVICE_NAME)


def service_form_screen(stdscr):

    curses.curs_set(0)
    stdscr.timeout(-1)
    stdscr.clear()

    height, width = stdscr.getmaxyx()

    if height < 12 or width < 55:
        msg = "Окно слишком маленькое (нужно минимум 55×12)"
        stdscr.addstr(height//2, max(0, (width - len(msg))//2), msg)
        stdscr.refresh()
        stdscr.getch()
        return

    current_option = 0

    def refresh_screen(show_message=False, msg_text="", msg_attr=0):
        stdscr.clear()

        title = f" Настройка сервиса {SERVICE_NAME} "
        stdscr.attron(curses.A_BOLD | curses.color_pair(1))
        stdscr.addstr(2, max(0, (width - len(title)) // 2), title)
        stdscr.attroff(curses.A_BOLD | curses.color_pair(1))

        stdscr.addstr(4, 4, "─" * (width - 8), curses.color_pair(4))

        try:
            is_active = SERVICE.is_active()
            is_enabled = SERVICE.is_enabled()

            status_run = "работает" if is_active else "остановлен"
            status_auto = "включён" if is_enabled else "отключён"

            color_run  = curses.color_pair(2) if is_active else curses.color_pair(3)
            color_auto = curses.color_pair(2) if is_enabled else curses.color_pair(3)

            stdscr.addstr(6, 6, f"Состояние сервиса:   {status_run}", color_run)
            stdscr.addstr(7, 6, f"Автозапуск (boot):   {status_auto}", color_auto)

            toggle_text = "Отключить автозапуск" if is_enabled else "Включить автозапуск"
        except Exception as e:
            toggle_text = "Ошибка"
            stdscr.addstr(6, 6, f"Не удалось получить статус: {str(e)}", curses.color_pair(3))

        options = [toggle_text, "Назад в меню"]

        stdscr.addstr(9, 4, "─" * (width - 8), curses.color_pair(4))

        for i, text in enumerate(options):
            y = 11 + i * 2
            x = 8

            if i == current_option:
                stdscr.attron(curses.color_pair(1) | curses.A_REVERSE)
                safe_addstr(stdscr, y, x, f"  {text}  ".ljust(width - x - 4))
                stdscr.attroff(curses.color_pair(1) | curses.A_REVERSE)
            else:
                safe_addstr(stdscr, y, x, f"  {text}")

        stdscr.addstr(height - 4, 6,
                        "↑↓ / j k — выбор    Enter — действие    q / ESC — назад",
                        curses.color_pair(4))

        if show_message and msg_text:
            safe_addstr(stdscr, height - 6, 6, msg_text, msg_attr)
            stdscr.refresh()
            curses.napms(1400)

        stdscr.refresh()

    refresh_screen()

    while True:
        key = stdscr.getch()

        if key in (curses.KEY_UP, ord('k')):
            current_option = (current_option - 1) % 2
            refresh_screen()

        elif key in (curses.KEY_DOWN, ord('j')):
            current_option = (current_option + 1) % 2
            refresh_screen()

        elif key in (10, 13, curses.KEY_ENTER):
            if current_option == 0:
                try:
                    if SERVICE.is_enabled():
                        SERVICE.disable()
                        refresh_screen(True, "Автозапуск отключён", curses.color_pair(3))
                    else:
                        SERVICE.enable()
                        refresh_screen(True, "Автозапуск включён", curses.color_pair(2))
                except Exception as e:
                    refresh_screen(True, f"Ошибка: {str(e)[:60]}", curses.color_pair(3))
                refresh_screen()

            elif current_option == 1:
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