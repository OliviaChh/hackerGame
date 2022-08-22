from collections import defaultdict
import random
from typing import Callable, Dict, Optional, List, Tuple

from behave import *
from director import * 
from director.common import *
import tkinter as tk


@given("I start the application")
def startup(context):
    random.seed(10017030)

    VacantLog(tk.Tk, "mainloop")
    context.after_binds = VacantLog(tk.Tk, "after")
    context.key_binds = VacantLog(tk.Tk, "bind")

    root = tk.Tk()
    context.window = root

    context.under_test.start_game(root, TASK=1)

    root.update()

    root.mainloop()


def find_canvas_by_filter(root: tk.Tk, filter: Callable[[tk.Canvas], bool]):
    widgets = find_widgets(WidgetSelector.by_type(tk.Canvas), root)
    assert len(widgets) > 1, f"there are no Canvas widgets in the application"

    for canvas in widgets:
        assert isinstance(canvas, tk.Canvas), "internal tester error: report to course staff"
        if filter(canvas):
            return canvas


"""Step operations"""

def step(context, times=1):
    if len(context.after_binds.logs) == 0:
        assert False, "no calls made to the tkinter after method, see: https://web.archive.org/web/20171112175007/http://www.effbot.org/tkinterbook/widget.htm#Tkinter.Widget.after-method"

    method_call = context.after_binds.logs[0]

    positional_arguments = method_call[0]

    if len(positional_arguments) < 2:
        assert False, f"call to after does not specify a delay and a callback, got: after({', '.join(positional_arguments)})"
    
    time = positional_arguments[0]
    callback = positional_arguments[1]

    for _ in range(times):
        callback()


@when("the game steps")
def steps_once(context):
    step(context)

@when("the game steps {times:Number} times")
def steps(context, times):
    step(context, times=times)


"""Keypress operations"""

class Event:
    chars = ('W', 'A', 'S', 'D')
    keysyms = ('Left', 'Right', 'Up', 'Down')

    def __init__(self, char, keysym, keycode):
        self.char = char
        self.keysym = keysym
        self.keycode = keycode

class Events:
    # LEFT = Event("\uf702", "Left", 2063660802)
    # UP = Event("\uf700", "Up", 2113992448)
    # RIGHT = Event("\uf704", "Right", 2080438019)
    # DOWN = Event("\uf701", "Down", 2097215233)
    # W = Event("w", "w", 222298199)
    A = Event("a", "a", 4194369)
    # S = Event("s", "s", 20971603)
    D = Event("d", "d", 37748804)
    Space = Event(" ", "space", 0)
    Return = Event(" ", "return", 0)

def keypress_func(key_binds):
    always_call = []
    for events in ("<KeyPress>", "<Any-KeyPress>", "<Key>", "<KeyRelease>"):
        kp = key_binds.get(events)
        if kp is not None:
            always_call.append(kp)

    key_calls = defaultdict(list)
    for key in ("a", "d", "space", "return"):
        for keybind in (key, key.upper(), key.capitalize(),
                        f"<{key}>", f"<{key.upper()}>", f"<{key.capitalize()}>",
                        f"<Key-{key}>", f"<Key-{key.upper()}>", f"<Key-{key.capitalize()}>",
                        f"<KeyRelease-{key}>", f"<KeyRelease-{key.upper()}>", f"<KeyRelease-{key.capitalize()}>",
                        f"<KeyPress-{key}>", f"<KeyPress-{key.upper()}>", f"<KeyPress-{key.capitalize()}>"):
            keycb = key_binds.get(keybind)
            if keycb is not None:
                key_calls[key].append(keycb)

    def callback(event):
        found_call = False
        for call in always_call:
            found_call = True
            call(event)
        keycb = key_calls[event.keysym.lower()]
        for call in keycb:
            found_call = True
            call(event)

        if not found_call:
            print(key_binds)
            assert False, f"unable to find an appropriate keyboard binding to call for {event.keysym.lower()}"
    
    return callback

def press(context, key):
    if len(context.key_binds.logs) == 0:
        assert False, "no calls made to the tkinter bind method, see: https://web.archive.org/web/20171112175007/http://www.effbot.org/tkinterbook/widget.htm#Tkinter.Widget.bind-method"

    method_calls = context.key_binds.logs

    key_binds = {}
    for call in method_calls:
        positional_arguments = call[0]

        if len(positional_arguments) < 2:
            assert False, f"call to bind does not specify a key and a callback, got: bind({', '.join(positional_arguments)})"
        
        key_bind = positional_arguments[0]
        callback = positional_arguments[1]

        key_binds[key_bind] = callback

    keypress_func(key_binds)(key)


@when("I press '{key:Text}'")
def press_key(context, key):
    if key not in ("A", "D", "Space", "Return"):
        assert False, f"internal error: invalid key to press: {key}"

    if key == "A":
        press(context, Events.A)
    elif key == "D":
        press(context, Events.D)
    elif key == "Space":
        press(context, Events.Space)
    elif key == "Return":
        press(context, Events.Return)

@when("I press '{key:Text}' {times:Number} times")
def press_key_multiple_times(context, key, times):
    for _ in range(times):
        press_key(context, key)

"""Common hackerview operations"""

GRID_SIZE = 7

def find_player_in_hacker_view(canvas: tk.Canvas) -> Optional[int]:
    for item in canvas.find_all():
        config = canvas.itemconfig(item)
        if "text" in config:
            if config["text"][4] == "P":
                return item


def is_hacker_view(canvas: tk.Canvas) -> bool:
    player = find_player_in_hacker_view(canvas)
    return player is not None


