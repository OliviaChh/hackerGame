from a3_support import *
import tkinter as tk
import random
from PIL import Image, ImageTk
from tkinter import messagebox
from tkinter import filedialog

def start_game(root, TASK=TASK):
    """Distinguish controller to start game"""
    controller = HackerController

    if TASK != 1:
        controller = AdvancedHackerController

    app = controller(root, GRID_SIZE)
    return app

def main():
    """Instantiates GUI for visualization."""
    root = tk.Tk()
    root.title(TITLE)
    app = start_game(root)
    root.mainloop() 

class Entity(object):
    """Abstract entity reresent element that can appear on the game"""
    def display(self) -> str:
        """This method needs to be implemented by subclasses"""
        raise NotImplementedError
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"
    
class Player(Entity):
    def display(self) -> str:
        """Return P"""
        return PLAYER
        
class Destroyable(Entity):   
    def display(self) -> str:
        """Return D"""
        return DESTROYABLE
    
class Collectable(Entity):  
    def display(self) -> str:
        """Return C"""
        return COLLECTABLE
    
class Blocker(Entity): 
    def display(self) -> str:
        """Return B"""
        return BLOCKER

class Bomb(Entity):
    def display(self) -> str:
        """Return O"""
        return BOMB

class Grid:
    """Represent the 2D grid of entities"""
    gamebox={}
    def __init__(self, size: int) -> None:
        self.size = size
        self.serialise_gamebox = {}
        
    def get_size(self) -> int:
        return self.size 
    
    def add_entity(self, position: "Position", entity: "Entity") -> None:
        """Add a given entity into the grid at a specified position when the positionis true"""
        if self.in_bounds(position)==True:
            Grid.gamebox[position] = entity      
        
    def get_entities(self) -> 'Dict[Position, Entity]':
        """Return the dictionary containing grid entities"""
        return Grid.gamebox
        
    def get_entity(self, position: Position) -> Optional[Entity]:
        """Return a entity from the grid at a specific position"""
        return Grid.gamebox.get(position)
        
    def remove_entity(self, position: Position) -> None:
        """Remove an entity from the grid"""
        Grid.gamebox.pop(position)
        
    def serialise(self) -> 'Dict[Tuple[int, int], str]':
        """Convert dictionary of Position and Entities into a simplified

        Return(Tuple):
            Tuples are represented by the x and y coordinates of a Positions
            and Entities are represented by their ‘display()‘ character.
        """
        for key in Grid.gamebox.keys():
            self.serialise_gamebox[(key.get_x(), key.get_y())]= Grid.gamebox[key].display()
        return self.serialise_gamebox
    
    def in_bounds(self, position: Position) -> bool:
        """Return a boolean based on whether the position is valid

        Precondition:
            x≥0 and x<gridsize
            y≥1 and y<gridsize
        """
        if ((0 <= position.get_x() and position.get_x() < self.size)
            and (1 <= position.get_y() and position.get_y() < self.size)):
            return True
        else:
            return False
        
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.get_size()})"


