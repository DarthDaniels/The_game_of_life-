import pygame as pg

pg.init()

default = (600, 600, 10, 0, 0, 0, 10, 200, 56, 3, 3, 2, 3, 1, 59, 1)
LINE_COLOR = (192, 192, 192)


def read_settings(settings_file_name):
    try:
        data = [int(string.split(sep="=")[-1]) for string in open(settings_file_name, "r").read().split(sep="\n")]
    except ValueError:
        data = default
    return data


def write_settings(settings_file_name):
    data = open(settings_file_name, "w")
    data.write(f'''WIDTH={WIDTH}\nHEIGHT={HEIGHT}\nFPS={FPS}
R0={R0}\nG0={G0}\nB0={B0}
R1={R1}\nG1={G1}\nB1={B1}
MIN={MIN}\nMAX={MAX}\nBOT={BOT}\nTOP={TOP}''')


def draw_grid(screen, line_color):
    for h in range(HEIGHT//PIXEL_SIZE):
        pg.draw.rect(screen, line_color, (0, (LINE_THICKNESS+PIXEL_SIZE)*h, WIDTH, LINE_THICKNESS))
    for w in range(WIDTH//PIXEL_SIZE):
        pg.draw.rect(screen, line_color, ((LINE_THICKNESS+PIXEL_SIZE)*w, 0, LINE_THICKNESS, HEIGHT))


def draw_pixels(m, screen, color_1):
    for line in range(len(m)):
        for elm in range(len(m[line])):
            if m[line][elm] == 1:
                pg.draw.rect(screen, color_1, (elm*(PIXEL_SIZE+LINE_THICKNESS), line*(PIXEL_SIZE+LINE_THICKNESS),
                             PIXEL_SIZE+LINE_THICKNESS, PIXEL_SIZE+LINE_THICKNESS))


def show_field(m, screen, line_color, color_1):
    draw_pixels(m, screen, color_1)
    draw_grid(screen, line_color)


def change_state(m, event_list):
    pos = pg.mouse.get_pos()
    changes_list = []
    _ = PIXEL_SIZE+LINE_THICKNESS
    for event in event_list:
        if event.type == pg.MOUSEBUTTONDOWN:
            x, y = pos[0]//_, pos[1]//_
            changes_list.append([x, y, 0 if m[y][x] == 1 else 1])
    return changes_list


def game(m, rule_about_borders):
    new_m = [[-1 for _ in range(len(m[0]))] for p in range(len(m))]

    for line_i in range(len(m)):
        for elm_i in range(len(m[0])):
            neighbours = 0
            for line_shift in [-1, 0, 1]:
                for elm_shift in [-1, 0, 1]:
                    if not(line_shift == 0 and elm_shift == 0):
                        if rule_about_borders:
                            if 0 <= line_i+line_shift < len(m) and 0 <= elm_i+elm_shift < len(m[0]):
                                if m[line_i+line_shift][elm_i+elm_shift] == 1:
                                    neighbours += 1
                        else:
                            if m[(line_i+line_shift) % len(m)][(elm_i+elm_shift) % len(m[0])] == 1:
                                neighbours += 1

            if m[line_i][elm_i] == 0:
                if MIN <= neighbours <= MAX:
                    new_m[line_i][elm_i] = 1
                else:
                    new_m[line_i][elm_i] = 0
            if m[line_i][elm_i] == 1:
                if BOT <= neighbours <= TOP:
                    new_m[line_i][elm_i] = 1
                else:
                    new_m[line_i][elm_i] = 0

    return new_m


WIDTH, HEIGHT, FPS, R0, G0, B0, R1, G1, B1, MIN, MAX, BOT, TOP, WORLD_BORDERS, PIXEL_SIZE, \
    LINE_THICKNESS = read_settings("settings.txt")

scr = pg.display.set_mode([WIDTH, HEIGHT])
pg.display.set_caption("Life Game +")
clock = pg.time.Clock()

matrix = [[0 for _ in range(WIDTH//(PIXEL_SIZE+LINE_THICKNESS))] for _ in range(HEIGHT//(PIXEL_SIZE+LINE_THICKNESS))]

run = True
time_is_going = False

while run:
    events = pg.event.get()
    pressed = pg.key.get_pressed()
    for evnt in events:
        if evnt.type == pg.QUIT:
            run = False
        if evnt.type == pg.KEYDOWN:
            if evnt.key == pg.K_SPACE:
                time_is_going = False if time_is_going else True

    scr.fill([R0, G0, B0])
    show_field(matrix, scr, LINE_COLOR, (R1, G1, B1))
    if time_is_going: matrix = game(matrix, WORLD_BORDERS)

    for changes in change_state(matrix, events):
        matrix[changes[1]][changes[0]] = changes[2]

    clock.tick(FPS)
    pg.display.update()

pg.quit()