def detect_hacker_view_size(hacker_view: tk.Canvas):
    item = find_player_in_hacker_view(hacker_view)
        
    x, y = hacker_view.coords(item)
    x_size, y_size = x // 3.5, y // 0.5

    logger.info(f"identified grid with cell size x: {x_size} y: {y_size}")

    return x_size, y_size


def format_serialized(serialized: Dict[Tuple[int, int], Tuple[int, ...]], dimensions: Tuple[int, int]):
    result = ""
    for row in range(dimensions[0]):
        for column in range(dimensions[1]):
            result += str(serialized[(row, column)])
        result += "\n"

    return result


def serialize_hacker_view(hacker_view: tk.Canvas):
    x_size, y_size = detect_hacker_view_size(hacker_view)

    columns = int(hacker_view.winfo_width() // x_size)
    rows = int(hacker_view.winfo_height() // y_size)

    logger.info(f"identified {columns} columns and {rows} rows in the hacker view")

    serialized = {}
    for row in range(rows):
        for column in range(columns):
            start_x, start_y = column * x_size, row * y_size
            in_position = hacker_view.find_enclosed(start_x, start_y, start_x + x_size, start_y + y_size)

            serialized[(row, column)] = in_position

    formatted = format_serialized(serialized, (rows, columns))
    logger.info(f"hacker view serialized into \n{formatted}")

    return serialized, (rows, columns)


def convert_to_board(view: tk.Canvas, serialized: Dict[Tuple[int, int], Tuple[int]]):
    result = {}
    for position, items in serialized.items():
        found = None
        for item in items:
            config = view.itemconfig(item)
            if "text" in config and len(config["text"][4]) == 1:
                found = config["text"][4]

        result[position] = found

    return result


@when("I can identify a hacker view with a player")
def identify_grid(context):
    hacker_view = find_canvas_by_filter(context.window, is_hacker_view)
    assert hacker_view is not None, f"unable to find a Canvas which looks like a hacker view" # TODO: add description of identification process

    context.last = hacker_view

@then("it has 7 rows and 7 columns")
def assert_view_size(context):
    hacker_view = context.last

    serialized, dimensions = serialize_hacker_view(hacker_view)

    assert dimensions[0] == GRID_SIZE, f"found {dimensions[0]} rows instead of {GRID_SIZE}"
    assert dimensions[1] == GRID_SIZE, f"found {dimensions[1]} columns instead of {GRID_SIZE}"

@then("the player is in the top row, column 4")
def assert_player_position(context):
    hacker_view = context.last

    serialized, dimensions = serialize_hacker_view(hacker_view)

    at_position = serialized[(0, 3)]

    assert len(at_position) > 0, "no items are found at (0, 3)"

    configs = []
    for item in at_position:
        config = hacker_view.itemconfig(item)
        if "text" in config and config["text"][4] == "P":
            return
        configs += [config]

    assert False, f"unable to find a player at (0, 3), found {configs}"


@then("row {row:Number} has the following entities: \"{entities:Text}\"")
def assert_row(context, row: int, entities: str):
    hacker_view = context.last

    serialized, dimensions = serialize_hacker_view(hacker_view)

    board = convert_to_board(hacker_view, serialized)

    index = GRID_SIZE - 1 - row
    
    actual_entities = ""
    for i in range(len(entities)):
        entity = board[(index, i)]
        entity = entity if entity is not None else "."
        actual_entities += entity

    assert entities == actual_entities, f"expected row {row} to be {entities} but found {actual_entities}"


"""Common scoreboard operations"""

def serialize_text(canvas: tk.Canvas) -> Dict[int, str]:
    result = {}
    for item in canvas.find_all():
        config = canvas.itemconfig(item)
        if "text" in config:
            result[item] = config["text"][4]
    
    return result

def find_text_lowercase(canvas: tk.Canvas, search_for: str) -> Optional[int]:
    texts = serialize_text(canvas)

    for item, text in texts.items():
        if text.lower() == search_for.lower():
            return item

    return None

def find_text_lowercase_substring(canvas: tk.Canvas, search_for: str) -> Optional[int]:
    texts = serialize_text(canvas)

    for item, text in texts.items():
        if search_for.lower() in text.lower():
            return item

    return None

def find_items_on_row(canvas: tk.Canvas, row: float) -> List[int]:
    return canvas.find_overlapping(0, row-1, canvas.winfo_width(), row+1)

def is_scoreboard(canvas: tk.Canvas) -> bool:
    title_id = find_text_lowercase(canvas, "score")
    return title_id is not None


def lookup_value(scoreboard: tk.Canvas, key: str) -> Optional[int]:
    key_id = find_text_lowercase_substring(scoreboard, key)
    assert key_id is not None, f"unable to find the text \"{key}\" in scoreboard"
    _, key_x = scoreboard.coords(key_id)

    items = find_items_on_row(scoreboard, key_x)
    for item, text in serialize_text(scoreboard).items():
        if item not in items:
            continue

        if text.isnumeric():
            return int(text)

    return None


@when("I can identify a score sidebar")
def identify_score(context):
    scoreboard = find_canvas_by_filter(context.window, is_scoreboard)
    assert scoreboard is not None, f"unable to find a Canvas which looks like a scoreboard" # TODO: add description of identification process

    context.last = scoreboard

@then("{key:Text} count equals {count:Number}")
def collected_count(context, key, count):
    value = lookup_value(context.last, key)
    assert value is not None, f"failed to find a value for key {key}" # TODO: explain why

    assert value == count, f"the value for {key} was {value}, expected {count}"