class Game:
    """The Game handles the controlling the actions"""
    def __init__(self, size: int) -> None:
        self.size = size
        self.count_shot = 0
        self.grid = Grid(size)
        self.total_collect = 0
        self.total_destroy = 0
        """When TASK == 3 have extra live"""
        self.destroy_top = 2 if TASK == 3 else 1
        
    def get_grid(self) -> "Grid":
        """Return the instance of the grid held by the game"""
        return self.grid
    
    def get_player_position(self) -> "Position":
        """Return the position of the player in the grid (top row, centre column)"""
        return Position(int(self.size/2-0.5),0)
    
    def get_num_collected(self) -> int:
        return self.total_collect

    def get_num_destroyed(self) -> int:
        return self.total_destroy

    def get_total_shots(self) -> int:
        return self.count_shot

    def rotate_grid(self, direction: str) -> None:
        """
        Rotate grid to right or left.
        Parameters(str):LEFT or RIGHT
        """
        new_playbox ={}
        if direction == LEFT:
            for key in Grid.gamebox.keys():
                new_key = key.add(Position(-1,0))
                if new_key.get_x() < 0:
                    new_key = Position(self.size-1,key.get_y())
                new_playbox[new_key]=Grid.gamebox[key]
            Grid.gamebox = new_playbox
                    
        if direction == RIGHT:
            for key in Grid.gamebox.keys():
                new_key = key.add(Position(1,0))
                if new_key.get_x() >= self.size :
                    new_key = Position(0,key.get_y())
                new_playbox[new_key]=Grid.gamebox[key]
            Grid.gamebox = new_playbox
    
    def _create_entity(self, display: str) -> 'Entity':
        """Return Entity use character"""
        if display == "C":
            return Collectable()
        elif display == "P":
            return Player()
        elif display == "D":
            return Destroyable()
        elif display =="B":
            return Blocker()

        if TASK== 3 and display =="O":
            return Bomb()
            
        raise NotImplementedError
        
    def step(self) -> None:
        """
        Moves all entities on the board by an offset of (0, -1)
        and new entities should be added to the grid (using generate_entities).
        """
        new_playbox ={}
        for key in self.get_grid().gamebox.keys():
                new_key = key.add(Position(0, -1))
                if new_key.get_y() > 0:
                    new_playbox[new_key]=self.get_grid().gamebox[key]
                if new_key.get_y() == 0 and self.get_grid().get_entity(key).display()=="D":
                    self.destroy_top -= 1                  
        Grid.gamebox = new_playbox
        self.generate_entities()

    def generate_entities(self) -> None:
        """
        Method given to the students to generate a random amount of entities to
        add into the game after each step.
        """
        # Generate amount
        entity_count = random.randint(0, self.get_grid().get_size() - 3)
        entities = random.choices(ENTITY_TYPES, k=entity_count)

        # Blocker in a 1 in 4 chance
        blocker = random.randint(1, 4) % 4 == 0

        # UNCOMMENT THIS FOR TASK 3 (CSSE7030)
        #bomb = False
        #if not blocker:
        #   bomb = random.randint(1, 4) % 4 == 0

        total_count = entity_count
        if blocker:
            total_count += 1
            entities.append(BLOCKER)

        # UNCOMMENT THIS FOR TASK 3 (CSSE7030)
        #if bomb:
        #    total_count += 1
        #    entities.append(BOMB)

        entity_index = random.sample(range(self.get_grid().get_size()),
                                     total_count)

        # Add entities into grid
        for pos, entity in zip(entity_index, entities):
            position = Position(pos, self.get_grid().get_size() - 1)
            new_entity = self._create_entity(entity)
            self.get_grid().add_entity(position, new_entity)

    def fire(self, shot_type: str) -> None:
        """
        Remove the entity D and C and O when they be fried.
        Parameters(str):character of entity
        """
        self.count_shot+=1
        position = self.get_position_by_entity(Grid.gamebox)
        entity = Grid.gamebox[position].display()
        if entity == "D" and shot_type == DESTROY:
            self.get_grid().remove_entity(position)
            self.total_destroy +=1
        elif entity == "C" and shot_type == COLLECT:
            self.get_grid().remove_entity(position)
            self.total_collect +=1
        elif entity == "O" and shot_type == DESTROY:
            self.get_grid().remove_entity(position)
            self.bomb(position)

    def bomb(self, position):
        """When Bomb be fried remove splash damage radius"""
        for splash in list(SPLASH):
            splash_x = splash[0]+position.get_x()
            splash_y = splash[1]+position.get_y()
            self.get_grid().remove_entity(Position(splash_x, splash_y))
            
    def has_won(self) -> bool:
        """Win when got 7 total collect and destroy entity not reach top of player position row"""
        if self.total_collect == 7 and self.destroy_top != 0:
            return True
        return False
    
    def has_lost(self) -> bool:
        """Loast when destroy entity reach top of player position row"""
        if self.destroy_top == 0:
            return True
        return False

    def get_position_by_entity(self, dicts) -> "Position":
        """
        Return a specific position by entity
        Parameters(dicts):Grid.gamebox
        """
        position_list = [k for k, v in dicts.items() if k.get_x()== self.get_player_position().get_x()]
        if len(position_list)!=0:
            return sorted(position_list, key=lambda x:x.get_y())[0]
        else:
            return None


