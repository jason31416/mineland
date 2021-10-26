import pygame
import pyratch
import time
import random
import math
import pylog
import os

sc = pyratch.window((800, 600), "mineland")

loadingbg = pyratch.sprite("src/loadingbg.png", sc.scsize)
titlebg = pyratch.sprite("src/title.png", sc.scsize)
startbt = pyratch.sprite("src/startbutton.png", (100, 37))
contbt = pyratch.sprite("src/continuebutton.png", (100, 37))

playerpic = 0

# world

WORLDWIDTH = 512
WORLDDEPTH = 96

world = [[0 for j in range(WORLDDEPTH+10)] for i in range(WORLDWIDTH+10)]


for i in range(30):
    sc.blit_sprite(titlebg)
    rect = pygame.Surface(sc.scsize, pygame.SRCALPHA)
    rect.fill((0, 0, 0, 255-i*8))
    sc.sc.blit(rect, (0, 0))
    sc.update(random.randint(0, 0) / 1000)
for i in range(30):
    sc.blit_sprite(titlebg)
    rect = pygame.Surface(sc.scsize, pygame.SRCALPHA)
    rect.fill((0, 0, 0, i*8))
    sc.sc.blit(rect, (0, 0))
    sc.update(1 / 1000)

for i in range(100):
    sc.blit_sprite(loadingbg)
    sc.drawrect(sc.scsize[0] / 2 - 150, sc.scsize[1] / 2+30, (300, 15), color=(150, 150, 150), wid=15)
    sc.drawrect(sc.scsize[0]/2-150, sc.scsize[1]/2+30, (i*3, 15), color=(0, 100, 255), wid=15)
    sc.drawtext(f"loading... {str(i)}%", (sc.scsize[0]/2-45, sc.scsize[1]/2+30))
    sc.update(random.randint(0, 0)/1000)

# main menu

isgamee = 0
startbt.goto(sc.scsize[0] / 2 - 50, sc.scsize[1] / 2 + 60)
contbt.goto(sc.scsize[0] / 2 - 50, sc.scsize[1] / 2 + 110)
playerp = pyratch.sprite("src/playerpic/playerb.png", (32, 32))

alp = 255


while not isgamee:
    sc.blit_sprite(loadingbg)
    sc.blit_sprite(startbt)
    sc.blit_sprite(contbt)
    playerp.goto(20, 20)
    sc.blit_sprite(playerp)
    if playerp.click():
        if playerpic == 0:
            playerp = pyratch.sprite("src/playerpic/playerr.png", (32, 32))
        else:
            playerp = pyratch.sprite("src/playerpic/playerb.png", (32, 32))
        playerpic = 1-playerpic
        time.sleep(0.2)
    alp = alp/1.03
    if alp > 0:
        rect = pygame.Surface((100, 37), pygame.SRCALPHA)
        rect.fill((alp / 2, alp / 2, alp / 2, alp))
        sc.sc.blit(rect, (sc.scsize[0] / 2 - 50, sc.scsize[1] / 2 + 60))
        rect = pygame.Surface((100, 37), pygame.SRCALPHA)
        rect.fill((alp / 2, alp / 2, alp / 2, alp))
        sc.sc.blit(rect, (sc.scsize[0] / 2 - 50, sc.scsize[1] / 2 + 110))
    sc.drawrect(sc.scsize[0] / 2 - 150, sc.scsize[1] / 2+30, (300, 15), color=(0, 100, 255), wid=15)
    sc.drawtext(f"loading... 100%", (sc.scsize[0] / 2 - 45, sc.scsize[1] / 2+30))
    if startbt.click():
        isgamee = 2
    if contbt.click():
        isgamee = 1
    sc.update(random.randint(0, 5) / 1000)

sc.blit_sprite(loadingbg)
worldname = sc.ask("worldname")

"""
0:air
1:dirt
2:rock
3:grass
4:wood
5:leave
6:crafting table
7:wooden axe
8:wooden pickaxe
9:stick
10:stone pickaxe
11:iron_r
12:coal_r
13:hammer
14:stove
15:iron_i
16:gold_r
17:gold_i
18:iron picaxe
"""

def basicblock(color0, color1, color2):
    xyz = pygame.Surface((32, 32))
    xyz.fill((color0, color1, color2))
    return xyz

