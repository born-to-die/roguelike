#! /usr/bin/env python
# -*- coding: utf-8 -*-

import pygame, sys, os
from pygame.locals import *

import base_config
import base_render_castray
import base_render_los

def displayUpdate(game):

    # TICK
    game.milli = game.clock.tick(base_config.fps)
    #game.seconds = game.milli / 1000.0
    #print(str(game.milli) + " " + str(game.seconds))

    if(base_config.debug):
        fps_text_draw = game.fontDefault.render(
            "FPS: " + str(game.clock.get_fps()),
            base_config.antialias,
            (255, 255, 255),
            (0, 0, 0)
        )
        game.screen.blit(fps_text_draw, (0, 0))

    pygame.display.update()

def Render(game):

    game.surfGame.fill((0, 0, 0))

    game.surfGame.blit(game.assTiles[game.map.landmap[game.player[game.active_player].y][game.player[game.active_player].x]], (64 * game.player[game.active_player].x, 64 * game.player[game.active_player].y))

    for i in range(72):

        c = base_render_castray.CastRay(game,
            game.player[game.active_player].x,
            game.player[game.active_player].y,
            2,
            i * 5
        )

        base_render_los.Los(game, game.player[game.active_player].x, game.player[game.active_player].y, c[0], c[1])

    #game.surfGame.blit(game.holeSprite, (game.coordstairSprites[0] * 64,
                                    #game.coordstairSprites[1] * 64))

def RenderTile(game, x, y):

    if(game.map.landmap[x][y] == 0):
        game.surfGame.blit(game.floorSprite, (x * 64, y * 64))

def RenderItems(game):

    for i in range(len(game.listItems)):
        game.listItems[i].Render(game.surfGame)

def RenderUnits(game):

    for i in range(len(game.listUnits)):
        if(not game.listUnits[i].life):
            game.listUnits[i].Render(game, False)

    for i in range(len(game.listUnits)):
        if(game.listUnits[i].life):
            if(not game.listUnits[i].animate):
                game.listUnits[i].Render(game, False)

def RenderDecors(game):

    for i in range(len(game.listDecors)):
        if(not game.listDecors[i].over):
            game.listDecors[i].Render(game.surfGame)

def RenderDecorsOver(game):

    for i in range(len(game.listDecors)):
        if(game.listDecors[i].over):
            game.listDecors[i].Render(game.surfGame)

def RenderLandmap(game):

    Render(game)

    # RENDER EXISTS
    for i in range(len(game.listNextmaps)):
        game.surfGame.blit(game.alistNextmaps[game.listNextmaps[i]][2], (int(game.alistNextmaps[game.listNextmaps[i]][0]) * 64, int(game.alistNextmaps[game.listNextmaps[i]][1]) * 64))

def RenderPlayer(game):

    game.player[game.active_player].Render(game, False)

def RenderAll(game):

    # DELETE ITEMS
    for i in range(len(game.listItems) - 1, -1, -1):
        if(game.listItems[i].delete):
            del game.listItems[i]

    # DELETE ENEMIES
    for i in range(len(game.listUnits) - 1, -1, -1):
        if(game.listUnits[i].health < 1 and game.listUnits[i].delete):
            del game.listUnits[i]

    for i in range(len(game.player)):
        if(i != game.active_player):
            game.player[i].Render(game, True)
            print("@")

    # RENDER LANDMAP
    Render(game)

    # RENDER EXISTS
    for i in range(len(game.listNextmaps)):
        game.surfGame.blit(game.alistNextmaps[game.listNextmaps[i]][2], (int(game.alistNextmaps[game.listNextmaps[i]][0]) * 64, int(game.alistNextmaps[game.listNextmaps[i]][1]) * 64))

    # RENDER DECORS
    for i in range(len(game.listDecors)):
        if(not game.listDecors[i].over):
            game.listDecors[i].Render(game.surfGame)

    game.screen.blit(game.surfGame, (0,0))
    #pygame.display.update()
    #input()

    # RENDER ITEMS
    for i in range(len(game.listItems)):
        game.listItems[i].Render(game.surfGame)



    # RENDER DEADS
    for i in range(len(game.listUnits)):
        if(not game.listUnits[i].life):
            game.listUnits[i].Render(game, False)

    # RENDER PLAYER
    game.player[game.active_player].Render(game, True)

    # UPDATE & RENDER ENEMIES
    for i in range(len(game.listUnits)):

        if(game.listUnits[i].life):

            game.listUnits[i].Action(game)

            game.listUnits[i].Render(game, True)

    for i in range(len(game.listDecors)):
        if(game.listDecors[i].over):
            game.listDecors[i].Render(game.surfGame)

def blitSurfGame(game):

    game.screen.blit(game.surfGame, (0,0))
