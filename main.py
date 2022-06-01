import tkinter

import pygame
import pygame.freetype
import random
from enum import Enum
from tkinter import *


pygame.init()


clock = pygame.time.Clock()
clock.tick(60)

root = Tk()
root.geometry("200x263")

def show_data():
    txt.delete(0.0, 'end')
    txtName = ent.get() # This is how you get name
    txtGender = var_chk.get() # This is how you get the gender

    if txtGender == 1:
        txtGender = "sir"
    else:
        txtGender = "ma'am"

    sentence = 'Hello, ' + str(txtName) + "\nI hope you are enjoying your day " + txtGender + "."
    txt.insert(0.0, sentence)

def stop_txt():
    root.destroy()

name = Label(root, text = "Name: ")
gender = Label(root, text = "Gender: ")

ent = Entry(root)

var_chk = IntVar()

rd1 = Radiobutton(root, text = "Male", variable=var_chk, value=1)
rd2 = Radiobutton(root, text="Female", variable=var_chk, value=2)

name.grid(row=0)
gender.grid(row=1)

ent.grid(row=0, column=1)
rd1.grid(row=1, column=1, sticky=W)
rd2.grid(row=1, column=1, sticky=E)

btn = Button(root, text="Register", bg="blue", fg="white", command=show_data)
btn.grid(row=2,columnspan=2)

txt = Text(root, width=25, height=10, wrap=WORD)
txt.grid(row=3, columnspan=2, sticky=W)

btn2 = Button(root, text="Continue", bg="purple", fg="white", command=stop_txt)
btn2.grid(row=4, columnspan=2)

root.mainloop()

BLUE = (106, 159, 181)
WHITE = (255, 255, 255)

def create_surface_with_text(text, font_size, text_rgb):
    font = pygame.freetype.SysFont("Courier", font_size, bold=True)
    surface, _ = font.render(text=text, fgcolor=text_rgb)
    return surface.convert_alpha()

class UIElement(pygame.sprite.Sprite):

    def __init__(self, center_position, text, font_size, text_rgb, action=None):
        super().__init__()

        self.mouse_over = False


        default_image = create_surface_with_text(text=text, font_size=font_size, text_rgb=text_rgb)


        highlighted_image = create_surface_with_text(text=text, font_size=font_size * 1.2, text_rgb=text_rgb)


        self.images = [default_image, highlighted_image]
        self.rects = [
            default_image.get_rect(center=center_position),
            highlighted_image.get_rect(center=center_position),
        ]
        self.action = action

    @property
    def image(self):
        return self.images[1] if self.mouse_over else self.images[0]

    @property
    def rect(self):
        return self.rects[1] if self.mouse_over else self.rects[0]

    def update(self, mouse_pos, mouse_up):
        if self.rect.collidepoint(mouse_pos):
            self.mouse_over = True
            if mouse_up:
                return self.action
        else:
            self.mouse_over = False

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class GameState(Enum):
    QUIT = -1
    TITLE = 0
    NEWGAME = 1
    NEXTGAME = 2

def main():
    pygame.init()

    screen = pygame.display.set_mode((1100, 950))

    # create a ui element
    quit_btn = UIElement(
        center_position=(400, 400),
        font_size=30,
        text_rgb=WHITE,
        text="Hello World",
        action=GameState.QUIT
    )

    # main loop
    while True:
        pygame.init()

        screen = pygame.display.set_mode((1100, 950))
        game_state = GameState.TITLE

        while True:
            if game_state == GameState.TITLE:
                game_state = title_screen(screen)

            if game_state == GameState.NEWGAME:
                game_state = play_level(screen)

            if game_state == GameState.NEXTGAME:
                game_state = new_level(screen)

            if game_state == GameState.QUIT:
                pygame.quit()
                return

def title_screen(screen):
    start_btn = UIElement(
        center_position=(185, 700),
        font_size=40,
        text_rgb=WHITE,
        text="Start",
        action=GameState.NEWGAME,
    )
    quit_btn = UIElement(
        center_position=(185, 800),
        font_size=40,
        text_rgb=WHITE,
        text="Quit",
        action=GameState.QUIT,
    )
    title_text = UIElement(
        center_position=(590, 100),
        font_size=50,
        text_rgb=WHITE,
        text="Welcome to the App!"
    )

    buttons = [start_btn, quit_btn, title_text]

    while True:
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True
        background = pygame.image.load("placement_color.png")
        background = pygame.transform.scale(background, (1100,950))
        screen.blit(background, (0,0))

        pygame.mouse.set_visible(True)
        for button in buttons:
            ui_action = button.update(pygame.mouse.get_pos(), mouse_up)
            if ui_action is not None:
                return ui_action
            button.draw(screen)

        pygame.display.flip()

def play_level(screen):
    next_btn = UIElement(
        center_position=(110, 820),
        font_size=40,
        text_rgb=WHITE,
        text="Next!",
        action=GameState.NEXTGAME,
    )
    return_btn = UIElement(
        center_position=(290, 900),
        font_size=40,
        text_rgb=WHITE,
        text="Return to Main Menu!",
        action=GameState.TITLE,
    )

    buttons = [next_btn, return_btn]

    while True:
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True
        concretebg = pygame.image.load("pastel_blue.png")
        concretebg = pygame.transform.scale(concretebg, (1100, 950))
        screen.blit(concretebg, (0, 0))

        for button in buttons:
            ui_action = button.update(pygame.mouse.get_pos(), mouse_up)
            if ui_action is not None:
                return ui_action
            button.draw(screen)

        pygame.display.flip()
        pygame.display.update()

def new_level(screen):
    back_btn = UIElement(
        center_position=(110, 820),
        font_size=40,
        text_rgb=WHITE,
        text="Back!",
        action=GameState.NEWGAME,
    )
    return_btn = UIElement(
        center_position=(290, 900),
        font_size=40,
        text_rgb=WHITE,
        text="Return to Main Menu!",
        action=GameState.TITLE,
    )

    buttons = [back_btn, return_btn]

    while True:
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True
        stageTwobg = pygame.image.load("pastel-green.png")
        stageTwobg = pygame.transform.scale(stageTwobg, (1100, 950))
        screen.blit(stageTwobg, (0, 0))

        for button in buttons:
            ui_action = button.update(pygame.mouse.get_pos(), mouse_up)
            if ui_action is not None:
                return ui_action
            button.draw(screen)

        pygame.display.flip()
        pygame.display.update()

# call main when the script is run
if __name__ == "__main__":
    main()