def loadblock(src):
    xyz = pygame.image.load(src)
    return pygame.transform.scale(xyz, (32, 32))
def loaditem(src):
    return pygame.image.load(src)

class Formula:
    product, materials = -1, [[-1, -1, -1], [-1, -1, -1], [-1, -1, -1]]
    typ = False
    ct = "f"
    num = 1
    def __init__(self, product, materials, num=1):
        self.num = num
        self.product, self.materials = product, materials
        if materials[0][2] == -1 and materials[1][2] == -1 and materials[2][2] == -1 and materials[2][1] == -1 and materials[2][0] == -1:
            self.typ = True

formulas = [Formula(1, [[3, -1, -1], [-1, -1, -1], [-1, -1, -1]]), Formula(6, [[4, 4, -1], [4, 4, -1], [-1, -1, -1]]), Formula(7, [[-1, 4, 4], [-1, 9, 4], [-1, 9, -1]]), Formula(9, [[4, -1, -1], [4, -1, -1], [-1, -1, -1]], num=2), Formula(8, [[4, 4, 4], [-1, 9, -1], [-1, 9, -1]]), Formula(10, [[2, 2, 2], [-1, 9, -1], [-1, 9, -1]]), Formula(13, [[2, 2, 2], [2, 2, 2], [-1, 9, -1]]), Formula(14, [[2, 12, 2], [2, 12, 2], [2, 2, 2]]), Formula(18, [[15, 15, 15], [-1, 9, -1], [-1, 9, -1]])]
tools = [(7, 4, 1.5), (7, 5, 1), (8, 2, 2), (10, 2, 4), (8, 11, 2), (10, 11, 4), (8, 12, 2), (10, 12, 4), (13, 11, 4), (13, 16, 4), (8, 16, 1), (10, 16, 2), (18, 16, 4), (18, 11, 6), (18, 12, 6), (18, 2, 6), (18, 14, 6)]
block = [basicblock(87, 250, 255), basicblock(150, 75, 0), basicblock(125, 125, 125), basicblock(0, 255, 0), basicblock(184, 134, 11), basicblock(15, 200, 0), loadblock("src/basicblocks/craftingtable.png"), loaditem("src/basicblocks/wooden_axe.png"), loaditem("src/basicblocks/wooden_pickaxe.png"), loadblock("src/basicblocks/stick.png"), loaditem("src/basicblocks/stone_pickaxe.png"), loadblock("src/basicblocks/iron_r.png"), loadblock("src/basicblocks/coal_r.png"), loaditem("src/basicblocks/hammer.png"), loadblock("src/basicblocks/stove.png"), loadblock("src/basicblocks/iron_i.png"), loadblock("src/basicblocks/gold_r.png"), loadblock("src/basicblocks/gold_i.png"), loaditem("src/basicblocks/iron_pickaxe.png")]
hitblocks = [1, 2, 3, 11, 12, 14, 16]
#todo:blocks

#           0    1     2     3    4    5   6    7      8      9  10      11    12    13    14   15  16   17   18
blockhard = [-1, 100, 1000, 100, 400, 50, 300, -1,    -1,    -1, -1,    1500,  1200, -1,  1000, -1, 2000, -1, -1]
breakval =  [-1, -1,   -1,   -1,  -1,  -1, -1, 10000, 10000, -1, 40000, 40000, -1,   3000, -1,  -1, -1,   -1, 80000]
breaking = breakval.copy()
backpack = [0]*1000

entitys = [0]*10000
aliveentity = []


class Entity:
    ex, ey = 0, 0
    eid: int = -1
    def __init__(self):
        while True:
            self.eid = random.randint(0, 10000)
            if entitys[self.eid] == 0:
                break
        entitys[self.eid] = self
        aliveentity.append(self.eid)
        self.eyf = 0

    def goto(self, ex, ey):
        self.ex, self.ey = ex, ey

    def gravity(self, mass=1):
        if self.eyf > 0:
            self.ey -= self.eyf
        if world[int(self.ex)][int(self.ey)+1] not in hitblocks:
            self.eyf -= gravity*mass
            self.ey -= self.eyf
        else:
            if world[int(self.ex)][int(self.ey)-1] not in hitblocks:
                self.ey -= 0.01*mass
            else:
                self.ey += 0.01*mass
            self.eyf = 0

    def destroy(self):
        entitys[self.eid] = 0
        aliveentity.remove(self.eid)
        del self

    def check(self):
        if abs(self.ex-x) > 15 or abs(self.ey-y) > 20:
            self.destroy()

    def update(self):
        self.gravity()

    def uupdate(self):
        self.check()
        self.update()


