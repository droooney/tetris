from tkinter import *
from functools import reduce
from timer import Timer
from figure import gen_rand_figure_constructor
from constants import *


class Tetris(Frame):
    def __init__(self, **kwargs):
        Frame.__init__(self, **kwargs)

        self.status = None
        self.timer = Timer(0, lambda: 0)
        self.clear_timer = Timer(0, lambda: 0)
        self.current_figure = None

        self.grid()
        self.grid_columnconfigure(0, minsize=CANVAS_WIDTH)
        self.grid_columnconfigure(1, minsize=SIDE_PANEL_WIDTH)
        self.grid_rowconfigure(0, minsize=CANVAS_HEIGHT)

        self.create_field()
        self.create_side_panel()
        self.change_status(GAME_ENDED)

    def create_field(self):
        canvas = self.field_canvas = Canvas(
            self,
            bd=0,
            width=CANVAS_WIDTH,
            height=CANVAS_HEIGHT,
            bg='#ececec'
        )
        canvas.grid(
            row=0,
            column=0
        )

        self.field = []

        for i in range(HEIGHT):
            row = []
            self.field.append(row)

            for j in range(WIDTH):
                y = i * SIZE + 3
                x = j * SIZE + 3

                canvas.create_rectangle(
                    x,
                    y,
                    x + SIZE,
                    y + SIZE
                )

                row.append(None)

    def empty_field(self):
        new_field = []

        for i in range(HEIGHT):
            row = []
            new_field.append(row)

            for j in range(WIDTH):
                row.append(None)

                cell = self.field[i][j]

                if cell:
                    self.field_canvas.delete(cell)

        self.field = new_field

    def create_side_panel(self):
        frame = self.side_panel = Frame(
            self,
            bd=10,
            width=SIDE_PANEL_WIDTH,
            height=SIDE_PANEL_HEIGHT
        )
        frame.grid(
            row=0,
            column=1
        )
        frame.grid_columnconfigure(0, minsize=SIDE_PANEL_WIDTH)

        self.create_points_frame()
        self.create_next_figure_panel()
        self.create_buttons()

    def create_points_frame(self):
        points_frame = Frame(
            self.side_panel,
            bd=10,
            highlightbackground='#000',
            highlightthickness=1
        )
        points_frame.grid(
            row=0,
            column=0
        )

        Label(
            points_frame,
            text='Points'
        ).grid(
            row=0,
            column=0
        )

        self.points = StringVar(value=0)
        Label(
            points_frame,
            textvariable=self.points
        ).grid(
            row=1,
            column=0
        )

    def create_next_figure_panel(self):
        next_figure_frame = Frame(
            self.side_panel,
            bd=10,
            highlightbackground='#000',
            highlightthickness=1
        )
        next_figure_frame.grid(
            row=1,
            column=0,
            pady=10
        )

        Label(
            next_figure_frame,
            text='Next:'
        ).grid(
            row=0,
            column=0
        )

        self.next_figure_canvas = Canvas(
            next_figure_frame,
            bd=0,
            width=NEXT_FIGURE_CANVAS_WIDTH,
            height=NEXT_FIGURE_CANVAS_HEIGHT,
            bg='#eee'
        )
        self.next_figure_canvas.grid(
            row=1,
            column=0
        )

    def create_buttons(self):
        buttons = Frame(self.side_panel)
        buttons.grid(
            row=2,
            column=0,
            pady=10
        )

        self.start_game_button = Button(
            buttons,
            text='Start',
            command=self.start_game
        )
        self.start_game_button.grid(
            row=0,
            column=0
        )

        self.pause_game_caption = StringVar(value='Pause')

        self.pause_game_button = Button(
            buttons,
            state=DISABLED,
            textvariable=self.pause_game_caption,
            command=self.pause_or_continue_game
        )
        self.pause_game_button.grid(
            row=1,
            column=0
        )

        self.end_game_button = Button(
            buttons,
            state=DISABLED,
            text='End',
            command=self.end_game
        )
        self.end_game_button.grid(
            row=2,
            column=0
        )

    def on_key_pressed(self, event):
        sym = event.keysym

        if sym == 'a' or sym == 'Left':
            # move left

            if self.current_figure and self.current_figure.is_inserted:
                self.current_figure.move_to_the_side(-1)
        elif sym == 'd' or sym == 'Right':
            # move right

            if self.current_figure and self.current_figure.is_inserted:
                self.current_figure.move_to_the_side(1)
        elif sym == 's' or sym == 'Down':
            # speed up falling

            if self.current_figure and self.current_figure.is_inserted:
                self.current_figure.move_down()
        elif sym == 'f':
            # fall immediately
            print('Fall')
        elif sym == 'space':
            # rotate figure

            if self.current_figure and self.current_figure.is_inserted:
                self.current_figure.rotate_right()

    def on_quit(self):
        print('quitting')
        self.end_game()
        root.destroy()

    def change_status(self, status):
        start_game_button_state = DISABLED
        pause_game_button_state = DISABLED
        end_game_button_state = DISABLED
        pause_button_caption = 'Pause'

        if status == IN_GAME:
            pause_game_button_state = NORMAL
            end_game_button_state = NORMAL
        elif status == GAME_ENDED:
            start_game_button_state = NORMAL
        elif status == GAME_PAUSED:
            pause_game_button_state = NORMAL
            end_game_button_state = NORMAL
            pause_button_caption = 'Continue'

        self.status = status
        self.start_game_button['state'] = start_game_button_state
        self.pause_game_button['state'] = pause_game_button_state
        self.end_game_button['state'] = end_game_button_state
        self.pause_game_caption.set(pause_button_caption)

    def start_game(self):
        self.set_level(1)
        self.set_score_coeff(1)
        self.set_lines_cleared(0)
        self.change_status(IN_GAME)
        self.set_interval(LEVEL_1_INTERVAL)
        self.set_score(0)
        self.empty_field()
        self.generate_figure()
        self.insert_figure()

    def pause_or_continue_game(self):
        if self.status == IN_GAME:
            self.pause_game()
        elif self.status == GAME_PAUSED:
            self.continue_game()

    def pause_game(self):
        self.change_status(GAME_PAUSED)
        self.timer.pause()
        self.clear_timer.pause()

    def continue_game(self):
        self.change_status(IN_GAME)
        self.timer.resume()
        self.clear_timer.resume()

    def end_game(self):
        self.change_status(GAME_ENDED)

        self.timer.cancel()
        self.clear_timer.cancel()

        print('end game')

    def set_lines_cleared(self, lines):
        self.lines_cleared = lines

    def set_level(self, level):
        self.level = level

    def set_interval(self, interval):
        self.interval = interval

    def set_score_coeff(self, coeff):
        self.score_coeff = coeff

    def set_score(self, score):
        self.score = score
        self.points.set(score)

    def generate_figure(self):
        self.next_figure = gen_rand_figure_constructor()(self)

    def insert_figure(self):
        self.current_figure = self.next_figure
        self.current_figure.insert()
        self.generate_figure()

    def check_lines(self):
        field = self.field
        lines = []

        for (y, row) in enumerate(self.field):
            if not all(row):
                continue

            lines.append(y)

            for (x, rect) in enumerate(row):
                field[y][x] = None
                self.field_canvas.delete(rect)

        if not lines:
            self.insert_figure()

            return

        score = POINTS[len(lines)]

        self.set_lines_cleared(self.lines_cleared + len(lines))

        level = self.lines_cleared // 10

        if self.level != level:
            self.set_level(level)
            self.set_interval(LEVEL_1_INTERVAL * (SPEED_INCREASE_COEFF ** level))
            self.set_score_coeff(SCORE_INCREASE_COEFF ** level)

        self.set_score(self.score + int(score*self.score_coeff))

        self.clear_timer = Timer(0.5, lambda: self.fall(lines))

    def fall(self, lines):
        field = self.field

        for (y, row) in enumerate(reversed(self.field)):
            y = HEIGHT - 1 - y

            if y in lines:
                continue

            rows_to_fall = reduce((lambda s, i: s + (1 if i > y else 0)), lines, 0)

            if any(field[y + rows_to_fall]) and rows_to_fall:
                print('Error:', field[y + rows_to_fall], y, y + rows_to_fall)

            for (x, rect) in enumerate(row):
                field[y][x] = None
                field[y + rows_to_fall][x] = rect

                if rect:
                    self.field_canvas.move(rect, 0, rows_to_fall * SIZE)

        self.insert_figure()


root = Tk()

my_app = Tetris(master=root)
my_app.master.wm_title('Tetris')
my_app.master.minsize(CONTAINER_WIDTH, CONTAINER_HEIGHT)
my_app.master.maxsize(CONTAINER_WIDTH, CONTAINER_HEIGHT)

root.protocol('WM_DELETE_WINDOW', my_app.on_quit)
root.bind('<Key>', my_app.on_key_pressed)

root.mainloop()