class AbstractField(tk.Canvas):
    """Provides base func- tionality for other view classes."""
    each_width = each_hight = MAP_WIDTH//GRID_SIZE
    def __init__(self, master, rows, cols, width, height, **kwargs):
        super().__init__(master, **kwargs)
        self.rows = rows
        self.cols = cols
        self.width = width
        self.height = height

    def get_bbox(self, position):
        """Returns(tuple):the pixel positions of the edges of the shape"""
        x_min = AbstractField.each_width*position.get_x()
        y_min = AbstractField.each_hight*position.get_y()
        x_max = AbstractField.each_width*(position.get_x()+1)
        y_max = AbstractField.each_hight*(position.get_y()+1)
        return (x_min, y_min, x_max, y_max)
    
    def pixel_to_position(self, pixel):
        """Converts the (x, y) pixel position (in graphics units) to a (row, column) position"""
        for r in range(self.rows):
            for c in range(self.cols):
                x_min = self.get_bbox(Position(r,c))[0]
                y_min = self.get_bbox(Position(r,c))[1]
                x_max = self.get_bbox(Position(r,c))[2]
                y_max = self.get_bbox(Position(r,c))[3]
                if (x_min < r and r < x_max) and (y_min < c and c < y_max):
                    return Position(r, c)
        
    def get_position_center(self, position):
        x_min = self.get_bbox(position)[0]
        y_min = self.get_bbox(position)[1]
        x_max = self.get_bbox(position)[2]
        y_max = self.get_bbox(position)[3]
        return ((x_min + x_max)/2, (y_min + y_max)/2)
        
    def annotate_position(self, position, text):
        """Annotates the center of the cell"""
        self.create_text(self.get_position_center(position), text=text, fill="white", font="Arial, 12")

     