# entities


class destroyed_block(Entity):
    def __init__(self, blockid, bx, by):
        super().__init__()
        self.blockid = blockid
        self.ex, self.ey = bx, by
    def update(self):
        sc.sc.blit(pygame.transform.scale(block[self.blockid], (10, 10)), ((self.ex - x + 12) * 33+10, (self.ey - round(y, 1) + 16) * 33+10))
        if abs(x - self.ex) <= 1 and abs(y - self.ey) <= 1:
            backpack[self.blockid] += 1
            self.destroy()
# creating world

def clonestruct(st: list, xx, yy):
    for i in st:
        world[xx+int(i.split(',')[0])][yy+int(i.split(',')[1])] = int(i.split(':')[2])



if isgamee == 2:
    try:
        os.mkdir(os.getcwd()+"/worlds/"+worldname)
        os.mkdir(os.getcwd() + "/worlds/" + worldname + "/mods")
    except FileExistsError:
        pylog.log("world already exist!", "WARN")
    open(r"worlds/"+worldname+"/map", "w").close()
    open(r"worlds/" + worldname + "/backpack", "w").close()
    for i in range(WORLDWIDTH):
        for j in range(35, WORLDDEPTH):
            world[i][j] = 2
        for j in range(32, random.randint(35, 37)):
            world[i][j] = 1
        world[i][31] = 3
    for i in range(WORLDWIDTH//15):
        rx = random.randint(4, WORLDWIDTH-4)
        hi = random.randint(2, 6)
        for j in range(31-hi, 31):
            world[rx][j] = 4
        cx = rx
        cy = 31-hi
        world[cx][cy-1] = 5
        world[cx+1][cy] = 5
        world[cx-1][cy] = 5
        world[cx][cy - 2] = 5
        world[cx+1][cy - 1] = 5
        world[cx+2][cy] = 5
        world[cx - 1][cy + 1] = 5
        world[cx - 2][cy] = 5
        world[cx + 1][cy + 1] = 5
        world[cx - 1][cy - 1] = 5
    for i in range(WORLDWIDTH):
        ry = random.randint(40, WORLDDEPTH-5)
        rx = random.randint(2, WORLDWIDTH-2)
        world[rx][ry] = 11
        ry = random.randint(40, 60)
        rx = random.randint(2, WORLDWIDTH - 2)
        world[rx][ry] = 12
    for i in range(WORLDWIDTH//4):
        ry = random.randint(60, WORLDDEPTH)
        rx = random.randint(2, WORLDWIDTH - 2)
        world[rx][ry] = 16
    isgamee = 1
    hp = 100
    x, y = WORLDWIDTH//2, 31
else:
    fl = open("worlds/"+worldname+"/map", "r+")
    rd = fl.read()
    for i in range(len(rd.split("\n"))):
        for j in range(len(rd.split("\n")[i].split(" "))):
            if rd.split("\n")[i].split(" ")[j] == "":
                continue
            world[i][j] = int(rd.split("\n")[i].split(" ")[j])
    fl.close()
    fl = open("worlds/" + worldname + "/backpack", "r+")
    rd = fl.read()
    for i in range(len(rd.split("\n")[0].split(" "))):
        try:
            backpack[i] = int(rd.split("\n")[0].split(" ")[i])
        except ValueError:
            pass
    x, y = float(rd.split("\n")[1].split(" ")[0]), float(rd.split("\n")[1].split(" ")[1])
    hp = int(float(rd.split("\n")[2]))
    fl.close()


def saveworld():
    global fl
    fl = open("worlds/"+worldname+"/backpack", "w+")
    fl.write("0 ")
    for i in backpack[1:]:
        fl.write(str(i)+" ")
    fl.write("\n"+str(x)+" "+str(y))
    fl.write("\n" + str(hp))
    fl.close()
    fl = open("worlds/"+worldname+"/map", "w+")
    for i in range(WORLDWIDTH):
        for j in range(WORLDDEPTH):
            fl.write(str(world[i][j])+" ")
        fl.write("\n")
    fl.close()

pyratch.setpyexit(saveworld)

sc.update()

jmp = 0
gravity = 0.003
digging = [-1, -1, -1]
thingsonhand = 0
openbp = 0
ticktime = round(time.time(), 4)
tick = 0
FPS = 0

#TODO:DOING

modevents = {
    "init": [],
    "update": []
}

def event_init(func):
    modevents["init"].append(func)

def event_update(func):
    modevents["update"].append(func)

for i in os.listdir(os.getcwd()+"/worlds/"+worldname+"/mods"):
    if i.split(".")[-1] == "py":
        fl = open(os.getcwd()+"/worlds/"+worldname+"/mods/"+i, "r+")
        ct = fl.read()
        fl.close()
        exec(ct)

class slot:
    def __init__(self, size=(40, 40)):
        self.sp = pyratch.sprite("src/slot.png", size)
        sss = pygame.Surface(size)
        sss.fill((150, 150, 150))
        self.sp.surface = sss
        self.obj = -1
        self.num = 1

slots = [slot() for ii in range(9)]
result = slot()

if playerpic == 1:
    playerx = pyratch.sprite("src/playerpic/playerr.png", (26, 26))
else:
    playerx = pyratch.sprite("src/playerpic/playerb.png", (26, 26))

playerx.goto(390, 501)

jmpd = y

for i in modevents["init"]:
    i()

# mainloop

while isgamee == 1:
    sc.sc.fill((87, 250, 255))
    tick += 1
    tm = round(time.time(), 4)
    if tick%30 == 0:
        if tm - ticktime > 0.02:
            pylog.log("fps too slow!", "warn")
    if tm - ticktime >= 0.00001 and tick%30 == 0:
        FPS = round(1 / (tm - ticktime))
    ticktime = tm
    if jmp > 0:
        y -= jmp
    if world[int(x)][int(y)] not in hitblocks:
        jmp -= gravity
        y -= jmp
    else:
        if y-jmpd > 10:
            hp -= (y-jmpd-9)*5
        jmpd = y
        if world[int(x)][int(y)-1] not in hitblocks:
            y -= 0.01
        else:
            y += 0.01
        jmp = 0
    for i in range(int(x)-13, int(x)+14):
        if i < 0 or i >= WORLDWIDTH:
            continue
        for j in range(int(y)-9, int(y) + 11):
            if j-7 < 0 or j-7 >= WORLDDEPTH:
                continue
            sc.sc.blit(block[world[i][j-7]], ((i-x+12)*33, (j-round(y, 1)+9)*33))
    sc.blit_sprite(playerx)
    sc.blit_sprite(playerp)

    if hp < 0:
        hp = 100
        x = WORLDWIDTH//2
        y = 31
        for i in [4, 11, 12, 15]:
            backpack[i] = backpack[i]//3*2

    sc.drawbetterrect(100, 20, (hp, 5), (255, 0, 0))
    keys = pyratch.inputs.getkeyspressed()
    evs = pyratch.events
    MUP = 0
    for ev in evs:
        if ev.type == pygame.KEYUP:
            if ev.key == pygame.K_q:
                openbp = 0
            if ev.key == pygame.K_e:
                if openbp != 0:
                    openbp = 0
                else:
                    openbp = 1
            if ev.key == pygame.K_u:
                for i in [(0, 0), (0, 1), (0, -1), (1, 0), (-1, 0)]:
                    blk = world[int(x) + i[0]][int(y) + i[1]]
                    if blk == 6:
                        if openbp != 0:
                            openbp = 0
                        else:
                            openbp = 2
        if ev.type == pygame.MOUSEBUTTONUP:
            MUP = 1
    if openbp == 1:
        sc.drawbetterrect(100, 100, (600, 400), (255, 245, 225))
        xxy = 0
        for i in range(len(backpack)):
            if backpack[i] != 0:
                sc.sc.blit(block[i], (xxy%11*50+150, xxy//11*70+150))
                if thingsonhand == i:
                    pygame.draw.polygon(sc.sc, (0, 0, 0), ((xxy%11*50+175, xxy//11*70+185), (xxy%11*50+170, xxy//11*70+195), (xxy%11*50+180, xxy//11*70+195)))
                if breakval[i] != -1:
                    sc.drawbetterrect(xxy%11*50+150, xxy//11*70+190, ((breaking[i]/breakval[i])*30, 5), (0, 255, 0))
                sc.drawtext(str(backpack[i]), (xxy%11*50+150, xxy//11*70+200))
                blockrect = block[i].get_rect()
                blockrect.x, blockrect.y = xxy % 11 * 50 + 150, xxy // 11 * 70 + 150
                if blockrect.collidepoint(pygame.mouse.get_pos()) and pyratch.inputs.getmousepressed():
                    thingsonhand = i
                xxy += 1
        cnttt = -1
        for i in slots[:4]:
            cnttt += 1
            i.sp.goto(200+cnttt%2*42, 400+cnttt//2*42)
            sc.blit_sprite(i.sp)
            if i.obj != -1:
                sc.sc.blit(block[i.obj], (200+cnttt%2*42+3, 400+cnttt//2*42+3))
            if i.sp.click():
                if i.obj == -1 and thingsonhand > 0:
                    i.obj = thingsonhand
                    backpack[thingsonhand] -= 1
                    if backpack[thingsonhand] <= 0:
                        thingsonhand = 0
                elif i.obj != -1:
                    backpack[i.obj] += 1
                    i.obj = -1
                time.sleep(0.2)
        result.sp.goto(300, 421)
        sc.blit_sprite(result.sp)
        result.obj = -1
        for i in formulas:
            if i.typ:
                if slots[0].obj == i.materials[0][0] and slots[1].obj == i.materials[0][1] and slots[2].obj == i.materials[1][0] and slots[3].obj == i.materials[1][1]:
                    result.obj = i.product
                    result.num = i.num
        if result.obj != -1:
            sc.sc.blit(block[result.obj], (303, 424))
        if result.sp.click():
            if result.obj != -1:
                backpack[result.obj] += result.num
                for i in slots[:4]:
                    i.obj = -1

            time.sleep(0.2)
        sc.update()
        continue
    elif openbp == 2:
        sc.drawbetterrect(100, 100, (600, 400), (255, 245, 225))
        xxy = 0
        for i in range(len(backpack)):
            if backpack[i] != 0:
                sc.sc.blit(block[i], (xxy % 11 * 50 + 150, xxy // 11 * 70 + 150))
                if thingsonhand == i:
                    pygame.draw.polygon(sc.sc, (0, 0, 0), (
                    (xxy % 11 * 50 + 175, xxy // 11 * 70 + 185), (xxy % 11 * 50 + 170, xxy // 11 * 70 + 195),
                    (xxy % 11 * 50 + 180, xxy // 11 * 70 + 195)))
                sc.drawtext(str(backpack[i]), (xxy % 11 * 50 + 150, xxy // 11 * 70 + 200))
                blockrect = block[i].get_rect()
                blockrect.x, blockrect.y = xxy % 11 * 50 + 150, xxy // 11 * 70 + 150
                if blockrect.collidepoint(pygame.mouse.get_pos()) and pyratch.inputs.getmousepressed():
                    thingsonhand = i
                xxy += 1
        cnttt = -1
        for i in slots[:9]:
            cnttt += 1
            i.sp.goto(200 + cnttt % 3 * 42, 350 + cnttt // 3 * 42)
            sc.blit_sprite(i.sp)
            if i.obj != -1:
                sc.sc.blit(block[i.obj], (200 + cnttt % 3 * 42 + 3, 350 + cnttt // 3 * 42 + 3))
            if i.sp.click():
                if i.obj == -1 and thingsonhand > 0:
                    i.obj = thingsonhand
                    backpack[thingsonhand] -= 1
                    if backpack[thingsonhand] <= 0:
                        thingsonhand = 0
                elif i.obj != -1:
                    backpack[i.obj] += 1
                    i.obj = -1
                time.sleep(0.2)
        result.sp.goto(340, 421)
        sc.blit_sprite(result.sp)
        result.obj = -1
        for i in formulas:
            if slots[0].obj == i.materials[0][0] and slots[1].obj == i.materials[0][1] and slots[2].obj == \
                    i.materials[0][2] and slots[3].obj == i.materials[1][0] and slots[4].obj == i.materials[1][1] and slots[5].obj == \
                    i.materials[1][2] and slots[6].obj == i.materials[2][0] and slots[7].obj == i.materials[2][1] and slots[8].obj == \
                    i.materials[2][2]:
                result.obj = i.product
                result.num = i.num
        if result.obj != -1:
            sc.sc.blit(block[result.obj], (343, 424))
        if result.sp.click():
            if result.obj != -1:
                backpack[result.obj] += result.num
                for i in slots[:9]:
                    i.obj = -1

            time.sleep(0.2)
        sc.update()
        continue
    if thingsonhand != 0:
        if breaking[thingsonhand] == 0:
            backpack[thingsonhand] -= 1
            if backpack[thingsonhand] == 0:
                thingsonhand = 0
            breaking[thingsonhand] = breakval[thingsonhand]
    if keys[pyratch.objects.K_a]:
        x -= 0.1
        if world[int(x-0.1)][int(y)] in hitblocks:
            x += 0.1
    if keys[pyratch.objects.K_d]:
        x += 0.1
        if world[int(x+0.4)][int(y)] in hitblocks:
            x -= 0.1
    if x >= WORLDWIDTH:
        x = WORLDWIDTH
    if x < 0:
        x = 0
    if y >= WORLDDEPTH:
        isgamee = 0
    if y < 0:
        y = 0
    if keys[pyratch.objects.K_w]:
        if y != WORLDDEPTH:
            if world[int(x)][int(y)] in hitblocks and world[int(x)][int(y)-1] not in hitblocks:
                jmp = 0.10
    if pyratch.inputs.getmousepressed():
        poss = pyratch.inputs.getmouseposition()
        #print((digging[0]+390)/33-24+x, (digging[1]+501)/33-31+y, digging[2])
        if poss[0] != digging[0] or poss[1] != digging[1]:
            digging[0], digging[1] = poss
            digging[2] = -1
        if digging[2] < 0:
            digging[2] = blockhard[world[int((digging[0]+390)/33-24+x)][int((digging[1]+501)/33-31+y)]]
        else:
            digging[2] -= 1
            bpm = world[int((digging[0] + 390) / 33 - 24 + x)][int((digging[1] + 501) / 33 - 31 + y)]
            for i in tools:
                if thingsonhand == i[0] and bpm == i[1]:
                    digging[2] -= i[2]
                    breaking[thingsonhand] -= 1
            if digging[2] < 0:

                # if bpm not in [0]:
                #     backpack[bpm] += 1
                if bpm == 11 and world[int((digging[0] + 390) / 33 - 24 + x)][int((digging[1] + 501) / 33 - 31 + y)+1] == 14 and thingsonhand == 13:
                    bpm = 15
                if bpm == 16 and world[int((digging[0] + 390) / 33 - 24 + x)][int((digging[1] + 501) / 33 - 31 + y) + 1] == 14 and thingsonhand == 13:
                    bpm = 17
                destroyed_block(bpm, int((digging[0]+390)/33-24+x), int((digging[1]+501)/33-31+y))

                world[int((digging[0]+390)/33-24+x)][int((digging[1]+501)/33-31+y)] = 0
    elif pyratch.inputs.getmousepressed(2):
        poss = pyratch.inputs.getmouseposition()
        if world[int((poss[0] + 390) / 33 - 24 + x)][int((poss[1] + 501) / 33 - 31 + y)] != 0:
            pass
        elif backpack[thingsonhand] <= 0 or thingsonhand == 0:
            thingsonhand = 0
        elif blockhard[thingsonhand] == -1:
            pass
        else:
            world[int((poss[0] + 390) / 33 - 24 + x)][int((poss[1] + 501) / 33 - 31 + y)] = thingsonhand
            backpack[thingsonhand] -= 1
            if backpack[thingsonhand] <= 0:
                thingsonhand = 0
    for i in modevents["update"]:
        i()
    for i in aliveentity:
        entitys[i].uupdate()
    sc.drawtext(f"FPS:{FPS}", (750, 580), size=18, color=((0, 0, 0) if FPS >= 50 else (255, 0, 0)))
    sc.update()
    while time.time() < tm+0.008:
        pass
    if tick%2000 == 0:
        saveworld()
    if tick%500 == 0 and hp <= 95:
        hp += 5
