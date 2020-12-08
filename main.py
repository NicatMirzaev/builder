import pygame
import os
from object import Object
from database import *
width = 1050
height = 700
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Builder (By Zoxy)")
load_database()
inventory_page = 0
inventory_max_object_per_page = 12
inventory_cell_image = pygame.image.load(os.path.join("Assets", "Game/inventory_cell2.png"))
arrow_left = pygame.image.load(os.path.join("Assets", "Game/arrow_left.png"))
arrow_right = pygame.image.load(os.path.join("Assets", "Game/arrow_right.png"))
def inventory_draw(win, inventory):
    count = 0
    win.blit(arrow_right, (width - 30, 642))
    win.blit(arrow_left, (width - 70, 642))
    for i in inventory:
        image = pygame.image.load(os.path.join("Assets", "Objects/{}".format(i.strip())))
        win.blit(image, ((count * 80) + 7, 626))
        count += 1


def get_selected_cell_id(x, y):
    returnid = -1
    for i in range(inventory_max_object_per_page):
        cellx = i * 80
        if x >= cellx and x <= cellx + 78 and y >= 626 and y <= 626 + 78:
            returnid = i
            break
    if returnid == -1:
        if x >= width - 30 and x <= (width - 30) + 12 and y >= 642 and y <= 642 + 21:
            returnid = -2
        elif x >= width - 70 and x <= (width - 70) + 12 and y >= 642 and y <= 642 + 21:
            returnid = -3
    return returnid

def get_inventory_objects(page):
    with open("inventory.txt") as inv:
        read = inv.readlines()
        return read[page * inventory_max_object_per_page: (inventory_page * inventory_max_object_per_page) + inventory_max_object_per_page]


def main():
    global inventory_page
    getobjects = get_objects()
    objects = []
    inventory = get_inventory_objects(0)
    selected_inventory_object = None
    selected_inventory_object_name = None
    selected_object = None
    rotating_object = None
    for object in getobjects:
        objects.append(Object(object[0], object[1], object[2], object[3], object[4]))
        
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONUP:
                if selected_object != None:
                    selected_object.clicked = False
                if rotating_object != None:
                    update_rotation(rotating_object.id, rotating_object.rotation)
                    rotating_object = None
                x, y = pygame.mouse.get_pos()
                selected_cell = get_selected_cell_id(x, y)
                if selected_cell != -1:
                    if selected_cell >= 0:
                        if selected_inventory_object != None:
                            selected_inventory_object = None
                        else:
                            if selected_cell < len(inventory):
                                selected_inventory_object_name = inventory[selected_cell].strip()
                                selected_inventory_object = pygame.image.load(os.path.join("Assets", "Objects/{}".format(selected_inventory_object_name)))
                    elif selected_cell == -2:
                        inventory_page += 1
                        inventory = get_inventory_objects(inventory_page)
                        if not inventory:
                            inventory_page -= 1
                            inventory = get_inventory_objects(inventory_page)
                    elif selected_cell == -3:
                        if inventory_page > 0:
                            inventory_page -= 1
                            inventory = get_inventory_objects(inventory_page)
                elif selected_inventory_object != None:
                    id = add_object(selected_inventory_object_name, x - 20, y - 20)
                    objects.append(Object(id, selected_inventory_object_name, x - 20, y - 20, 0))

                else:
                    click = []
                    for i in objects:
                        clicked = i.click(x, y)
                        if clicked != -1:
                            click = [i, clicked]
                    if click[1] != -1:
                        if click[1] == 0:
                            if selected_object != None:
                                selected_object.clicked = False
                            selected_object = click[0]
                            click[0].clicked = True
                        elif selected_object != None and click[1] == 1:
                            delete_object(selected_object.id)
                            objects.remove(selected_object)
                            selected_object = None
                        elif selected_object != None and click[1] == 2:
                            rotating_object = click[0]



        if rotating_object != None:
            rotating_object.rotate(pygame.mouse.get_pos())
        win.fill((0, 0, 0))
        for i in objects:
            i.draw(win)

        if selected_inventory_object != None:
            x, y = pygame.mouse.get_pos()
            win.blit(selected_inventory_object, (x - 20, y - 20))
        for i in range(inventory_max_object_per_page):
            win.blit(inventory_cell_image, (i * 80, 620))
        inventory_draw(win, inventory)
        pygame.display.update()


main()