class GameField(AbstractField):
    """A visual representation of the game grid which inherits from AbstractField"""
    def __init__(self, master, size, width, height, **kwargs):
        self.master = master
        self.size = GRID_SIZE
        self.width = MAP_WIDTH
        self.height = MAP_WIDTH

        """Original GameField Canvas"""
        self.gamefield_org = tk.Canvas(self.master, width=self.width, height=self.height, bg=FIELD_COLOUR)
        self.gamefield_org.pack(side=tk.LEFT, fill=tk.BOTH)
        
    def draw_grid(self, entities):
        """Draws the entities includes the Player entity"""
        if entities.display() == "P":
            self.gamefield_org.create_rectangle(self.get_bbox(Game.get_player_position(Game(self.size))), fill="#A482DB")
            self.gamefield_org.create_text(self.get_position_center(Game.get_player_position(Game(self.size))), text="P", fill="white", font="Arial, 12")
            
        else:
            for position in self.get_position_by_entity(Grid.gamebox, entities.display()):
                if entities.display() == "C":
                    self.gamefield_org.create_rectangle(self.get_bbox(position), fill="#9FD7D5")
                    self.gamefield_org.create_text(self.get_position_center(position), text="C", fill="white", font="Arial, 12")     
                elif entities.display() == "D":
                    self.gamefield_org.create_rectangle(self.get_bbox(position), fill="#F93A3A")
                    self.gamefield_org.create_text(self.get_position_center(position), text="D", fill="white", font="Arial, 12")
                elif entities.display() == "B":
                    self.gamefield_org.create_rectangle(self.get_bbox(position), fill="#B2B2B2")
                    self.gamefield_org.create_text(self.get_position_center(position), text="B", fill="white", font="Arial, 12")
           
    def draw_player_area(self):
        self.gamefield_org.create_rectangle((0, 0, 400, MAP_WIDTH//GRID_SIZE), fill=PLAYER_AREA)

    def get_position_by_entity(self, dicts, value) -> "Position":
        """
        Return specific position by entity
        Parameters:
            dicts(dictionary):Grid.gamebox
            value(str):Character of entity
        """
        position_list = [k for k, v in dicts.items() if v.display() == value]
        return position_list


class ScoreBar(AbstractField):
    """A visual representation of shot statistics from the player which inherits from AbstractField."""
    def __init__(self, master, rows, **kwargs):
        self.master = master
        self.rows = rows
        self.cols = 2
        self.width = SCORE_WIDTH
        self.height = MAP_WIDTH
        
        """Original ScoreBar Canvas with text"""
        self.scorebar_org = tk.Canvas(self.master, width=self.width, height=self.height, bg=SCORE_COLOUR)
        self.scorebar_org.create_text(100, 30, text="Score", fill="white", font="Arial, 20")
        self.scorebar_org.create_text(20, 100, text="Collected:", fill="white", font="Arial, 12", anchor=tk.NW)
        self.scorebar_org.create_text(20, 150, text="Destroyed:", fill="white", font="Arial, 12", anchor=tk.NW)
        self.scorebar_org.pack(side=tk.RIGHT, fill=tk.BOTH)

        if TASK ==3:
            self.scorebar_org.create_text(20, 200, text="Lives:", fill="white", font="Arial, 12", anchor=tk.NW)

   
class HackerController(object):
    """Acts as the controller for the Hacker game"""
    def __init__(self, master, size):
        self.master = master
        self.size = size
        self.game = Game(self.size)
        
        """Hacker label"""
        self.hacker_label = tk.Label(self.master, text=TITLE, bg=TITLE_BG, fg='white', font=TITLE_FONT)
        self.hacker_label.pack(fill=tk.X)
        
        """GameField and ScoreBar"""
        self.gamefield = GameField(self.master, self.size, MAP_WIDTH, MAP_HEIGHT)
        self.scorebar = ScoreBar(self.master, self.size)

        """Scorebar number"""
        self.collect = self.scorebar.scorebar_org.create_text(120, 100, text=f"{self.game.get_num_collected()}", fill="white", font="Arial, 12", anchor=tk.NW)
        self.destroy = self.scorebar.scorebar_org.create_text(120, 150, text=f"{self.game.get_num_destroyed()}", fill="white", font="Arial, 12", anchor=tk.NW)
        if TASK == 3:
            self.live = self.scorebar.scorebar_org.create_text(120, 200, text=f"{self.game.destroy_top}", fill="white", font="Arial, 12", anchor=tk.NW)

        """Event of keypress"""
        self.master.bind("a", self.handle_keypress)
        self.master.bind("d", self.handle_keypress)
        self.master.bind("<space>", self.handle_keypress)
        self.master.bind("<Return>", self.handle_keypress)
        
        """Game Start"""
        self.draw(self.game)
        self.master.after(2000, self.step)
              
    def handle_keypress(self, event):
        """
        Keypress a is turning left
        Keypress d is turning left
        Keypress space is destroy entity
        Keypress Return is collect entity
        """
        if event.keysym == "a":           
            self.handle_rotate(LEFT)
        elif event.keysym == "d":
            self.handle_rotate(RIGHT)
        elif event.keysym == "space":
            self.handle_fire(DESTROY)
            self.scorebar.scorebar_org.itemconfig(self.destroy, text=f"{self.game.get_num_destroyed()}")
        elif event.keysym == "Return":
            self.handle_fire(COLLECT)
            self.scorebar.scorebar_org.itemconfig(self.collect, text=f"{self.game.get_num_collected()}")
        else:
            return None
        
    def draw(self, game):
        """Clears and redraws the view based on the current game state"""
        self.gamefield.gamefield_org.update()
        self.gamefield.gamefield_org.delete("all")
        self.gamefield.draw_player_area()
        self.gamefield.draw_grid(Player())
        self.gamefield.draw_grid(Collectable())
        self.gamefield.draw_grid(Destroyable())
        self.gamefield.draw_grid(Blocker())
        
    def handle_rotate(self, direction):
        """Handles rotation of the entities and redrawing the game"""
        self.game.rotate_grid(direction)
        self.draw(self.game)
        
    def handle_fire(self, shot_type):
        """
        Handles the firing of the specified shot type and redrawing of the game
        Parameters(str):character of entity
        """
        self.game.fire(shot_type)
        self.draw(self.game)
        
    def step(self):
        """The step method is called every 2 seconds"""
        self.game.step()
        self.draw(self.game)
        if self.game.has_won():
            self.master.after_cancel(self.step)
            self.master.destroy()
        elif self.game.has_lost():
            self.master.after_cancel(self.step)
            self.master.destroy()
        else:
            self.master.after(2000, self.step)


class AdvancedHackerController(HackerController):
    """Acts as the controller for the Hacker game TASK 2,3"""
    def __init__(self, master, size, **kwargs):
        self.master = master
        self.size = size
        self.game = Game(self.size)
        self.timer_s = 0
        
        """Hacker Banner"""
        self.hacker_label = tk.Label(self.master, text=TITLE, bg=TITLE_BG, fg='white', font=TITLE_FONT)
        self.hacker_label.pack(fill=tk.X)

        """Each main class"""
        self.status = StatusBar(self.master)
        self.gamefield = ImageGameField(self.master, self.size, MAP_WIDTH, MAP_HEIGHT)
        self.scorebar = ScoreBar(self.master, self.size)

        """Bottom Banner"""    
        self.count_num = tk.Label(self.status.num_frame, text=f"{self.game.get_total_shots()}")
        self.count_num.pack(side=tk.LEFT, padx=100)
        self.time_num = tk.Label(self.status.num_frame, text=f"{self.timer_s//60}m{self.timer_s%60}s")
        self.time_num.pack(side=tk.LEFT, padx=75)

        """Bottom Button"""
        self.button = tk.Button(self.status.frame, textvariable=self.status.text, command=self.game_play_pause)        
        self.button.pack(side=tk.LEFT, padx=70)

        """Scorebar number"""
        self.collect = self.scorebar.scorebar_org.create_text(120, 100, text=f"{self.game.get_num_collected()}", fill="white", font="Arial, 12", anchor=tk.NW)
        self.destroy = self.scorebar.scorebar_org.create_text(120, 150, text=f"{self.game.get_num_destroyed()}", fill="white", font="Arial, 12", anchor=tk.NW)

        if TASK == 3:
            self.live = self.scorebar.scorebar_org.create_text(120, 200, text=f"{self.game.destroy_top}", fill="white", font="Arial, 12", anchor=tk.NW)

        """Event of keypress"""
        self.master.bind("a", self.handle_keypress)
        self.master.bind("d", self.handle_keypress)
        self.master.bind("<space>", self.handle_keypress)
        self.master.bind("<Return>", self.handle_keypress)

        """Menu"""
        menubar = tk.Menu(self.master)
        master.config(menu=menubar)
        filemenu = tk.Menu(menubar)
        menubar.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="New game", command=self.event_new)
        filemenu.add_command(label="Save game", command=self.event_save)
        filemenu.add_command(label="Load game", command=self.event_load)
        filemenu.add_command(label="Quit", command=self.event_quit)

        """Game Start"""
        self.draw(self.game)
        self.master.after(2000, self.step)
        self.update_timer()
           
    def game_play_pause(self):
        """A controller of play and pause button"""
        self.status.play_pause()
        if self.status.is_play == False:
            self.draw(self.game)
            self.master.after(2000, self.step)
            self._timer = self.master.after(1000,self.update_timer)
        else:
            self.master.after_cancel(self.step)
            self.update_timer()
        
    def update_timer(self):
        """Bottom banner timer update"""
        if self.status.is_play:
            if self._timer is not None:
                self.master.after_cancel(self._timer)
            if self._step_timer is not None:
                self.master.after_cancel(self._step_timer)
                
        else:
            self.time_num.configure(text=f'{self.timer_s//60}m {self.timer_s%60}s')
            self.timer_s += 1
            self._timer = self.master.after(1000,self.update_timer)
        
    def handle_keypress(self, event):
        """
        Keypress a is turning left
        Keypress d is turning left
        Keypress space is destroy entity
        Keypress Return is collect entity
        """
        if self.status.is_play == False:
            if event.keysym == "a":           
                self.handle_rotate(LEFT)
            elif event.keysym == "d":
                self.handle_rotate(RIGHT)
            elif event.keysym == "space":
                self.handle_fire(DESTROY)
                self.scorebar.scorebar_org.itemconfig(self.destroy, text=f"{self.game.get_num_destroyed()}")
            elif event.keysym == "Return":
                self.handle_fire(COLLECT)
                self.scorebar.scorebar_org.itemconfig(self.collect, text=f"{self.game.get_num_collected()}")
        
    def draw(self, game):
        """Clears and redraws the view based on the current game state"""
        self.gamefield.img_org.update()
        self.gamefield.img_org.delete("all")
        self.gamefield.draw_player_area()
        self.gamefield.create_img(Player())
        self.gamefield.create_img(Collectable())
        self.gamefield.create_img(Blocker())
        self.gamefield.create_img(Destroyable())
        
    def handle_rotate(self, direction):
        """Handles rotation of the entities and redrawing the game"""
        self.game.rotate_grid(direction)
        self.draw(self.game)
        
    def handle_fire(self, shot_type):
        """
        Handles the firing of the specified shot type and redrawing of the game
        Parameters(str):character of entity
        """
        self.game.fire(shot_type)
        self.draw(self.game)
        self.count_num.configure(text=f"{self.game.get_total_shots()}")

    def step(self):
        """The step method is called every 2 seconds"""
        self.game.step()
        self.draw(self.game)
        if self.game.has_won():
            self.master.after_cancel(self.step)
            self.master.destroy()
        elif self.game.has_lost():
            self.master.after_cancel(self.step)
            self.master.destroy()
        else:
            self._step_timer = self.master.after(2000, self.step)

    def event_new(self):
        """Start a new Hacker game"""
        self.gamefield.img_org.delete("all")
        Grid.gamebox={}
        self.timer_s = 0
        self.game.total_collect = 0
        self.game.total_destroy = 0
        self.total_shot = 0
        self.time_num.configure(text=f'{self.timer_s//60}m {self.timer_s%60}s')
        self.scorebar.scorebar_org.itemconfig(self.collect, text=f"{self.game.get_num_collected()}")
        self.scorebar.scorebar_org.itemconfig(self.destroy, text=f"{self.game.get_num_destroyed()}")
        self.count_num.configure(text=f"{self.total_shot}")     

    def event_save(self) :
        """Save the current game info"""
        filename = filedialog.asksaveasfile(title='Save in game.txt', defaultextension=(".txt"))
        if filename:
            with open('game.txt','w') as data:
                a = str(Grid.gamebox).strip('{')
                a = a.strip('}')
                data.write(a)  
                self.master.destroy()
        
    def event_load(self) :
        """Load the current game info"""
        f = open("game.txt", "r")
        f=f.read()
        
    def event_quit(self) :
        """Close the application"""
        box = tk.messagebox.askquestion('quit','Exit?')
        if box == 'yes':
            self.master.destroy()
        if box == 'no':
            return None
        
class ImageGameField(AbstractField):
    """
    A visual representation of the game grid which inherits from AbstractField
    similarly to GameField but image replace rectangles.
    """
    def __init__(self, master, size, width, height, **kwargs):
        self.master = master
        self.size = GRID_SIZE
        self.width = MAP_WIDTH
        self.height = MAP_WIDTH

        """Original ImageGameField Canvas"""
        self.img_org = tk.Canvas(self.master, width=self.width, height=self.height, bg=FIELD_COLOUR)
        self.img_org.pack(expand=1 ,side=tk.LEFT, fill=tk.BOTH)
        
        self.img_list=[]

    def create_img(self, entities):
        """Load and create the image in ImageGameField Canvas"""
        pil_P = Image.open("images/P.png")
        self.img_org.P=ImageTk.PhotoImage(pil_P)
        pil_C = Image.open("images/C.png")
        self.img_org.C=ImageTk.PhotoImage(pil_C)
        pil_D = Image.open("images/D.png")
        self.img_org.D=ImageTk.PhotoImage(pil_D)
        pil_B = Image.open("images/B.png")
        self.img_org.B=ImageTk.PhotoImage(pil_B)
        pil_O = Image.open("images/O.png")
        self.img_org.O=ImageTk.PhotoImage(pil_O)
        
        """Keep reference to image"""
        self.img_list.append(self.img_org.P)
        self.img_list.append(self.img_org.C)
        self.img_list.append(self.img_org.D)
        self.img_list.append(self.img_org.B)
        self.img_list.append(self.img_org.O)
        
        if entities.display() == "P":
            self.img_org.create_image(171, 0, anchor=tk.NW, image=self.img_org.P)
        else:
            for position in self.get_position_by_entity(Grid.gamebox, entities.display()):
                if entities.display() == "C":
                    self.img_org.create_image(self.get_bbox(position)[0],self.get_bbox(position)[1], anchor=tk.NW, image=self.img_org.C)
                elif entities.display() == "D":
                    self.img_org.create_image(self.get_bbox(position)[0],self.get_bbox(position)[1], anchor=tk.NW, image=self.img_org.D)
                elif entities.display() == "B":
                    self.img_org.create_image(self.get_bbox(position)[0],self.get_bbox(position)[1], anchor=tk.NW, image=self.img_org.B)
           
    def draw_player_area(self):
        self.img_org.create_rectangle((0, 0, 400, MAP_WIDTH//GRID_SIZE), fill=PLAYER_AREA)

    def get_position_by_entity(self, dicts, value) -> "Position":
        """
        Return specific position by entity
        Parameters:
            dicts(dictionary):Grid.gamebox
            value(str):Character of entity
        """
        position_list = [k for k, v in dicts.items() if v.display() == value]
        return position_list
        
class StatusBar(tk.Frame):
    """Status of Shot counter and Game timer and Play Pause button"""
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        """Number Frame"""
        self.num_frame = tk.Frame(self.master)
        self.num_frame.pack(side=tk.BOTTOM,fill=tk.X)
        
        """Word Frame"""
        self.frame = tk.Frame(self.master)
        self.frame.pack(side=tk.BOTTOM,fill=tk.X)
        
        """Word"""
        self.count = tk.Label(self.frame, text="Total Shots").pack(side=tk.LEFT, padx=70)
        self.time = tk.Label(self.frame, text="Timer").pack(side=tk.LEFT,padx=70)
        
        """Word Button"""
        self.is_play = False
        self.text = tk.StringVar()
        self.text.set("  Pause   ")

    def play_pause(self):
        """Change represent of button word"""
        self.is_play = not self.is_play
        if self.is_play:
            self.text.set("   Play   ")
        else:
            self.text.set("   Pause   ")









if __name__ == '__main__':
    main()
