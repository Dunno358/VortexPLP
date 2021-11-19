from typing import Type
import pygame
from pygame import Surface, rect
from pygame import font
from pygame.event import get_blocked, post
from pygame.locals import *
import os
from datetime import datetime
from random import randint
from random import uniform
import sys
import os
import time
import unicodedata
pygInit = pygame.init()
pygame.mixer.init()
pygame.key.set_repeat(500, 100)
print("\nPygame init: {}/7 Succed and {} failed".format(pygInit[0],pygInit[1]))
print("Init_Start_Time: ",str(datetime.now())[10:])
print("Witaj {}!".format(os.getlogin()))# - RETURNS NAME OF CURRENT USER

#14.09.2021

#COLORS
darkThemeMainCol = (30,30,30)
darkThemeSubCol = (45,45,45)
lightThemeMainCol = (230,230,230)
lightThemeSubCol = (190,190,190)
lt_gray = (240,240,240)
dark_gray = (120,120,120)
darker_gray = (80,80,80)
black = (0,0,0)
red = (150,0,0)
dark_red  = (90,0,0)
green = (0,150,0)
dark_green = (0,90,0)
logoBlue = (0,0,250)
dark_blue = (0,0,100)
lt_blue = (45, 119, 194)
orange = (161, 72, 0)
lt_brown = (61, 55, 31)
purple = (47,41,86)
gold = (189, 153, 38)
TD_darkGreen = (97,100,74)
TD_pathColor = (191,178,134)
TD_darkGray = (38, 38, 38)
dark_brown = (56, 38, 10)
lt_brown = (79, 53, 13)

def cipher(textin):
    ciphered = ""
    for char in textin:
        char = ord(char) + 1
        ciphered += chr(char)
    return ciphered 
def decipher(textin):
    deciphered = ""
    for char in textin:
        char = ord(char) - 1
        deciphered += chr(char)
    return deciphered
def getDisplayStyle():
    file = open(r"{}/metaData/settings/display.txt".format(dirPath),"r")
    readFile = file.read()
    file.close() 
    display = decipher(readFile)
    return display 

#DIR PATH
dirPath = os.path.dirname(os.path.realpath(__file__))
dirPath = dirPath[:-5] #-15 for .exe, -5 for .py
print("Dir Path: ",dirPath)



#DISPLAY
displaySize = pygame.display.Info()
size_w_minus = displaySize.current_w//91
size_h_minus = displaySize.current_h//10
""" if getDisplayStyle() == "window":
    size_w=displaySize.current_w-size_w_minus
    size_h=displaySize.current_h-size_h_minus
    size=[size_w,size_h]
else:
    size_w=displaySize.current_w
    size_h=displaySize.current_h
    size=[size_w,size_h] """
size_w=displaySize.current_w
size_h=displaySize.current_h
size=[size_w,size_h]
windowLogo = pygame.image.load(r"{}/Images/python-logo.png".format(dirPath))
clock = pygame.time.Clock()

#TESTING RESOLUTIONS
#size_w=1920
#size_h=1080

#ADMIN
#admin = False
admin = True

#ACTIVITIES
activeAny = False
activeCourse = False
activeLooking = False
activeSettings = False
activeContacts = False
activeBook = False
activities = [activeCourse,activeLooking,activeSettings,activeBook,activeContacts]
activeLesson = ""
eventsBlocked = False
searching = False
selectingDisplay = False
exiting = False

#LEVELS
courseLvl = 1
maxCourseLvl = 0
iterator = 1

#TEXTS
name=""
lookForPhrase=""
text = ""

#ERROR
errorShowed = False

#HOLDER
storedItems = []
errorText = ''
errorFontSize = 2

#TIME
wait = False
storedTime = ""
timer = ''
storedTimeValue = 0

#ACTIVE/INACTIVE
activeMenu = True
activeMain = True
notBlocked = True
wrong = False
confirmed = True
activeWriting = False
done = False
bckgrMusicPlayed = False
soundEnabled = False #True

#DRAGGING ITEMS
held = False

#CLICKING GAME
selected = ""
chosen = ""
inFight = False
hp1 = size_w/2.66
hp2 = size_w/6
loadingBar = False

#CORDS
rectCenter = (size_w/1.5)/2 + size_w/5
storedCords = []

#Dungeon
DG_icons = []

#Tower Defense
TD_circs = []
TD_pathCords = []
TD_guards = []
TD_guardRects = []
TD_guardSubRects = []
TD_consoleRects = []
TD_queue = []
TD_icon = ""
TD_time = ""
TD_lvlType = ""
TD_wdthStart = size_w/4.9
TD_hghtStart = size_h/1.63
TD_wdthStart2 = size_w/4.9
TD_hghtStart2 = size_h/1.63
TD_hp = size_w/19
TD_hp2 = size_w/19
TD_firstDone = False
TD_firstDone2 = False
TD_done = False
TD_enemy = None
TD_enemy2 = None
TD_actualEnemy = None
TD_actualEnemy2 = None
TD_consoleShown = False
TD_consoleOK = True
TD_active = []
TD_active2 = []
TD_consoleActiveRect = ""
TD_eventRects = []
TD_consoleTxts = ["","","",""]
TD_enemies = []
TD_friends = []
TD_iterator = 1
TD_round = 1
TD_count = 0
TD_toDefeat = 0
TD_unitsPassed = 0
TD_added = False
TD_added2 = False
TD_Lvls = [3,4,9,10,11,12,13,14,15,16,17]
TD_excludeLvls = 3
TD_excludedLvls = [12,14,16]
TD_friendsLvl = [13]
TD_subDone = False
TD_btnClicked = False

#SHOOTING RANGE
SR_icons = []
SR_cords = []
SR_iterator = 0
SR_holder = 0
SR_holder2 = 0

#PRIZE
iconsUnlock = []
iconsLocked = []
class Write(pygame.sprite.Sprite):
    def __init__(self,size,text,color,center):
        pygame.sprite.Sprite.__init__(self)
        self.textObject = pygame.font.Font(r"{}\Fonts\TrajanPro-Regular.ttf".format(dirPath),size)
        self.writeText = self.textObject.render(str(text),True,color)
        self.textRect = self.writeText.get_rect()
        self.textRect.center = center
        self.surface = screen.blit(self.writeText,self.textRect)
    def get_rect(self):
        return self.surface
class WriteItalic(pygame.sprite.Sprite):
    def __init__(self,size,text,color,center):
        pygame.sprite.Sprite.__init__(self)
        self.textObject = pygame.font.SysFont("Arial", size, bold=True, italic=True)
        self.writeText = self.textObject.render(str(text),True,color)
        self.textRect = self.writeText.get_rect()
        self.textRect.center = center
        self.surface = screen.blit(self.writeText,self.textRect)
    def get_rect(self):
        return self.surface

def isCorrectActivity():
    it = 0 
    for x in activities:
        if x == True:
            it += 1
    if it > 1:
        print("SideBarEctivities:::::STATUS_ERROR:\nExpected: 1\nGet: {}".format(it))
def getName():
    nameFile = open(r"{}/metaData/userInfo/Name.txt".format(dirPath),"r")
    readFile = nameFile.read()
    nameFile.close() 
    name = decipher(readFile)
    return name
def clearName():
    nameFile = open(r"{}/metaData/userInfo/Name.txt".format(dirPath),"w")
    nameFile.close() 
def getActualSecond():
    now = str(datetime.now())
    now = now[17:-5]
    return float(now)
def getCourseLvl():
    permitionsFile = open(r"{}/Metadata/course/permitions.txt".format(dirPath),"r")
    permitionLvl = permitionsFile.read()
    permitionsFile.close()
    permitionLvl = int(decipher(permitionLvl[34:]))
    return permitionLvl
def changeCourselvl(newLvl):
    permitionsFile = open(r"{}/Metadata/course/permitions.txt".format(dirPath),"w")
    permitionsFile.write(cipher("Current courseLvl permitions are: {}".format(str(newLvl))))
    permitionsFile.close()    
def getTheme():
    nameFile = open(r"{}/metaData/userInfo/Theme.txt".format(dirPath),"r")
    readFile = nameFile.read()
    nameFile.close() 
    theme = decipher(readFile)
    return theme  
def changeTheme(theme):
    themeFile = open(r"{}/Metadata/userInfo/Theme.txt".format(dirPath),"w")
    themeFile.write(cipher(theme))
    themeFile.close() 
def getPsswd():
    file = open(r"{}/metaData/settings/admpswd.txt".format(dirPath),"r")
    readFile = file.read()
    file.close() 
    _pswd = decipher(readFile)
    return _pswd      
def passwordConfirm(pswd):
    global activeMain,text,admin,wrong,storedTime
    if not activeMain:
        bckgr = pygame.draw.rect(screen, color1, [size_w/4.39,size_h/3.3,size_w/1.6,size_h/2], 0,15)
        
        inputBox = pygame.draw.rect(screen, color2, [size_w/3.88,size_h/2.34,size_w/1.78,size_h/8], 0,15)
        inputBoxBord = pygame.draw.rect(screen, lt_gray, [size_w/3.88,size_h/2.34,size_w/1.78,size_h/8], size_w//450,15)
        
        if language == "ENG":
            topText = Write(round(size_w//100*2.5),"enter administrator password",color3,[size_w/1.84,size_h/2.72])
        else:
            topText = Write(round(size_w//100*2.5),"wprowadź hasło administratora",color3,[size_w/1.84,size_h/2.72])
        pswdtxt = Write(round(size_w//100*4),"*"*len(text),color3,[size_w/1.84,size_h/1.95])
        
        if language == "ENG":
            confirm = "confirm"
            back = "back"
            wrongTxt = "wrong"
        else:
            confirm = "potwierdź"
            back = "wróć"
            wrongTxt = "źle"            

        confirmBtn = pygame.draw.rect(screen, dark_green, [size_w/1.6,size_h/1.65,size_w/6,size_h/7], 0,15)
        confirmTxt = Write(round(size_w//100*2),confirm,color1,[size_w/1.41,size_h/1.47])
        
        backBtn = pygame.draw.rect(screen, dark_red, [size_w/3.42,size_h/1.65,size_w/6,size_h/7], 0,15)
        backTxt = Write(round(size_w//100*3),back,color1,[size_w/2.65,size_h/1.47])

        if wrong and getActualSecond()-storedTime<2:
            Write(round(size_w//100*3),wrongTxt,red,[size_w/1.84,size_h/1.49])  

        if event.type == MOUSEMOTION:
            if confirmBtn.collidepoint(mouse_pos):
                pygame.draw.rect(screen, green, [size_w/1.6,size_h/1.65,size_w/6,size_h/7], size_w//200,15)
                Write(round(size_w//100*2),confirm,color3,[size_w/1.41,size_h/1.47])
            elif backBtn.collidepoint(mouse_pos):
                pygame.draw.rect(screen, red, [size_w/3.42,size_h/1.65,size_w/6,size_h/7], size_w//200,15)
                Write(round(size_w//100*3),back,color3,[size_w/2.65,size_h/1.47])
        elif event.type == MOUSEBUTTONDOWN:
            if backBtn.collidepoint(mouse_pos):
                activeMain = True
                confirmed = True
                wrong = False
            elif confirmBtn.collidepoint(mouse_pos):
                if text == pswd:
                    admin = True
                    activeMain = True
                    confirmed = True
                    wrong = False
                else:
                    wrong = True  
                    storedTime = getActualSecond()     
        if event.type == KEYDOWN:
            if event.key == pygame.K_BACKSPACE and not activeMain:
                try:
                    text=text[:-1]                      
                except:
                    pass
            elif event.key == pygame.K_RETURN:
                if text == pswd:
                    admin = True
                    activeMain = True
                    confirmed = True
                    wrong = False
                else:
                    wrong = True   
                    storedTime = getActualSecond()
            elif event.key == pygame.K_ESCAPE:
                activeMain = True
                confirmed = True                
            elif len(text) < 20 and event.key!=K_BACKSPACE:
                if keys[K_LSHIFT]:
                    if event.key==K_9:
                        text += "("
                    elif event.key==K_8:
                        text += "*"
                    elif event.key==K_7:
                        text += "&"
                    elif event.key==K_6:
                        text += "^"
                    elif event.key==K_5:
                        text += "%"
                    elif event.key==K_4:
                        text += "$"
                    elif event.key==K_3:
                        text += "#"
                    elif event.key==K_2:
                        text += "@"
                    elif event.key==K_1:
                        text += "!"                        
                    elif event.key==K_0:
                        text += ")"
                    elif event.key==K_LEFTBRACKET:
                        text += "["
                    elif event.key == K_RIGHTBRACKET:
                        text += "]"
                    elif event.key == K_QUOTE:
                        text += "\""
                    elif event.key == K_3:
                        text += "#"
                    elif event.key == K_SEMICOLON:
                        text += ":"
                    else:
                        try:
                            text += chr(event.key).upper()
                        except:
                            pass
                else:
                    try:
                        if event.key != K_LSHIFT:
                            text += chr(event.key)
                    except:
                        pass      
def getLang():
    file = open(r"{}/metaData/userInfo/Lang.txt".format(dirPath),"r")
    readFile = file.read()
    file.close() 
    lang = decipher(readFile)
    return lang[20:]      
def changeLang(lang):
    text = "Current Language is:"
    langFile = open(r"{}/Metadata/userInfo/Lang.txt".format(dirPath),"w")
    langFile.write(cipher(text+lang))
    langFile.close()     
def changeDisplayStyle(displayStyle):
    langFile = open(r"{}/Metadata/settings/display.txt".format(dirPath),"w")
    langFile.write(cipher(displayStyle))
    langFile.close()  
def resetEvents():
    events = [MOUSEBUTTONDOWN,MOUSEBUTTONUP,MOUSEMOTION,KEYUP,KEYDOWN]
    for event in events:
        if pygame.event.get_blocked(event):
            pygame.event.set_allowed(event)
def errorInit(text,fontSize=2):
    global errorText,errorFontSize,errorShowed
    errorText = text
    errorFontSize = fontSize
    errorShowed = True
def errorHandling(): 
    global activities,activeAny,activeMain,activeMenu,errorShowed,activeCourse,errorText,errorFontSize
    global courseLvl
    if errorShowed:
        pygame.event.set_blocked([MOUSEMOTION,KEYUP,KEYDOWN])
        pygame.draw.rect(screen, color1, [size_w/5,size_h/16,size_w/1.5,size_h/1.1],0,10)
        pygame.draw.rect(screen, color2, [size_w/5,size_h/16,size_w/1.5,size_h/1.1],0,10)

        pygame.draw.rect(screen, color1, [size_w/3.43,size_h/3.94,size_w/2,size_h/2.5], 0,size_w//200)
        pygame.draw.rect(screen, red, [size_w/3.43,size_h/3.94,size_w/2,size_h/2.5], size_w//450,size_w//200)
        
        if not isinstance(errorText,list):
            Write(round(size_w//100*errorFontSize),errorText,red,[size_w/1.82,size_h/2.65])
        elif isinstance(errorText,list):
            hght = size_h/2.65
            for txt in errorText:
                Write(round(size_w//100*errorFontSize),txt,red,[size_w/1.82,hght])
                hght += size_h/20

        okBtn = course.centeredBtn(1.93,dark_red,"OK",adjustToDialog=True)

        if event.type == MOUSEBUTTONDOWN:
            if okBtn.collidepoint(mouse_pos):
                pygame.event.set_allowed([MOUSEMOTION,KEYUP,KEYDOWN])
                activities[0] = False
                activities[1] = False
                activities[2] = False
                activities[3] = False
                activities[4] = False
                courseLvl = 1
                activeAny = False
                activeMenu = True
                activeMain = True
                errorShowed = False
                start.welcomeScreen()


class Start(pygame.sprite.Sprite):
    global language
    language = getLang()
    def useScreenDef():
        global sideBarOpt1,sideBarOpt2,sideBarOpt3,sideBarOpt4,sideBarOpt5, sideBarIcons
        global screen
        global color1,color2,color3

        if getTheme().upper() == "LIGHT":
            color1 = lightThemeMainCol
            color2 = lightThemeSubCol
            color3 = black
        elif getTheme().upper() == "DARK":
            color1 = darkThemeMainCol
            color2 = darkThemeSubCol
            color3 = lt_gray

        screen = pygame.display.set_mode(size)
        screen.fill(color1)
        pygame.display.set_caption("VortexPLP")#Python_Learning_Project
        pygame.display.set_icon(windowLogo)

        sideBar_w = size_w//11 
        sideBar_h = size_h - size_h//18
        sideBarRctWStart = 20+sideBar_w//7
        sideBarRctHStart = size_w/21.4
        spaceBetween = sideBar_h/5.65
        sideBar = pygame.draw.rect(screen,color2,[20,20,sideBar_w,sideBar_h],0,30)

        sideBarRctWE = sideBar_w/1.4
        sideBarRctHghtE = sideBar_h//8 
        sideBarRWdth = sideBarRctWE-sideBarRctWStart
        sideBarRHght = sideBarRctHghtE - sideBarRctHStart

        sideBarOpt1 = pygame.draw.rect(screen,color1,[sideBarRctWStart,sideBarRctHStart,sideBarRctWE,sideBarRctHghtE],size_w//270,15)
        sideBarOpt2 = pygame.draw.rect(screen,color1,[sideBarRctWStart,sideBarRctHStart+spaceBetween,sideBarRctWE,sideBarRctHghtE],size_w//270,15)
        sideBarOpt3 = pygame.draw.rect(screen,color1,[sideBarRctWStart,sideBarRctHStart+spaceBetween*2,sideBarRctWE,sideBarRctHghtE],size_w//270,15)
        sideBarOpt4 = pygame.draw.rect(screen,color1,[sideBarRctWStart,sideBarRctHStart+spaceBetween*3,sideBarRctWE,sideBarRctHghtE],size_w//270,15)
        sideBarOpt5 = pygame.draw.rect(screen,color1,[sideBarRctWStart,sideBarRctHStart+spaceBetween*4,sideBarRctWE,sideBarRctHghtE],size_w//270,15)
       
        try:
            courseIcon = pygame.image.load(r"{}/Images/python-iconx128.png".format(dirPath))
            magnifierIcon = pygame.image.load(r"{}/Images/magnifier-iconx128.png".format(dirPath))
            settingsIcon = pygame.image.load(r"{}/Images/settings-iconx128.png".format(dirPath))
            prizeIcon = pygame.image.load(r"{}/Images/install/cup.png".format(dirPath))
            contactsIcon = pygame.image.load(r"{}/Images/contacts-iconx128.png".format(dirPath))
            sideBarIcons = [courseIcon,magnifierIcon,settingsIcon,prizeIcon,contactsIcon]
        except:
            errorInit("Failed to load SideBar Icons",fontSize=1.6)
            sideBarIcons = []

        for icon in sideBarIcons:
            index = sideBarIcons.index(icon)
            icon = pygame.transform.scale(icon,[int(size_w//21.3),int(size_h//12)])
            sideBarIcons[index] = icon

        it =sideBarRctHStart*1.15            
        for icon in sideBarIcons:
            screen.blit(icon,(sideBarRctWStart+size_w/120,it))  #int(size_w/29)
            it+=sideBar_h/5.6        

        Write(size_w//100,"V0.0.0.9",color3,[size_w/1.81,10]) 
        logoTxt1 = WriteItalic(round(size_w//100*6),"Vortex",logoBlue,[size_w/2,size_h/5.15])
        logoTxt1 = WriteItalic(round(size_w//100*4),"PLP",red,[size_w/1.59,size_h/5.5])

        WriteItalic(round(size_w//100*3.5),"Content is being loaded for you...",color3,[size_w/1.84,size_h/2.65])
        WriteItalic(round(size_w//100*1.5),"Loading sounds...",color3,[size_w/1.86,size_h/2.16])
        WriteItalic(round(size_w//100*1.5),"Loading images...",color3,[size_w/1.86,size_h/1.9])
        WriteItalic(round(size_w//100*1.5),"Loading fun...",color3,[size_w/1.86,size_h/1.7])
        
        Write(round(size_w//100*2.5),"Please be patient",color3,[size_w/1.84,size_h/1.2])

        pygame.display.update()
    def sideBarEvents():
        global sideBarOpts,iterator,activeAny,activeMain
        sideBarOpts = [sideBarOpt1,sideBarOpt2,sideBarOpt3,sideBarOpt4,sideBarOpt5]
        exitBtn = pygame.draw.rect(screen, dark_red, [size_w/1.13,size_h/153.6,size_w/10,size_h/12], 0,15)
        if language == "ENG":
            exitTxt = Write(round(size_w//100*2.5),"Exit",color1,[size_w/1.07,size_h/19.2])
        else:
            exitTxt = Write(round(size_w//100*2),"Wyjdź",color1,[size_w/1.07,size_h/19.2])
        if event.type == MOUSEMOTION:
            for Opt in sideBarOpts:
                if Opt.collidepoint(mouse_pos):
                    pygame.draw.rect(screen,color3,[Opt[0],Opt[1],Opt[2],Opt[3]],size_w//270,15)
                else:
                    pygame.draw.rect(screen,color1,[Opt[0],Opt[1],Opt[2],Opt[3]],size_w//270,15) 
            if exitBtn.collidepoint(mouse_pos):
                pygame.draw.rect(screen, red, [size_w/1.13,size_h/153.6,size_w/10,size_h/12], 0,15)
                if language == "ENG":
                    Write(round(size_w//100*2.5),"Exit",color3,[size_w/1.07,size_h/19.2])     
                else:
                    Write(round(size_w//100*2),"Wyjdź",color3,[size_w/1.07,size_h/19.2])            
        for activity in activities:
            if activity:
                index = activities.index(activity)
                rect = sideBarOpts[index]
                pygame.draw.rect(screen,color3,[rect[0],rect[1],rect[2],rect[3]],size_w//270,15)
        if event.type == MOUSEBUTTONDOWN:
            if exitBtn.collidepoint(mouse_pos):
                pygame.quit()
                sys.exit()   
            for opt in sideBarOpts:
                if opt.collidepoint(mouse_pos):
                    index = sideBarOpts.index(opt)  
                    activeAny = True
                    activeMain = True
                    for actIndex in range(len(activities)):
                        activities[actIndex] = False
                    activities[index] = True
    def setNameScreen():
        global name,readFile
        nameFile = open(r"{}/metaData/userInfo/Name.txt".format(dirPath),"r")
        readFile = nameFile.read()
        nameFile.close()
        if len(readFile) < 1:
            if language == "ENG":
                strs = [
                    "Hi, how do you want me to call you?",
                    "Skip",
                    "Confirm",
                    "Note: if you skip this part name of your account will be used"
                ]
            else:
                strs = [
                    "Cześć, jak mam się do ciebie zwracać?",
                    "Pomiń",
                    "Potwierdź",
                    "Notka: jeśli pominiesz tą część nazwa twojego konta będzie użyta"
                ]
            pygame.draw.rect(screen, color1, [size_w/5,size_h/16,size_w/1.5,size_h/1.1],0,10)
            Write(size_w//100*3,strs[0],color3,[size_w/1.8,size_h/3.5])

            inputBox = pygame.draw.rect(screen, color2, [size_w/3,size_h/2.5,size_w/2.5,size_h/4],0,10)

            skipBtn = pygame.draw.rect(screen, dark_red, [size_w/2.8,size_h/1.5,size_w/6,size_h/8],0,10)
            skipBtnTxt = Write(size_w//100*2,strs[1],color3,[size_w/2.28,size_h/1.37])

            confirmBtn = pygame.draw.rect(screen, dark_green, [size_w/1.85,size_h/1.5,size_w/6,size_h/8],0,10)
            confirmBtnTxt = Write(size_w//100*2,strs[2],color3,[size_w/1.60,size_h/1.37])

            Write(size_w//100,strs[3],color3,[size_w/1.9,size_h/1.1])


            pygame.draw.rect(screen, color2, [size_w/3,size_h/2.5,size_w/2.5,size_h/4],0,10)
            
            Write(size_w//100*2,name+"|",color3,[size_w/1.9,size_h/1.9])

            if event.type == MOUSEMOTION:
                if skipBtn.collidepoint(mouse_pos):
                    skipBtn = pygame.draw.rect(screen, red, [size_w/2.8,size_h/1.5,size_w/6,size_h/8],0,10)
                    skipBtnTxt = Write(size_w//100*2,strs[1],color3,[size_w/2.28,size_h/1.37])
                else:
                    skipBtn = pygame.draw.rect(screen, dark_red, [size_w/2.8,size_h/1.5,size_w/6,size_h/8],0,10)
                    skipBtnTxt = Write(size_w//100*2,strs[1],color3,[size_w/2.28,size_h/1.37])
                if confirmBtn.collidepoint(mouse_pos):
                    confirmBtn = pygame.draw.rect(screen, green, [size_w/1.85,size_h/1.5,size_w/6,size_h/8],0,10)
                    confirmBtnTxt = Write(size_w//100*2,strs[2],color3,[size_w/1.60,size_h/1.37])      
                else:
                    confirmBtn = pygame.draw.rect(screen, dark_green, [size_w/1.85,size_h/1.5,size_w/6,size_h/8],0,10)
                    confirmBtnTxt = Write(size_w//100*2,strs[2],color3,[size_w/1.60,size_h/1.37])  
            elif event.type == MOUSEBUTTONDOWN:
                if skipBtn.collidepoint(mouse_pos) and event.button == 1:
                    nameFile = open(r"{}/metaData/userInfo/Name.txt".format(dirPath),"w")
                    writeToFile = nameFile.write(cipher(str(os.getlogin())))
                    nameFile.close() 
                    start.useScreenDef() 
                elif confirmBtn.collidepoint(mouse_pos) and event.button==1:
                    nameFile = open(r"{}/metaData/userInfo/Name.txt".format(dirPath),"w")
                    writeToFile = nameFile.write(cipher(name.capitalize()))
                    nameFile.close() 
                    start.useScreenDef() 
            elif event.type == KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    try:
                        name=name[:-1]                      
                    except:
                        pass
                elif event.key == K_RETURN:
                    nameFile = open(r"{}/metaData/userInfo/Name.txt".format(dirPath),"w")
                    writeToFile = nameFile.write(cipher(name.capitalize()))
                    nameFile.close() 
                    start.useScreenDef()                     
                elif len(name) < 18 and event.key!=K_BACKSPACE:
                    try:
                        name += chr(event.key)
                    except:
                        pass
    def welcomeScreen():
        global activeAny
        if len(getName()) > 0 and not activeAny:
            if getLang() == "ENG":
                strs = [
                    "Welcome",
                    "Want to take a quick guide before start?"
                ]
            else:
                strs = [
                    "Witaj",
                    "Chcesz rozpocząć krótki poradnik przed startem?"
                ]                
            pygame.draw.rect(screen, color2, [size_w/5,size_h/16,size_w/1.5,size_h/1.1],0,10)
            Write(size_w//100*3,"{} {}!".format(strs[0],getName()),color3,[size_w/1.8,size_h/5])

            Write(round(size_w//100*1.8),strs[1],color3,[size_w/1.8,size_h/1.5])
            guideBtn = pygame.draw.rect(screen, dark_green, [size_w/2.1,size_h/1.35,size_w/6,size_h/8],0,10)
            guideBtnTxt = Write(round(size_w//100*2.5),"Start",color3,[size_w/1.78,size_h/1.24])

            logoName = "Vortex"

            #Full black
            logoBckgr = pygame.draw.rect(screen, color1, [size_w/2.85,size_h/3.2,size_w/2.5,size_h/4],0,10)
            
            #border 8px
            #logoBckgr = pygame.draw.rect(screen, color1, [size_w/2.85,size_h/3.2,size_w/2.5,size_h/4],8,10)

            #Circle
            pygame.draw.circle(screen, color2, [size_w/1.80,size_h/2.3], size_w//19, 10)
            logoTxt = Write(size_w//35*3,logoName,color2,[size_w/1.85,size_h/2.2])
           
            logoSize = size_w//50*3
            logoTxt1 = WriteItalic(logoSize,logoName,logoBlue,[size_w/2,size_h/2.3])
            logoRect1 = logoTxt1.get_rect()
            wdth = logoRect1[0]+logoRect1[2]+size_w/25
            logoTxt1 = WriteItalic(logoSize-logoSize//3,"PLP",red,[wdth,size_h/2.5])
            #logoTxt1 = WriteItalic(logoSize-logoSize//3,"PLP",red,[size_w/2+(size_w//50*3*len(logoName)/2.65),size_h/2.5])
            if event.type == MOUSEMOTION:
                if guideBtn.collidepoint(mouse_pos):
                    guideBtn = pygame.draw.rect(screen, green, [size_w/2.1,size_h/1.35,size_w/6,size_h/8],0,10)
                    guideBtnBrd = pygame.draw.rect(screen, dark_green, [size_w/2.1,size_h/1.35,size_w/6,size_h/8],size_w//675,10)
                    guideBtnTxt = Write(round(size_w//100*2.5),"Start",color3,[size_w/1.78,size_h/1.24])      
                else:
                    guideBtn = pygame.draw.rect(screen, dark_green, [size_w/2.1,size_h/1.35,size_w/6,size_h/8],0,10)
                    guideBtnTxt = Write(round(size_w//100*2.5),"Start",color3,[size_w/1.78,size_h/1.24]) 
    def finishBar():
        global admin
        if not admin:
            startPoint = [size_w/1.07,size_h/6.51]
            endPoint = [size_w/1.07,size_h/1.15]
            fullH = size_h/1.15-size_h/6.51
            actualPercent = getCourseLvl()/10
            customEndPoint = [size_w/1.07,size_h/1.15-actualPercent*fullH]
            pygame.draw.rect(screen, color1, [size_w/1.12,size_h/7.6,size_w/12,size_h/1.2], 0)
            pygame.draw.line(screen, dark_gray, startPoint, endPoint, size_w//500)
            pygame.draw.line(screen, green, endPoint, customEndPoint, size_w//500)
            pygame.draw.circle(screen, green, [size_w/1.069,size_h/1.15-actualPercent*fullH], size_w//200, 0)
            Write(round(size_w//100*2),f"{int(actualPercent*100)}%",green,[size_w/1.07,size_h/1.08])
    def courseLvlBar():
        global admin,activeMenu,maxCourseLvl,courseLvl
        if not admin:
            if not activeMenu:
                pygame.draw.rect(screen, color1, [size_w/8.13,size_h/16,size_w/16,size_h/1.1], 0,size_w//450)
                startPoint = [size_w/6.5,size_h/6.51]
                endPoint = [size_w/6.5,size_h/1.15]
                fullH = size_h/1.15-size_h/6.51
                actualPercent = courseLvl/maxCourseLvl
                customEndPoint = [size_w/6.5,size_h/1.15-actualPercent*fullH]
                pygame.draw.line(screen, dark_gray, startPoint, endPoint, size_w//500)
                pygame.draw.line(screen, logoBlue, endPoint, customEndPoint, size_w//500)
                pygame.draw.circle(screen, logoBlue, [size_w/6.47,size_h/1.15-actualPercent*fullH], size_w//200, 0)
                Write(round(size_w//100*2),f"{int(actualPercent*100)}%",lt_blue,[size_w/6.5,size_h/1.08])
    class adminTools(pygame.sprite.Sprite):
        global admin
        def iterators():
            global iterator,courseLvl,SR_icons
            if admin:
                motionColor = (38,38,38)
                itBtn = pygame.draw.rect(screen, color2, [size_w/1.12,size_h/1.65,size_w/12,size_h/14], 0,15)
                itTxt = Write(size_w//100,"Iterator+",color3,[size_w/1.07,size_h/1.56])
                minItBtn = pygame.draw.rect(screen, color2, [size_w/1.12,size_h/2.02,size_w/12,size_h/14], 0,15)
                minItTxt = Write(size_w//100,"Iterator-",color3,[size_w/1.07,size_h/1.88])  
                lvlBtn = pygame.draw.rect(screen, color2, [size_w/1.12,size_h/2.58,size_w/12,size_h/14], 0,15)
                lvlTxt = Write(size_w//100,"Next Level",color3,[size_w/1.07,size_h/2.37]) 
                if event.type == MOUSEBUTTONDOWN:
                    if itBtn.collidepoint(mouse_pos):
                        pygame.draw.rect(screen, color1, [size_w/1.12,size_h/1.65,size_w/12,size_h/14], 0,15)
                        Write(size_w//100,"Iterator+",color3,[size_w/1.07,size_h/1.56])
                        iterator += 1
                    elif minItBtn.collidepoint(mouse_pos):
                        pygame.draw.rect(screen, color1, [size_w/1.12,size_h/2.02,size_w/12,size_h/14], 0,15)
                        Write(size_w//100,"Iterator-",color3,[size_w/1.07,size_h/1.88])
                        if iterator > 1:
                            iterator -= 1   
                    if lvlBtn.collidepoint(mouse_pos):
                        lvlBtn = pygame.draw.rect(screen, color1, [size_w/1.12,size_h/2.58,size_w/12,size_h/14], 0,15)
                        lvlTxt = Write(size_w//100,"Next Level",color3,[size_w/1.07,size_h/2.37]) 
                        courseLvl += 1 
                        SR_icons.clear() 
                        course.tower_defence.clearAdminTools() 
                elif event.type == MOUSEMOTION:
                    if itBtn.collidepoint(mouse_pos):
                        pygame.draw.rect(screen, motionColor, [size_w/1.12,size_h/1.65,size_w/12,size_h/14], 0,15)
                        Write(size_w//100,"Iterator+",color3,[size_w/1.07,size_h/1.56])
                    elif minItBtn.collidepoint(mouse_pos):
                        pygame.draw.rect(screen, motionColor, [size_w/1.12,size_h/2.02,size_w/12,size_h/14], 0,15)
                        Write(size_w//100,"Iterator-",color3,[size_w/1.07,size_h/1.88])
                    elif lvlBtn.collidepoint(mouse_pos):
                        lvlBtn = pygame.draw.rect(screen, motionColor, [size_w/1.12,size_h/2.58,size_w/12,size_h/14], 0,15)
                        lvlTxt = Write(size_w//100,"Next Level",color3,[size_w/1.07,size_h/2.37]) 
        def counterCords():
            if admin:
                bckgr = pygame.draw.rect(screen, color3, [size_w-size_w//10,size_h-size_h//10,size_w//8,size_h//12], 0) 
                try:     
                    Write(round(size_w//100*1.5),"size_w/{}".format(round(size_w/mouse_pos[0],2)),color1,[size_w-size_w//20,size_h-size_h//12])   
                    Write(round(size_w//100*1.5),"size_h/:{}".format(round(size_h/mouse_pos[1],2)),color1,[size_w-size_w//20,size_h-size_h//20])  
                except:
                    pass  
        def counterFPS(fpsLock=1000):
            if admin:
                clock.tick(fpsLock)
                pygame.draw.rect(screen, color1, [size_w/1.11,size_h/1.32,size_w//8,size_h//12], 0)
                Write(round(size_w//100*1.5),int(clock.get_fps()),green,[size_w/1.06,size_h/1.21])
        def changingLvl():
            global admin
            if admin:
                bckgr = pygame.draw.rect(screen, color2, [size_w/8.13,size_h/16,size_w/16,size_h/1.1], 0,size_w//450)
                hght = size_h/12.39
                rects = []
                for it in range(9):
                    if it+1 == getCourseLvl():
                        rect = pygame.draw.rect(screen, logoBlue, [size_w/7.81,hght,size_w/18.5,size_h/14], size_w//450,size_w//250)
                    else:
                        rect = pygame.draw.rect(screen, color3, [size_w/7.81,hght,size_w/18.5,size_h/14], size_w//450,size_w//250)
                    rects.append(rect)
                    Write(round(size_w//100*1.5),str(it+1),color3,[size_w/7.81+(size_w/18.5/2),hght+(size_h/14/2)])
                    hght += size_h/10
                if event.type == MOUSEBUTTONDOWN:
                    for rect in rects:
                        if rect.collidepoint(mouse_pos):
                            index = rects.index(rect)
                            changeCourselvl(index+1)
                            pygame.draw.rect(screen, green, [rect[0],rect[1],rect[2],rect[3]], size_w//450,size_w//250)
            else:
                pygame.draw.rect(screen, color1, [size_w/8.13,size_h/16,size_w/16,size_h/1.1], 0,size_w//450)
class Course(pygame.sprite.Sprite):
    global actualLesson
    actualLesson = str(activeLesson)[17:-23]
    mentorIcon = ""
    class dungeon(pygame.sprite.Sprite):
        global hpBarEmpty
        def singleUnitInit(iconsList,wdthPict,hghtPict):
            global icons,wdth,hght,icoW,icoH
            icons = iconsList
            wdth = wdthPict
            hght = hghtPict
            icoW = icons[0].get_width()
            icoH = icons[0].get_height()
        def singleUnitDraw(hitBoxCords,dialogHght,textListIfNotDialog,dialogText,dialogTop=True,textRect=False):
            global inFight
            global endBtn,fightBtn,rects
            rects = []
            cords = hitBoxCords
            txtHght = size_h/2.5
            hghtToAdd = size_h/25
            for cord in cords:
                rect = pygame.draw.rect(screen, color2, cord, 1) #HITBOX COLOR2 BY DEFAULT
                rects.append(rect)
            if not inFight:
                if dialogTop:
                    course.dialogTop(dialogHght,dialogText)
                    screen.blit(icons[0],[wdth,hght])
                elif not dialogTop and len(icons)>2:
                    screen.blit(icons[2],[size_w/3.7,size_h/4.38])
                    if textRect:
                        pygame.draw.rect(screen, color1, [size_w/1.94,size_h/2.68,size_w/3.8,size_h/20*len(textListIfNotDialog)], size_w//300,20)
                    for text in textListIfNotDialog:
                        WriteItalic(round(size_w//100*1.5),text,color3,[size_w/1.55,txtHght])
                        txtHght += hghtToAdd
                endBtn = pygame.draw.rect(screen, color2, [size_w/2.29,size_h/1.2,size_w/7,size_h/10], 1,15)
                fightBtn = pygame.draw.rect(screen, dark_red, [size_w/2.29,size_h/1.2,size_w/7,size_h/10], 0,15)
                if getLang() == "ENG":
                    Write(size_w//100*2,"Fight",color1,[size_w/1.97,size_h/1.13])  
                else:
                    Write(size_w//100*2,"Walka",color1,[size_w/1.97,size_h/1.13])
            else:
                screen.blit(icons[0],[wdth,hght])
        def singleUnitHp(enemyName):
            global inFight,hp1,hp2
            global activeMain,hpWdth
            if inFight:
                hpWdth =  size_w/3.05
                global hpBarEmpty
                hpBarEmpty = hp1+hpWdth < hpWdth + size_w/150
                if not hpBarEmpty:
                    if activeMain:
                        hpBar = pygame.draw.rect(screen, dark_red, [size_w/3.05,size_h/6.41,hp1,size_h/16], 0 , 15) #hp1*size_w/455
                        Write(size_w//100*2,enemyName,color3,[size_w/1.95,size_h/8.75])
                        userHp = pygame.draw.rect(screen, dark_red, [size_w/2.3,size_h/1.25,hp2,size_h/16], 0,15) #hp2*size_w/1370
                        pygame.draw.rect(screen, color1, [size_w/2.3,size_h/1.25,size_w/6,size_h/16], size_w//450,15)
                        if getLang() == "ENG":
                            Write(size_w//100*2,"You",color3,[size_w/1.95,size_h/1.11])
                        else:
                            Write(size_w//100*2,"Ty",color3,[size_w/1.95,size_h/1.11])
                pygame.draw.rect(screen, color1, [size_w/3.05,size_h/6.41,size_w/2.66,size_h/16], size_w//450 , 15)
        def singleUnitAfterFight(endText):
            global endBtn,hp1
            hpWdth = size_w/3.05
            hpBarEmpty = hp1+hpWdth < hpWdth + size_w/150
            if hpBarEmpty:
                pygame.draw.rect(screen, color2, [size_w/3.35,size_h/4.55,size_w/2,size_h/1.7], 0)
                if getLang() == "ENG":
                    Write(size_w//100*4,"X Defeated X",dark_red,[size_w/1.94,size_h/1.98])
                else:
                    Write(size_w//100*4,"X Pokonany X",dark_red,[size_w/1.94,size_h/1.98])
                endBtn = pygame.draw.rect(screen, dark_red, [size_w/2.29,size_h/1.2,size_w/7,size_h/10], 0,15)
                Write(size_w//100*2,endText,color1,[size_w/1.97,size_h/1.13])
        def singleUnitQuestions(questions,answers,goodAnswers):
            global iterator,activeMain
            if iterator%4==0 and iterator<25:
                activeMain = False
                index = round(iterator//4-1)
                course.gameQuestion(questions[index],answers[index],goodAnswers[index])
        def singleUnitMotionEvent(endText):
            global hp1,endBtn
            hpWdth = size_w/3.05
            hpBarEmpty = hp1+hpWdth < hpWdth + size_w/150
            if event.type == MOUSEMOTION:
                if endBtn.collidepoint(mouse_pos) and inFight and hpBarEmpty:
                    pygame.draw.rect(screen, red, [size_w/2.29,size_h/1.2,size_w/7,size_h/10], 0,15)
                    pygame.draw.rect(screen, dark_red, [size_w/2.29,size_h/1.2,size_w/7,size_h/10], size_w//450,15)
                    Write(size_w//100*2,endText,color3,[size_w/1.97,size_h/1.13])  
                if fightBtn.collidepoint(mouse_pos) and not inFight:
                    pygame.draw.rect(screen, red, [size_w/2.29,size_h/1.2,size_w/7,size_h/10], 0,15)
                    pygame.draw.rect(screen, dark_red, [size_w/2.29,size_h/1.2,size_w/7,size_h/10], size_w//450,15)
                    if getLang() == "ENG":
                        Write(size_w//100*2,"Fight",color3,[size_w/1.97,size_h/1.13])    
                    else:
                        Write(size_w//100*2,"Walka",color3,[size_w/1.97,size_h/1.13]) 
        def singleUnitClickEvent(isBoss):
            global hp1,hp2,courseLvl,soundEnabled
            global iterator,inFight,notBlocked,chosen,DG_icons
            if event.type == MOUSEBUTTONDOWN:
                for rect in rects:
                    if rect.collidepoint(mouse_pos) and inFight and activeMain and not hpBarEmpty:
                        hp1 -= size_w/70
                        index = rects.index(rect)
                        screen.blit(icons[1],[wdth,hght])
                        course.coursorMarked()
                        if soundEnabled:
                            try:
                                if chosen == 0:
                                    pygame.mixer.music.load(f"{dirPath}/Music/monster_hurt.ogg")
                                else:
                                    pygame.mixer.music.load(f"{dirPath}/Music/punch.ogg")
                                pygame.mixer.music.play(1)
                            except:
                                errorInit("Failed to load sounds: singleUnitClickEvent",fontSize=1.5)
                        iterator += 1  
                if fightBtn.collidepoint(mouse_pos) and not inFight:
                    inFight = True
                elif endBtn.collidepoint(mouse_pos) and inFight and hpBarEmpty:
                    if isBoss:
                        inFight = False
                        notBlocked = True
                        chosen = ""
                        hp1 = size_w/2.66
                        hp2 = size_w/6
                        iterator = 1
                        courseLvl += 1
                    else:
                        inFight = False
                        chosen = ""
                        hp1 = size_w/2.66
                        hp2 = size_w/6
                        iterator = 1
                    DG_icons = []
    class tower_defence():
        def drawPath():
            global TD_pathCords
            it = 1
            cords = [
                [size_w/5,size_h/1.72,size_w/5,size_h/7],
                [size_w/2.84,size_h/1.72,size_w/8,size_h/7],
                [size_w/2.39,size_h/2.31,size_w/17,size_h/5],
                [size_w/2.39,size_h/3.15,size_w/17,size_h/7],
                [size_w/2.24,size_h/3.15,size_w/5,size_h/7],
                [size_w/1.7,size_h/3.15,size_w/8,size_h/7],
                [size_w/1.528,size_h/2.45,size_w/17,size_h/5],
                [size_w/1.528,size_h/1.77,size_w/17,size_h/6.28],
                [size_w/1.48,size_h/1.72,size_w/5.22,size_h/7]
            ]
            for cord in cords:
                if it%2==0 and it!=8:
                    path = pygame.draw.rect(screen, TD_pathColor, cord, 0,30)
                elif it==8:
                    path = pygame.draw.rect(screen, TD_pathColor, cord, 0,10)
                else:
                    path = pygame.draw.rect(screen, TD_pathColor, cord, 0)
                TD_pathCords.append(path)
                it += 1
        def drawMap(trees=True,guards=True):
            global TD_guards,TD_guardRects,TD_darkGreen,TD_guardSubRects
            if guards:

                cords = [
                    [size_w/5,size_h/5.57,size_w/1.5,size_h/1.5],
                    [size_w/3.29,size_h/15.67,size_w/1.78,size_h/8],
                    [size_w/5,size_h/1.18,size_w/16,size_h/8],
                    [size_w/3.36,size_h/1.18,size_w/1.76,size_h/8],
                    [size_w/3.82,size_h/1.13,size_w/16,size_h/11]
                ]

                try:
                    guard = pygame.image.load(r"{}/Images/Game/2dmap/guard.png".format(dirPath))
                    guard = pygame.transform.scale(guard, [int(size_w/14.22),int(size_h/8)])
                    cords = [
                        [size_w/3.24,size_h/2.3],
                        [size_w/2.04,size_h/2.16],
                        [size_w/1.75,size_h/2.16],
                        [size_w/1.37,size_h/2.33]
                    ]
                    for cord in cords:
                        #guardIcon = screen.blit(guard,cord)
                        holdGuard = [cord[0]+guard.get_width()/2,cord[1]+guard.get_height()/2]
                        holdGuardRect = [cord[0],cord[1],guard.get_width(),guard.get_height()]
                        TD_guards.append(holdGuard)
                        TD_guardRects.append(holdGuardRect)
                    for guardian in TD_guards:
                        wdth = guardian[0]
                        hght = guardian[1]
                        circ = pygame.draw.circle(screen, TD_darkGreen, [wdth,hght], size_w/10, size_w//900)
                        TD_circs.append(circ)

                    for cord in cords:
                        screen.blit(guard,cord)
                except:
                    errorInit("Failed to load 'guard.png'")

            if trees:
                try:
                    tree = pygame.image.load(r"{}/Images/Game/2dmap/tree.png".format(dirPath))
                    tree = pygame.transform.scale(tree, [int(size_w/10.6),int(size_h/6)])
                    treeCords = [
                        [size_w/3.93,size_h/4.29], #up1
                        [size_w/2.95,size_h/11.82], #up2
                        [size_w/2.1,size_h/7.18], #up3
                        [size_w/1.68,size_h/10.82], #up4
                        [size_w/1.38,size_h/7.5], #up5
                        [size_w/2.65,size_h/1.32], #down1
                        [size_w/1.73,size_h/1.32] #down2
                    ]
                    for cords in treeCords:
                        screen.blit(tree,cords)
                except:
                    errorInit("Failed to load 'tree.png'")
    
            course.tower_defence.drawPath()
        def nextBtn(color,text,border=False,colorIfBorder=(0,0,0)):
            okBtn = pygame.draw.rect(screen, color, [size_w/2.05,size_h/2.29,size_w/8,size_h/10], 0,15)
            if border:
                pygame.draw.rect(screen, colorIfBorder, [size_w/2.05,size_h/2.29,size_w/8,size_h/10], size_w//450,15)
            Write(size_w//100*2,text,color1,[size_w/1.82,size_h/2.29+size_h/19])
            return okBtn
        def makingGuards():
            global selected,storedTime,chosen,storedCords,done,circles,loadingBar,TD_icon
            if isinstance(TD_icon,str):
                try:
                    TD_icon = pygame.image.load(r"{}/Images/Game/potion.png".format(dirPath))
                    TD_icon = pygame.transform.scale(TD_icon,[int(size_w/42.68),int(size_h/12)])
                except:
                    errorInit("Failed to load 'potion.png'",fontSize=1.8)
                    TD_icon = None
            cords=[[size_w/2.72,size_h/1.92],
                    [size_w/1.91,size_h/1.94],
                    [size_w/1.67,size_h/1.94],
                    [size_w/1.33,size_h/1.95]       
            ]
            circles = []

            for cord in cords:
                circ = pygame.draw.circle(screen, orange, cord, size_w/50, 0)
                pygame.draw.circle(screen, dark_red, cord, size_w/50, size_w//450)
                circles.append(circ)

            for cord in storedCords:
                if cord in circles:
                   pygame.draw.circle(screen, lt_blue, [cord[0]+cord[2]/2,cord[1]+cord[3]/2], size_w/50, 0) 
                   pygame.draw.circle(screen, logoBlue, [cord[0]+cord[2]/2,cord[1]+cord[3]/2], size_w/50, size_w//450) 

            try:
                if circles[selected] not in storedCords and done:
                    storedCords.append(circles[selected])
            except:
                pass

            if event.type == MOUSEMOTION:
                for circ in circles:
                    if circ.collidepoint(mouse_pos) and circ not in storedCords:
                        pygame.draw.circle(screen, red, [circ[0]+circ[2]/2,circ[1]+circ[3]/2], size_w/50, 0)
                        pygame.draw.circle(screen, dark_red, [circ[0]+circ[2]/2,circ[1]+circ[3]/2], size_w/50, size_w//450)
            elif event.type == MOUSEBUTTONDOWN:
                for circ in circles:
                    index = circles.index(circ)
                    if isinstance(chosen,str):
                        if circ.collidepoint(mouse_pos) and circ not in storedCords:
                            selected = index
                            chosen = index
                            storedTime = getActualSecond()
                            loadingBar = True
                            if soundEnabled:
                                try:
                                    pygame.mixer.music.load(f"{dirPath}/Music/water_pouring.ogg")
                                    pygame.mixer.music.play(1)
                                except:
                                    errorInit("Failed to load 'water_pouring.ogg' at makingGuards",fontSize=1.5)


            correctWidth = mouse_pos[0] > size_w/4.93 and mouse_pos[0] < size_w/1.2
            correctHight = mouse_pos[1] > size_h/3.41 and mouse_pos[1] < size_h/1.17
            if not loadingBar:
                if correctWidth and correctHight:
                    try:
                        screen.blit(TD_icon,[mouse_pos[0]+size_w//400,mouse_pos[1]])
                    except:
                        pass
            else:
                try:
                    blitWdth = circles[selected][0] + circles[selected][2]/2
                    blitHght = circles[selected][1] + circles[selected][3]/2
                    screen.blit(TD_icon,[blitWdth,blitHght])
                except:
                    pass
        def loadingBar(time):
            global selected,chosen,activeMenu,activeLesson,courseLvl,done,loadingBar,storedTime
            if activities[0] and not activeMenu and str(activeLesson)[17:-23]=="lesson4" and courseLvl == 4:
                if isinstance(chosen,int):
                    try:
                        wdth = circles[selected][0]-size_w/40
                    except:
                        wdth = size_w/2.11
                    done = False
                    pygame.draw.rect(screen, color1, [wdth,size_h/2.55,size_w/10,size_h/20], size_w//450)
                    actualSecond = getActualSecond()
                    if storedTime > 57:
                        storedTime = storedTime - 1.5
                        actualSecond = actualSecond - 1.5
                    if actualSecond - storedTime > 1.5:
                        pygame.draw.rect(screen, red, [wdth,size_h/2.55,size_w/10,size_h/20], 0)
                        pygame.draw.rect(screen, color1, [wdth,size_h/2.55,size_w/10,size_h/20], size_w//450)
                        chosen = ""
                        done = True
                        loadingBar = False
                        return selected
                    elif actualSecond - storedTime > 1.25:
                        pygame.draw.rect(screen, red, [wdth,size_h/2.55,size_w/12,size_h/20], 0)
                        pygame.draw.rect(screen, color1, [wdth,size_h/2.55,size_w/10,size_h/20], size_w//450)
                    elif actualSecond - storedTime > 1:
                        pygame.draw.rect(screen, red, [wdth,size_h/2.55,size_w/18,size_h/20], 0)
                        pygame.draw.rect(screen, color1, [wdth,size_h/2.55,size_w/10,size_h/20], size_w//450)
                    elif actualSecond - storedTime > 0.75:
                        pygame.draw.rect(screen, red, [wdth,size_h/2.55,size_w/25,size_h/20], 0)
                        pygame.draw.rect(screen, color1, [wdth,size_h/2.55,size_w/10,size_h/20], size_w//450)
                    elif actualSecond - storedTime > 0.5:
                        pygame.draw.rect(screen, red, [wdth,size_h/2.55,size_w/50,size_h/20], 0)
                        pygame.draw.rect(screen, color1, [wdth,size_h/2.55,size_w/10,size_h/20], size_w//450)
                    elif actualSecond - storedTime > 0.25:
                        pygame.draw.rect(screen, red, [wdth,size_h/2.55,size_w/80,size_h/20], 0)
                        pygame.draw.rect(screen, color1, [wdth,size_h/2.55,size_w/10,size_h/20], size_w//450)
        def enemiesPath(second):
            global iterator,TD_wdthStart,TD_hghtStart,TD_firstDone,TD_guardRects,eventsBlocked
            global TD_guardSubRects,TD_enemy,TD_done,admin,TD_circs,TD_pathCords,TD_guards,TD_unitsPassed
            global TD_time,TD_active,TD_iterator,TD_hp,TD_consoleShown,TD_friends,TD_enemies
            global TD_actualEnemy,TD_actualEnemy2,TD_wdthStart2,TD_hghtStart2,TD_enemy2,TD_firstDone2
            global TD_hp2,TD_queue,TD_lvlType,TD_Lvls,TD_excludeLvls,TD_excludedLvls,TD_friendsLvl
            lessonOk = str(activeLesson)[17:-23]=="lesson4"
            lvlOk = courseLvl in TD_Lvls[TD_excludeLvls:] and courseLvl not in TD_excludedLvls
            if activities[0] and not activeMenu and lessonOk and lvlOk and not TD_consoleShown:
                language = getLang()
                eventsBlocked = True
                if len(TD_queue)<2:
                    try:
                        enemyGhost = pygame.image.load(r"{}/Images/Game/2dmap/ghost.png".format(dirPath))
                        enemyGhost = pygame.transform.scale(enemyGhost, [int(size_w/19.51),int(size_h/10.97)])
                        enemyGhost = pygame.transform.flip(enemyGhost, True, False)
                        friendJav = pygame.image.load(r"{}/Images/Game/2dmap/jav.png".format(dirPath))
                        friendJav = pygame.transform.scale(friendJav, [int(size_w/21.34),int(size_h/12)])
                        werewolf = pygame.image.load(r"{}/Images/Game/2dmap/werewolf.png".format(dirPath))
                        werewolf = pygame.transform.scale(werewolf, [int(size_w/21.34),int(size_h/12)])
                        dwarf = pygame.image.load(r"{}/Images/Game/2dmap/dwarf.png".format(dirPath))
                        dwarf = pygame.transform.scale(dwarf, [int(size_w/19.51),int(size_h/10.97)])
                        dwarf = pygame.transform.flip(dwarf, True, False)
                        reptill = pygame.image.load(r"{}/Images/Game/2dmap/reptill.png".format(dirPath))
                        reptill = pygame.transform.scale(reptill, [int(size_w/19.51),int(size_h/10.97)])
                        reptill = pygame.transform.flip(reptill, True, False)
                        fairyFriend = pygame.image.load(r"{}/Images/Game/2dmap/fairy2.png".format(dirPath))
                        fairyFriend = pygame.transform.scale(fairyFriend, [int(size_w/19.51),int(size_h/10.97)])
                        fairyFriend = pygame.transform.flip(fairyFriend, True, False)   
                        demon = pygame.image.load(r"{}/Images/Game/2dmap/demon.png".format(dirPath))
                        demon = pygame.transform.scale(demon, [int(size_w/21.34),int(size_h/12)])    
                        fairyFriend2 = pygame.image.load(r"{}/Images/Game/2dmap/fairy.png".format(dirPath))
                        fairyFriend2 = pygame.transform.scale(fairyFriend2, [int(size_w/21.34),int(size_h/12)])
                        fairyFriend2 = pygame.transform.flip(fairyFriend2, True, False)   
                        evilFairy = pygame.image.load(r"{}/Images/Game/2dmap/evilFairy.png".format(dirPath))
                        evilFairy = pygame.transform.scale(evilFairy, [int(size_w/19.51),int(size_h/10.97)])
                        evilFairy = pygame.transform.flip(evilFairy, True, False)  
                        armored = pygame.image.load(r"{}/Images/Game/2dmap/armoredFriend.png".format(dirPath))
                        armored = pygame.transform.scale(armored, [int(size_w/19.51),int(size_h/10.97)])
                        armored = pygame.transform.flip(armored, True, False)          
                        TD_enemies = [enemyGhost,werewolf,reptill,demon,evilFairy]
                        TD_friends = [friendJav,dwarf,fairyFriend,fairyFriend2,armored]
                        TD_queue = [
                            enemyGhost,
                            friendJav,
                            werewolf,
                            dwarf,
                            reptill,
                            fairyFriend,
                            demon,
                            fairyFriend2,
                            evilFairy,
                            armored
                            ]
                    except:
                        if language == "ENG":
                            errorInit("Failed to load TD Icons")
                        else:
                            errorInit("Błąd wczytywania TD Icons")
                try:
                    if TD_lvlType.lower() == "mixed":
                        TD_actualEnemy = TD_queue[iterator]
                        TD_actualEnemy2 = TD_queue[iterator-1]
                    elif TD_lvlType.lower() == "onlyfriend":
                        TD_actualEnemy = TD_queue[iterator]
                        TD_actualEnemy2 = TD_queue[iterator]
                    elif TD_lvlType.lower() == "onlyenemy":
                        TD_actualEnemy = TD_queue[iterator-1]
                        TD_actualEnemy2 = TD_queue[iterator-1]
                except:
                    TD_actualEnemy = None
                    TD_actualEnemy2 = None
                    print("TD_lvlType does not follow any of this: 'mixed','onlyfriend','onlyenemy'")
                secondGo = True
                if TD_lvlType == 'mixed':
                    TD_iterator = 1.5
                if getActualSecond()%100>=1 and not TD_done:
                    if TD_wdthStart<size_w/2.36 and not TD_firstDone:
                        course.tower_defence.drawPath()
                        TD_wdthStart += size_w/1000*TD_iterator
                        secondGo = False
                    elif TD_hghtStart>size_h/2.76 and not TD_firstDone:
                        course.tower_defence.drawPath()
                        TD_hghtStart -= size_h/700*TD_iterator
                    elif TD_wdthStart<size_w/1.52:
                        course.tower_defence.drawPath()
                        TD_wdthStart += size_w/1000*TD_iterator
                        TD_firstDone = True
                    elif TD_hghtStart<size_h/1.63:
                        course.tower_defence.drawPath()
                        TD_hghtStart += size_h/700*TD_iterator
                    elif TD_wdthStart<size_w/1.23:
                        course.tower_defence.drawPath()
                        TD_wdthStart += size_w/1000*TD_iterator
                    else:
                        try:
                            guard = pygame.image.load(r"{}/Images/Game/2dmap/guard.png".format(dirPath))
                            guard = pygame.transform.scale(guard, [int(size_w/14.22),int(size_h/8)])
                            course.tower_defence.drawPath()
                            #pygame.draw.rect(screen, TD_darkGreen, TD_guardSubRects[3], width=0)
                            guardW = TD_guardRects[3][0]
                            guardH = TD_guardRects[3][1]
                            screen.blit(guard,[guardW,guardH]) 
                        except:
                            if language == "ENG":
                                errorInit(["Failed to load 'guard.png'","at enemiesPath-first"])
                            else:
                                errorInit(["Błąd wczytywania 'guard.png'","w enemiesPath-first"])
                        if pygame.event.get_blocked(MOUSEMOTION):
                            pygame.event.set_allowed(MOUSEMOTION)
                        #TD_done = True
                        holdIterator = iterator
                        course.tower_defence.reset()
                        course.tower_defence.drawMap()
                        if courseLvl not in TD_friendsLvl or TD_lvlType == 'mixed':
                            iterator = holdIterator + 2
                        else:
                            TD_unitsPassed += 1
                            TD_iterator = 2
                    if secondGo:
                        if TD_wdthStart2<size_w/2.36 and not TD_firstDone2:
                            course.tower_defence.drawPath()
                            TD_wdthStart2 += size_w/1000*TD_iterator
                        elif TD_hghtStart2>size_h/2.76 and not TD_firstDone2:
                            course.tower_defence.drawPath()
                            TD_hghtStart2 -= size_h/700*TD_iterator
                        elif TD_wdthStart2<size_w/1.52:
                            TD_firstDone2 = True
                            course.tower_defence.drawPath()
                            TD_wdthStart2 += size_w/1000*TD_iterator
                        elif TD_hghtStart2<size_h/1.63:
                            course.tower_defence.drawPath()
                            TD_hghtStart2 += size_h/700*TD_iterator
                        elif TD_wdthStart2<size_w/1.01: #1.23
                            course.tower_defence.drawPath()
                            TD_wdthStart2 += size_w/1000*TD_iterator
                        else:
                            try:
                                guard = pygame.image.load(r"{}/Images/Game/2dmap/guard.png".format(dirPath))
                                guard = pygame.transform.scale(guard, [int(size_w/14.22),int(size_h/8)])
                                course.tower_defence.drawPath()
                                pygame.draw.rect(screen, TD_darkGreen, TD_guardSubRects[3], width=0)
                                guardW = TD_guardRects[3][0]
                                guardH = TD_guardRects[3][1]
                                screen.blit(guard,[guardW,guardH]) 
                            except:
                                if language == "ENG":
                                    errorInit(["Failed to load 'guard.png'","at enemiesPath-secondGo"])
                                else:
                                    errorInit(["Błąd wczytywania 'guard.png'","w enemiesPath-secondGo"])
                            if pygame.event.get_blocked(MOUSEMOTION):
                                pygame.event.set_allowed(MOUSEMOTION)
                            #TD_done = True
                            holdIterator = iterator
                            course.tower_defence.reset()
                            course.tower_defence.drawMap()
                            if courseLvl not in TD_friendsLvl or TD_lvlType == 'mixed':
                                iterator = holdIterator + 2
                            else:
                                TD_unitsPassed += 1
                                TD_iterator = 2

                try:
                    if not TD_done:
                        if TD_hp>0:
                            enemy = screen.blit(TD_actualEnemy,[TD_wdthStart,TD_hghtStart])
                            wdth = TD_wdthStart-size_w/800
                            hght = TD_hghtStart-size_h/40
                            hp = pygame.draw.rect(screen, dark_red, [wdth,hght,TD_hp,size_h/45], 0,size_w//200)
                            hpBar = pygame.draw.rect(screen, color1, [wdth,hght,size_w/19,size_h/45], size_w//800,size_w//200)
                        if secondGo and TD_hp2>0:
                            enemy2 = screen.blit(TD_actualEnemy2,[TD_wdthStart2,TD_hghtStart2])
                            wdth2 = TD_wdthStart2-size_w/800
                            hght2 = TD_hghtStart2-size_h/40
                            hp2 = pygame.draw.rect(screen, dark_red, [wdth2,hght2,TD_hp2,size_h/45], 0,size_w//200)
                            hpBar2 = pygame.draw.rect(screen, color1, [wdth2,hght2,size_w/19,size_h/45], size_w//800,size_w//200)
                            enemy2 = [enemy2[0] + enemy2[2]/2,enemy2[1] + enemy2[3]/2]
                            TD_enemy2 = enemy2
                    enemy = [enemy[0] + enemy[2]/2,enemy[1] + enemy[3]/2]
                    TD_enemy = enemy
                except:
                    enemy = [0,0]
                    enemy2 = [0,0]
        def targeting():
            global TD_consoleShown,TD_count,TD_Lvls,TD_excludeLvls,courseLvl,TD_excludedLvls
            lvlOk = courseLvl in TD_Lvls[TD_excludeLvls:] and courseLvl not in TD_excludedLvls
            if activities[0] and not activeMenu and str(activeLesson)[17:-23]=="lesson4" and lvlOk and not TD_consoleShown:
                global TD_enemy,TD_enemy2,TD_guardSubRects,TD_circs,TD_guardRects,TD_active,TD_done,TD_eventRects
                global iterator,TD_hp,TD_hp2,TD_round,TD_consoleTxts,TD_friends,TD_enemies,TD_actualEnemy2,TD_actualEnemy
                global TD_added,TD_added2,TD_toDefeat,TD_unitsPassed,TD_friendsLvl
                if not TD_done:
                    if TD_hp2<=0:
                        course.tower_defence.reset()
                    pygame.event.set_blocked(MOUSEMOTION)
                    pygame.event.set_blocked(KEYDOWN)
                    pygame.event.set_blocked(KEYUP)
                    pygame.event.set_blocked(MOUSEBUTTONDOWN)
                    menuConditionW = mouse_pos[0]>size_w/4.95 and mouse_pos[0]<size_w/3.32
                    menuConditionH = mouse_pos[1]>size_h/14.77 and mouse_pos[1]<size_h/6.05
                    onMenu = menuConditionH and menuConditionH
                    consoleCondW = mouse_pos[0]>size_w/5 and mouse_pos[0]<size_w/4.39
                    consoleCondH = mouse_pos[1]>size_h/3.75 and mouse_pos[1]<size_h/2.31
                    onConsole = consoleCondW and consoleCondH
                    inRectW = mouse_pos[0]>size_w/5 and mouse_pos[0]<size_w/1.17
                    inRectH = mouse_pos[1]>size_h/16 and mouse_pos[1]<size_h/1.03
                    inRect = inRectW and inRectH
                    leftArrowW = mouse_pos[0]>size_w/3.84 and mouse_pos[0]<size_w/3.38
                    leftArrowH = mouse_pos[1]>size_h/1.18 and mouse_pos[1]<size_h/1.14
                    onLeftArrow = leftArrowH and leftArrowH
                    rightArrowW = mouse_pos[0]>size_w/1.36 and mouse_pos[0]<size_w/1.3
                    rightArrowH = mouse_pos[1]>size_h/1.18 and mouse_pos[1]<size_h/1.14
                    onRightArrow = rightArrowH and rightArrowH
                    if onMenu or onLeftArrow or onRightArrow or onConsole or not inRect:
                        pygame.event.set_allowed(MOUSEBUTTONDOWN)
                    if "ENEMY" in TD_consoleTxts[0].upper() and TD_consoleOK:
                        first = "enemy"
                        second = "friend"
                    elif  "FRIEND" in TD_consoleTxts[0].upper() and TD_consoleOK:
                        first = "friend"
                        second = "enemy"
                    else:
                        first = None
                        second = None
                    TD_guardSubRects = [
                        [size_w/3.43,size_h/2.31,size_w/8.5,size_h/6.7],
                        [size_w/2.1,size_h/2.18,size_w/11,size_h/5.5],
                        [size_w/1.77,size_h/2.18,size_w/11,size_h/5.5],
                        [size_w/1.405,size_h/2.31,size_w/8.5,size_h/6.7]
                    ]
                    try:
                        guard = pygame.image.load(r"{}/Images/Game/2dmap/guard.png".format(dirPath))
                        guard = pygame.transform.scale(guard, [int(size_w/14.22),int(size_h/8)])
                    except:
                        if language == "ENG":
                            errorInit("Failed to load 'guard.png' at targeting",fontSize=1.7)
                        else:
                            errorInit("Błąd wczytywania 'guard.png' w targeting",fontSize=1.6)

                    cords = [
                        [size_w/5,size_h/5.57,size_w/1.5,size_h/1.5],
                        [size_w/3.29,size_h/15.67,size_w/1.78,size_h/8],
                        [size_w/5,size_h/1.18,size_w/16,size_h/8],
                        [size_w/3.36,size_h/1.18,size_w/1.76,size_h/8],
                        [size_w/3.82,size_h/1.13,size_w/16,size_h/11]
                    ]

                    if len(TD_circs)<1:
                        course.tower_defence.drawMap()

                    attackEnemy = first == "enemy" and TD_consoleTxts[1].lower() == "attack()" or second == "enemy" and TD_consoleTxts[3].lower() == "attack()"
                    attackFriend = first == "friend" and TD_consoleTxts[1].lower() == "attack()" or second == "friend" and TD_consoleTxts[3].lower() == "attack()"
                    letEnemy = first == "enemy" and TD_consoleTxts[1].lower() == "wait()" or second == "enemy" and TD_consoleTxts[3].lower() == "wait()"
                    letFriend = first == "friend" and TD_consoleTxts[1].lower() == "wait()" or second == "friend" and TD_consoleTxts[3].lower() == "wait()"
                    
                    attackingAllowed = TD_enemy not in TD_friends and not letFriend

                    for circ in TD_circs:
                        try:
                            index = TD_circs.index(circ)
                            if circ.collidepoint(TD_enemy) and TD_hp>0 and circ not in TD_active and attackingAllowed:
                                if index not in TD_active and attackingAllowed:
                                    TD_active.append(index)
                                try:
                                    pygame.draw.rect(screen, TD_darkGreen, TD_guardSubRects[index], width=0)
                                    guardW = TD_guardRects[index][0]
                                    guardH = TD_guardRects[index][1]
                                    screen.blit(guard,[guardW,guardH])
                                except:
                                    pass
                                lineColor = red
                                if letEnemy and TD_actualEnemy in TD_enemies or letFriend and TD_actualEnemy in TD_friends:
                                    pass
                                else:
                                    if getActualSecond()%2==0:
                                        if TD_hp > 0:
                                            TD_hp -= size_w/900*len(TD_active)/1.5
                                            lineColor = lt_blue
                                            try:
                                                if soundEnabled:
                                                    pygame.mixer.music.load(f"{dirPath}/Music/punch.ogg")
                                                    pygame.mixer.music.play(1)
                                            except:
                                                if language == "ENG":
                                                    errorInit("Failed to load 'punch.ogg'")
                                                else:
                                                    errorInit("Błąd wczytywania 'punch.ogg'")
                                        else:
                                            #course.tower_defence.drawMap()
                                            pygame.event.post(KEYUP)
                                    wdthStart = circ[0] + circ[2]/2
                                    hghtStart = circ[1] + circ[3]/2
                                    pygame.draw.line(screen, lineColor, [wdthStart,hghtStart], TD_enemy, 3) 
                            elif circ.collidepoint(TD_enemy2) and TD_hp2>0 and circ not in TD_active2:
                                if index not in TD_active2:
                                    TD_active2.append(index)
                                try:
                                    pygame.draw.rect(screen, TD_darkGreen, TD_guardSubRects[index], width=0)
                                    guardW = TD_guardRects[index][0]
                                    guardH = TD_guardRects[index][1]
                                    screen.blit(guard,[guardW,guardH])
                                except:
                                    pass
                                lineColor = red
                                attackEnemy = first == "enemy" and TD_consoleTxts[1].lower() == "attack()" or second == "enemy" and TD_consoleTxts[3].lower() == "attack()"
                                attackFriend = first == "friend" and TD_consoleTxts[1].lower() == "attack()" or second == "friend" and TD_consoleTxts[3].lower() == "attack()"
                                letEnemy = first == "enemy" and TD_consoleTxts[1].lower() == "wait()" or second == "enemy" and TD_consoleTxts[3].lower() == "wait()"
                                letFriend = first == "friend" and TD_consoleTxts[1].lower() == "wait()" or second == "friend" and TD_consoleTxts[3].lower() == "wait()"
                                if letEnemy and TD_actualEnemy2 in TD_enemies or letFriend and TD_actualEnemy2 in TD_friends:
                                    pass
                                else:
                                    if getActualSecond()%2==0:
                                        if TD_hp2 > 0:
                                            TD_hp2 -= TD_hp2/4*len(TD_active2)#size_w/550*len(TD_active2)
                                            lineColor = lt_blue
                                            pygame.mixer.music.load(f"{dirPath}/Music/punch.ogg")
                                            pygame.mixer.music.play(1)
                                        else:
                                            course.tower_defence.drawMap()
                                            course.tower_defence.reset()
                                            pygame.event.post(KEYUP)
                                    wdthStart = circ[0] + circ[2]/2
                                    hghtStart = circ[1] + circ[3]/2
                                    pygame.draw.line(screen, lineColor, [wdthStart,hghtStart], TD_enemy2, 3) 
                            else:
                                if index in TD_active2:
                                    TD_active2.remove(index)
                                try:
                                    if index<TD_active2[0]:
                                        pygame.draw.rect(screen, TD_darkGreen, TD_guardSubRects[index], width=0)
                                        guardW = TD_guardRects[index][0]
                                        guardH = TD_guardRects[index][1]
                                        screen.blit(guard,[guardW,guardH])  
                                except:
                                    pass      
                        except:
                            pass
                    if TD_hp<=0 and not TD_added:
                        TD_count += 1
                        TD_added = True
                        course.tower_defence.drawMap()
                    if TD_hp2<=0 and not TD_added2:
                        TD_count += 1
                        TD_added2 = True
                        course.tower_defence.drawMap()
                    pygame.draw.rect(screen, TD_darkGreen, [size_w/1.94,size_h/1.13,size_w/12,size_h/12], width=0)
                    if courseLvl in TD_friendsLvl:
                        Write(round(size_w//100*1.7),f"{TD_unitsPassed}/{TD_toDefeat}",color3,[size_w/1.87,size_h/1.11])
                        if TD_count >= 1:
                            if language == "ENG":
                                course.tower_defence.levelLost("Friendly unit has been killed!")
                            else:
                                course.tower_defence.levelLost("Sojusznicza jednostka zabita!")
                            courseLvl -= 1
                    else:
                        Write(round(size_w//100*1.7),f"{TD_count}/{TD_toDefeat}",color3,[size_w/1.87,size_h/1.11])
                    if (TD_count == TD_toDefeat and TD_lvlType!="onlyfriend") or TD_unitsPassed==TD_toDefeat:
                        if language == "ENG":
                            course.dialogTop(6.41,"Great job! Click anywhere","to go to the next level",bckgr=True)
                        else:
                            course.dialogTop(6.41,"Brawo! Kliknij gdziekolwiek,","by iść na następny lvl",bckgr=True)
                        courseLvl += 1 
                        TD_count = 0
                        TD_done = True
                else:
                    if pygame.event.get_blocked(MOUSEMOTION):
                        pygame.event.set_allowed(MOUSEMOTION)
        def adminTools():
            global iterator,TD_wdthStart,TD_hghtStart,TD_firstDone,TD_guardRects,eventsBlocked
            global TD_guardSubRects,TD_enemy,TD_done,admin,TD_circs,TD_pathCords,TD_guards
            global TD_time,TD_active,TD_iterator,TD_Lvls,TD_excludeLvls
            lvlOk = courseLvl in TD_Lvls[TD_excludeLvls:]
            if activities[0] and not activeMenu and str(activeLesson)[17:-23]=="lesson4" and lvlOk:          
                if admin:
                    rstBtn = pygame.draw.rect(screen, color2, [size_w/1.14,size_h/7.92,size_w/10,size_h/16], 0,15)
                    rstTxt = Write(round(size_w/100*1.5),"Reset",color3,[size_w/1.08,size_h/6.4])
                    multipliers = []
                    rectCords = [size_h/5.02,size_h/3.9,size_h/3.19]
                    values = [1,2,5]
                    for x in range(3):
                        multiplier = pygame.draw.rect(screen, color2, [size_w/1.11,rectCords[x],size_w/20,size_h/20], 0,15)
                        Write(round(size_w//100*1.5),f"x{values[x]}",color3,[size_w/1.11+size_w/40,rectCords[x]+size_h/40])
                        multipliers.append(multiplier)
                    if event.type == MOUSEBUTTONDOWN:
                        if rstBtn.collidepoint(mouse_pos):
                            course.tower_defence.reset()
                        else:
                            for multiplier in multipliers:
                                if multiplier.collidepoint(mouse_pos):
                                    index = multipliers.index(multiplier)
                                    TD_iterator = values[index] 
                else:
                    course.tower_defence.clearAdminTools()
        def clearAdminTools():
            pygame.draw.rect(screen, color1, [size_w/1.15,size_h/9.04,size_w/8,size_h/3.7], width=0)
            if pygame.event.get_blocked(MOUSEMOTION):
                pygame.event.set_allowed(MOUSEMOTION)
        def reset():
            global iterator,TD_wdthStart,TD_hghtStart,TD_firstDone,TD_guardRects,eventsBlocked,activeMenu
            global TD_guardSubRects,TD_enemy,TD_done,admin,TD_circs,TD_pathCords,TD_guards
            global TD_time,TD_active,TD_iterator,TD_hp,TD_round,TD_consoleShown,TD_consoleRects
            global TD_consoleActiveRect,TD_consoleTxts,TD_enemies,TD_friends,TD_hghtStart2,TD_wdthStart2
            global TD_actualEnemy2,TD_hp2,TD_firstDone2,TD_enemy2,TD_queue,TD_lvlType,TD_active2
            global TD_subDone,TD_added,TD_added2
            TD_circs = []
            TD_queue = []
            TD_pathCords = []
            TD_guards = []
            TD_guardRects = []
            TD_guardSubRects = []
            TD_consoleRects = []
            TD_enemies = []
            TD_friends = []
            TD_consoleActiveRect = ""
            TD_added = False
            TD_added2 = False
            TD_time = ""
            TD_wdthStart = size_w/4.9
            TD_hghtStart = size_h/1.63
            TD_wdthStart2 = size_w/4.9
            TD_hghtStart2 = size_h/1.63
            TD_firstDone = False
            TD_firstDone2 = False
            TD_done = False
            TD_subDone = False
            TD_enemy = None
            TD_enemy2 = None
            TD_actualEnemy2 = None
            TD_active = []  
            TD_active2 = []
            TD_iterator = 1   
            TD_round = 1
            TD_hp = size_w/19 
            TD_hp2 = size_w/19 
            TD_consoleShown = False
            if not activeMenu:
                course.tower_defence.drawMap()
        def console():
            global TD_consoleShown

            btnColor = TD_darkGray
            txtColor = lt_gray
            if TD_consoleShown:
                global TD_consoleRects,TD_consoleActiveRect,activeWriting,text,TD_consoleTxts,TD_consoleOK
                global iterator,TD_count
                pygame.event.set_allowed(MOUSEMOTION)
                pygame.event.set_allowed(KEYDOWN)
                pygame.event.set_allowed(KEYUP)
                btnColor = TD_darkGreen
                txtColor = TD_darkGreen

                bckgr = pygame.draw.rect(screen, color1, [size_w/3.83,size_h/5.69,size_w/1.8,size_h/1.27], 0,size_w//450)
                border = pygame.draw.rect(screen, color3, [size_w/3.83,size_h/5.69,size_w/1.8,size_h/1.27], size_w//450,size_w//450)
                backBtn = pygame.draw.rect(screen, color1, [size_w/4.35,size_h/3.75,size_w/30,size_h/6], 0,size_w//450)
                backBtnBord = pygame.draw.rect(screen, color3, [size_w/4.35,size_h/3.75,size_w/30,size_h/6], size_w//450,size_w//450)
                backBtnTxt = Write(round(size_w//100*2),"<",color3,[size_w/4.07,size_h/2.86])
                applyBtn = course.centeredBtn(1.21,dark_green,"Apply")

                hght = size_h/4.44
                wrongAnswers = 0
                for it in range(4):
                    rect = pygame.draw.rect(screen, color2, [size_w/3.7,hght,size_w/1.88,size_h/8], 0,size_w//50)
                    TD_consoleRects.append(rect)
                    try:
                        firstLineOK = TD_consoleTxts[it].upper() in ["IF ENEMY:","IF FRIEND:"]
                        commandsOK = TD_consoleTxts[it].upper() in ["ATTACK()","WAIT()"]
                        thirdLineOK = TD_consoleTxts[it].upper() in ["ELIF ENEMY:","ELIF FRIEND:","ELSE:"]
                        if it==TD_consoleActiveRect:
                            pygame.draw.rect(screen, lt_gray, [size_w/3.7,hght,size_w/1.88,size_h/8], size_w//450,size_w//50)
                            if it == 0 and firstLineOK:
                                pass
                            elif it == 1 and commandsOK:
                                pass
                            elif it == 2 and thirdLineOK:
                                pass
                            elif it == 3 and commandsOK:
                                pass
                            elif len(TD_consoleTxts[it])<1:
                                pass
                            else:
                                wrongAnswers += 1
                        else:
                            if it == 0 and firstLineOK:
                                pygame.draw.rect(screen, green, [size_w/3.7,hght,size_w/1.88,size_h/8], size_w//450,size_w//50)
                            elif it == 1 and commandsOK:
                                pygame.draw.rect(screen, green, [size_w/3.7,hght,size_w/1.88,size_h/8], size_w//450,size_w//50)
                            elif it == 2 and thirdLineOK:
                                pygame.draw.rect(screen, green, [size_w/3.7,hght,size_w/1.88,size_h/8], size_w//450,size_w//50)
                            elif it == 3 and commandsOK:
                                pygame.draw.rect(screen, green, [size_w/3.7,hght,size_w/1.88,size_h/8], size_w//450,size_w//50)
                            elif len(TD_consoleTxts[it])<1:
                                pygame.draw.rect(screen, dark_gray, [size_w/3.7,hght,size_w/1.88,size_h/8], size_w//450,size_w//50)
                            else:
                                pygame.draw.rect(screen, red, [size_w/3.7,hght,size_w/1.88,size_h/8], size_w//450,size_w//50)
                                wrongAnswers += 1
                    except:
                        pass
                    hght += size_h/7

                if wrongAnswers>0:
                    TD_consoleOK = False
                else:
                    TD_consoleOK = True
                
                try:
                    for it in range(len(TD_consoleTxts)):
                        index = it
                        wdth = TD_consoleRects[index][0] + TD_consoleRects[index][2]/2
                        hght = TD_consoleRects[index][1] + TD_consoleRects[index][3]/2
                        if index != TD_consoleActiveRect:
                            shownTxt = Write(round(size_w//100*2),TD_consoleTxts[index],color2,[wdth,hght])
                            txtRect = shownTxt.get_rect()
                            wdthS = txtRect[0] 
                            startOK = TD_consoleTxts[index-1].upper().startswith("IF") or TD_consoleTxts[index-1].upper().startswith("ELIF") or TD_consoleTxts[index-1].upper().startswith("ELSE")
                            startPoint = size_w/3.38
                            if startOK and TD_consoleTxts[index-1].endswith(":"):
                                startPoint = size_w/3
                            while wdthS>startPoint:
                                wdthS -= size_w/100
                            Write(round(size_w//100*2),TD_consoleTxts[index],color3,[wdthS+txtRect[2]/2,hght])
                        else:
                            shownTxt = Write(round(size_w//100*2),TD_consoleTxts[index],color3,[wdth,hght])
                            txtRect = shownTxt.get_rect()
                            clearBtn = pygame.draw.rect(screen, dark_red, [size_w/1.35,txtRect[1]-size_h/40,size_w/20,size_h/12], 0,size_w//450)
                            clearTxt = Write(round(size_w//100*2),"X",color1,[size_w/1.35+clearBtn[2]/2,hght])
                except:
                    pass

            btnL = pygame.draw.rect(screen, btnColor, [size_w/5,size_h/3.73,size_w/50,size_h/6], 0)
            btnR = pygame.draw.rect(screen, btnColor, [size_w/4.78,size_h/3.73,size_w/50,size_h/6], 0,size_w//450)
            Write(round(size_w//100*2),">",txtColor,[size_w/4.71,size_h/2.83])

            if event.type == MOUSEMOTION:
                try:
                    if applyBtn.collidepoint(mouse_pos):
                        course.centeredBtn(1.21,green,"Apply")
                except:
                    pass
                try:
                    if clearBtn.collidepoint(mouse_pos):
                        clearBtn = pygame.draw.rect(screen, red, [clearBtn[0],clearBtn[1],clearBtn[2],clearBtn[3]], 0,size_w//450)
                        clearTxt = Write(round(size_w//100*2),"X",color3,[clearBtn[0]+clearBtn[2]/2,clearBtn[1]+clearBtn[3]/2])
                except:
                    pass                    
            elif event.type == MOUSEBUTTONDOWN:
                if btnL.collidepoint(mouse_pos) or btnR.collidepoint(mouse_pos):
                    TD_consoleShown = True
                try:
                    if TD_count not in [1,2]:
                        if backBtn.collidepoint(mouse_pos) or applyBtn.collidepoint(mouse_pos):
                            pygame.draw.rect(screen, TD_darkGreen, [size_w/5,size_h/16,size_w/1.5,size_h/1.1],0,10)
                            TD_consoleActiveRect = ""
                            TD_consoleShown = False
                            activeWriting = False
                            text = ""
                            holdIterator = iterator
                            course.tower_defence.reset()
                            iterator = holdIterator
                except:
                    pass
                try:
                    if clearBtn.collidepoint(mouse_pos):
                        TD_consoleTxts[TD_consoleActiveRect] = ""
                except:
                    pass  
                for rect in TD_consoleRects:
                    if rect.collidepoint(mouse_pos):
                        index = TD_consoleRects.index(rect)
                        TD_consoleActiveRect = index
                        activeWriting = True
            elif activeWriting and event.type == KEYDOWN:
                try:
                    if event.key == K_RETURN:
                        if isinstance(TD_consoleActiveRect,int):
                            if TD_consoleActiveRect < 4:
                                TD_consoleActiveRect += 1
                    elif event.key == K_BACKSPACE:
                        TD_consoleTxts[TD_consoleActiveRect] = TD_consoleTxts[TD_consoleActiveRect][:-1]
                    elif len(TD_consoleTxts[TD_consoleActiveRect]) < 25:
                        if keys[K_LSHIFT] or keys[K_RSHIFT]:
                            if event.key==K_9:
                                TD_consoleTxts[TD_consoleActiveRect] += "()"
                            elif event.key==K_8:
                                TD_consoleTxts[TD_consoleActiveRect] += "*"
                            elif event.key==K_7:
                                TD_consoleTxts[TD_consoleActiveRect] += "&"
                            elif event.key==K_6:
                                TD_consoleTxts[TD_consoleActiveRect] += "^"
                            elif event.key==K_5:
                                TD_consoleTxts[TD_consoleActiveRect] += "%"
                            elif event.key==K_4:
                                TD_consoleTxts[TD_consoleActiveRect] += "$"
                            elif event.key==K_3:
                                TD_consoleTxts[TD_consoleActiveRect] += "#"
                            elif event.key==K_2:
                                TD_consoleTxts[TD_consoleActiveRect] += "@"
                            elif event.key==K_1:
                                TD_consoleTxts[TD_consoleActiveRect] += "!"                        
                            elif event.key==K_0:
                                TD_consoleTxts[TD_consoleActiveRect] += ")"
                            elif event.key==K_LEFTBRACKET:
                                TD_consoleTxts[TD_consoleActiveRect] += "["
                            elif event.key == K_RIGHTBRACKET:
                                TD_consoleTxts[TD_consoleActiveRect] += "]"
                            elif event.key == K_QUOTE:
                                TD_consoleTxts[TD_consoleActiveRect] += "\""
                            elif event.key == K_SEMICOLON:
                                TD_consoleTxts[TD_consoleActiveRect] += ":"
                            elif event.key == K_SLASH:
                                TD_consoleTxts[TD_consoleActiveRect] += "?"
                            elif event.key==K_MINUS:
                                TD_consoleTxts[TD_consoleActiveRect] += "_"
                            else:
                                TD_consoleTxts[TD_consoleActiveRect] += chr(event.key)
                        elif keys[K_RALT or K_LALT]:
                            if event.key==K_l:
                                TD_consoleTxts[TD_consoleActiveRect] += "ł"        
                            elif event.key==K_z:
                                TD_consoleTxts[TD_consoleActiveRect] += "ż"   
                        else:
                            if event.key != K_LSHIFT:
                                TD_consoleTxts[TD_consoleActiveRect] += chr(event.key)
                except:
                    pass
        def showUnit(unit,name,txtUnderName):
            pygame.draw.circle(screen, lt_blue, [size_w/1.89,size_h/2.18], size_w/6, 0)
            pygame.draw.circle(screen, logoBlue, [size_w/1.89,size_h/2.18], size_w/6, size_w//100)
            screen.blit(unit,[size_w/2.23,size_h/3.46])
            pygame.draw.rect(screen, logoBlue, [size_w/2.63,size_h/1.55,size_w/3.3,size_h/8], 0,size_w//100)
            WriteItalic(size_w//100*2,name,lt_gray,[size_w/1.89,size_h/1.41])
            if len(txtUnderName) > 0:
                pygame.draw.rect(screen, logoBlue, [size_w/2.77,size_h/1.35,size_w/3,size_h/8], 0,size_w//100)
                WriteItalic(round(size_w//100*3.5),txtUnderName,lt_gray,[size_w/1.91,size_h/1.24])
        def levelLost(text):
            language = getLang()
            pygame.draw.rect(screen, color2, [size_w/3.45,size_h/3.86,size_w/2,size_h/2], 0,size_w//250)
            pygame.draw.rect(screen, color1, [size_w/3.45,size_h/3.86,size_w/2,size_h/2], size_w//250,size_w//250)
            Write(round(size_w//100*2.5),text,red,[size_w/1.9,size_h/2.2])
            if language == "ENG":
                Write(round(size_w//100*5.5),"Lost",red,[size_w/1.88,size_h/2.8])
                Write(round(size_w//100*2),"Click anywhere to restart...",red,[size_w/1.92,size_h/1.63])
            else:
                Write(round(size_w//100*5.5),"Porażka",red,[size_w/1.88,size_h/2.8])
                Write(round(size_w//100*2),"Kliknij gdziekolwiek...",red,[size_w/1.92,size_h/1.63])                
        def handlingFinalLvl():
            global activeMenu,activeLesson,activities,TD_consoleShown
            global TD_count,iterator,courseLvl,TD_btnClicked
            lvlOk = courseLvl == 17
            if activities[0] and not activeMenu and str(activeLesson)[17:-23]=="lesson4" and lvlOk and not TD_consoleShown:
                if TD_count == 2 and iterator < 6:
                    iterator += 2 #7
                elif TD_count == 4 and iterator < 8:
                    iterator += 2 #9
                #if not TD_btnClicked:
                #    course.dialogTop(6.41,"Click anywhere when you're ready","to start final wave",bckgr=False)
    class shooting_range():
        class quiz():
            def start(questionsList,allAnswersList,correctAnswersIndexes):
                global mentorIcon,activeMain,held,courseLvl,notBlocked,iterator,activeMenu,chosen,timer
                global bckgrMusicPlayed,errorShowed,storedItems,storedCords,chosen,selected,storedTime
                global storedTimeValue
                global SR_icons,SR_cords,SR_iterator,SR_holder,SR_holder2
                notBlocked = False
                if len(SR_icons)<1:
                    if isinstance(selected,str):
                        selected = 2
                    try:
                        shoot_shield = pygame.image.load(r"{}/Images/Game/sr/shoot_shield.png".format(dirPath))
                        shoot_shield = pygame.transform.scale(shoot_shield, [int(size_w/14.22),int(size_h/8)])
                        SR_icons.append(shoot_shield)
                    except:
                        errorInit("Failed to load shoot_shield")      
                    try:
                        if selected == 1:
                            iron_sight = pygame.image.load(r"{}/Images/Game/iron_sight.png".format(dirPath))
                            iron_sight = pygame.transform.scale(iron_sight, [int(size_w/3.90),int(size_h/2.19)])
                        elif selected == 2:
                            iron_sight = pygame.image.load(r"{}/Images/Game/iron_sight2.png".format(dirPath))
                            iron_sight = pygame.transform.scale(iron_sight, [int(size_w/2),int(size_h/2.3)])
                        SR_icons.append(iron_sight)
                    except:
                        errorInit("Failed to load iron_sight")
                    try:
                        if selected == 1:
                            iron_sight = pygame.image.load(r"{}/Images/Game/iron_sight_shoot.png".format(dirPath))
                            iron_sight = pygame.transform.scale(iron_sight, [int(size_w/3.90),int(size_h/2.09)])
                        elif selected == 2:
                            iron_sight = pygame.image.load(r"{}/Images/Game/iron_sight2_shoot.png".format(dirPath))
                            iron_sight = pygame.transform.scale(iron_sight, [int(size_w/2),int(size_h/2.19)]) 
                        SR_icons.append(iron_sight)
                    except:
                        errorInit("Failed to load 'iron_sight_shoot.png'",fontSize=1.7)
                    try:
                        mini_iron_sight = pygame.image.load(r"{}/Images/Game/iron_sight.png".format(dirPath))
                        mini_iron_sight = pygame.transform.scale(mini_iron_sight, [int(size_w/25),int(size_h/15)])
                        SR_icons.append(mini_iron_sight)
                    except:
                        errorInit("Failed to load 'mini_iron_sight.png'",fontSize=1.7)
                    try:
                        mini_iron_sight2 = pygame.image.load(r"{}/Images/Game/iron_sight2.png".format(dirPath))
                        mini_iron_sight2 = pygame.transform.scale(mini_iron_sight2, [int(size_w/16),int(size_h/15)])
                        SR_icons.append(mini_iron_sight2)
                    except:
                        errorInit("Failed to load mini_iron_sight2")
                

                questions = questionsList

                allAnswers = allAnswersList

                correctAnswers = correctAnswersIndexes #0-A 1-B 2-C

                if iterator-1<len(questions):
                    timer = round(float(time.process_time()) - storedTimeValue,2)
                    storedTime = timer
                    wdth = size_w/3.12
                    for x in range(3):
                        cord = screen.blit(SR_icons[0],[wdth,size_h/2.34]) 
                        if cord not in SR_cords:
                            SR_cords.append(cord)
                        wdth += size_w/6


                    try:
                        Write(round(size_w//100*2.1),questions[iterator-1],red,[size_w/1.89,size_h/3.96])
                    except:
                        print("questions out of range",iterator)

                    answersBckgr = pygame.draw.rect(screen, color2, [size_w/4.24,size_h/1.75,size_w/1.7,size_h/8], 0)

                    answers = ['A','B','C']
                    for cord in SR_cords:
                        index = SR_cords.index(cord)
                        try:
                            txtwdth = cord[0]+cord[2]/2
                            txthght = cord[1]+cord[3]/2
                            WriteItalic(round(size_w//100*2.5),answers[index],logoBlue,[txtwdth,txthght])
                        except:
                            pass
                        try:
                            Write(round(size_w//100*0.95),allAnswers[iterator-1][index],red,[txtwdth,txthght-size_h/12])
                        except:
                            print("allAnswers out of range")

                    try:
                        for cord in storedCords:
                            pygame.draw.circle(screen,darker_gray,cord,size_w//200)
                    except:
                        pass

                    if 20-SR_iterator > 0:
                        color=green
                    else:
                        color=red

                    Write(round(size_w//100*1.5),f"Ammo: {20-SR_iterator}/20",color,[size_w/1.24,size_h/1.08])
                    Write(round(size_w//100*1.5),f"Points: {SR_holder}",green,[size_w/3.95,size_h/1.08])
                    reloadBtn = pygame.draw.rect(screen, purple, [size_w/2.38,size_h/1.19,size_w/5,size_h/12], 0,size_w//250)
                    reloadTxt = Write(round(size_w//100*2),"Reload",color1,[size_w/1.91,size_h/1.13])

                    if selected == 1:
                        circ_color1 = logoBlue
                        circ_color2 = lt_gray
                    else:
                        circ_color1 = lt_gray
                        circ_color2 = logoBlue

                    precirc1 = pygame.draw.circle(screen, color2, [size_w/2.08,size_h/6.86], size_w//35, size_w//600)
                    screen.blit(SR_icons[3],[precirc1[0]+precirc1[2]/6,precirc1[1]+precirc1[3]/8])
                    circ1 = pygame.draw.circle(screen, circ_color1, [size_w/2.08,size_h/6.86], size_w//35, size_w//600)
                    
                    precirc2 = pygame.draw.circle(screen, color2, [size_w/1.78,size_h/6.86], size_w//35, size_w//600)
                    screen.blit(SR_icons[4],[precirc2[0]-precirc1[2]/20,precirc2[1]+precirc2[3]/8])
                    circ2 = pygame.draw.circle(screen, circ_color2, [size_w/1.78,size_h/6.86], size_w//35, size_w//600)

                    #GUN BLITING
                    try:
                        correctH = mouse_pos[1]<size_h/1.75 and mouse_pos[1]>size_h/7.92
                        correctW = mouse_pos[0]<size_w/1.35 and mouse_pos[0]>size_w/3.07
                        sight_rect = SR_icons[1].get_rect()
                        if correctH and correctW:
                            pygame.mouse.set_visible(False)
                            if selected == 1:
                                cords = [mouse_pos[0]-sight_rect[2]/2.1,mouse_pos[1]-sight_rect[3]/7]
                            elif selected == 2:
                                cords = [mouse_pos[0]-sight_rect[2]/2,mouse_pos[1]-sight_rect[3]/12]
                            screen.blit(SR_icons[1],cords)
                        else:
                            pygame.mouse.set_visible(True)
                    except:
                        pass

                    if event.type == MOUSEMOTION:
                        if reloadBtn.collidepoint(mouse_pos):
                            reloadBtn = pygame.draw.rect(screen, logoBlue, [size_w/2.38,size_h/1.19,size_w/5,size_h/12], 0,size_w//250)
                            reloadBtn = pygame.draw.rect(screen, dark_blue, [size_w/2.38,size_h/1.19,size_w/5,size_h/12], size_w//200,size_w//250)
                            reloadTxt = Write(round(size_w//100*2),"Reload",color3,[size_w/1.91,size_h/1.13]) 
                    elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                        correctH = mouse_pos[1]<size_h/1.87 and mouse_pos[1]>size_h/7.92
                        correctW = mouse_pos[0]<size_w/1.35 and mouse_pos[0]>size_w/3.07
                        if 20-SR_iterator > 0:
                            if correctW and correctH:
                                if selected == 1:
                                    cords = [mouse_pos[0]-sight_rect[2]/2.1,mouse_pos[1]-sight_rect[3]/7]
                                elif selected == 2:
                                    cords = [mouse_pos[0]-sight_rect[2]/2,mouse_pos[1]-sight_rect[3]/12]
                                screen.blit(SR_icons[2],cords)
                                SR_iterator += 1
                                SR_holder2 += 1
                            for cord in SR_cords:
                                index = SR_cords.index(cord)  
                                try:
                                    if cord.collidepoint(mouse_pos):
                                        course.coursorMarked()
                                        storedCords.append([mouse_pos[0],mouse_pos[1]])
                                        if index==correctAnswers[iterator-1]:
                                            SR_holder += 1
                                            Write(round(size_w//100*8),"Correct",green,[size_w/1.94,size_h/2.09])
                                        else:
                                            Write(round(size_w//100*8),"Wrong",red,[size_w/1.94,size_h/2.09])
                                        iterator += 1
                                except:
                                    print("correctAnswers out of range")
                        if reloadBtn.collidepoint(mouse_pos):
                            SR_iterator = 0
                        if circ1.collidepoint(mouse_pos):
                            selected = 1
                            SR_icons.clear()
                        if circ2.collidepoint(mouse_pos):
                            selected = 2
                            SR_icons.clear()
                    elif event.type == KEYDOWN:
                        if event.key == K_r:
                            SR_iterator = 0
                else:
                    pygame.mouse.set_visible(True)
                    WriteItalic(round(size_w/100*2),f"Points: {SR_holder}/{len(questions)}",green,[size_w/1.82,size_h/3.13])
                    WriteItalic(round(size_w/100*2),f"Score: {int(SR_holder/len(questions)*100)}%",green,[size_w/1.82,size_h/2.63])
                    try:
                        if int(len(questions)/SR_holder2*100)>100:
                            WriteItalic(round(size_w/100*2),f"Accuracy: 100%",green,[size_w/1.82,size_h/2.19])
                        else:
                            WriteItalic(round(size_w/100*2),f"Accuracy: {int(len(questions)/SR_holder2*100)}%",green,[size_w/1.82,size_h/2.19])
                    except:
                        pass
                    WriteItalic(round(size_w/100*2),f"Time: {storedTime}s",green,[size_w/1.82,size_h/1.89])
                    if SR_holder==len(questions):
                        course.dialogTop(6.41,"That's a very nice score, actually the best I saw!","Go futher for new challenges, soldier",fontSize=1.3)
                        nextBtn = course.centeredBtn(1.55,dark_green,"Next",adjustToDialog=True)
                    elif SR_holder>len(questions)/2:
                        course.dialogTop(6.41,"Not bad, not bad recruit, but you could do better.","Go futher for new challenges, soldier",fontSize=1.3)
                        nextBtn = course.centeredBtn(1.55,dark_green,"Next",adjustToDialog=True)
                    elif SR_holder<len(questions)/2:
                        course.dialogTop(6.41,"I'm afraid that's bellow average I can accept,","I believe you can do better - try again!",fontSize=1.3)
                        againBtn = course.centeredBtn(1.55,purple,"Try again",adjustToDialog=True)
                    
                    if event.type == MOUSEMOTION:
                        try:
                            if nextBtn.collidepoint(mouse_pos):
                                course.centeredBtn(1.55,green,"",adjustToDialog=True)
                                course.centeredBtn(1.55,dark_green,"Next",adjustToDialog=True,border=size_w//250)
                        except:
                            pass
                        try:
                            if againBtn.collidepoint(mouse_pos):
                                course.centeredBtn(1.55,lt_blue,"",adjustToDialog=True)
                                course.centeredBtn(1.55,logoBlue,"Try again",adjustToDialog=True,border=size_w//250)
                        except:
                            pass
                    elif event.type == MOUSEBUTTONDOWN:
                        try:
                            if nextBtn.collidepoint(mouse_pos):
                                courseLvl += 1
                                iterator = 1
                                SR_iterator = 0
                                SR_holder = 0
                                SR_holder2 = 0
                                storedCords.clear()
                                SR_icons.clear()
                                storedTimeValue += storedTime
                                storedTime = ""                                
                        except:
                            pass
                        try:
                            if againBtn.collidepoint(mouse_pos):
                                iterator = 1
                                SR_iterator = 0
                                SR_holder = 0
                                SR_holder2 = 0
                                storedCords.clear()
                                SR_icons.clear()
                                storedTimeValue += storedTime
                                storedTime = ""
                        except:
                            pass           
        def loopExample():
            global held,courseLvl,iterator,activeMenu,chosen
            global errorShowed,storedItems,storedCords,chosen,selected
            if activities[0] :
                if not activeMenu and str(activeLesson)[17:-23]=="lesson5" and not errorShowed and courseLvl==10:
                    pygame.draw.rect(screen, color2, [size_w/3.05,size_h/1.43,size_w/7.6,size_h/20], 0)
                    if selected == 1:
                        if getActualSecond()%0.5==0:
                            WriteItalic(round(size_w/100*2.2),"Working",green,[size_w/2.54,size_h/1.38])
                        else:
                            WriteItalic(round(size_w/100*2),"Working",dark_green,[size_w/2.54,size_h/1.38])
                    else:
                        WriteItalic(round(size_w/100*2),"Not Working",dark_red,[size_w/2.54,size_h/1.38])  
                    pygame.draw.rect(screen, color2, [size_w/1.47,size_h/1.43,size_w/7.6,size_h/20], 0)
                    if chosen == 1:
                        if getActualSecond()%0.5==0:
                            WriteItalic(round(size_w/100*2.2),"Working",green,[size_w/1.34,size_h/1.38])
                        else:
                            WriteItalic(round(size_w/100*2),"Working",dark_green,[size_w/1.34,size_h/1.38]) 
                    else:
                        WriteItalic(round(size_w/100*2),"Not Working",dark_red,[size_w/1.34,size_h/1.38])               
        def continueTimer():
            global mentorIcon,activeMain,held,courseLvl,notBlocked,iterator,activeMenu,done
            global bckgrMusicPlayed,errorShowed,storedItems,storedCords,chosen,selected,storedTime
            if activities[0]:
                if not activeMenu and str(activeLesson)[17:-23]=="lesson5" and not errorShowed and courseLvl==13: 
                    try:  
                        if isinstance(selected,int):
                            color = dark_green
                        else:
                            color = green
                        timer = round(float(time.process_time()) - storedTime,1)
                        pygame.draw.rect(screen, color2, [size_w/2.3,size_h/3.37,size_w/5,size_h/10], width=0)
                        iterator = str(timer)[:-2]
                        Write(round(size_w//100*2.5),f"Iterator: {iterator}",color,[size_w/1.85,size_h/2.82])  
                    except:
                        pass  
        def drawingCircles():
            global storedTime,activities,activeLesson,errorShowed,courseLvl,storedTimeValue,storedCords
            global iterator,done,notBlocked
            if activities[0]:
                if not activeMenu and str(activeLesson)[17:-23]=="lesson6" and not errorShowed:
                    if courseLvl == 7:
                        cords = [
                            [size_w/2.73,size_h/1.64],
                            [size_w/2.09,size_h/1.64],
                            [size_w/1.7,size_h/1.64],
                            [size_w/1.47,size_h/1.64]
                        ]
                        circColor = [green,orange,red,purple]
                        if not done:
                            storedTimeValue = round(float(time.process_time()),1)
                            done = True
                        storedTime = round(float(time.process_time())-storedTimeValue,1)

                        if storedTime>0.5:
                            iterator = 0
                            pygame.draw.circle(screen, circColor[0], cords[0], size_w//30, width=0)
                        if storedTime>1:
                            iterator = 1
                            pygame.draw.circle(screen, circColor[1], cords[1], size_w//30, width=0)
                        if storedTime>1.5:
                            iterator = 2
                            pygame.draw.circle(screen, circColor[2], cords[2], size_w//30, width=0)
                        if storedTime>2:
                            iterator = 3
                            pygame.draw.circle(screen, circColor[3], cords[3], size_w//30, width=0)
                            notBlocked = True
                        if storedTime>0.5 and storedTime < 2.2:
                            Write(round(size_w//100*3),"circle",color3,[cords[iterator][0],size_h/1.39])
                        if storedTime < 2.2:
                            pygame.event.post(pygame.event.Event(pygame.KEYDOWN))  
        def clearVars():
            global SR_cords,SR_holder,SR_holder2,SR_icons,SR_iterator
            SR_cords.clear()
            SR_icons.clear()
            SR_holder = 0
            SR_holder2 = 0
            SR_iterator = 0
        def rangeOfRects():
            global activities,activeMenu,activeLesson,errorShowed,courseLvl,done,storedTime,storedTimeValue
            global notBlocked
            if activities[0]:
                if not activeMenu and str(activeLesson)[17:-23]=="lesson6" and not errorShowed and courseLvl == 16 and done:                
                    storedTime = round(float(time.process_time())-storedTimeValue,1)
                    pygame.draw.rect(screen, color2, [size_w/2.69,size_h/3.1,size_w/6,size_h/20], 0)
                    opt1 = Write(round(size_w//100*1.5),"Full",color3,[size_w/2.21,size_h/2.92])
                    wdth = size_w/2.69
                    hght = size_h/2.6
                    for x in range(3):
                        for x in range(5):
                            pygame.draw.rect(screen, green, [wdth,hght,size_w/40,size_h/30], 0)
                            wdth += size_w/30
                        wdth = size_w/2.69
                        hght += size_h/20
                    
                    if storedTime >1.0:
                        pygame.draw.rect(screen, color2, [size_w/1.72,size_h/3.12,size_w/6,size_h/20], 0)
                        opt2 = Write(round(size_w//100*1.5),"Range(10)",color3,[size_w/1.51,size_h/2.92])
                        wdth = size_w/1.73
                        hght = size_h/2.6
                        for x in range(2):
                            for x in range(5):
                                pygame.draw.rect(screen, green, [wdth,hght,size_w/40,size_h/30], 0)
                                wdth += size_w/30
                            wdth = size_w/1.73
                            hght += size_h/20

                    if storedTime >1.5:
                        pygame.draw.rect(screen, color2, [size_w/2.69,size_h/1.74,size_w/6,size_h/20], 0)
                        opt3 = Write(round(size_w//100*1.5),"Range(3,10)",color3,[size_w/2.21,size_h/1.67])
                        wdth = size_w/2.69
                        hght = size_h/1.57
                        for x in range(2):
                            for y in range(5):
                                if x == 0 and y < 3:
                                    pass
                                else:
                                    pygame.draw.rect(screen, green, [wdth,hght,size_w/40,size_h/30], 0)
                                wdth += size_w/30
                            wdth = size_w/2.69
                            hght += size_h/20
                    
                    if storedTime >2.0:
                        pygame.draw.rect(screen, color2, [size_w/1.72,size_h/1.74,size_w/6,size_h/20], 0)
                        opt4 = Write(round(size_w//100*1.5),"Range(0,10,2)",color3,[size_w/1.51,size_h/1.67])
                        wdth = size_w/1.73
                        hght = size_h/1.57
                        for x in range(2):
                            for y in range(5):
                                if x == 0 and y%2==0:
                                    pass
                                elif x == 1 and y%2==1:
                                    pass
                                else:
                                    pygame.draw.rect(screen, green, [wdth,hght,size_w/40,size_h/30], 0)
                                wdth += size_w/30
                            wdth = size_w/1.73
                            hght += size_h/20
                        notBlocked = True
        def counting():
            global iterator,activities,errorShowed,activeMain,activeMenu,done,storedTimeValue
            if activities[0] and not errorShowed and not activeMenu:
                if str(activeLesson)[17:-23]=="lesson6" and (courseLvl in [20,22]): 
                    if done or courseLvl == 22: 
                        iterator = int(float(time.process_time())-storedTimeValue)
                        pygame.draw.rect(screen, color2, [size_w/2.02,size_h/1.93,size_w/20,size_h/20], 0)
                        Write(round(size_w//100*2.5),iterator,red,[size_w/1.92,size_h/1.82])
                        if iterator%51==0 and iterator > 49:
                            storedTimeValue = round(float(time.process_time()),1)
        def doubleForRectDraw():
            global activities,activeMenu,activeLesson,errorShowed,courseLvl,storedTimeValue,notBlocked
            global SR_holder,SR_holder2
            if activities[0]: 
                if not activeMenu and str(activeLesson)[17:-23]=="lesson6" and not errorShowed:
                    if courseLvl == 24:
                        if not isinstance(SR_holder,int):
                            SR_holder = 0
                        if not isinstance(SR_holder2,int):
                            SR_holder2 = 0

                        if SR_holder2 > 4 and SR_holder2%5==0:
                            storedTimeValue = round(float(time.process_time()),1)
                            if SR_holder <= 4:
                                SR_holder += 1
                        
                        if SR_holder <= 4:
                            SR_holder2 = int(float(time.process_time())-storedTimeValue)

                        pygame.draw.rect(screen, color2, [size_w/1.38,size_h/2.15,size_w/8,size_h/10], 0)
                        pygame.draw.rect(screen, color2, [size_w/1.38,size_h/1.57,size_w/8,size_h/10], 0)
                        if SR_holder <= 4:
                            Write(round(size_w//100*2.2),f"Round: {SR_holder}",red,[size_w/1.27,size_h/1.92])
                            Write(round(size_w//100*2.2),f"Round: {SR_holder2}",red,[size_w/1.27,size_h/1.45])
                            notBlocked = False
                        else:
                            Write(round(size_w//100*2.2),"Ended",red,[size_w/1.27,size_h/1.92])
                            Write(round(size_w//100*2.2),"Ended",red,[size_w/1.27,size_h/1.45]) 
                            notBlocked = True                       
                        
                        wdth = size_w/2.18
                        hght = size_h/5.49
                        for x in range(SR_holder+1):
                            if x == 5:
                                for x in range(5):
                                    pygame.draw.rect(screen, color2, [wdth,hght,size_w/45,size_h/30], 0)
                                    wdth += size_w/35                            
                            elif x<SR_holder:
                                for x in range(5):
                                    pygame.draw.rect(screen, green, [wdth,hght,size_w/45,size_h/30], 0)
                                    wdth += size_w/35
                            else:
                                for x in range(SR_holder2):
                                    pygame.draw.rect(screen, green, [wdth,hght,size_w/45,size_h/30], 0)
                                    wdth += size_w/35
                            wdth = size_w/2.18
                            hght += size_h/25
    def startScreen():
        global activeAny,activeLesson,activeMenu,wait,storedTime

        if activities[0] and activeMenu:
            pygame.draw.rect(screen, color2, [size_w/5,size_h/16,size_w/1.5,size_h/1.1],0,10)

            permitions = getCourseLvl()
            line1 = permitions >= 4
            line2 = permitions >= 7
            line3 = permitions >= 9

            lines = [line1,line2,line3]
            colors = []
            linePoint = [size_w/4.43,size_w/2.46,size_w/1.74]
            wToAdd = size_w/12.5
            lineHeight = []
            for x in range(3):
                if lines[x]:
                    colors.append(green)
                else:
                    colors.append(dark_green)

            lineH = size_h/4.5
            for x in range(3):
                firstmainLine = pygame.draw.line(screen, colors[x], [size_w/4.5,lineH], [size_w/1.2,lineH], size_w//168) 
                secondmainLine = pygame.draw.line(screen, colors[x], [size_w/4.5,lineH-size_h/15], [size_w/4.5,lineH+size_h/15], size_w//168)  
                thirdmainLine = pygame.draw.line(screen, colors[x], [size_w/1.2,lineH-size_h/15], [size_w/1.2,lineH+size_h/15], size_w//168) 
                lineHeight.append(lineH)
                lineH += size_h//3.5

            for line in lines:
                if not line:
                    trueCount = lines.count(True)
                    index = (getCourseLvl()-3*trueCount)-1
                    firstGreenLine = pygame.draw.line(screen, green, [linePoint[index],lineHeight[3-lines.count(False)]], [linePoint[index]+wToAdd,lineHeight[3-lines.count(False)]], size_w//168) 
                    leftBorderLine = pygame.draw.line(screen, green, [size_w/4.5,lineHeight[3-lines.count(False)]-size_h/15], [size_w/4.5,lineHeight[3-lines.count(False)]+size_h/15], size_w//168)
                    if index>0:
                        secondGreenLine = pygame.draw.line(screen, green, [linePoint[index-1],lineHeight[3-lines.count(False)]], [linePoint[index-1]+wToAdd,lineHeight[3-lines.count(False)]], size_w//168) 
                        if index == 2:
                            thirdGreenLine = pygame.draw.line(screen, green, [linePoint[index-2],lineHeight[3-lines.count(False)]], [linePoint[index-2]+wToAdd,lineHeight[3-lines.count(False)]], size_w//168)


            circleW = size_w/2.8
            circleH = size_h/4.5
            global circles,circlesCords
            circles = []
            circlesCords = []
            it=1

            for x in range(3):
                for x in range(3):
                    if it>getCourseLvl():
                        circle = pygame.draw.circle(screen, dark_gray, [circleW,circleH], size_w//20, 0)
                    else:
                        circle = pygame.draw.circle(screen, green, [circleW,circleH], size_w//20, 0)
                    pygame.draw.circle(screen, dark_green, [circleW,circleH], size_w//20, 3)
                    circleNr = Write(size_w//100*3,it,color1,[circleW,circleH])
                    circles.append(circle)
                    circlesCords.append([circleW,circleH])
                    circleW += size_w/6
                    it += 1
                circleW = size_w/2.8
                circleH += size_h//3.5
            isCorrectActivity()

        if pygame.event.get_blocked(MOUSEMOTION):
            pygame.event.set_allowed(MOUSEMOTION)

        if event.type == MOUSEMOTION and activities[0] and activeMenu:
            lineH = size_h/4.5
            for x in range(3):
                firstmainLine = pygame.draw.line(screen, colors[x], [size_w/4.5,lineH], [size_w/1.2,lineH], size_w//168) 
                secondmainLine = pygame.draw.line(screen, colors[x], [size_w/4.5,lineH-size_h/15], [size_w/4.5,lineH+size_h/15], size_w//168)  
                thirdmainLine = pygame.draw.line(screen, colors[x], [size_w/1.2,lineH-size_h/15], [size_w/1.2,lineH+size_h/15], size_w//168) 
                lineH += size_h//3.5
            for line in lines:
                if not line:
                    trueCount = lines.count(True)
                    index = (getCourseLvl()-3*trueCount)-1
                    firstGreenLine = pygame.draw.line(screen, green, [linePoint[index],lineHeight[3-lines.count(False)]], [linePoint[index]+wToAdd,lineHeight[3-lines.count(False)]], size_w//168) 
                    leftBorderLine = pygame.draw.line(screen, green, [size_w/4.5,lineHeight[3-lines.count(False)]-size_h/15], [size_w/4.5,lineHeight[3-lines.count(False)]+size_h/15], size_w//168)
                    if index>0:
                        secondGreenLine = pygame.draw.line(screen, green, [linePoint[index-1],lineHeight[3-lines.count(False)]], [linePoint[index-1]+wToAdd,lineHeight[3-lines.count(False)]], size_w//168)
                        if index == 2:
                            thirdGreenLine = pygame.draw.line(screen, green, [linePoint[index-2],lineHeight[3-lines.count(False)]], [linePoint[index-2]+wToAdd,lineHeight[3-lines.count(False)]], size_w//168)
            it = 1
            if getLang() == "ENG":
                courseOpts = ["Start","Vars","Lists","If/Else","While","For","Functs","Class","Files"]
            else:
                courseOpts = ["Start","Zmienne","Listy","If/Else","While","For","Funkcje","Klasy","Pliki"]
            for circle in circles:
                index = circles.index(circle)
                if circle.collidepoint(mouse_pos):   
                    pygame.draw.circle(screen, green, circlesCords[index], size_w//20, 0)
                    pygame.draw.circle(screen, dark_green, circlesCords[index], size_w//20, size_w//450)
                    if getLang() == "PL" and it == 2:
                        Write(round(size_w//100*1.5),courseOpts[it-1],color1,circlesCords[index])
                    else:
                        Write(size_w//100*2,courseOpts[it-1],color1,circlesCords[index])
                else:
                    if index<getCourseLvl():
                        pygame.draw.circle(screen, green, circlesCords[index], size_w//20, 0)
                    else:
                        pygame.draw.circle(screen, dark_gray, circlesCords[index], size_w//20, 0)
                    pygame.draw.circle(screen, dark_green, circlesCords[index], size_w//20, size_w//450)
                    Write(size_w//100*3,it,color1,circlesCords[index])
                it += 1
        elif event.type == MOUSEBUTTONDOWN and activities[0] and activeMenu:
            it = 1
            lessons = [course.lesson1,course.lesson2,course.lesson3,course.lesson4,course.lesson5,course.lesson6,course.lesson7,course.lesson8,course.lesson9]
            for circle in circles:
                index2 = circles.index(circle)
                if circle.collidepoint(mouse_pos) and index2<getCourseLvl():  
                    courseMenu = False
                    activeLesson = lessons[index2]
                    activeMenu = False
                elif circle.collidepoint(mouse_pos) and index2>=getCourseLvl():
                    wait = True
                    storedTime = getActualSecond()
                it += 1 
        if wait:   
            if getLang() == "ENG":
                Write(round(size_w//100*2.5),"Finish previous lessons before that!",color3,[size_w/1.91,size_h/2.75])
            else:
                Write(round(size_w//100*2.5),"Najpierw ukończ poprzednie lekcje!",color3,[size_w/1.91,size_h/2.75])
            if getActualSecond()-storedTime > 0.8:
                wait = False
    def standardLessonEvents(lesson,maxLvl,condition=True,bckgr=True,standard=True,customCol=""):
        global activeMenu,courseLvl,activeLesson,selected,chosen,inFight,notBlocked,loadingBar
        global hp1,hp2,loadingBar,storedCords,storedTime,TD_circs,bckgrMusicPlayed,SR_icons
        global iterator,done,maxCourseLvl,admin
        actualLesson = str(activeLesson)[17:-23]
        if not activeMenu and activities[0] and actualLesson==lesson:
            maxCourseLvl = maxLvl
            bckgrMusicPlayed = True
            if bckgr:
                if loadingBar:
                    pass
                elif standard:
                    pygame.draw.rect(screen, color2, [size_w/5,size_h/16,size_w/1.5,size_h/1.1],0,10)
                else:
                    pygame.draw.rect(screen, customCol, [size_w/5,size_h/16,size_w/1.5,size_h/1.1],0,10)


            menuBtn = pygame.draw.rect(screen, dark_green, [size_w/4.93,size_h/15.04,size_w/10,size_h/10], 0,30)
            menuTxt = Write(size_w//100*2,"Menu",color3,[size_w/3.95,size_h/8.54])
            
            if courseLvl != maxLvl and notBlocked==True:
                if standard:
                    nextBtn = pygame.draw.rect(screen, color2, [size_w/1.45,size_h/1.25,size_w/8,size_h/8], 0,30)
                else:
                    nextBtn = pygame.draw.rect(screen, customCol, [size_w/1.45,size_h/1.25,size_w/8,size_h/8], 0,30)
                nextArrow = Write(size_w//100*4,"->",color3,[size_w/1.33,size_h/1.16]) 
            if courseLvl != 1:
                if standard:
                    backBtn = pygame.draw.rect(screen, color2, [size_w/4.56,size_h/1.25,size_w/8,size_h/8], 0,30)
                else:
                    backBtn = pygame.draw.rect(screen, customCol, [size_w/4.56,size_h/1.25,size_w/8,size_h/8], 0,30)
                backArrow = Write(size_w//100*4,"<-",color3,[size_w/3.59,size_h/1.16]) 
            if admin:
                Write(round(size_w//100*1.5),"{}/{}".format(courseLvl,maxLvl),color3,[size_w/1.19,size_h/11.53])


            if event.type == MOUSEMOTION:
                if menuBtn.collidepoint(mouse_pos):
                    menuBtn = pygame.draw.rect(screen, green, [size_w/4.93,size_h/15.04,size_w/10,size_h/10], 0,30)
                    pygame.draw.rect(screen, dark_green, [size_w/4.93,size_h/15.04,size_w/10,size_h/10], size_w//168,30)
                    menuTxt = Write(size_w//100*2,"Menu",color3,[size_w/3.95,size_h/8.54]) 
                try:
                    if nextBtn.collidepoint(mouse_pos) and courseLvl != maxLvl and notBlocked == True:
                        nextArrow = Write(size_w//100*4,"->",color1,[size_w/1.33,size_h/1.16])    
                except:
                    pass
                try:
                    if backBtn.collidepoint(mouse_pos) and courseLvl != 1:
                        backArrow = Write(size_w//100*4,"<-",color1,[size_w/3.59,size_h/1.16])  
                except:
                    pass 
            elif event.type == MOUSEBUTTONDOWN:
                if menuBtn.collidepoint(mouse_pos):
                    courseLvl = 1
                    bckgrMusicPlayed = False
                    if bckgr:
                        pygame.draw.rect(screen, color2, [size_w/5,size_h/16,size_w/1.5,size_h/1.1],0,10)
                    course.startScreen()
                    activeMenu = True 
                    chosen = "" 
                    selected = ""  
                    storedTime = ""
                    inFight = False 
                    loadingBar = False
                    notBlocked = True
                    done = False
                    hp1 = size_w/2.66
                    hp2 = size_w/6
                    iterator = 1
                    storedCords = []
                    course.shooting_range.clearVars()
                    course.tower_defence.reset()
                    course.tower_defence.clearAdminTools()
                    course.eventsReset()
                    pygame.mouse.set_visible(True)
                try:
                    if nextBtn.collidepoint(mouse_pos): 
                        if courseLvl<maxLvl and condition:
                            courseLvl += 1 
                            selected = ""  
                        storedTime = getActualSecond() 
                except:
                    pass
                try:
                    if backBtn.collidepoint(mouse_pos) and courseLvl > 1:
                        iterator = 1
                        courseLvl -=1
                        selected = ""
                        SR_icons.clear()
                        notBlocked = True
                except:
                    pass
                print("LVL",courseLvl) 
    def dialogStandard(hStart,*args,big=False,fontSize=2,iconH=2.1,rectH=3):
        try:
            if size_w < 1890:
                screen.blit(mentorIcon,[size_w/2.72,size_h/iconH])
            else:
                screen.blit(mentorIcon,[size_w/2.9,size_h/iconH])
        except:
            print("dialogStandard() blit error")
        width = size_w/1.57
        hMinus = size_h/18.3
        pygame.draw.rect(screen, color1, [size_w/2.12,size_h/rectH,size_w/3,size_h/14*len(args)], size_w//200,30)
        height = size_h/hStart
        for arg in args:
            WriteItalic(round(size_w//100*fontSize),arg,color3,[width,height])
            height += hMinus
    def dialogTop(hStart,*args,bckgr=False,fontSize=1.5):
                try:    
                    if size_w < 1890:
                        screen.blit(mentorIcon,[size_w/3.5,size_h/10])
                    else:
                        screen.blit(mentorIcon,[size_w/3.5,size_h/10])   
                except:
                    print("dialogTop() icon blit error")
                if bckgr:
                    pygame.draw.rect(screen, color2, [size_w/2.57,size_h/9,size_w/3,size_h/12*len(args)], 0,30) 
                pygame.draw.rect(screen, color1, [size_w/2.57,size_h/9,size_w/3,size_h/12*len(args)], size_w//200,30)
                hMinus = size_h/14.1
                height = size_h/hStart    
                for arg in args:  
                    WriteItalic(round(size_w//100*fontSize),arg,color3,[size_w/1.82,height]) 
                    height += hMinus
    def coursorMarked():
        mw = mouse_pos[0]
        mh = mouse_pos[1]          
        pygame.draw.line(screen, red, [mw+size_w/200,mh+size_h/200], [mw+size_w/100,mh+size_h/100], size_w//500)    
        pygame.draw.line(screen, red, [mw-size_w/200,mh+size_h/200], [mw-size_w/100,mh+size_h/100], size_w//500) 
        pygame.draw.line(screen, red, [mw+size_w/200,mh-size_h/200], [mw+size_w/100,mh-size_h/100], size_w//500) 
        pygame.draw.line(screen, red, [mw-size_w/200,mh-size_h/200], [mw-size_w/100,mh-size_h/100], size_w//500)   
    def itemChooseGame(text,iconsList,valueName,valueList,goodIndex):
        global selected,iterator
        Write(round(size_w//100*1.5),text,color3,[size_w/1.8,size_h/7])
        weapons = iconsList 
        damage = valueList 
        rects = []
        wdth = size_w/3.2
        Rwdth = size_w/3.5
        Txtwdth = size_w/2.8
        height = size_h/1.9
        for weapon in weapons:
            index = weapons.index(weapon)
            rect = pygame.draw.rect(screen, color1, [Rwdth,size_h/5,size_w/7,size_h/4], 0,15)
            confirmBtn = pygame.draw.rect(screen, color2, [size_w/2.29,size_h/1.35,size_w/7,size_h/10], 0,15)
            if index == selected:
                pygame.draw.rect(screen, color3, [Rwdth,size_h/5,size_w/7,size_h/4], size_w//270,15)
            elif selected == "OK":
                pygame.draw.rect(screen, dark_green, [size_w/1.9,size_h/1.35,size_w/20,size_h/10], 0,15)
                pygame.draw.line(screen, green, [size_w/1.86,size_h/1.31], [size_w/1.82,size_h/1.23], size_w//300)
                pygame.draw.line(screen, green, [size_w/1.82,size_h/1.23], [size_w/1.78,size_h/1.28], size_w//300)
            try:
                if selected>=0:
                    confirmBtn = pygame.draw.rect(screen, dark_green, [size_w/2.14,size_h/1.35,size_w/7,size_h/10], 0,15)
                    if getLang() == "ENG":
                        Write(round(size_w//100*1.5),"Confirm",color1,[size_w/1.86,size_h/1.26])
                    else:
                        Write(round(size_w//100*1.5),"Potwierdź",color1,[size_w/1.86,size_h/1.26])
            except:
                pass
            rects.append(rect)
            pygame.draw.rect(screen, color1, [Rwdth,size_h/2.1,size_w/7,size_h/10], 0,15)
            Write(round(size_w//100*1.5),"{}: {}".format(valueName,damage[index]),color3,[Txtwdth,height])
            screen.blit(weapon,[wdth,size_h/4.46])
            wdth += size_w/5
            Rwdth += size_w/5
            Txtwdth += size_w/5

            if event.type == MOUSEBUTTONDOWN and selected != "OK":
                for rect in rects:
                    index = rects.index(rect)
                    if rect.collidepoint(mouse_pos):
                        selected = index
                try:
                    if confirmBtn.collidepoint(mouse_pos) and selected >=0:
                        if selected == goodIndex:
                            iterator += 1
                            selected = "OK"
                        else:
                            pygame.draw.rect(screen, dark_red, [size_w/2.14,size_h/1.35,size_w/7,size_h/10], 0,15)
                except:
                    pass
            elif event.type == MOUSEMOTION:
                try:
                    if confirmBtn.collidepoint(mouse_pos) and selected >=0:
                        confirmBtn = pygame.draw.rect(screen, green, [size_w/2.14,size_h/1.35,size_w/7,size_h/10], 0,15)
                        if getLang() == "ENG":
                            Write(round(size_w//100*1.5),"Confirm",color1,[size_w/1.86,size_h/1.26])
                        else:
                            Write(round(size_w//100*1.5),"Potwierdź",color1,[size_w/1.86,size_h/1.26])
                except:
                    pass
    def gameQuestion(question,answers,goodAnswerIndex,fontSize=2):
        global activeMain,hp2,iterator,storedTime,soundEnabled
        pygame.draw.rect(screen, color1, [size_w/3.7,size_h/4.05,size_w/2,size_h/2], 0,10)
        pygame.draw.rect(screen, color2, [size_w/1.62,size_h/1.24,size_w/5.5,size_h/15], width=0)
        dmg = int((size_w/50)/hp2*100)
        if getLang() == "ENG":
            Write(round(size_w//100*1),f"Attack will take {dmg}% of your HP",red,[size_w/1.41,size_h/1.21])
            Write(round(size_w//100*1.5),"Enemy attacking, answer question to block",color3,[size_w/1.93,size_h/3.31])
        else:
            Write(round(size_w//100*1),f"Atak zabierze {dmg}% aktualnego życia",red,[size_w/1.41,size_h/1.21])
            Write(round(size_w//100*1.5),"Wróg atakuje, odpowiedz na pytanie by zablokować",color3,[size_w/1.93,size_h/3.31])
        Write(round(size_w//100*fontSize),question,color3,[size_w/1.93,size_h/2.4])
        if len(answers) > 3:
            raise ValueError("gameQuestion max answer capability is 3")
        wdth = size_w/2.59
        rectWdth = size_w/3.05
        rects = []
        wdths = []
        for answer in answers:
            rect = pygame.draw.rect(screen, color2, [rectWdth,size_h/1.98,size_w/9,size_h/15],0,15)
            rects.append(rect)
            wdths.append(wdth)
            Write(round(size_w//100*1.5),answer,color1,[wdth,size_h/1.85])
            wdth += size_w/8
            rectWdth += size_w/8
        wdth = size_w/2.59
        if event.type == MOUSEMOTION:
            for rect in rects:
                index = rects.index(rect)
                if rect.collidepoint(mouse_pos):
                    Write(round(size_w//100*1.5),answers[index],color3,[wdths[index],size_h/1.85])
            wdth += size_w/8  
        if event.type == MOUSEBUTTONDOWN:
            for rect in rects:
                index = rects.index(rect)
                if rect.collidepoint(mouse_pos):
                    if index == goodAnswerIndex:
                        activeMain = True
                        iterator += 1
                        if soundEnabled:
                            pygame.mixer.music.load(f"{dirPath}/Music/shield_impact.ogg")
                            pygame.mixer.music.play(1)
                    elif index != goodAnswerIndex:
                        hp2 -= size_w/50
                        activeMain = True
                        iterator += 1
                        if soundEnabled:
                            pygame.mixer.music.load(f"{dirPath}/Music/ouch.ogg")
                            pygame.mixer.music.play(1)
            wdth += size_w/8     
    def consoleGame(textToShow,goodAnswer,btnText="Attack",fontSize=2.5,textLen=23,multipleAnswers=False,answersList=[],fontSize2=2):
        global text,activeMain,iterator,keys
        print(activeMain)
        pygame.draw.rect(screen, color2, [size_w/3.11,size_h/14,size_w/2.6,size_h/10], 0)
        Write(round(size_w//100*1.4),textToShow,color3,[size_w/1.94,size_h/8.99])
        rect = pygame.draw.rect(screen, color1, [size_w/3.11,size_h/6.3,size_w/2.6,size_h/6], 0,15)
        confirmBtn = pygame.draw.rect(screen, dark_green, [size_w/1.36,size_h/5.3,size_w/8,size_h/8], 0,15)
        Write(size_w//100*2,btnText,color1,[size_w/1.25,size_h/4])
        if activeMain:
            pygame.draw.rect(screen, color2, [size_w/3,size_h/5.8,size_w/2.8,size_h/8], size_w//450,15) 
            Write(round(size_w//100*fontSize),text+"|", color2, [size_w/1.95,size_h/4.1])  
        else:
            pygame.draw.rect(screen, color3, [size_w/3,size_h/5.8,size_w/2.8,size_h/8], size_w//450,15) 
            Write(round(size_w//100*fontSize2),text+"|", color3, [size_w/1.95,size_h/4.1])     
        if event.type == MOUSEBUTTONDOWN:
            if rect.collidepoint(mouse_pos):
                activeMain = False
            else:
                activeMain = True
            if activeMain:
                if confirmBtn.collidepoint(mouse_pos):
                    if multipleAnswers:
                        for answer in answersList:
                            if text.lower().replace(" ","") == answer.lower().replace(" ",""):
                                text = ""
                                iterator += 1
                    else:
                        if text.lower().replace(" ","") == goodAnswer.lower().replace(" ",""):
                            text = ""
                            iterator += 1
        elif event.type == MOUSEMOTION:
            if confirmBtn.collidepoint(mouse_pos):
                pygame.draw.rect(screen, green, [size_w/1.36,size_h/5.3,size_w/8,size_h/8], 0,15)
                pygame.draw.rect(screen, dark_green, [size_w/1.36,size_h/5.3,size_w/8,size_h/8], size_w//450,15)
                Write(size_w//100*2,btnText,color3,[size_w/1.25,size_h/4])
        elif event.type == KEYDOWN and not activeMain:
            if event.key == pygame.K_BACKSPACE and not activeMain:
                try:
                    text=text[:-1]                      
                except:
                    pass
            if event.key == pygame.K_RETURN:
                if multipleAnswers:
                    for answer in answersList:
                        if text.lower().replace(" ","") == answer.lower().replace(" ",""):
                            text = ""
                            iterator += 1
                            activeMain = True
                else:
                    if text.lower().replace(" ","") == goodAnswer.lower().replace(" ",""):
                        text = ""
                        iterator += 1
                        activeMain = True
            elif len(text) < textLen and event.key!=K_BACKSPACE:
                if keys[K_LSHIFT]:
                    if event.key==K_9:
                        text += "("
                    elif event.key==K_8:
                        text += "*"
                    elif event.key==K_7:
                        text += "&"
                    elif event.key==K_6:
                        text += "^"
                    elif event.key==K_5:
                        text += "%"
                    elif event.key==K_4:
                        text += "$"
                    elif event.key==K_3:
                        text += "#"
                    elif event.key==K_2:
                        text += "@"
                    elif event.key==K_1:
                        text += "!"                        
                    elif event.key==K_0:
                        text += ")"
                    elif event.key==K_LEFTBRACKET:
                        text += "["
                    elif event.key == K_RIGHTBRACKET:
                        text += "]"
                    elif event.key == K_QUOTE:
                        text += "\""
                    elif event.key == K_3:
                        text += "#"
                    elif event.key == K_SEMICOLON:
                        text += ":"
                    else:
                        try:
                            text += chr(event.key)
                        except:
                            pass
                elif keys[K_RALT or K_LALT]:
                    if event.key==K_l:
                        text += "ł"        
                    elif event.key==K_z:
                        text += "ż"   
                else:
                    try:
                        if event.key != K_LSHIFT:
                            text += chr(event.key)
                    except:
                        pass
    def centeredBtn(hStart,color,text,border=0,fontSize=2,adjustToDialog=False):
        if adjustToDialog:
            showBtn = pygame.draw.rect(screen, color, [size_w/2.02,size_h/hStart,size_w/8,size_h/10], border,15)
            Write(round(size_w//100*fontSize),text,color1,[size_w/1.79,size_h/hStart+size_h/19])
        else:
            showBtn = pygame.draw.rect(screen, color, [size_w/2.16,size_h/hStart,size_w/8,size_h/10], border,15)
            Write(round(size_w//100*fontSize),text,color1,[size_w/1.9,size_h/hStart+size_h/19])
        return showBtn
    def eventsReset():
        events = [MOUSEMOTION,MOUSEBUTTONUP,MOUSEBUTTONDOWN,MOUSEWHEEL,KEYDOWN,KEYUP]
        for event in events:
            if pygame.event.get_blocked(event):
                pygame.event.set_allowed(event)
    def consoleExample(text,hght=1.51,fontSize=2.5,left=False):
        pygame.draw.rect(screen, color1, [size_w/3.11,size_h/hght,size_w/2.6,size_h/6], 0,15)
        pygame.draw.rect(screen, color3, [size_w/3,size_h/hght+size_h/44.1,size_w/2.8,size_h/8], size_w//450,15) 
        if not left:
            WriteItalic(round(size_w//100*fontSize),text, color3, [size_w/1.95,size_h/hght+size_h/11.15])
        elif left=='mega':
            WriteItalic(round(size_w//100*fontSize),text, color3, [size_w/2.47,size_h/hght+size_h/11.15])
        else:
            WriteItalic(round(size_w//100*fontSize),text, color3, [size_w/2.15,size_h/hght+size_h/11.15])
    def lesson1():
        global activeMenu,courseLvl,mentorIcon,activeLesson,theme,language,iterator,notBlocked,storedItems
        global bckgrMusicPlayed,soundEnabled,errorShowed
        if not errorShowed:
            course.standardLessonEvents("lesson1",11) 
        if activities[0] and not activeMenu and str(activeLesson)[17:-23]=="lesson1" and not errorShowed:
            language = getLang()
            try:
                if getTheme().lower() == "light":
                    mentorIcon = pygame.image.load(r"{}/Images/Game/orcM.png".format(dirPath))
                else:
                    mentorIcon = pygame.image.load(r"{}/Images/Game/orc.png".format(dirPath))
                mentorIcon = pygame.transform.scale(mentorIcon, [int(size_w/10.6),int(size_h/6)])
            except:
                errorInit("[Lesson1] Failed to load mentor icon!",fontSize=1.7)
            if courseLvl == 1 and activities[0]: #LVL1
                if language == "ENG":
                    course.dialogStandard(2.6,"Hello! My name is Romo and","I will help you to get through","beggining of this course.")
                    Write(round(size_w//100*1.5),"Click here",color3,[size_w/1.33,size_h/1.08]) 
                else:
                    course.dialogStandard(2.6,"Witaj! Na imię mi Romo i","pomogę ci przejść przez","początek tego kursu.")
                    Write(round(size_w//100*1.5),"Kliknij tutaj",color3,[size_w/1.33,size_h/1.08]) 
            elif courseLvl==2:
                if language == "ENG":
                    course.dialogStandard(2.6,"Let's start with what Python is","and what it's used for")  
                else:
                    course.dialogStandard(2.6,"Zacznijmy od tego","czym jest Python","i gdzie jest stosowany")
            elif courseLvl==3:
                notBlocked = False
                if language == "ENG":
                    pythonList = [
                        "High-level programming language",
                        "Object oriented",
                        "Easy to learn because of english-based syntax"
                    ]
                else:
                    pythonList = [
                        "Wysoko-poziomowym językiem programowania",
                        "Zorientowany obiektowo",
                        "Łatwy do nauki dzięki mocno angielskiej składni"
                    ]
                colors = [red,dark_blue,dark_green]
                if language == "ENG":
                    course.dialogTop(6.41,"So, Python is:","(Move mouse over question mark)")
                else:
                    course.dialogTop(6.41,"Tak więc, Python jest:","(Najedź myszką na znak zapytania)")
                obj = pygame.draw.rect(screen, color1, [1,1,1,1], width=0)
                if iterator == 1:
                    txt = WriteItalic(round(size_w//100*4),"?",red,[size_w/1.82,size_h/2.47])
                    obj = txt.get_rect()
                elif iterator == 2:
                    WriteItalic(round(size_w//100*2),pythonList[0],red,[size_w/1.82,size_h/2.47])
                    pygame.draw.line(screen, red, [size_w/4.78,size_h/3.05], [size_w/4.78,size_h/2.17], size_w//250)
                    pygame.draw.line(screen, red, [size_w/1.17,size_h/3.05], [size_w/1.17,size_h/2.17], size_w//250)
                    txt = WriteItalic(round(size_w//100*4),"?",dark_blue,[size_w/1.82,size_h/1.79])
                    obj = txt.get_rect()
                elif iterator == 3:
                    pygame.draw.line(screen, red, [size_w/4.78,size_h/3.05], [size_w/4.78,size_h/2.17], size_w//250)
                    pygame.draw.line(screen, red, [size_w/1.17,size_h/3.05], [size_w/1.17,size_h/2.17], size_w//250)
                    WriteItalic(round(size_w//100*2),pythonList[0],red,[size_w/1.82,size_h/2.47])
                    pygame.draw.line(screen, dark_blue, [size_w/4.78,size_h/2.16], [size_w/4.78,size_h/1.55], size_w//250)
                    pygame.draw.line(screen, dark_blue, [size_w/1.17,size_h/2.16], [size_w/1.17,size_h/1.55], size_w//250)
                    WriteItalic(round(size_w//100*2),pythonList[1],dark_blue,[size_w/1.82,size_h/1.79])
                    txt = WriteItalic(round(size_w//100*4),"?",dark_green,[size_w/1.82,size_h/1.38])
                    obj = txt.get_rect()
                elif iterator == 4:
                    pygame.draw.line(screen, red, [size_w/4.78,size_h/3.05], [size_w/4.78,size_h/2.17], size_w//250)
                    pygame.draw.line(screen, red, [size_w/1.17,size_h/3.05], [size_w/1.17,size_h/2.17], size_w//250)
                    WriteItalic(round(size_w//100*2),pythonList[0],red,[size_w/1.82,size_h/2.47])
                    pygame.draw.line(screen, dark_blue, [size_w/4.78,size_h/2.16], [size_w/4.78,size_h/1.55], size_w//250)
                    pygame.draw.line(screen, dark_blue, [size_w/1.17,size_h/2.16], [size_w/1.17,size_h/1.55], size_w//250)
                    WriteItalic(round(size_w//100*2),pythonList[1],dark_blue,[size_w/1.82,size_h/1.79]) 
                    pygame.draw.line(screen, dark_green, [size_w/4.78,size_h/1.55], [size_w/4.78,size_h/1.25], size_w//250)
                    pygame.draw.line(screen, dark_green, [size_w/1.17,size_h/1.55], [size_w/1.17,size_h/1.25], size_w//250) 
                    WriteItalic(round(size_w//100*2),pythonList[2],dark_green,[size_w/1.82,size_h/1.38]) 
                    notBlocked = True
                if event.type == MOUSEMOTION:
                    if obj.collidepoint(mouse_pos):
                        iterator += 1
                elif event.type == MOUSEBUTTONDOWN:
                    randW = uniform(1.21,4.00)
                    randH = uniform(1.07,11.1)
                    WriteItalic(round(size_w//100*0.7),"*Click*",color3,[size_w/randW,size_h/randH])
            elif courseLvl == 4:
                if len(storedItems)<4:
                    notBlocked = False
                else:
                    notBlocked = True
                if language == "ENG":
                    pythonList = [
                        "Web development",
                        "GUI Development",
                        "Machine Learning",
                        "Artificial Intelligence"
                    ]
                else:
                    pythonList = [
                        "Web development",
                        "GUI Development",
                        "Nauczanie maszynowe",
                        "Sztuczna Inteligencja"
                    ]
                lang = [
                    "Django, Flask",
                    "tkInter, Kivy",
                    "matplotlib, scipy",
                    "TensorFlow, Theano"
                ]
                colors=[red,dark_blue,dark_green,orange]

                if language == "ENG":
                    course.dialogTop(6.41,"Are you wondering for what is it used?","Then open the chests!")
                else:
                    course.dialogTop(6.41,"Zastanawiasz się do czego z kolei","takiego języka się używa?","Zatem otwórz skrzynki!")
                wdth = size_w/4.17
                hght = size_h/1.79
                rects = []
                for x in range(4):
                    if x not in storedItems:
                        rect = pygame.draw.rect(screen, dark_brown, [wdth,hght,size_w/12,size_h/8], 0,size_w//250)
                        rects.append(rect)
                        pygame.draw.rect(screen, darkThemeMainCol, [wdth,hght,size_w/12,size_h/8], size_w//450,size_w//250)
                        pygame.draw.line(screen, darkThemeMainCol, [wdth,hght+size_h/16], [wdth+size_w/12.2,hght+size_h/16], size_w//450)
                        pygame.draw.rect(screen, gold, [wdth+size_w/30,hght+size_h/25,size_w/55,size_h/55], 0)
                    else:
                        rect = pygame.draw.rect(screen, color2, [wdth,hght,size_w/12,size_h/8], 0,size_w//250)
                        rects.append(rect)  
                        WriteItalic(round(size_w//100*1.7),pythonList[x],colors[x],[wdth+size_w/25,hght])
                        WriteItalic(round(size_w//100*1.4),lang[x],colors[x],[wdth+size_w/25,hght+size_h/25])                      
                    wdth += size_w/6

                if event.type == MOUSEMOTION:
                    for rect in rects:
                        index = rects.index(rect)
                        if rect.collidepoint(mouse_pos) and index not in storedItems:
                            pygame.draw.rect(screen, lt_brown, [rect[0],rect[1],rect[2],rect[3]], size_w//450,size_w//250)
                            pygame.draw.line(screen, lt_brown, [rect[0],rect[1]+size_h/16], [rect[0]+size_w/12.2,rect[1]+size_h/16], size_w//450)
                elif event.type == MOUSEBUTTONDOWN:
                    for rect in rects:
                        if rect.collidepoint(mouse_pos):
                            if soundEnabled:
                                try:
                                    pygame.mixer.music.load(f"{dirPath}/Music/wooden_chest.ogg")
                                    pygame.mixer.music.play(1)
                                except:
                                    errorInit("Failed to load 'wooden_chest.ogg'!",fontSize=1.7)
                            index = rects.index(rect)
                            storedItems.append(index)
                            print(index,storedItems)
            elif courseLvl==5:
                if language == "ENG":
                    course.dialogStandard(2.7,"Now we will install Python,","just follow my lead!")   
                else:
                    course.dialogStandard(2.7,"Teraz zainstalujemy Pythona,","pokażę ci jak!")    
            elif courseLvl == 6:
                if language == "ENG":  
                    strs = [
                        "Now when we know a little bit about it,",
                        "why not to install it?",
                        "Download Python for Windows",
                        "Or visit Python webpage and do it yourself"
                    ] 
                    download="Download"
                    go="Go"
                else:
                    strs = [
                        "Teraz, gdy coś już o nim wiemy,",
                        "czemu go nie zainstalować?",
                        "Zainstaluj Python dla Windows",
                        "Lub odwiedź stronę Python i zrób to sam"
                    ]  
                    download="Pobierz"
                    go="Idź"     
                WriteItalic(round(size_w//100*3),strs[2],color3,[size_w/1.79,size_h/2.88])              
                link = course.centeredBtn(2.38,dark_green,download,adjustToDialog=True,fontSize=1.7)
                WriteItalic(round(size_w//100*2.2),strs[3],color3,[size_w/1.79,size_h/1.73])
                link2 = course.centeredBtn(1.49,dark_green,go,adjustToDialog=True,fontSize=2.4)
                course.dialogTop(6.41,strs[0],strs[1]) 
                if event.type == MOUSEBUTTONDOWN:
                    if link.collidepoint(mouse_pos):
                        os.system(r"start https://www.python.org/ftp/python/3.9.7/python-3.9.7-amd64.exe")
                    elif link2.collidepoint(mouse_pos):
                        os.system(r"start https://www.python.org/downloads/")
                elif event.type == MOUSEMOTION:
                    if link.collidepoint(mouse_pos):
                        course.centeredBtn(2.38,green,download,adjustToDialog=True,fontSize=1.7)
                        course.centeredBtn(2.38,dark_green,"",adjustToDialog=True,fontSize=1.7,border=size_w//350)
                    elif link2.collidepoint(mouse_pos):
                        course.centeredBtn(1.49,green,go,adjustToDialog=True,fontSize=1.7)
                        course.centeredBtn(1.49,dark_green,"",adjustToDialog=True,fontSize=1.7,border=size_w//350)
            elif courseLvl == 7:
                if language == "ENG":
                    strs = [
                        "Installation is pretty user friendly,",
                        "just remember to mark following:",
                        "Add Python [version] to PATH",
                        "Now you can safely choose \"Install now\"",
                        "Or \"Customize installation\" if you want to choose what will be installed"
                    ]
                else:
                    strs = [
                        "Instalacja jest całkiem intuicyjna,",
                        "ale pamiętaj by zaznaczyć następujące:",
                        "Add Python [version] to PATH",
                        "Teraz możesz bezpiecznie wybrać \"Install now\"",
                        "Lub \"Customize installation\" jeśli chcesz mieć kontrole co zostanie zainstalowane"
                    ]            
                course.dialogTop(6.41,strs[0],strs[1])
                pygame.draw.rect(screen, color3, [size_w/2.56,size_h/2.99,size_w/50,size_h/30], size_w//450)
                txt = Write(round(size_w//100*1.5),strs[2],color3,[size_w/1.78,size_h/2.86])
                pygame.draw.line(screen, green, [size_w/2.42,size_h/3.07], [size_w/2.49,size_h/2.81], size_w//450)
                pygame.draw.line(screen, green, [size_w/2.49,size_h/2.81], [size_w/2.58,size_h/2.99], size_w//450)
                WriteItalic(round(size_w//100*2),strs[3],color3,[size_w/1.83,size_h/2.02])
                WriteItalic(round(size_w//100*1.6),strs[4],color3,[size_w/1.83,size_h/1.62])
            elif courseLvl == 8:
                if language == "ENG":
                    course.dialogStandard(2.6,"Now it's time to install IDE","(Integrated Developer","Enviroment), Of course there's","no need for that, but it will","make it a lot easier for you",big=True)
                else:
                    course.dialogStandard(2.6,"Teraz zainstalujmy IDE","(Integrated Developer","Enviroment), Oczywiście nie ma","takiej potrzeby, ale to","znacznie ułatwi ci pracę",big=True)
            elif courseLvl == 9:
                if size_w < 1890:
                    screen.blit(mentorIcon,[size_w/3.72,size_h/1.65])
                else:
                    screen.blit(mentorIcon,[size_w/3.9,size_h/1.65])    
                txtRect = pygame.draw.rect(screen, color1, [size_w/2.65,size_h/1.8,size_w/2.7,size_h/5], size_w//200,30) 
                if language == "ENG":
                    txts = [
                        "There are plenty of IDEs,",
                        "But those above are recommended"
                    ]  
                else:
                    txts = [
                        "Jest mnóstwo IDE,",
                        "Ale powyższe są zalecane"
                    ]  
                IDEs = [
                    "Visual Studio Code",
                    "Visual Studio Community",
                    "PyCharm",
                    "Atom",
                    "Sublime Text"
                ]
                links = [
                    "https://code.visualstudio.com/",
                    "https://visualstudio.microsoft.com/pl/downloads/",
                    "https://www.jetbrains.com/pycharm/",
                    "https://atom.io/",
                    "https://www.sublimetext.com/"
                ]
                colors = [
                    (34,133,197),
                    (84,46,117),
                    (32,208,136),
                    (68,68,68),
                    (247,166,52)
                ]
                rects = []
                height = size_h/1.65         
                for txt in txts:
                    WriteItalic(round(size_w//100*1.8),txt,color3,[size_w/1.8,height])
                    height += size_h/12

                width = size_w/2.65
                widthCirc = size_w/2.43
                for x in range(len(IDEs)):
                    rect = pygame.draw.rect(screen, color1, [width,size_h/9,size_w/15,size_h/10], size_w//150)
                    rects.append(rect)
                    pygame.draw.circle(screen, colors[x], [widthCirc,size_h/6.35], size_w//100*1)
                    width += size_w/14
                    widthCirc += size_w/14

                widthCirc = size_w/2.43
                if event.type == MOUSEMOTION:
                    for rect in rects:
                        index = rects.index(rect)
                        if rect.collidepoint(mouse_pos):
                            pygame.draw.circle(screen, lt_gray, [widthCirc,size_h/6.35], size_w//100*1)
                            WriteItalic(round(size_w//100*3),IDEs[index],colors[index],[size_w/1.8,size_h/3])
                            WriteItalic(round(size_w//100*2.5),links[index],colors[index],[size_w/1.8,size_h/2.2])
                            if language == "ENG":
                                Write(round(size_w//100*1.5),"Click to open",colors[index],[size_w/1.8,size_h/4.06])
                            else:
                                Write(round(size_w//100*1),"Kliknij by otworzyć",colors[index],[size_w/1.8,size_h/4.06])
                        widthCirc += size_w/14
                elif event.type == MOUSEBUTTONDOWN:
                    for rect in rects:
                        index = rects.index(rect)
                        if rect.collidepoint(mouse_pos):
                            os.system(r"start {}".format(links[index]))
            elif courseLvl == 10:
                if language == "ENG":
                    course.dialogStandard(2.6,"One last thing,","Remember that python files","extension is",big=True)
                else:
                    course.dialogStandard(2.6,"Ostatnia rzecz,","Pamiętaj, że rozszerzeniem","plików jest",big=True)
                WriteItalic(size_w//100*3,".py",dark_blue,[size_w/1.37,size_h/2.04])      
            elif courseLvl == 11:
                if size_w < 1890:
                    screen.blit(mentorIcon,[size_w/2.9,size_h/6.1])
                else:  
                    screen.blit(mentorIcon,[size_w/3.1,size_h/6.1])
                try:
                    cup = pygame.image.load(r"{}/Images/Install/cup.png".format(dirPath))
                    cup = pygame.transform.scale(cup, [int(size_w/5.33),int(size_h/3)])
                    screen.blit(cup,[size_w/2.13,size_h/2.4]) 
                except:
                    errorInit("Failed to load 'cup.png'!") 

                pygame.draw.rect(screen, color1, [size_w/2.24,size_h/7.14,size_w/4,size_h/8], size_w//150,15)
                if language == "ENG":
                    Write(round(size_w//100*1.5),"Romo is proud",color3,[size_w/1.77,size_h/4.9])
                    finish = "Finish"
                else:
                    Write(round(size_w//100*1.5),"Romo jest dumny",color3,[size_w/1.77,size_h/4.9])
                    finish = "Zakończ"

                finishBtn = pygame.draw.rect(screen, dark_green, [size_w/2.12,size_h/1.26,size_w/6,size_h/8], 0,size_w//68)
                Write(round(size_w//100*2),finish,color3,[size_w/1.81,size_h/1.17])        

                if event.type == MOUSEMOTION:
                    if finishBtn.collidepoint(mouse_pos):
                        pygame.draw.rect(screen, color1, [size_w/2.12,size_h/1.26,size_w/6,size_h/8], size_w//200,size_w//68) 
                elif event.type == MOUSEBUTTONDOWN:
                    if finishBtn.collidepoint(mouse_pos):
                        if getCourseLvl() < 2:
                            changeCourselvl(2)
                        activeMenu = True
                        courseLvl = 1
                        bckgrMusicPlayed = False
    def lesson2():
        global activeMenu,courseLvl,mentorIcon,wait,storedTime,activeMain,type,chosen,inFight,notBlocked,theme
        global hp1,hp2,iterator,activeMain,rectCenter,langugage,bckgrMusicPlayed,errorShowed
        if activeMain and not errorShowed:
            course.standardLessonEvents("lesson2",16,condition=notBlocked)
        if activities[0] and not activeMenu and str(activeLesson)[17:-23]=="lesson2" and not errorShowed:
            language = getLang()
            try:
                if getTheme().lower() == "light":
                    mentorIcon = pygame.image.load(r"{}/Images/Game/orcM.png".format(dirPath))
                else:
                    mentorIcon = pygame.image.load(r"{}/Images/Game/orc.png".format(dirPath))
                mentorIcon = pygame.transform.scale(mentorIcon, [int(size_w/10.6),int(size_h/6)])
            except:
                errorInit("Failed to load mentor icon!",fontSize=1.8)
            if courseLvl == 1:
                if language == "ENG":
                    course.dialogStandard(2.65,"Now when you're ready","it's time for some adventure!")
                else:
                    course.dialogStandard(2.65,"Teraz, gdy jesteś gotów","nastał czas na przygodę!")
            elif courseLvl == 2:
                if language == "ENG":
                    course.dialogStandard(2.6,"But before that there's still","one thing you have to learn:","What are variables","and how to use them",big=True)
                else:
                    course.dialogStandard(2.6,"Ale zanim wciąż jest jedna","rzecz, której musisz się nauczyć:","Czym są zmienne","i jak ich używać",big=True)
            elif courseLvl == 3:
                colors = [dark_blue,(122, 55, 6),(8, 102, 75),(66, 2, 74),dark_red]
                height = size_h/3.7
                hMinus = size_h/7
                rectStartH = height - size_h/19.2
                typesH = []
                rects = []

                if language == "ENG":
                    vars = ["Numeric Type","Text Type","List Type","Bool Type","Binary Type"]
                    descriptions = [
                        [
                        "A whole number like 5 or 25",
                        "A number with additional part like 5.4 or 25.4",
                        "Two numbers: Python object and C structure from C API"
                        ],
                        [
                        "Group of characters making words between \" \""
                        ],
                        [
                            "List of values seperated by \",\" between [ ]",
                            "Same as list but ordered,unchangeable,allows duplicates and is between ()",
                            "Similar to tupple but unordered and doesn't allow duplicates",
                            "Set of pairs as key:keyword between { }"
                        ],
                        [
                            "Value that can contain only True or False"
                        ],
                        [
                            "\"bytes\" object: immutable sequence of integers 0 <= x < 256 as ASCII chars",
                            "Array of bytes, the bytearray type is sequence of integers 0 <= x < 256",
                            "Buffer protocol to access internal data of an obj: memory array/buffer"
                        ]
                    ]
                    allTypes = [
                    ["Integer",
                    "Float",
                    "Complex"],
                    ["String"],
                    ["List","Tupple","Set","Dictionary"],
                    ["Boolean"],
                    ["bytes","bytearray","memoryview"]
                    ]
                else:
                    vars = ["Numeryczne","Tekstowe","Listy/Zbiory","Logiczne","Binarne"]
                    descriptions = [
                        [
                        "Cały numer jak 5 lub 25",
                        "Numer z częścią po kropce jak np. 25.4",
                        "Dwie liczby: objekt Python i struktura C z C API"
                        ],
                        [
                        "Zestaw znaków tworzących słowa między \" \""
                        ],
                        [
                            "Lista wartości oddzielone \",\" miedzy [ ]",
                            "Jak lista, ale nieuporządkowana,niezmienna,pozwala na duplikaty i między ()",
                            "Podobne do krotki ale nieuporządkowane i nie pozwala na duplikaty",
                            "Zestaw par jako key:keyword między { }"
                        ],
                        [
                            "Zmienna, która przyjmuje tylko True i False"
                        ],
                        [
                            "objekt \"bit\": niezmienna sekwencja lb. całk. 0 <= x < 256 jako ASCII znaki",
                            "Zbiór bitów, które są sekwencją lb. całkowitych 0 <= x < 256",
                            "Protokół buforujący udostępniający info o obiekcie: zbiór danych/bufor"
                        ]
                    ]                    
                    allTypes = [
                    ["Integer",
                    "Float",
                    "Complex"],
                    ["String"],
                    ["List","Tupple","Set","Dictionary"],
                    ["Boolean"],
                    ["bytes","bytearray","memoryview"]
                    ]

                if activeMain:
                    if language == "ENG":
                        course.dialogTop(6.41,"Those are grouped in categories:")
                    else:
                        course.dialogTop(6.41,"Są one podzielone na kategorie:")
                    for var in vars:
                        rect = pygame.draw.rect(screen, color2, [size_w/2.4,rectStartH,size_w/3.5,size_h/9], 3)
                        rects.append(rect)
                        type = Write(round(size_w//100*3.5),var,color3,[size_w/1.8,height])
                        typesH.append(height)
                        height += hMinus
                        rectStartH += hMinus
                    if event.type == MOUSEMOTION:
                        for rect in rects:
                            index = rects.index(rect)
                            if rect.collidepoint(mouse_pos):
                                Write(round(size_w//100*3.5),vars[index],colors[index],[size_w/1.8,typesH[index]])
                                nextArrow = Write(size_w//100*3,"->",colors[index],[size_w/1.4,typesH[index]])   
                else:
                    backBtn = pygame.draw.rect(screen, dark_red, [size_w/4.93,size_h/15.04,size_w/10,size_h/10], 0,30)
                    if language == "ENG":
                        back = "Back"
                    else:
                        back = "Wróć"
                    backTxt = Write(size_w//100*2,back,color3,[size_w/3.95,size_h/8.54])               
                if event.type == MOUSEBUTTONDOWN:
                    global secondRects,actualList
                    if activeMain:
                        secondRects = []
                        actualList = []
                    height = size_h/3.7
                    rectHS = height - size_h/19.2
                    for rect in rects:
                        index = rects.index(rect)
                        if rect.collidepoint(mouse_pos):
                            activeMain = False
                            pygame.draw.rect(screen, color2, [size_w/5,size_h/16,size_w/1.5,size_h/1.1],0,10)
                            actualList = allTypes[index]
                            for type in allTypes[index]:
                                if not activeMain:
                                    rect = pygame.draw.rect(screen, color1, [size_w/4.2,rectHS,size_w/1.65,size_h/9], 0,15)
                                    secondRects.append(rect)
                                    Write(size_w//100*2,type,colors[index],[size_w/1.8,height])                   
                                    height += size_h/7
                                    rectHS += size_h/7
                    try:
                        if backBtn.collidepoint(mouse_pos):
                            activeMain = True
                    except:
                        pass
                elif event.type == MOUSEMOTION and not activeMain:
                    try:
                        if backBtn.collidepoint(mouse_pos):
                            backBtn = pygame.draw.rect(screen, red, [size_w/4.93,size_h/15.04,size_w/10,size_h/10], 0,30)
                            backTxt = Write(size_w//100*2,back,color3,[size_w/3.95,size_h/8.54])   
                        else:
                            backBtn = pygame.draw.rect(screen, dark_red, [size_w/4.93,size_h/15.04,size_w/10,size_h/10], 0,30)
                            backTxt = Write(size_w//100*2,back,color3,[size_w/3.95,size_h/8.54])                                    
                    except:
                        pass   
                    height = size_h/3.7
                    heightOver = size_h/3.7
                    for rect in secondRects:
                        index = secondRects.index(rect)
                        index2 = allTypes.index(actualList)
                        desc = descriptions[index2]
                        if size_w<1300:
                            leng = 1.3
                        elif index2 == 2 or index2 == 4:
                            leng = 1.2
                        elif index2 == 0:
                            leng = 1.8
                        else:
                            leng = 2
                        if rect.collidepoint(mouse_pos):
                            pygame.draw.rect(screen, dark_gray, [rect[0],rect[1],rect[2],rect[3]], 0,15) 
                            Write(round(size_w//100*leng),desc[index],colors[index2],[size_w/1.86,heightOver])   
                        else:
                            pygame.draw.rect(screen, color1, [rect[0],rect[1],rect[2],rect[3]], 0,15) 
                            Write(size_w//100*2,actualList[index],colors[index2],[size_w/1.8,heightOver])
                        heightOver += size_h/7
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        activeMain = True
            elif courseLvl == 4:
                if language == "ENG":
                    course.dialogStandard(2.6,"Before our journey we will","have to buy some items, by","the way we will test what you","have learned",big=True) 
                else:
                    course.dialogStandard(2.6,"Zanim zaczniemy podróż","musimy kupić pare","przedmiotów, przy okazji","sprawdzimy czego się nauczyłeś",big=True)
            elif courseLvl == 5:
                swordIcon = pygame.image.load(r"{}/Images/Game/sword.png".format(dirPath))
                axeIcon = pygame.image.load(r"{}/Images/Game/axe.png".format(dirPath))
                bowIcon = pygame.image.load(r"{}/Images/Game/bow.png".format(dirPath))
                items = [swordIcon,axeIcon,bowIcon]
                for item in items:
                    index = items.index(item)
                    item = pygame.transform.scale(item, [int(size_w/10.6),int(size_h/6)])
                    items[index] = item
                if iterator <= 1:
                    notBlocked = False
                else:
                    notBlocked = True
                if language == "ENG":
                    course.itemChooseGame("Choose a weapon with integer type of damage",items,"Damage",[5.5,8,3.6],1)
                else:
                    course.itemChooseGame("Wybierz broń o lb. całkowitej obrażeń",items,"Obrażenia",[5.5,8,3.6],1)
            elif courseLvl == 6:
                shield1 = pygame.image.load(r"{}/Images/Game/shield1.png".format(dirPath))
                shield2 = pygame.image.load(r"{}/Images/Game/shield2.png".format(dirPath))
                shield3 = pygame.image.load(r"{}/Images/Game/shield3.png".format(dirPath))
                shields = [shield1,shield2,shield3]
                for shield in shields:
                    index = shields.index(shield)
                    shield = pygame.transform.scale(shield, [int(size_w/10.6),int(size_h/6)])
                    shields[index] = shield
                if iterator <= 2:
                    notBlocked = False
                else:
                    notBlocked = True
                if language == "ENG":
                    course.itemChooseGame("We need shield: fire resistance and float type of armor",shields,"Armor",[4.1,4,3.63],0)
                else:
                    course.itemChooseGame("Zmiennoprzecinkowa wartość pancerza i odporność(ogień)",shields,"Pancerz",[4.1,4,3.63],0)
                wdth = size_w/3.5
                txtWdth = size_w/2.8
                bools = [True,True,False]
                for rect in range(3):
                    pygame.draw.rect(screen, color1, [wdth,size_h/1.7,size_w/7,size_h/10], 0,15)
                    if language == "ENG":
                        Write(round(size_w//100*0.9),"Fire resistance: {}".format(bools[rect]),color3,[txtWdth,size_h/1.55])
                    else:
                        Write(round(size_w//100*0.9),"Odporność(ogień): {}".format(bools[rect]),color3,[txtWdth,size_h/1.55])
                    wdth += size_w/5
                    txtWdth += size_w/5
            elif courseLvl == 7:
                if language == "ENG":
                    course.dialogStandard(2.6,"Great! Now we're ready!","Follow me into darkness","we will defeat a great enemy:","The Cursed Knight",big=True)
                else:
                    course.dialogStandard(2.6,"Brawo! Jesteśmy gotowi!","Podążaj za mną w ciemność","pokonamy potężnego wroga:","Przeklętego Rycerza",big=True)
                notBlocked = True
            elif courseLvl == 8:
                global selected,goBtn,DG_icons
                notBlocked = False
                if not isinstance(chosen,int):
                    cave1 = pygame.image.load(r"{}/Images/Game/cave.jpg".format(dirPath))
                    caveList = [cave1,pygame.transform.flip(cave1, True, False),cave1]
                    for cave in caveList:
                        index = caveList.index(cave)
                        cave = pygame.transform.scale(cave, [int(size_w/5.33),int(size_h/4.55)])
                        caveList[index] = cave
                    if language == "ENG":
                        txts = ["\'Enter at your own risk\"","Death awaits","\"You're already dead\""]
                    else:
                        txts = ["\'Wejdź na własne ryzyko\"","Śmierć czeka","\"Już jesteś martwy\""]
                    test = 5
                    wdth = size_w/4.3
                    txtWdth = size_w/3.09
                    rects = []
                    wToAdd = caveList[0].get_width() + size_w/80
                    for cave in caveList:
                        index = caveList.index(cave)
                        screen.blit(cave,[wdth,size_h/2])
                        rect = pygame.draw.rect(screen, color1, [wdth,size_h/2,caveList[0].get_width(),caveList[0].get_height()], size_w//270,1)
                        rects.append(rect)
                        Write(round(size_w//100*1.3),txts[index],orange,[txtWdth,size_h/2.08])
                        wdth += wToAdd
                        txtWdth += wToAdd
                        goBtn = pygame.draw.rect(screen, color2, [size_w/2.05,size_h/1.24,size_w/12,size_h/8], 0, 15)
                    try:
                        if int(selected) >= 0:
                            goBtn = pygame.draw.rect(screen, dark_green, [size_w/2.05,size_h/1.24,size_w/12,size_h/8], 0, 15)
                            if language == "ENG":
                                Write(size_w//100*2,"Go",color1,[size_w/1.89,size_h/1.15])
                            else:
                                Write(size_w//100*2,"Wejdź",color1,[size_w/1.89,size_h/1.15])
                    except:
                        pass
                    for rect in rects:
                        if selected == rects.index(rect):
                            pygame.draw.rect(screen, orange, [rect[0],rect[1],rect[2],rect[3]], size_w//270,1)
                    if language == "ENG":
                        course.dialogTop(6.41,"We're lucky that we got here so fast","But now we have to choose one of those","Caves, I bet one with correct string")
                    else:
                        course.dialogTop(6.41,"Mamy szczęście, że jesteśmy tak szybko","Ale teraz musimy wybrać jedną z tych","Jaskiń, brałbym tą z dobrze","napisanym stringiem")
                    if event.type == MOUSEBUTTONDOWN:
                        for rect in rects:
                            index = rects.index(rect)
                            if rect.collidepoint(mouse_pos):
                                selected = index
                        try:
                            if goBtn.collidepoint(mouse_pos) and selected >= 0:
                                chosen = selected
                        except:
                            pass
                    elif event.type == MOUSEMOTION:
                        try:
                            if goBtn.collidepoint(mouse_pos) and selected >=0:
                                goBtn = pygame.draw.rect(screen, green, [size_w/2.05,size_h/1.24,size_w/12,size_h/8], 0, 15)
                                pygame.draw.rect(screen, dark_green, [size_w/2.05,size_h/1.24,size_w/12,size_h/8], size_w//270, 15)
                                if language == "ENG":
                                    Write(size_w//100*2,"Go",color1,[size_w/1.89,size_h/1.15])
                                else:
                                    Write(size_w//100*2,"Wejdź",color1,[size_w/1.89,size_h/1.15])
                        except:
                            pass
                else:
                    if chosen == 0:
                        if len(DG_icons)<1:
                            troll = pygame.image.load(r"{}/Images/Game/troll.png".format(dirPath)) 
                            trollDialog =  pygame.image.load(r"{}/Images/Game/trollDialog.png".format(dirPath))
                            trollM = pygame.image.load(r"{}/Images/Game/trollMarked.png".format(dirPath))  
                            troll = pygame.transform.scale(troll, [int(size_w/4.55),int(size_h/1.64)])  
                            trollM = pygame.transform.scale(trollM, [int(size_w/4.55),int(size_h/1.64)])
                            trollDialog = pygame.transform.scale(trollDialog, [int(size_w/4.55),int(size_h/2.71)]) 
                            DG_icons = [troll,trollM,trollDialog]
                        course.dungeon.singleUnitInit(DG_icons,size_w/2.52,size_h/4.86)
                        tw = DG_icons[0].get_width()
                        th = DG_icons[0].get_height()
                        cords = [
                            [size_w/2.07,size_h/2.27,tw/4,th/2.6],
                            [size_w/2.24,size_h/1.91,tw/6.2,th/2.5],
                            [size_w/1.98,size_h/1.48,tw/6.2,th/6],
                            [size_w/2.24,size_h/2.34,tw/6.2,th/12],
                            [size_w/1.83,size_h/1.68,tw/6.2,th/6],
                            [size_w/1.85,size_h/2.27,tw/10,th/4.2]
                        ]
                        if language == "ENG":
                            course.dungeon.singleUnitDraw(cords,0,["Grog smell human, Grog hungry","Grog will eat little human"],"",dialogTop=False,textRect=True)
                            course.dungeon.singleUnitHp("Troll")
                            questions = ["What numeric type will be result of 15.0-12.0",
                            "What type is [1,2,3]",
                            "{\"one\":\"two\",\"three\":\"four\"} is",
                            "Which one is Set type",
                            "Select correct string elements",
                            "1.0 is type"]
                            asnwers = [["Integer","Float","Complex"],
                            ["Set","Dictionary","List"],
                            ["Dictionary","Set","Tupple"],
                            ["(1,2,3)","(1,1,3)","(1,3,2)"],
                            ["` `","\" \"","/* */"],
                            ["Float","Integer","Complex"]]
                            cave = "Cave"
                        else:
                            course.dungeon.singleUnitDraw(cords,0,["Grog czuje człowiek, Grog głodny","Grog zje mały człowiek"],"",dialogTop=False,textRect=True)
                            course.dungeon.singleUnitHp("Trol")
                            questions = ["Jakim typem będzie wynik 15.0-12.0",
                            "Jaki to typ: [1,2,3]",
                            "{\"jeden\":\"dwa\",\"trzy\":\"cztery\"} to",
                            "Który to typ Set",
                            "Wybierz poprawne elementy string",
                            "1.0 to typ:"]
                            asnwers = [["Integer","Float","Complex"],
                            ["Set","Dictionary","List"],
                            ["Dictionary","Set","Tupple"],
                            ["(1,2,3)","(1,1,3)","(1,3,2)"],
                            ["` `","\" \"","/* */"],
                            ["Float","Integer","Complex"]
                            ] 
                            cave = "Jaskinia"
                        goodAnswers = [1,2,0,2,1,1]
                        course.dungeon.singleUnitQuestions(questions,asnwers,goodAnswers)
                        course.dungeon.singleUnitAfterFight(cave)
                        course.dungeon.singleUnitMotionEvent(cave)
                        course.dungeon.singleUnitClickEvent(False)
                    elif chosen == 1:
                        if len(DG_icons)<1:
                            hunter = pygame.image.load(r"{}/Images/Game/knight2.png".format(dirPath))
                            hunter = pygame.transform.scale(hunter, [int(size_w/5.26),int(size_h/1.92)])
                            hunterMarked = pygame.image.load(r"{}/Images/Game/knight2M.png".format(dirPath))
                            hunterMarked = pygame.transform.scale(hunterMarked, [int(size_w/5.26),int(size_h/1.92)])
                            hunterDialog = pygame.image.load(r"{}/Images/Game/knight3.png".format(dirPath))
                            hunterDialog = pygame.transform.scale(hunterDialog, [int(size_w/4.55),int(size_h/2.71)])
                            DG_icons = [hunter,hunterMarked,hunterDialog]
                        course.dungeon.singleUnitInit(DG_icons,size_w/2.42,size_h/4.5)
                        hw = DG_icons[0].get_width()
                        hh = DG_icons[0].get_height()
                        wdth = size_w/2.23
                        cords = [
                            [wdth,size_h/4.38+hh/2,hw/1.8,hh/2],
                            [wdth+hw/6,size_h/4.38+hh/6,hw/3,hh/3],
                            [wdth+hw/4,size_h/4.38,hw/6,hh/6]
                        ]
                        if language == "ENG":
                            course.dungeon.singleUnitDraw(cords,0,["I've been looking for you Cursed Knight","Today is your last day"],"",dialogTop=False)
                            course.dungeon.singleUnitHp("Bounty hunter")
                            questions = ["What numeric type will be result of 3*2.1",
                            "What type is { 1:2,3:4 }",
                            "(1,1,2,3,3) is",
                            "Which one is Integer type",
                            "Select Float type result",
                            "3.4+2.6 is type"]
                            asnwers = [["Integer","Float","Complex"],
                            ["Set","Dictionary","List"],
                            ["Dictionary","Set","Tupple"],
                            ["2","15.0","3.4"],
                            ["3+4","15/7","7*7"],
                            ["Float","Integer","Complex"]
                            ]
                            cave = "Cave"
                        else:
                            course.dungeon.singleUnitDraw(cords,0,["Szukałem cię Przeklęty Rycerzu","Dzisiaj jest twój ostatni dzień"],"",dialogTop=False)
                            course.dungeon.singleUnitHp("Łowca nagród")
                            questions = ["Jakiego typu numerycznego jest 3*2.1",
                            "Jakiego typu jest { 1:2,3:4 }",
                            "(1,1,2,3,3) to",
                            "Która wartość to Integer",
                            "Wybierz wynik typu float",
                            "3.4+2.6 to typ:"]
                            asnwers = [["Integer","Float","Complex"],
                            ["Set","Dictionary","List"],
                            ["Dictionary","Set","Tupple"],
                            ["2","15.0","3.4"],
                            ["3+4","15/7","7*7"],
                            ["Float","Integer","Complex"]
                            ]  
                            cave = "Jaskinia"                          
                        goodAnswers = [1,1,2,0,1,0]
                        course.dungeon.singleUnitQuestions(questions,asnwers,goodAnswers)
                        course.dungeon.singleUnitAfterFight(cave)
                        course.dungeon.singleUnitMotionEvent(cave)
                        course.dungeon.singleUnitClickEvent(False)
                    elif chosen == 2:
                        global winBtn
                        if len(DG_icons) < 1:
                            knight = pygame.image.load(r"{}/Images/Game/knight1.png".format(dirPath))
                            knightMarked = pygame.image.load(r"{}/Images/Game/knight1M.png".format(dirPath))
                            DG_icons = [knight,knightMarked]
                        for icon in DG_icons:
                            index = DG_icons.index(icon)
                            icon = pygame.transform.scale(icon, [int(size_w/2.985),int(size_h/1.92)])
                            DG_icons[index] = icon
                        course.dungeon.singleUnitInit(DG_icons,size_w/2.69,size_h/4.38)
                        wdth = size_w/2.69
                        hght = size_h/4.38
                        kw = DG_icons[0].get_width()
                        kh = DG_icons[0].get_height()
                        rects = []
                        cords = [
                            [size_w/2.04,size_h/2.37,kw/6,kh/2],
                            [size_w/1.98,size_h/2.67,kw/12,kh/12]
                        ]
                        if language == "ENG":
                            course.dungeon.singleUnitDraw(cords,6.41,[],"That's him! The Cursed Knight!")
                            course.dungeon.singleUnitHp("The Cursed Knight")
                            questions = ["What numeric type will be result of 3*2.1",
                            "What type is { 1:2,3:4 }",
                            "(1,1,2,3,3) is",
                            "Which one is Integer type",
                            "Select Float type result",
                            "3.4+2.6 is type"]
                            asnwers = [["Integer","Float","Complex"],
                            ["Set","Dictionary","List"],
                            ["Dictionary","Set","Tupple"],
                            ["2","15.0","3.4"],
                            ["3+4","15/7","7*7"],
                            ["Float","Integer","Complex"]
                            ]
                            next = "Next"
                        else:
                            course.dungeon.singleUnitDraw(cords,6.41,[],"To on! Przeklęty Rycerz!")
                            course.dungeon.singleUnitHp("Przeklęty Rycerz")
                            questions = ["Jakiego typu numerycznego jest 3*2.1",
                            "Jakiego typu jest { 1:2,3:4 }",
                            "(1,1,2,3,3) to",
                            "Która wartość to Integer",
                            "Wybierz wynik typu float",
                            "3.4+2.6 to typ:"]
                            asnwers = [["Integer","Float","Complex"],
                            ["Set","Dictionary","List"],
                            ["Dictionary","Set","Tupple"],
                            ["2","15.0","3.4"],
                            ["3+4","15/7","7*7"],
                            ["Float","Integer","Complex"]
                            ]  
                            next = "Dalej"
                        goodAnswers = [1,1,2,0,1,0]
                        course.dungeon.singleUnitQuestions(questions,asnwers,goodAnswers)
                        course.dungeon.singleUnitAfterFight(next) 
                        course.dungeon.singleUnitMotionEvent(next)
                        course.dungeon.singleUnitClickEvent(True)            
            elif courseLvl == 9:
                if language == "ENG":
                    course.dialogStandard(2.65,"You did it!","You defeated The Cursed Knight!")
                else:
                    course.dialogStandard(2.65,"Zrobiłeś to!","Pokonałeś Przeklętego Rycerza!")
            elif courseLvl == 10:
                if language == "ENG":
                    Write(size_w//100*4,"Not so fast!",color3,[size_w/1.94,size_h/2.45])
                    Write(size_w//100*4,"You think you could",color3,[size_w/1.94,size_h/1.89])
                    Write(size_w//100*4,"defeat me so easily?",color3,[size_w/1.94,size_h/1.56])
                else:
                    Write(size_w//100*4,"Nie tak szybko!",color3,[size_w/1.94,size_h/2.45])
                    Write(size_w//100*4,"Myślisz, że pokonasz",color3,[size_w/1.94,size_h/1.89])
                    Write(size_w//100*4,"mnie tak łatwo?",color3,[size_w/1.94,size_h/1.56])                    
            elif courseLvl == 11:
                if language == "ENG":
                    course.dialogStandard(2.65,"Damn! Are you seeing this?","He's transforming into a dragon!")
                else:
                    course.dialogStandard(2.65,"Widzisz to?","On zmienia się w smoka!!")
            elif courseLvl == 12:
                dragon = pygame.image.load(r"{}/Images/Game/dragon.png".format(dirPath))
                dragon = pygame.transform.scale(dragon,[int(size_w/2.132),int(size_h/2.4)])
                screen.blit(dragon,[size_w/3.47,size_h/2.5])
                if language == "ENG":
                    course.dialogTop(6.41,"It won't be as easy as earlier","For dragon we have to use","Another tactic")
                else:
                    course.dialogTop(6.41,"Nie będzie tak łatwo jak wcześniej","Będziemy musieli użyć","Innej taktyki")
            elif courseLvl == 13:
                if iterator == 1:
                    notBlocked = False
                if language == "ENG":
                    strs = [
                        "You will have to write variables",
                        "In rectangle shown below with",
                        "Given values, just by yourself,",
                        "Lemme show you",
                        "Show",
                        "That's a variable named \"damage\"",
                        "With integer type value of 20",
                        "damage = 20",
                    ]
                else:
                    strs = [
                        "Będziesz musiał pisać zmienne",
                        "o własciwych wartościach w ",
                        "miejscu poniżej, sam",
                        "Ci pokażę",
                        "Pokaż",
                        "To zmienna o nazwie \"obrażenia\"",
                        "O wartości 20 typu Integer",
                        "obrażenia = 20",
                    ]
                pygame.draw.rect(screen, color1, [size_w/3.11,size_h/1.5,size_w/2.6,size_h/6], 0,15)
                pygame.draw.rect(screen, color2, [size_w/3,size_h/1.45,size_w/2.8,size_h/8], size_w//450,15)
                if iterator == 1:
                    course.dialogTop(6.41,strs[0],strs[1],strs[2],strs[3])
                    showBtn = pygame.draw.rect(screen, dark_green, [size_w/2.16,size_h/1.98,size_w/8,size_h/10], 0,15)
                    showTxt = Write(size_w//100*2,strs[4],color1,[size_w/1.9,size_h/1.8])
                    Write(round(size_w//100*2.5),"|", color2, [size_w/1.95,size_h/1.32])
                else:
                    pygame.draw.rect(screen, color2, [size_w/3.27,size_h/11.53,size_w/2,size_h/2],0,10)
                    showBtn = pygame.draw.rect(screen, color2, [size_w/2.16,size_h/1.98,size_w/8,size_h/10], 0,15)
                    course.dialogTop(6.41,strs[5],strs[6])
                    Write(round(size_w//100*2.5),strs[7], color3, [size_w/1.95,size_h/1.32])

                if event.type == MOUSEMOTION:
                    if showBtn.collidepoint(mouse_pos) and iterator == 1:
                        pygame.draw.rect(screen, green, [size_w/2.16,size_h/1.98,size_w/8,size_h/10], 0,15)
                        pygame.draw.rect(screen, dark_green, [size_w/2.16,size_h/1.98,size_w/8,size_h/10], size_w//450,15)
                        Write(size_w//100*2,strs[4],color1,[size_w/1.9,size_h/1.8])
                elif event.type == MOUSEBUTTONDOWN:
                    if showBtn.collidepoint(mouse_pos) and iterator == 1:
                        iterator = 2
                        notBlocked = True
            elif courseLvl == 14:
                dragonMR = pygame.image.load(r"{}/Images/Game/dragonMarkedRed.png".format(dirPath))  
                dragonMR = pygame.transform.scale(dragonMR, [int(size_w/2.132),int(size_h/2.4)])    
                dragon = pygame.image.load(r"{}/Images/Game/dragon.png".format(dirPath))
                dragon = pygame.transform.scale(dragon,[int(size_w/2.132),int(size_h/2.4)])           
                screen.blit(dragon,[size_w/3.47,size_h/2.5])
                dragonRect = dragon.get_rect(center=[size_w/1.96,size_h/1.51])
                cords = [
                    [size_w/2.3,size_h/1.7,size_w/6,size_h/8],
                    [size_w/2.1,size_h/1.4,size_w/8,size_h/8],
                    [size_w/3.44,size_h/2.5,size_w/6,size_h/6],
                    [size_w/2.16,size_h/2.11,size_w/6,size_h/8.5],
                    [size_w/1.59,size_h/2.11,size_w/8,size_h/8.5],
                    [size_w/1.66,size_h/1.56,size_w/12,size_h/8.5]
                ]
                rects = []
                for cord in cords:
                    rect = pygame.draw.rect(screen, color2, cord, 1)
                    rects.append(rect)
                screen.blit(dragon,[size_w/3.47,size_h/2.5])
                if language == "ENG":
                    commandsList = [
                        "Declare integer \"damage\" with value of 8",
                        "Declare float \"block\" with value of 3.15",
                        "Declare boolean \"dodge\" with value of True",
                        "Declare string \"shout\" with value of \"I won\""
                    ]   
                    goodVars = [
                        ["damage = 8", "damage=8"],
                        ["block = 3.15","block=3.15"],
                        ["dodge = True","dodge=True"],
                        ["shout = \"I won\"","shout=\"I won\""]                    
                    ]
                else:
                    commandsList = [
                        "Zadeklaruj integer \"obrażenia\" o wartości 8",
                        "Zadeklaruj float \"blok\" o wartości 3.15",
                        "Zadeklaruj boolean \"unik\" o wartości True",
                        "Zadeklaruj string \"krzyk\" o wartości \"Wygrałem\""
                    ]   
                    goodVars = [
                        ["obrażenia = 8", "obrażenia=8"],
                        ["blok = 3.15","blok=3.15"],
                        ["unik = True","unik=True"],
                        ["krzyk = \"Wygrałem\"","krzyk=\"Wygrałem\""]                    
                    ]                    
                try:
                    if language == "ENG":
                        course.consoleGame(commandsList[iterator-2],"",multipleAnswers=True,answersList=goodVars[iterator-2],btnText="Attack") 
                    else:
                        course.consoleGame(commandsList[iterator-2],"",multipleAnswers=True,answersList=goodVars[iterator-2],btnText="Atak")   
                except:
                    pass
                if iterator < 6:
                    notBlocked = False
                else:
                    courseLvl += 1
                    activeMain = True
                if event.type == MOUSEBUTTONDOWN:
                    for rect in rects:
                        if rect.collidepoint(mouse_pos):
                            screen.blit(dragonMR,[size_w/3.47,size_h/2.5])  
                            course.coursorMarked() 
            elif courseLvl == 15:
                if iterator == 6:
                    notBlocked = True
                if language == "ENG":
                    course.dialogStandard(2.6,"This time you really did it!","I'm very proud of you and this","was an honour to work with you") 
                else:
                    course.dialogStandard(2.6,"Tym razem naprawdę to zrobiłeś!","Jestem z ciebie dumny, był","to honor walczyć u twego boku")
            elif courseLvl == 16:
                if language == "ENG":
                    strs = [
                        "But it's time to say goodbye,",
                        "take this axe of mine",
                        "so you can remember me",
                        "Finish"
                    ]
                else:
                    strs = [
                        "Jednak czas się pożegnać,",
                        "podarowuje ci ten topór",
                        "ażebyś mnie zapamiętał",
                        "Zakończ"
                    ] 
                axe = pygame.image.load(r"{}/Images/Game/romosaxe.png".format(dirPath))
                axe = pygame.transform.scale(axe, [int(size_w/5.33),int(size_h/3)])
                screen.blit(axe,[size_w/2.25,size_h/2.45])             
                course.dialogTop(6.41,strs[0],strs[1],strs[2])   
                finishBtn = pygame.draw.rect(screen, dark_green, [size_w/2.3,size_h/1.26,size_w/6,size_h/8], 0,20)
                Write(round(size_w//100*2),strs[3],color1,[size_w/1.94,size_h/1.17])    
                if event.type == MOUSEMOTION:
                    if finishBtn.collidepoint(mouse_pos):
                        pygame.draw.rect(screen, green, [size_w/2.3,size_h/1.26,size_w/6,size_h/8], 0,20) 
                        pygame.draw.rect(screen, dark_green, [size_w/2.3,size_h/1.26,size_w/6,size_h/8], size_w//200,20)
                        Write(round(size_w//100*2),strs[3],color3,[size_w/1.94,size_h/1.17])   
                    else:
                        pygame.draw.rect(screen, dark_green, [size_w/2.3,size_h/1.26,size_w/6,size_h/8], 0,20) 
                        Write(round(size_w//100*2),strs[3],color1,[size_w/1.94,size_h/1.17])  
                elif event.type == MOUSEBUTTONDOWN:
                    if finishBtn.collidepoint(mouse_pos):
                        if getCourseLvl() < 3:
                            changeCourselvl(3)
                        activeMenu = True
                        courseLvl = 1  
                        iterator = 1      
                        bckgrMusicPlayed = False                    
    def lesson3():
        global mentorIcon,activeMain,held,courseLvl,notBlocked,iterator,activeMenu,chosen
        global bckgrMusicPlayed,errorShowed
        if activeMain and not errorShowed:
            course.standardLessonEvents("lesson3",28,condition=notBlocked)
        if activities[0] and not activeMenu and str(activeLesson)[17:-23]=="lesson3" and not errorShowed:
            try:
                mentorIcon = pygame.image.load(r"{}/Images/Game/wizard.png".format(dirPath))
                mentorIcon = pygame.transform.scale(mentorIcon, [int(size_w/10.6),int(size_h/6)])
            except:
                errorInit("Failed to load mentor icon!",fontSize=1.8)
            language = getLang()
            if courseLvl == 1:
                if language == "ENG":
                    course.dialogStandard(2.6,"Hello there! I'm professor","Magnus and I will teach","you something about","magic, my apprentice",big=True)
                else:
                    course.dialogStandard(2.6,"Witaj! Jestem profesor","Magnus i nauczę cię","czegoś w sprawie","magii, mój uczniu",big=True)
            elif courseLvl == 2:
                notBlocked = False
                flower = pygame.image.load(r"{}/Images/Game/flower.png".format(dirPath))
                flower = pygame.transform.scale(flower, [int(size_w/10.6),int(size_h/6)])
                flowerM= pygame.image.load(r"{}/Images/Game/flowerM.png".format(dirPath))
                flowerM = pygame.transform.scale(flowerM, [int(size_w/10.6),int(size_h/6)])
                basket = pygame.image.load(r"{}/Images/Game/basket.png".format(dirPath))
                basket = pygame.transform.scale(basket, [int(size_w/5.33),int(size_h/3)])
                if language == "ENG":
                    course.dialogTop(6.41,"But first, we need few ingredients","Add this special flower to basket")
                else:
                    course.dialogTop(6.41,"Ale najpierw, potrzebujemy składników","Wrzuć ten specjalny kwiat do koszyka")
                hght = size_h/1.58 #1.85 for >1890
                flowerWdth = flower.get_width()
                flowerHght = flower.get_height()
                basketWdth = basket.get_width()
                basketHght = basket.get_height()
                maxCordsW = [size_w/4.18,size_w/1.21]
                maxCordsH = [size_h/5.09,size_h/1.13]
                isWidthCorrect = mouse_pos[0]>maxCordsW[0] and mouse_pos[0] < maxCordsW[1]
                isHeightCorrect = mouse_pos[1]>maxCordsH[0] and mouse_pos[1] < maxCordsH[1]
                if held and isWidthCorrect and isHeightCorrect:
                    pygame.draw.rect(screen, color2, [size_w/4.72,size_h/2.77,size_w/1.6,size_h/2.2], width=0)
                    screen.blit(flowerM,[mouse_pos[0]-flowerWdth/2,mouse_pos[1]-flowerHght/2])
                    screen.blit(basket,[size_w/1.57,size_h/2.15])
                else:
                    screen.blit(flower,[size_w/3.8,hght])
                    screen.blit(basket,[size_w/1.57,size_h/2.15])
                flowerRect = flower.get_rect(center=[size_w/3.8+flowerWdth/2,size_h/1.58+flowerHght/2])
                basketRect = basket.get_rect(center=[size_w/1.57+basketWdth/2,size_h/2.15+basketHght/2])
                if event.type == MOUSEBUTTONDOWN:
                    if flowerRect.collidepoint(mouse_pos):
                        held = True
                elif event.type == MOUSEBUTTONUP:
                    held = False                   
                elif event.type == MOUSEMOTION:
                    if flowerRect.collidepoint(mouse_pos) and not held:
                        screen.blit(flowerM,[size_w/3.8,hght])
                    if held and basketRect.collidepoint(mouse_pos):
                        notBlocked = True
                        held = False
                        courseLvl += 1
            elif courseLvl == 3:
                notBlocked = False
                if language == "ENG":
                    course.dialogStandard(2.6,"No! But not like this!","Do this magic way,","let me show you")
                    show = "Show"
                else:
                    course.dialogStandard(2.6,"Ale nie tak!","Trzeba to zrobić za pomocą","magii, pokaże ci")
                    show = "Pokaż"
                course.centeredBtn(1.33,dark_green,show)
                if event.type == MOUSEMOTION:
                    if course.centeredBtn(1.33,dark_green,show).collidepoint(mouse_pos):
                        course.centeredBtn(1.33,green,show)
                elif event.type == MOUSEBUTTONDOWN:
                    if course.centeredBtn(1.33,dark_green,show).collidepoint(mouse_pos):
                        courseLvl += 1
            elif courseLvl == 4:
                notBlocked = True
                if language == "ENG":
                    course.dialogTop(6.41,"Your basket is now empty,","so according to list it","looks like below")
                    course.consoleExample("basket = [ ]")
                else:
                    course.dialogTop(6.41,"Twój koszyk jest teraz pusty,","więc porównując go do listy","wygląda jak poniżej")
                    course.consoleExample("koszyk = [ ]")
            elif courseLvl == 5:
                if language == "ENG":
                    course.dialogTop(6.41,"If we want to add something to this","in more magic way we could","use append() function")
                    course.consoleExample("basket.append(flower)")    
                else:
                    course.dialogTop(6.41,"Jeśli chcemy coś do niego dodać","w magiczny sposób możemy","użyć funkcji append()")
                    course.consoleExample("koszyk.append(kwiat)") 
            elif courseLvl == 6:
                notBlocked = False
                if language == "ENG":
                    strs = [
                        "Now try to add flower to basket the same way",
                        "basket.append(flower)",
                        "Cast",
                        "Enter correct command in box above",
                        "Congrats! You may go futher",
                    ]
                else:
                    strs = [
                        "Teraz spróbuj dodać kwiat w ten sam sposób",
                        "koszyk.append(kwiat)",
                        "Czaruj",
                        "Wprowadź poprawną komendę powyżej",
                        "Gratulacje! Możesz iść dalej",
                    ]
                course.consoleGame(strs[0],strs[1],strs[2])  
                if iterator > 1:
                    notBlocked = True
                if not activeMain:
                    pygame.draw.rect(screen, color2, [size_w/3.49,size_h/1.82,size_w/2,size_h/10], width=0)
                if iterator == 1:
                    Write(size_w//100*2,strs[3],red,[size_w/1.9,size_h/1.68])
                else:
                    Write(size_w//100*2,strs[4],green,[size_w/1.9,size_h/1.68]) 
                    activeMain = True 
            elif courseLvl == 7:
                iterator = 1 
                if language == "ENG":
                    course.dialogStandard(2.6,"Great! I see you're getting it","Let's go to my laboratory now,","shall we?") 
                else:
                    course.dialogStandard(2.6,"Świetnie! Widzę, że łapiesz","Udajmy się teraz do mojego","laboratorium") 
            elif courseLvl == 8:
                cauldron = pygame.image.load(r"{}/Images/Game/cauldron.png".format(dirPath))
                cauldron = pygame.transform.scale(cauldron, [int(size_w/5.33),int(size_h/3)])
                if language == "ENG":
                    strs = [
                        "Oh right, now we need to",
                        "add three different ingredients",
                        "I will take care of first one",
                        "cauldron.append(ingredient)",
                        "cauldron = [ ]"
                    ]
                else:
                    strs = [
                        "W porządku, teraz musimy",
                        "dodać różne inne składniki,",
                        "zajmę się pierwszym",
                        "kocioł.append(składnik)",
                        "kocioł = [ ]"
                    ]
                course.dialogTop(6.41,strs[0],strs[1],strs[2])
                screen.blit(cauldron,[size_w/2.35,size_h/2.7])
                course.consoleExample(strs[3])   
                Write(size_w//100*2,strs[4],color3,[size_w/1.42,size_h/1.94])
            elif courseLvl == 9:
                notBlocked = False
                if language == "ENG":
                    strs = [
                        "Okay, now you will add second",
                        "ingredient with extend() function",
                        "that is used to add list elements to another",
                        "list, but as elements not another list",
                        "list1.extend(list2)",
                        "Are you ready?",
                    ]
                else:
                    strs = [
                        "Dobrze, teraz musimy dodać drugi",
                        "składnik przez funkcje extend()",
                        "używaną do dodawania elementów",
                        "listy, ale elementów a nie całej listy",
                        "lista1.extend(lista2)",
                        "Jesteś gotów?",
                    ]                    
                course.dialogTop(6.41,strs[0],strs[1],strs[2],strs[3])  
                course.consoleExample(strs[4])      
                Write(size_w//100*4,strs[5],color3,[size_w/2.3,size_h/1.8])    
                startBtn = pygame.draw.rect(screen, dark_green, [size_w/1.58,size_h/1.99,size_w/8,size_h/10], 0,15)  
                Write(size_w//100*2,"Start",color1,[size_w/1.44,size_h/1.81])
                if event.type == MOUSEMOTION:
                    if startBtn.collidepoint(mouse_pos):
                        pygame.draw.rect(screen, green, [size_w/1.58,size_h/1.99,size_w/8,size_h/10], 0,15)  
                        pygame.draw.rect(screen, dark_green, [size_w/1.58,size_h/1.99,size_w/8,size_h/10], size_w//450,15)  
                        Write(size_w//100*2,"Start",color3,[size_w/1.44,size_h/1.81])
                elif event.type == MOUSEBUTTONDOWN:
                     if startBtn.collidepoint(mouse_pos):
                        courseLvl += 1
            elif courseLvl == 10:
                if language == "ENG":
                    strs = [
                        "Now extend cauldron with ingredients",
                        "cauldron.extend(ingredients)",
                        "Add",
                        "Enter correct command in box above",
                        "Congrats! You may go futher"
                    ]
                else:
                    strs = [
                        "Rozszerz kocioł o składniki(extend)",
                        "kocioł.extend(składniki)",
                        "Dodaj",
                        "Podaj poprawną komendę powyżej",
                        "Gratulacje! Możesz iść dalej"
                    ]                    
                course.consoleGame(strs[0],strs[1],strs[2],1.8,28,fontSize2=1.7)
                if iterator > 1:
                    notBlocked = True
                if not activeMain:
                    pygame.draw.rect(screen, color2, [size_w/3.49,size_h/1.82,size_w/2,size_h/10], width=0)                    
                if iterator == 1:
                    Write(size_w//100*2,strs[3],red,[size_w/1.9,size_h/1.68])
                else:
                    activeMain = True
                    Write(size_w//100*2,strs[4],green,[size_w/1.9,size_h/1.68]) 
            elif courseLvl==11:
                if language == "ENG":
                    course.dialogStandard(2.6,"Good job, in the meantime","I separated individual parts of","flower you got so now it is:","flower = [petals,stalk,pollen]",big=True)
                else:
                    course.dialogStandard(2.6,"Brawo, ja w międzyczasie","podzieliłem kwiat, który","zdobyłeś na części:","kwiat = [płatki,łodyga,pyłek]",big=True) 
            elif courseLvl == 12:
                if language == "ENG":
                    strs = [
                        "To complete next task you have to",
                        "know a little bit about indexes,",
                        "so there's a list = [part1,part2] and",
                        "indexes starts from 0,",
                        "then part1 is index 0 and",
                        "part2 is index 1"
                    ]
                else:
                    strs = [
                        "By wykonać to zadanie musisz",
                        "wiedzieć trochę o indexach,",
                        "więc jest lista = [część1,część2] i",
                        "indexy zaczynają sie od 0,",
                        "także część1 to index 0 a",
                        "część2 to index 1"
                    ]                    
                if size_w<1300:
                    course.dialogStandard(2.6,strs[0],strs[1],strs[2],strs[3],strs[4],strs[5],fontSize=1.7)
                else:
                    course.dialogStandard(2.9,strs[0],strs[1],strs[2],strs[3],strs[4],strs[5],rectH=3.7,iconH=2.6,fontSize=1.7)
            elif courseLvl == 13:
                iterator = 1
                if language == "ENG":
                    course.consoleExample("list = [part1,part2,part3]",4.3)
                    course.consoleExample("list[0]",2.35)
                    Write(size_w//100*2,"is part1", color3,[size_w/1.3,size_h/1.95])
                    course.consoleExample("list.index(part3)",1.64)
                    Write(size_w//100*2,"is 2", color3,[size_w/1.3,size_h/1.43])
                else:
                    course.consoleExample("lista = [nr1,nr2,nr3]",4.3)
                    course.consoleExample("lista[0]",2.35)
                    Write(size_w//100*2,"to nr1", color3,[size_w/1.3,size_h/1.95])
                    course.consoleExample("lista.index(nr3)",1.64)
                    Write(size_w//100*2,"to 2", color3,[size_w/1.3,size_h/1.43])                    
            elif courseLvl == 14:
                notBlocked = False
                if language == "ENG":
                    strs = [
                        "cauldron = []",
                        "Correct order to append: petals,pollen,stalks",
                        "cauldron = [petals]",
                        "cauldron = [petals,pollen]",
                        "cauldron = [petals,pollen,stalks]",
                        "You may go futher",
                        "flower = [petals,stalks,pollen]",
                        "Add"
                    ]
                    answers = ["cauldron.append(flower[0])",
                    "cauldron.append(flower[2])",
                    "cauldron.append(flower[1])"]
                else:
                    strs = [
                        "kocioł = []",
                        "Prawidłowa kolejność: płatki,pyłek,łodyga",
                        "kocioł = [płatki]",
                        "kocioł = [płatki,pyłek]",
                        "kocioł = [płatki,pyłek,łodyga]",
                        "Możesz iść dalej",
                        "kwiat = [płatki,łodyga,pyłek]",
                        "Dodaj"
                    ]
                    answers = ["kocioł.append(kwiat[0])",
                    "kocioł.append(kwiat[2])",
                    "kocioł.append(kwiat[1])"]                    
                course.consoleExample(strs[0],1.44)
                wdth = size_w/3
                rect1 = pygame.draw.rect(screen, dark_red, [wdth,size_h/2.75,size_w/12,size_h/8], 0,15)
                txt1 = Write(size_w//100*4,"X",color1,[size_w/2.69,size_h/2.32])
                rect2 = pygame.draw.rect(screen, dark_red, [wdth+size_w/8,size_h/2.75,size_w/12,size_h/8], 0,15)
                txt2 = Write(size_w//100*4,"X",color1,[size_w/2,size_h/2.32])
                rect3 = pygame.draw.rect(screen, dark_red, [size_w/1.7,size_h/2.75,size_w/12,size_h/8], 0,15)
                txt3 = Write(size_w//100*4,"X",color1,[size_w/1.59,size_h/2.32])
                try:
                    if iterator < 4:
                        course.consoleGame(strs[1],answers[iterator-1],strs[7],textLen=26) #0 2 1
                except:
                    pass
                if iterator >= 2:
                    course.consoleExample(strs[2],1.44)
                    rect1 = pygame.draw.rect(screen, dark_green, [wdth,size_h/2.75,size_w/12,size_h/8], 0,15)
                    txt1 = Write(size_w//100*8,"+",green,[size_w/2.69,size_h/2.32])     
                if iterator >= 3:
                    course.consoleExample(strs[3],1.44)
                    rect2 = pygame.draw.rect(screen, dark_green, [wdth+size_w/8,size_h/2.75,size_w/12,size_h/8], 0,15)
                    txt2 = Write(size_w//100*8,"+",green,[size_w/2,size_h/2.32])     
                if iterator >= 4:
                    course.consoleExample(strs[4],1.44,2)
                    activeMain = True
                    rect3 = pygame.draw.rect(screen, dark_green, [size_w/1.7,size_h/2.75,size_w/12,size_h/8], 0,15)
                    txt3 = Write(size_w//100*8,"+",green,[size_w/1.59,size_h/2.32])           
                    notBlocked = True     
                    Write(size_w//100*3,strs[5],green,[size_w/1.94,size_h/4.36])                                  
                course.consoleExample(strs[6],1.91,2.3)
            elif courseLvl == 15:
                global sec
                hght = size_h/3.2
                txthght = size_h/2.65
                if language == "ENG":
                    txts = ["Selecting specified group of items",
                    "Selecting group of items from start",
                    "Selecting group of items from end"]
                    descs = [
                        ["To select specified group of items we have to enter start and end",
                        "indexes. It looks similar to giving single index but has few",
                        "differences, syntax: list[startIndex:endIndex] | return group",
                        "from startIndex(included) to endIndex(not included)"],
                        [
                            "To select group of items from start we won't use start index,",
                            "so syntax stay like this: list[:endIndex] where endIndex is",
                            "of course not included and returned group",
                            "start from first item in list"
                        ],
                        [
                            "If we want to select group of items from end we have to",
                            "add \"-\" to our syntax, because that sign means from end",
                            "of list, so syntax: list[:-endIndex], where this time endIndex",
                            "means amount of items to be skipped beggining from end of list"
                        ]
                    ]
                    back = "Back"
                else:
                    txts = ["Określona grupa przedmiotów",
                    "Grupa przedmiotów od początku",
                    "Grupa przedmiotów od końca"]
                    descs = [
                        ["By wybrać konkretną grupę przedmiotów musimy dać pierwszy i ostatni",
                        "index. Jest to podobne do poprzedniej metody, ale bardziej rozbudowane:", 
                        "składnia: lista[pierwszyIndex:ostatniIndex] | zwraca grupę przedmiotów", 
                        "od pierwszyIndex(włącznie) do ostatniIndex(nie włączając)"], 
                        [
                            "By wybrać grupę od początku nie użyjemu startowego indexu,", 
                            "więc składnia wygląda tak: lista[:ostatniIndex] gdzie", 
                            "ostatniIndex nie jest włączony, a zwrócona grupa", 
                            "zaczyna się od pierwszego elementu listy"
                        ],
                        [
                            "Jeśli chcemy zacząć grupę od końca listy musimy dodać", 
                            "\"-\" do naszej składni, gdyż ten znak znaczy \"od końca\" listy,", 
                            "więc składnia to: lista[:-ostatniIndex], gdzie tym razem ostatniIndex", 
                            "oznacza liczbe rzeczy do ominięcia poczynając od końca listy" 
                        ]
                    ]
                    back = "Powrót"
                rects = []
                txtCords = []
                if activeMain:
                    sec = getActualSecond()
                    if language == "ENG":
                        course.dialogTop(6.41,"About indexes there's still few more","things, so let's check them out")
                    else:
                        course.dialogTop(6.41,"Co do indexów wciąż jest jeszcze pare","rzeczy, więc sprawdźmy je")
                    for it in range(3):
                        rect = pygame.draw.rect(screen, color1, [size_w/3.25,hght,size_w/2.2,size_h/8], 0,15)
                        rects.append(rect)
                        txt=Write(size_w//100*2,txts[it],color2,[size_w/1.85,txthght])
                        txtCords.append([size_w/1.85,txthght])
                        hght += size_h/6
                        txthght += size_h/6
                else:
                    storedTime = getActualSecond()-sec
                    timeToWait = 5
                    pygame.draw.rect(screen, color2, [size_w/5,size_h/16,size_w/1.5,size_h/1.1],0,10)
                    backBtn = course.centeredBtn(12.8,dark_red,back)
                    bckgr = pygame.draw.rect(screen, color1, [size_w/4.37,size_h/3.46,size_w/1.65,size_h/2], 0,10)
                    descHght = size_h/2.59
                    for desc in descs[iterator]:
                        pygame.draw.rect(screen, color2, [size_w/4.01,size_h/3.16,size_w/1.8,size_h/2.3], size_w//450,15)
                        pygame.draw.line(screen, color2, [size_w/4.01,size_h/2.3], [size_w/1.248,size_h/2.3], size_w//450)
                        pygame.draw.line(screen, color2, [size_w/4.01,size_h/1.86], [size_w/1.248,size_h/1.86], size_w//450)
                        pygame.draw.line(screen, color2, [size_w/4.01,size_h/1.57], [size_w/1.248,size_h/1.57], size_w//450)
                        if getTheme().lower() == "light":
                            WriteItalic(round(size_w//100*1.5),desc,color3,[size_w/1.91,descHght])
                        else:
                            WriteItalic(round(size_w//100*1.5),desc,dark_gray,[size_w/1.91,descHght])
                        descHght += size_h/10
                if event.type == MOUSEMOTION:
                    for rect in rects:
                        index = rects.index(rect)
                        if rect.collidepoint(mouse_pos):
                            pygame.draw.rect(screen, color3, [rect[0],rect[1],rect[2],rect[3]], size_w//450,15)
                            Write(size_w//100*2,txts[index],color3,txtCords[index])
                    if not activeMain:
                        try:
                            if backBtn.collidepoint(mouse_pos):
                                course.centeredBtn(12.8,red,back)
                        except:
                            pass
                elif event.type == MOUSEBUTTONDOWN:
                    for rect in rects:
                        index = rects.index(rect)
                        if rect.collidepoint(mouse_pos):
                            activeMain = False
                            iterator = index
                    if not activeMain:
                        try:
                            if backBtn.collidepoint(mouse_pos):
                                activeMain = True
                        except:
                            pass
                elif event.type == KEYDOWN:
                    if not activeMain and event.key == K_ESCAPE:
                        activeMain = True
            elif courseLvl == 16:
                if language == "ENG":
                    course.dialogStandard(2.6,"Great, now you know how to","select an item or group of items","from list, but what can you do","with selected?")
                else:
                    course.dialogStandard(2.6,"Świetnie, teraz wiesz jak","wybrać przedmiot lub całą","grupę z listy, ale co można","zrobić z wybranymi?")
            elif courseLvl == 17:
                iterator = 1
                if language == "ENG":
                    course.dialogTop(6.41,"You can easily change value of","selected item(s), by typing selected item","with equal sign and it's new value")
                    course.consoleExample("list[0] = new value",2.44)
                    course.consoleExample("list[1:3] = [new1,new2]",1.62)
                else:
                    course.dialogTop(6.41,"Możesz łatwo zmienić wartość","wybranych wpisując wybrany przedmiot wraz","ze znakiem równości oraz jego nową wartość",fontSize=1.3)
                    course.consoleExample("lista[0] = nowa wartość",2.44)
                    course.consoleExample("lista[1:3] = [nowe1,nowe2]",1.62)                    
            elif courseLvl == 18:
                notBlocked = False
                if language == "ENG":
                    txts = [
                        ["ingredients[1] = \"emerald\"","ingredients[1]=\"emerald\""],
                        "Now replace ingredient to fit recipe",
                        "ingredients[1] = \"emerald\"",
                        "Replace",
                        "recipe = [\"powder\",\"emerald\",\"acid\"]",
                        "ingredients = [\"powder\",\"ruby\",\"acid\"]"
                    ]
                else:
                    txts = [
                        ["składniki[1] = \"emerald\"","składniki[1]=\"emerald\""],
                        "Zastąp składnik by pasował do przepisu",
                        "składniki[1] = \"emerald\"",
                        "Zastąp",
                        "przepis = [\"proszek\",\"emerald\",\"kwas\"]",
                        "składniki = [\"proszek\",\"rubin\",\"kwas\"]"
                    ]                    
                answers = txts[0]
                course.consoleGame(txts[1],txts[2],txts[3],textLen=26,multipleAnswers=True,answersList=answers)
                course.consoleExample(txts[4],1.67,1.5)
                pygame.draw.rect(screen, color2, [size_w/1.37,size_h/2.39,size_w/10,size_h/7], width=0)
                if iterator > 1:
                    notBlocked = True
                    activeMain = True
                    pygame.draw.line(screen, green, [size_w/1.3,size_h/2.02], [size_w/1.28,size_h/1.9], size_w//450)
                    pygame.draw.line(screen, green, [size_w/1.28,size_h/1.9], [size_w/1.25,size_h/2.24], size_w//450)
                    course.consoleExample(txts[4],2.49,1.5)
                else:
                    Write(size_w//100*4,"X",red,[size_w/1.28,size_h/2.04])
                    course.consoleExample(txts[5],2.49,1.5)
            elif courseLvl == 19:
                iterator = 1
                if language == "ENG":
                    course.dialogStandard(2.6,"Great job my apprentice, but","it's not over yet, you still","have few things to learn, let's","don't waste no more time")
                else:
                    course.dialogStandard(2.6,"Świetna robota uczniu, ale to","jeszcze nie koniec, wciąż","masz jeszcze pare rzeczy do","nauczenia, nie marnujmy czasu")
            elif courseLvl == 20:
                if language == "ENG":
                    course.dialogTop(6.41,"Append() and extend() are helpful, but","those add only at the end of list,","but how to add to destinated place?")
                    course.consoleExample("list = [part1,part3,part4]",2.67)
                    course.consoleExample("list.insert(1,part2)",1.84)
                    course.consoleExample("list = [part1,part2,part3,part4]",1.4,2.3)
                else:
                    course.dialogTop(6.41,"Append() i extend() są pomocne, ale te","dodają tylko na koniec listy, jak więc","dodać coś w konkretne miejsce?")
                    course.consoleExample("lista = [część1,część3,część4]",2.67,2.3)
                    course.consoleExample("lista.insert(1,część2)",1.84)
                    course.consoleExample("lista = [część1,część2,część3,część4]",1.4,1.8)                    
            elif courseLvl == 21:
                iterator = 1
                if language == "ENG":
                    course.dialogStandard(2.6,"insert() allows to add item at","index given before item","(remember index start from 0)","Syntax: list.insert(index,item)")
                else:
                    course.dialogStandard(2.6,"insert() pozwala na dodanie","przedmiotu w podany index","(index zaczyna się od 0)","Składnia:","lista.insert(index,przedmiot)")
            elif courseLvl == 22:
                notBlocked = False
                if language == "ENG":
                    strs = [
                        ["ingredients.insert(2,\"bat eye\")","ingredients.insert(2, \"bat eye\")"],
                        "insert \"bat eye\" at index=2",
                        "Insert",
                        ["ruby powder,", "fire essence,", "moringa leaves,", "powdered black pearl"],
                        ["ruby powder,", "fire essence,","bat eye,","moringa leaves,", "powdered black pearl"],
                        "Ingredients",
                        "Well done!",
                        "Enter correct formula in box above"
                    ]
                else:
                    strs = [
                    ["składniki.insert(2,\"oko\")","składniki.insert(2, \"oko\")"],
                    "Umieść(insert) \"oko\" w miejsce index=2",
                    "Umieść",
                    ["rubinowy pył,", "esencja ognia,", "liście moringi,", "pył z czarnej perły"],
                    ["rubinowy pył,", "esencja ognia,","oko,","liście moringi,", "pył z czarnej perły"],
                    "Składniki",
                    "Brawo!",
                    "Wpisz właściwą formułę powyżej"
                    ]
                answers = strs[0]
                course.consoleGame(strs[1],"",strs[2],1.5,32,multipleAnswers=True,answersList=answers)
                if iterator <= 1:
                    ingredients = strs[3]
                else:
                    ingredients = strs[4]
                pygame.draw.rect(screen, color1, [size_w/3.11,size_h/2.25,size_w/2.6,size_h/2.5], 0,15)
                pygame.draw.rect(screen, color2, [size_w/3.29,size_h/3.02,size_w/2.4,size_h/10], width=0)
                Write(size_w//100*2,"=",color3,[size_w/2.04,size_h/2.04])
                Write(size_w//100*2,"[",lt_blue,[size_w/1.99,size_h/2.04])
                Write(size_w//100*2,strs[5],dark_green,[size_w/2.43,size_h/2.04])
                hght = size_h/1.81
                wdth = size_w/1.75
                for item in ingredients:    
                    if ingredients.index(item) == 3 and iterator <= 1:
                        wdth = size_w/1.85   
                    elif iterator > 1: 
                        if ingredients.index(item) == 4: 
                            wdth = size_w/1.85 
                        elif ingredients.index(item) == 2:
                            wdth = size_w/1.68
                        else:
                            wdth =  size_w/1.75        
                    Write(size_w//100*2,item,orange,[wdth,hght])
                    hght += size_w/40
                if iterator > 1:
                    Write(size_w//100*2,"]",lt_blue,[size_w/1.97,size_h/1.28])
                    notBlocked = True
                    activeMain = True
                    Write(size_w//100*2,strs[6],green,[size_w/1.97,size_h/2.65])
                else:
                    Write(size_w//100*2,"]",lt_blue,[size_w/1.97,size_h/1.36])
                    Write(size_w//100*2,strs[7],red,[size_w/1.97,size_h/2.65])
            elif courseLvl == 23:
                iterator = 1
                if language == "ENG":
                    course.dialogStandard(2.6,"Hmm, seems like we got too","many products so you have to","remove one 'cause it can","destroy results of our work,","let me show you how")
                else:
                    course.dialogStandard(2.6,"Hmm wygląda, że mamy za","dużo produktów, więc musisz","usunąć jeden, ponieważ","to może zniszczyć rezultaty","naszej pracy, pokaże Ci")
            elif courseLvl == 24:
                if language == "ENG":
                    txts = ["Remove()",
                    "Pop()",
                    "Del"]
                    syntax = ["list.remove(item)",
                    "list.pop(index)",
                    "del list[index]"]
                    descs = [
                        ["list = [item1,item2,item3,item4]",
                        "Remove() function allow us to delete direct item from list",
                        "list.remove(item3)",
                        "list = [item1,item2,item4]"],
                        [
                            "list = [item1,item2,item3,item4]",
                            "Pop() allow us to delete item with direct index from list,",
                            "list.pop() | list.pop(1)",
                            "list = [item1,item2,item3] | list = [item1,item3,item4]"
                        ],
                        [
                            "list = [item1,item2,item3,item4]",
                            "Del allow us to delete item with direct index or even all list",
                            "del list[1] | del list",
                            "list = [item1,item3,item4] | None"
                        ]
                    ]
                    back = "Back"
                    threeWays = "There are three ways to do that:"
                else:
                    txts = ["Remove()",
                    "Pop()",
                    "Del"]
                    syntax = ["lista.remove(obiekt)",
                    "lista.pop(index)",
                    "del lista[index]"]
                    descs = [
                        ["lista = [obiekt1,obiekt2,obiekt3,obiekt4]",
                        "Funkcja remove() pozwala usunać konkretny obiekt z listy",
                        "lista.remove(obiekt3)",
                        "lista = [obiekt1,obiekt2,obiekt4]"],
                        [
                            "lista = [obiekt1,obiekt2,obiekt3,obiekt4]",
                            "Pop() pozwala na usunięcie z listy obiektu o danym indexie,",
                            "lista.pop() | lista.pop(1)",
                            "lista = [obiekt1,obiekt2,obiekt3] | lista = [obiekt1,obiekt3,obiekt4]"
                        ],
                        [
                            "lista = [obiekt1,obiekt2,obiekt3,obiekt4]",
                            "Del pozwala usunąć obiekt o określonycm indexie lub nawet całą liste",
                            "del lista[1] | del lista",
                            "lista = [obiekt1,obiekt3,obiekt4] | None"
                        ]
                    ]
                    back = "Powrót"
                    threeWays = "Są na to trzy sposoby:"
                hght = size_h/3.2
                txthght = size_h/2.65
                rects = []
                txtCords = []
                if activeMain:
                    #sec = getActualSecond()
                    course.dialogTop(6.41,threeWays)
                    for it in range(3):
                        rect = pygame.draw.rect(screen, color1, [size_w/3.25,hght,size_w/2.2,size_h/8], 0,15)
                        rects.append(rect)
                        txt=Write(size_w//100*2,txts[it],color2,[size_w/1.85,txthght])
                        txtCords.append([size_w/1.85,txthght])
                        hght += size_h/6
                        txthght += size_h/6
                else:
                    #storedTime = getActualSecond()-sec
                    #timeToWait = 5
                    pygame.draw.rect(screen, color2, [size_w/5,size_h/16,size_w/1.5,size_h/1.1],0,10)
                    backBtn = course.centeredBtn(12.8,dark_red,back)
                    bckgr = pygame.draw.rect(screen, color1, [size_w/4.37,size_h/3.46,size_w/1.65,size_h/2], 0,10)
                    descHght = size_h/2.59
                    if isinstance(chosen,int):
                        for desc in descs[chosen]:
                            pygame.draw.rect(screen, color2, [size_w/4.01,size_h/3.16,size_w/1.8,size_h/2.3], size_w//450,15)
                            pygame.draw.line(screen, color2, [size_w/4.01,size_h/2.3], [size_w/1.248,size_h/2.3], size_w//450)
                            pygame.draw.line(screen, color2, [size_w/4.01,size_h/1.86], [size_w/1.248,size_h/1.86], size_w//450)
                            pygame.draw.line(screen, color2, [size_w/4.01,size_h/1.57], [size_w/1.248,size_h/1.57], size_w//450)
                            if getTheme().lower() == "light":
                                WriteItalic(round(size_w//100*1.5),desc,color3,[size_w/1.91,descHght])
                            else:
                                WriteItalic(round(size_w//100*1.5),desc,dark_gray,[size_w/1.91,descHght])
                            descHght += size_h/10
                if event.type == MOUSEMOTION:
                    for rect in rects:
                        index = rects.index(rect)
                        if rect.collidepoint(mouse_pos):
                            pygame.draw.rect(screen, color1, [rect[0],rect[1],rect[2],rect[3]], 0,15)
                            pygame.draw.rect(screen, color3, [rect[0],rect[1],rect[2],rect[3]], size_w//450,15)
                            Write(size_w//100*2,syntax[index],color3,txtCords[index])
                    if not activeMain:
                        try:
                            if backBtn.collidepoint(mouse_pos):
                                course.centeredBtn(12.8,red,back)
                        except:
                            pass
                elif event.type == MOUSEBUTTONDOWN:
                    for rect in rects:
                        index = rects.index(rect)
                        if rect.collidepoint(mouse_pos):
                            activeMain = False
                            chosen = index
                    if not activeMain:
                        try:
                            if backBtn.collidepoint(mouse_pos):
                                activeMain = True
                        except:
                            pass
                elif event.type == KEYDOWN:
                    if not activeMain and event.key == K_ESCAPE:
                        activeMain = True
            elif courseLvl == 25: 
                if language == "ENG":
                    answer = [
                        "products.remove(magic ruby)",
                        "products.pop(2)",
                        "del products[2]",
                    ]
                    txts = [
                        "Get rid of magic ruby",
                        "Remove",
                        "products = [dymerit,water essence,magic ruby,cursed stone]",
                        "products = [dymerit,water essence,cursed stone]"
                    ]
                    fontSize = 1.2
                    lenText = 29
                    gameFontSize = 2
                else:
                    answer = [
                        "produkty.remove(magiczny rubin)",
                        "produkty.pop(2)",
                        "del produkty[2]",
                    ]
                    txts = [
                        "Pozbądź się magicznego rubinu",
                        "Usuń",
                        "produkty = [dymerit,esencja wody,magiczny rubin,przeklęty kamień]",
                        "produkty = [dymerit,esencja wody,przeklęty kamień]"
                    ]
                    fontSize = 1
                    lenText = 33
                    gameFontSize = 1.7
                course.consoleGame(txts[0],"",txts[1],textLen=lenText,multipleAnswers=True,answersList=answer,fontSize2=gameFontSize,fontSize=gameFontSize)
                pygame.draw.rect(screen, color2, [size_w/1.37,size_h/2.14,size_w/10,size_h/7], width=0)
                if iterator<2:
                    notBlocked = False
                    Write(size_w//100*4,"X",red,[size_w/1.28,size_h/1.82])
                    course.consoleExample(txts[2],2.2,fontSize)
                else:
                    notBlocked = True
                    course.consoleExample(txts[3],2.2,1.4)
                    pygame.draw.line(screen, green, [size_w/1.3,size_h/1.85], [size_w/1.28,size_h/1.7], size_w//450)
                    pygame.draw.line(screen, green, [size_w/1.28,size_h/1.7], [size_w/1.25,size_h/1.98], size_w//450)
            elif courseLvl == 26:
                iterator = 1
                if language == "ENG":
                    txts = [
                        "We're almost done here",
                        "Now let's sort the rest by",
                        "sort() function",
                        "products = [dymerit,water essence,cursed stone]",
                        "products.sort()",
                        "products = [cursed stone,dymerit,water essence]",
                    ]
                else:
                    txts = [
                        "Już prawie skończyliśmy",
                        "Posortujmy teraz resztę",
                        "funkcją sort()",
                        "produkty = [dymerit,esencja wody,przeklęty kamień]",
                        "produkty.sort()",
                        "produkty = [przeklęty kamień,dymerit,esencja wody]",
                    ]                    
                course.dialogTop(6.41,txts[0],txts[1],txts[2])
                course.consoleExample(txts[3],2.69,fontSize=1.4)
                course.consoleExample(txts[4],1.85)
                course.consoleExample(txts[5],1.43,1.4)
            elif courseLvl == 27: 
                if language == "ENG":
                    txts = [
                        "As you can see sort() function",
                        "sorts list elements alphabetically",
                        "or from lowest to highest if it's",
                        "about integers. You can also",
                        "give argument reverse=True",
                        "list.sort(reverse=True)",
                        "that will sort list inversely"
                    ]
                else:
                    txts = [
                        "Jak widzisz funkcja sort()",
                        "sortuje obiekty alfabetycznie lub",
                        "od najniższego do najwyższego",
                        "W przypadku typu integer/float",
                        "Jest też argument reverse:",
                        "list.sort(reverse=True) - teraz",
                        "lista jest sortowana odwrotnie"
                    ]                    
                course.dialogStandard(2.5,txts[0],txts[1],txts[2],txts[3],txts[4],txts[5],txts[6])
            elif courseLvl == 28: 
                if language == "ENG":
                    txts = [
                        "Congrats my appretince!",
                        "Potion is finally done(so is Lesson 3)!",
                        "Finish"
                    ]
                else:
                    txts = [
                        "Gratulacje mój uczniu!",
                        "Eliksir ukończony(tak jak lekcja 3)!",
                        "Ukończ"
                    ]                    
                potion = pygame.image.load(r"{}/Images/Game/potion.png".format(dirPath))
                potion = pygame.transform.scale(potion,[int(size_w/10.6),int(size_h/3)])
                course.dialogTop(6.41,txts[0],txts[1])
                screen.blit(potion,[size_w/2.08,size_h/3.04])
                finishBtn = course.centeredBtn(1.25,dark_green,txts[2])
                if event.type == MOUSEMOTION:
                    if finishBtn.collidepoint(mouse_pos):
                        course.centeredBtn(1.25,green,txts[2])
                        pygame.draw.rect(screen, dark_green, [size_w/2.16,size_h/1.25,size_w/8,size_h/10], size_w//450,15)
                elif event.type == MOUSEBUTTONDOWN:
                    if finishBtn.collidepoint(mouse_pos):
                        if getCourseLvl() < 4:
                            changeCourselvl(4)
                        activeMenu = True
                        courseLvl = 1  
                        iterator = 1 
                        bckgrMusicPlayed = False
    def lesson4():
        global mentorIcon,activeMain,held,courseLvl,notBlocked,iterator,activeMenu,notBlocked
        global storedCords,done,language,chosen,loadingBar,storedTime,TD_lvlType,TD_Lvls,TD_iterator
        global TD_count,TD_subDone,TD_toDefeat,TD_done,TD_consoleTxts,wrong,TD_consoleShown
        global bckgrMusicPlayed,errorShowed,TD_unitsPassed
        language = getLang()
        if activities[0] and not activeMenu and str(activeLesson)[17:-23]=="lesson4" and not errorShowed:
            try:
                mentorIcon = pygame.image.load(r"{}/Images/Game/wizard.png".format(dirPath))
                mentorIcon = pygame.transform.scale(mentorIcon, [int(size_w/10.6),int(size_h/6)])
            except:
                errorInit("Failed to load mentor icon!",fontSize=1.8)
            if activeMain and not errorShowed:
                if courseLvl in TD_Lvls:
                    course.standardLessonEvents("lesson4",19,condition=notBlocked,standard=False,customCol=TD_darkGreen) 
                else:
                    course.standardLessonEvents("lesson4",19,condition=notBlocked) 
            if courseLvl == 1:
                if language == "ENG":
                    txts = [
                        "Now when potion is ready we",
                        "can start the fun part, come",
                        "along and let me show you why",
                        "this potion was so important"
                    ]
                else:
                    txts = [
                        "Teraz możemy rozpocząć",
                        "zabawniejszą część, chodź",
                        "ze mną, pokaże Ci dlaczego",
                        "ten eliksir jest tak ważny"
                    ]
                course.dialogStandard(2.6,txts[0],txts[1],txts[2],txts[3])
            elif courseLvl == 2:
                if language == "ENG":
                    txts = [
                        "Strange evil forces",
                        "are pushing through magic",
                        "forest and we need to stop them"
                    ]
                else:
                    txts = [
                        "Dziwne, mroczne siły",
                        "kroczą przez magiczny las,",
                        "musimy zatem je powstrzymać"
                    ]                    
                course.dialogStandard(2.6,txts[0],txts[1],txts[2])
            elif courseLvl == 3:
                notBlocked = False
                if language == "ENG":
                    txts = [
                        "To accomplish that we need help,",
                        "we need guards and this",
                        "potion will help us with that",
                        "Okay"              
                    ]
                else:
                    txts = [
                        "By to wykonać potrzebujemy pomocy,",
                        "potrzebujemy obrońców, a ten",
                        "eliksir pomoże nam w tym",
                        "Dalej"              
                    ]
                course.tower_defence.drawMap(guards=False)
                course.dialogTop(6.41,txts[0],txts[1],txts[2],bckgr=True)
                okBtn = course.tower_defence.nextBtn(dark_green,txts[3])
                if event.type == MOUSEMOTION:
                    if okBtn.collidepoint(mouse_pos):
                        okBtn = course.tower_defence.nextBtn(green,txts[3],True,dark_green)
                elif event.type == MOUSEBUTTONDOWN:
                    if okBtn.collidepoint(mouse_pos):
                        courseLvl += 1
            elif courseLvl == 4:
                notBlocked = False
                if language == "ENG":
                    txts = [
                        f"Spill potion at shown places {len(storedCords)}/4",
                        "(click it and wait until it spilling ends)",
                        "Good, we can go futher,",
                        "click arrow in the bottom right",
                        "corner when you're ready"
                    ]
                    fontSize = 1.5
                else:
                    txts = [
                        f"Rozlej eliksir we wskazanych miejscach {len(storedCords)}/4",
                        "(kliknij i czekaj, aż zakończy się)",
                        "Dobrze, możemy iść dalej,",
                        "klinij strzałkę w prawym dolnym",
                        "rogu, gdy tylko będziesz gotowy"
                    ]   
                    fontSize = 1.3  
                if not isinstance(chosen,int):               
                    course.tower_defence.drawMap(guards=False)
                course.tower_defence.makingGuards()
                if len(storedCords) < 4:
                    course.dialogTop(6.41,txts[0],txts[1],bckgr=True,fontSize=fontSize)
                elif len(storedCords) >= 4:
                    notBlocked = True
                    course.dialogTop(6.41,txts[2],txts[3],txts[4],bckgr=True)
            elif courseLvl == 5:
                storedCords = []
                chosen = ""
                selected = ""
                storedTime = ""
                done = False
                if language == "ENG":
                    txts = [
                        "Great job! Now we have to",
                        "give potion some time so it",
                        "can do it's job, now",
                        "I will show something you",
                        "will need during fight"
                    ]
                else:
                    txts = [
                        "Brawo! Teraz musimy dać",
                        "eliksirowi troche czasu, by",
                        "mógł wypełnić swoje zadanie,",
                        "a ja pokażę ci coś co może",
                        "się przydać podczas walki"
                    ]
                course.dialogStandard(2.6,txts[0],txts[1],txts[2],txts[3],txts[4])
            elif courseLvl == 6:
                if language == "ENG":
                    txts = [
                        "You see, there might be a need to",
                        "change our guardians instructions",
                        "in case of unforeseen circumstances",
                        "and then we will use if instruction"
                        ]
                    statement = "statement:"
                    action = "action"
                else:
                    txts = [
                        "Widzisz, może zaistnieć potrzeba, by",
                        "zmienić instrukcje naszych obrońców",
                        "w wypadku nieprzewidzianych zdarzeń,",
                        "a do tego użyjemy instrukcji if"
                        ]  
                    statement = "warunek:"
                    action = "akcja"
                course.dialogTop(6.41,txts[0],txts[1],txts[2],txts[3])
                course.consoleExample(f"if {statement}",hght=2.16,left=True)
                course.consoleExample(f"{action}",hght=1.6)
                course.tower_defence.clearAdminTools()
            elif courseLvl == 7:
                global sec
                events = [MOUSEMOTION,KEYDOWN,KEYUP,MOUSEBUTTONDOWN]
                for item in events:
                    if pygame.event.get_blocked(item):
                        pygame.event.set_allowed(item)
                hght = size_h/3.2
                txthght = size_h/2.65
                if language == "ENG":
                    txts = ["If Syntax",
                    "Elif Syntax",
                    "Else Syntax"]
                    descs = [
                        ["IF dictate statements that need to be fuflfilled to perform",
                        "given action. Remember about \":\" at the end of statement", 
                        "line and tabulation line below, just before action",
                        "to be made if statement is correct",
                        "if statement:",
                        "           action"
                        ],
                        [
                            "ELIF works similarly to IF, but it's checking it's own statement when",
                            "IF before it is not fulfilled and of course it's own statement is fulfilled",
                            "if statement1:",
                            "           action",
                            "elif statement2:",
                            "           action"
                        ],
                        [
                            "ELSE on the other hand is kind of opposite to IF keyword, but it's used",
                            "along with it. ELSE works when statement of related if is not fulfilled.",
                            "if statement1:",
                            "           action",
                            "else:",
                            "           action"
                        ]
                    ]
                    back = "Back"
                else:
                    txts = ["Składnia If",
                    "Składnia Elif",
                    "Składnia Else"]
                    descs = [
                        ["IF stawia warunki, które muszą zostać wypełnione, aby wykonać",
                        "daną akcję. Pamiętaj o \":\" na końcu linijki sprawdzającej", 
                        "warunek oraz o tabie linijkę niżej, zaraz przed zdefiniowaniem",
                        "akcji do wykonania, jeśli warunek zostanie spełniony", 
                        "if warunek:",
                        "           akcja"
                        ],
                        [
                            "ELIF działa podobnie do IF, ale sprawdza swój warunek, gdy poprzednie",
                            "IF nie jest spełnione i oczywiście sam jego warunek jest spełniony",
                            "if warunek:",
                            "           akcja",
                            "elif warunek:",
                            "           akcja"
                        ],
                        [
                            "ELSE z drugiej strony działa inaczej niż IF oraz ELIF, choć jest używane",
                            "z nimi. ELSE wykona się, gdy warunek IF przed ELSE nie jest spełniony.",
                            "if statement1:",
                            "           action",
                            "else:",
                            "           action"
                        ]
                    ]
                    back = "Powrót"
                rects = []
                txtCords = []
                if activeMain:
                    sec = getActualSecond()
                    if language == "ENG":
                        course.dialogTop(6.41,"So here's what you need","to know before start")
                    else:
                        course.dialogTop(6.41,"Tak więc oto czego potrzebujesz","zanim pójdziemy dalej")
                    for it in range(3):
                        rect = pygame.draw.rect(screen, color1, [size_w/3.25,hght,size_w/2.2,size_h/8], 0,15)
                        rects.append(rect)
                        txt=Write(size_w//100*2,txts[it],color2,[size_w/1.85,txthght])
                        txtCords.append([size_w/1.85,txthght])
                        hght += size_h/6
                        txthght += size_h/6
                else:
                    storedTime = getActualSecond()-sec
                    timeToWait = 5
                    pygame.draw.rect(screen, color2, [size_w/5,size_h/16,size_w/1.5,size_h/1.1],0,10)
                    backBtn = course.centeredBtn(12.8,dark_red,back)
                    bckgr = pygame.draw.rect(screen, color1, [size_w/4.36,size_h/4.68,size_w/1.65,size_h/1.44], 0,10)
                    descHght = size_h/3.31
                    for desc in descs[iterator]:
                        if getTheme().lower() == "light":
                            WriteItalic(round(size_w//100*1.5),desc,color3,[size_w/1.91,descHght])
                        else:
                            WriteItalic(round(size_w//100*1.5),desc,dark_gray,[size_w/1.91,descHght])
                        descHght += size_h/10
                    pygame.draw.rect(screen, color2, [size_w/4.01,size_h/3.96,size_w/1.8,size_h/1.65], size_w//450,15)
                    lineHght = size_h/2.89
                    for it in range(5):
                        pygame.draw.line(screen, color2, [size_w/4.01,lineHght], [size_w/1.248,lineHght], size_w//450)
                        lineHght += size_h/10
                if event.type == MOUSEMOTION:
                    for rect in rects:
                        index = rects.index(rect)
                        if rect.collidepoint(mouse_pos):
                            pygame.draw.rect(screen, color3, [rect[0],rect[1],rect[2],rect[3]], size_w//450,15)
                            Write(size_w//100*2,txts[index],color3,txtCords[index])
                    if not activeMain:
                        try:
                            if backBtn.collidepoint(mouse_pos):
                                course.centeredBtn(12.8,red,back)
                        except:
                            pass
                elif event.type == MOUSEBUTTONDOWN:
                    for rect in rects:
                        index = rects.index(rect)
                        if rect.collidepoint(mouse_pos):
                            activeMain = False
                            iterator = index
                    if not activeMain:
                        try:
                            if backBtn.collidepoint(mouse_pos):
                                activeMain = True
                        except:
                            pass
                elif event.type == KEYDOWN:
                    if not activeMain and event.key == K_ESCAPE:
                        activeMain = True
            elif courseLvl == 8:
                notBlocked = False
                storedTime = ""
                iterator = 1
                if language == "ENG":
                    course.dialogTop(6.41,"So that's all I wanted to teach","you before fight, ready?")  
                    ready = "Ready"
                else:
                    course.dialogTop(6.41,"To wszystko czego chciałem cię","nauczyć przed walką, gotowy?") 
                    ready = "Gotów"
                startBtn = course.centeredBtn(2.19,dark_green,ready)      
                
                if event.type == MOUSEMOTION:
                    if startBtn.collidepoint(mouse_pos):
                            course.centeredBtn(2.19,green,"")  
                            course.centeredBtn(2.19,dark_green,ready,size_w//450) 
                elif event.type == MOUSEBUTTONDOWN:
                    if startBtn.collidepoint(mouse_pos):
                            courseLvl += 1
            elif courseLvl == 9:
                unitBeingShowed = False
                TD_count = 0
                course.eventsReset()
                course.tower_defence.drawMap()
                course.tower_defence.clearAdminTools()
                if language == "ENG":
                    wave = "First wave"
                else:
                    wave = "Fala pierwsza"
                startBtn = course.centeredBtn(2.98,purple,wave,fontSize=1.6)
                if isinstance(storedTime,float):
                    if storedTime > 56:
                        storedTime -= 3
                    correctEvent = event.type == KEYDOWN or event.type==KEYUP
                    if getActualSecond()-storedTime>=0.5 and TD_subDone and correctEvent:
                        #course.tower_defence.reset()
                        course.tower_defence.drawMap()
                        course.tower_defence.adminTools()
                        course.tower_defence.console()
                        courseLvl += 1
                    else:
                        enemyGhost = pygame.image.load(r"{}/Images/Game/2dmap/ghost.png".format(dirPath))
                        enemyGhost = pygame.transform.scale(enemyGhost, [int(size_w/5.33),int(size_h/3)])
                        enemyGhost = pygame.transform.flip(enemyGhost, True, False)
                        if language == "ENG":
                            course.tower_defence.showUnit(enemyGhost,"Phantom",wave)
                            WriteItalic(round(size_w//100*3),"Press any key to start...",lt_gray,[size_w/1.88,size_h/9.6])
                        else:
                            course.tower_defence.showUnit(enemyGhost,"Phantom",wave)
                            WriteItalic(round(size_w//100*3),"Wciśnij dowolny przycisk...",lt_gray,[size_w/1.88,size_h/9.6])                            
                        unitBeingShowed = True
                if not unitBeingShowed and not TD_subDone:
                    if language == "ENG":
                        course.dialogTop(6.41,"My beautiful archespors are ready,","time to face evil forces",bckgr=True)
                    else: 
                        course.dialogTop(6.41,"Moje piękne archespory są gotowe,","czas stawić czoła złu",bckgr=True)

                if event.type == KEYDOWN and TD_subDone:
                    course.tower_defence.reset()
                if event.type == MOUSEMOTION and not unitBeingShowed:
                    if startBtn.collidepoint(mouse_pos):
                        course.centeredBtn(2.98,logoBlue,"",fontSize=1.6)
                        course.centeredBtn(2.98,dark_blue,wave,fontSize=1.6,border=size_w//150)
                elif event.type == MOUSEBUTTONDOWN and not unitBeingShowed:
                    if startBtn.collidepoint(mouse_pos):
                        storedTime = getActualSecond()
                        TD_subDone = True
            elif courseLvl == 10:
                storedTime = ""
                TD_lvlType = "onlyenemy"
                TD_toDefeat = 4
                course.tower_defence.drawMap()
                course.tower_defence.adminTools()
                course.tower_defence.console()
            elif courseLvl == 11:
                unitBeingShowed = False
                course.eventsReset()
                course.tower_defence.drawMap()
                course.tower_defence.adminTools()
                course.tower_defence.console()
                continueBtn = course.centeredBtn(2.53,green,"Continue",fontSize=1.7,adjustToDialog=True)

                if isinstance(storedTime,float):
                    if storedTime > 56:
                        storedTime -= 3
                    correctEvent = event.type == KEYDOWN or event.type==KEYUP
                    if getActualSecond()-storedTime>=0.5 and TD_subDone and correctEvent:
                        #course.tower_defence.reset()
                        course.tower_defence.drawMap()
                        course.tower_defence.adminTools()
                        course.tower_defence.console()
                        courseLvl += 1
                    else:
                        friendJav = pygame.image.load(r"{}/Images/Game/2dmap/jav.png".format(dirPath))
                        friendJav = pygame.transform.scale(friendJav, [int(size_w/5.33),int(size_h/3)])
                        course.tower_defence.showUnit(friendJav,"Jav","Second Wave")
                        WriteItalic(round(size_w//100*3),"Press any key to start...",lt_gray,[size_w/1.88,size_h/9.6])
                        unitBeingShowed = True
                if not unitBeingShowed and not TD_subDone:
                    course.dialogTop(6.41,"Ready for more? I bet you are!","But wait, are those Javs?","Javs! Our friends!",bckgr=True)
                if event.type == KEYDOWN or event.type == KEYUP and TD_subDone:
                    course.tower_defence.reset()
                elif event.type == MOUSEMOTION and not unitBeingShowed:
                    if continueBtn.collidepoint(mouse_pos):
                        course.centeredBtn(2.53,dark_green,"Continue",fontSize=1.7,adjustToDialog=True,border=size_w//250)
                elif event.type == MOUSEBUTTONDOWN and not unitBeingShowed:
                    if continueBtn.collidepoint(mouse_pos):
                        storedTime = getActualSecond()
                        TD_subDone = True  
            elif courseLvl == 12:
                notBlocked = False
                course.tower_defence.drawMap()
                course.tower_defence.console()
                course.eventsReset()

                if language == "ENG":
                    ready = "Ready"
                    console = "Console"
                    continuee = "Continue"
                    next = "Next"
                else:
                    ready = "Gotów"
                    console = "Konsola"
                    continuee = "Kontynuuj"
                    next = "Dalej" 

                if TD_count == 0:
                    if language == "ENG":
                        course.dialogTop(6.41,"But as friends are approaching","we have to adjust our defenses",bckgr=True)
                    else:
                        course.dialogTop(6.41,"Ale jako, że nadciągają przyjaciele","musimy dostosować obronę",bckgr=True)
                elif TD_count == 1:
                    if not TD_consoleShown:
                        if language == "ENG":
                            course.dialogTop(6.41,"Click marked button",bckgr=True)
                        else:
                            course.dialogTop(6.41,"Wciśnij oznaczony przycisk",bckgr=True)
                        pygame.draw.rect(screen, red, [size_w/4.99,size_h/3.8,size_w/30,size_h/5.8], size_w//250,size_w//150)
                        pygame.draw.line(screen, red, [size_w/4.14,size_h/3.59], [size_w/3.83,size_h/3.92], size_w//250)
                        pygame.draw.line(screen, red, [size_w/4.14,size_h/3.06], [size_w/3.83,size_h/3.27], size_w//250)
                        pygame.draw.line(screen, red, [size_w/4.14,size_h/2.41], [size_w/3.83,size_h/2.27], size_w//250)
                        pygame.draw.line(screen, red, [size_w/4.14,size_h/2.63], [size_w/3.83,size_h/2.5], size_w//250)
                    else:
                        if language == "ENG":
                            consoleTxts = [
                                "We will use if/else that you learnt earlier.",
                                "As statement you can give either friend or",
                                "enemy keyword and wait() or attack() as",
                                "action. Remeber we can't harm Javs!"
                            ]
                            next = "Next"
                            fontSizeConsole = 1.5
                        else:
                            consoleTxts = [
                                "Użyjemy if/else którego nauczyliśmy się wcześniej.",
                                "Jako argument można dać słowo friend lub",
                                "enemy oraz funkcje wait() lub attack() jako",
                                "akcje. Pamiętaj, że nie możemy zranić Javów!"
                            ]
                            next = "Dalej" 
                            fontSizeConsole = 1.3                           
                        course.dialogTop(6.41,consoleTxts[0],consoleTxts[1],consoleTxts[2],consoleTxts[3],bckgr=True,fontSize=fontSizeConsole)
                        consoleNextBtn = course.centeredBtn(2.13,dark_green,next,adjustToDialog=True)
                        if event.type == MOUSEMOTION:
                            try:
                                if consoleNextBtn.collidepoint(mouse_pos):
                                    course.centeredBtn(2.13,green,next,adjustToDialog=True)
                                    course.centeredBtn(2.13,dark_green,"",adjustToDialog=True,border=size_w//250)
                            except:
                                pass
                elif TD_count == 2:
                    if language == "ENG":
                        consoleTxts = [
                            "Here's an example:",
                            "if enemy:",
                            "        attack()",
                            "Try doing it with keyword 'friend'",
                            "and wait() function!"
                        ]
                    else:
                        consoleTxts = [
                            "Oto przykład:",
                            "if enemy:",
                            "        attack()",
                            "Spróbuj tego ze słowem friend i funkcją wait()"
                        ]
                    if TD_consoleShown:
                        if language == "ENG":
                            course.dialogTop(6.41,consoleTxts[0],consoleTxts[1],consoleTxts[2],consoleTxts[3],consoleTxts[4],bckgr=True)
                        else:
                            course.dialogTop(6.41,consoleTxts[0],consoleTxts[1],consoleTxts[2],consoleTxts[3],bckgr=True,fontSize=1.4)
                        consoleNextBtn = course.centeredBtn(1.83,dark_green,"Ok",adjustToDialog=True)
                        if event.type == MOUSEMOTION:
                            try:
                                if consoleNextBtn.collidepoint(mouse_pos):
                                    course.centeredBtn(1.83,green,"Ok",adjustToDialog=True)
                                    course.centeredBtn(1.83,dark_green,"",adjustToDialog=True,border=size_w//250)
                            except:
                                pass
                elif TD_count == 3 and not TD_consoleShown:                       
                    #TODO translating ENG->PL
                    if language == "ENG":
                        course.dialogTop(6.41,"Are you ready to go further?",bckgr=True)
                    else:
                        course.dialogTop(6.41,"Jesteś gotów iść dalej?",bckgr=True)
                    readyBtn = course.centeredBtn(4.11,dark_green,ready,adjustToDialog=True)
                    correctCommands = TD_consoleTxts[0] == "if friend:" and TD_consoleTxts[1] == "wait()"
                    if event.type == MOUSEMOTION:
                        if readyBtn.collidepoint(mouse_pos):
                            course.centeredBtn(4.11,green,ready,adjustToDialog=True)
                            course.centeredBtn(4.11,dark_green,"",adjustToDialog=True,border=size_w//250)
                    elif event.type == MOUSEBUTTONDOWN:
                        if readyBtn.collidepoint(mouse_pos):
                            if correctCommands:
                                courseLvl += 1
                                TD_count = 0
                                wrong = False
                                course.tower_defence.reset()
                            else:
                                wrong = True
                    if not correctCommands and wrong:
                        pygame.draw.rect(screen, color2, [size_w/2.49,size_h/2.64,size_w/3,size_h/3], 0,size_w//150)
                        pygame.draw.rect(screen, color1, [size_w/2.49,size_h/2.64,size_w/3,size_h/3], size_w//250,size_w//150)
                        if language == "ENG":
                            Write(round(size_w//100*1.5),"Commands are not correct!",red,[size_w/1.75,size_h/2.33])
                            Write(round(size_w//100*1.5),"Continue anyway?",red,[size_w/1.75,size_h/1.99])
                        else:
                            Write(round(size_w//100*1.5),"Komendy nie są poprawne!",red,[size_w/1.75,size_h/2.33])
                            Write(round(size_w//100*1.5),"Kontynuować mimo to?",red,[size_w/1.75,size_h/1.99])                            
                        consoleBtn = pygame.draw.rect(screen, dark_green, [size_w/2.31,size_h/1.8,size_w/8,size_h/10], 0,size_w//250)
                        Write(round(size_w//100*1.7),console,color1,[size_w/2.03,size_h/1.66])
                        continueBtn = pygame.draw.rect(screen, dark_green, [size_w/1.73,size_h/1.8,size_w/8,size_h/10], 0,size_w//250)
                        Write(round(size_w//100*1.7),continuee,color1,[size_w/1.56,size_h/1.66])
                if not TD_consoleShown and TD_count == 0:
                    nextBtn = course.centeredBtn(2.82,dark_green,next,adjustToDialog=True)
                if event.type == MOUSEMOTION:
                    try:
                        if nextBtn.collidepoint(mouse_pos):
                            course.centeredBtn(2.82,green,next,adjustToDialog=True)
                            course.centeredBtn(2.82,dark_green,"",adjustToDialog=True,border=size_w//250)
                    except:
                        pass
                    try:
                        if consoleBtn.collidepoint(mouse_pos):
                            pygame.draw.rect(screen, green, [size_w/2.31,size_h/1.8,size_w/8,size_h/10], 0,size_w//250)
                            Write(round(size_w//100*1.7),console,color1,[size_w/2.03,size_h/1.66])
                        if continueBtn.collidepoint(mouse_pos):
                            pygame.draw.rect(screen, green, [size_w/1.73,size_h/1.8,size_w/8,size_h/10], 0,size_w//250)
                            Write(round(size_w//100*1.7),continuee,color1,[size_w/1.56,size_h/1.66])
                    except:
                        pass
                elif event.type == MOUSEBUTTONDOWN:
                    try:
                        if nextBtn.collidepoint(mouse_pos) and TD_count !=1:
                            TD_count += 1
                    except:
                        pass
                    try:
                        if consoleNextBtn.collidepoint(mouse_pos):
                            TD_count += 1
                    except:
                        pass
                    try:
                        if consoleBtn.collidepoint(mouse_pos):
                            TD_consoleShown = True
                        if continueBtn.collidepoint(mouse_pos):
                            courseLvl += 1
                            TD_count = 0
                            course.tower_defence.reset()
                    except:
                        pass
            elif courseLvl == 13:
                storedTime = ""
                TD_lvlType = "onlyfriend"
                TD_toDefeat = 3
                TD_iterator = 2
                course.tower_defence.drawMap()
                course.tower_defence.adminTools()
                course.tower_defence.console()      
            elif courseLvl == 14:
                notBlocked = False
                course.tower_defence.drawMap()
                course.tower_defence.console()
                course.eventsReset()  
                if language == "ENG":
                    strs = [
                        "Now when we already told our",
                        "archespors to not attack friends,",
                        "let's ensure ourselves that enemies", 
                        "will be attacked as they should",
                        "Add 'else' or 'elif enemy' after",
                        "existing 'if' controlling friends",
                        "and use attack() function",
                        "That's the spirit! I heard of some",
                        "dwarfs trying to escape werewolfs",
                        "hordes attacking, get ready!"
                    ]
                    next = "Next"
                    console = "Console"
                    ready = "Ready"
                else:
                    strs = [
                        "Teraz, gdy nauczyliśmy nasze",
                        "archespory, by nie atakować przyjaciół,",
                        "upewnijmy się, żeby wrogowie byli", 
                        "atakowani tak jak powinni",
                        "Dodaj 'else' lub 'elif enemy' po",
                        "isniejącym 'if' kontrolującym",
                        "przyjaciół i użyj funkcji attack()",
                        "O to chodzi! Słyszałem o krasnoludach",
                        "próbujących uciec przed hordą",
                        "wilkołaków, przygotuj się!"
                    ]
                    next = "Dalej"
                    console = "Konsola"
                    ready = "Gotów"                    

                commandsCorrect = TD_consoleTxts[2] in ['else:','elif enemy:'] and TD_consoleTxts[3] == 'attack()'

                if not TD_consoleShown:
                    if TD_count == 0:
                        course.dialogTop(6.41,strs[0],strs[1],strs[2],strs[3],bckgr=True)    
                        nextBtn = course.centeredBtn(2.15,dark_green,next,adjustToDialog=True)
                    elif TD_count == 3:
                        if not commandsCorrect:
                            course.dialogTop(6.41,strs[4],strs[5],strs[6],bckgr=True) 
                            nextBtn = course.centeredBtn(2.61,dark_green,console,adjustToDialog=True)
                        else:
                            course.dialogTop(6.41,strs[7],strs[8],strs[9],bckgr=True) 
                            nextBtn = course.centeredBtn(2.61,dark_green,ready,adjustToDialog=True)

                try:
                    if not TD_consoleShown:
                        if event.type == MOUSEMOTION:
                            if nextBtn.collidepoint(mouse_pos) and TD_count == 0:
                                course.centeredBtn(2.15,green,next,adjustToDialog=True)             
                                course.centeredBtn(2.15,dark_green,"",adjustToDialog=True,border=size_w//250) 
                            elif nextBtn.collidepoint(mouse_pos) and not commandsCorrect and TD_count == 3:
                                course.centeredBtn(2.61,green,console,adjustToDialog=True)             
                                course.centeredBtn(2.61,dark_green,"",adjustToDialog=True,border=size_w//250) 
                            elif nextBtn.collidepoint(mouse_pos) and TD_count == 3 and commandsCorrect:
                                course.centeredBtn(2.61,green,ready,adjustToDialog=True)             
                                course.centeredBtn(2.61,dark_green,"",adjustToDialog=True,border=size_w//250) 
                        elif event.type == MOUSEBUTTONDOWN:
                            if nextBtn.collidepoint(mouse_pos) and TD_count == 0:
                                TD_count += 3
                            elif nextBtn.collidepoint(mouse_pos) and TD_count == 3 and not commandsCorrect:
                                TD_consoleShown = True
                            elif nextBtn.collidepoint(mouse_pos) and TD_count == 3 and commandsCorrect:
                                TD_count = 0
                                TD_unitsPassed = 0
                                courseLvl += 1
                                course.tower_defence.reset()
                                iterator = 3
                except:
                    pass  
            elif courseLvl == 15:
                TD_lvlType = "mixed"
                TD_toDefeat = 3
                TD_iterator = 1
                course.tower_defence.drawMap()
                course.tower_defence.adminTools()
                course.tower_defence.console()      
            elif courseLvl == 16:
                notBlocked = False
                course.tower_defence.drawMap()
                course.tower_defence.console()
                course.eventsReset()  
                if language == "ENG":
                    ready = "Ready"   
                    strs= [
                        "We're almost done here apprentice,",
                        "only few more enemies to beat and",
                        "and friends to save, ready?"
                    ]
                else:
                    ready = "Gotów"   
                    strs= [
                        "To już prawie koniec mój uczniu,",
                        "jeszcze tylko kilku przeciwników,",
                        "do pokonania i przyjaciół do uratowania"
                    ]                   
                course.dialogTop(6.41,strs[0],strs[1],strs[2],bckgr=True) 
                readyBtn= course.centeredBtn(2.57,dark_green,ready,adjustToDialog=True)

                if event.type == MOUSEMOTION:
                    if readyBtn.collidepoint(mouse_pos):
                        course.centeredBtn(2.57,green,ready,adjustToDialog=True)
                        course.centeredBtn(2.57,dark_green,"",adjustToDialog=True,border=size_w//250)
                elif event.type == MOUSEBUTTONDOWN:
                    if readyBtn.collidepoint(mouse_pos):
                        TD_count = 0
                        TD_unitsPassed = 0
                        courseLvl += 1
                        course.tower_defence.reset()
                        iterator = 5
            elif courseLvl== 17:
                TD_lvlType = 'mixed'
                TD_toDefeat = 6
                course.tower_defence.drawMap()
                course.tower_defence.adminTools()
                course.tower_defence.console()                 
            elif courseLvl == 18:  
                notBlocked = True
                course.eventsReset()
                if language == "ENG":
                    course.dialogStandard(2.65,"Great job my apprentice!","People are very grateful","and so do I")
                else:
                    course.dialogStandard(2.65,"Dobra robota mój uczniu!","Ludzie są ci wdzięczni,","tak jak i ja jestem ci wdzięczny")
            elif courseLvl == 19:
                if language == "ENG":
                    finish = "Finish"
                    strs = [
                        "Failed to load 'book.png'",
                        "Here, take this as reward and souvenir",
                        "to remember me, that was an honour"
                    ]
                else:
                    finish = "Zakończ"
                    strs = [
                        "Błąd wczytywania 'book.png'",
                        "Weź to jako nagrodę oraz pamiątke,",
                        "by mnie pamiętać, to był zaszczyt!"
                    ]                    
                try:
                    book = pygame.image.load(f"{dirPath}/Images/Game/book.png") #In case of missing: https://iconarchive.com/show/library-icons-by-robinweatherall/book-icon.html
                    book = pygame.transform.scale(book, [int(size_w/5.33),int(size_h/3)])
                    screen.blit(book,[size_w/2.27,size_h/3.27])
                except:
                    errorInit(strs[0])
                course.dialogTop(6.41,strs[1],strs[2])
                finishBtn = course.centeredBtn(1.37,dark_green,finish)

                if event.type == MOUSEMOTION:
                    if finishBtn.collidepoint(mouse_pos):
                        course.centeredBtn(1.37,green,finish)
                        course.centeredBtn(1.37,dark_green,"",border=size_w//250)
                elif event.type == MOUSEBUTTONDOWN:
                    if finishBtn.collidepoint(mouse_pos):
                        if getCourseLvl() < 5:
                            changeCourselvl(5)
                        activeMenu = True
                        courseLvl = 1  
                        iterator = 1 
                        bckgrMusicPlayed = False                        
    def lesson5():
        global mentorIcon,activeMain,held,courseLvl,notBlocked,iterator,activeMenu,done
        global bckgrMusicPlayed,errorShowed,storedItems,storedCords,chosen,selected,storedTime,storedTimeValue
        global SR_icons,SR_cords,SR_iterator,SR_holder,SR_holder2
        if activeMain and not errorShowed:
            course.standardLessonEvents("lesson5",20,condition=notBlocked)
        if activities[0] and not activeMenu and str(activeLesson)[17:-23]=="lesson5" and not errorShowed:
            try:
                mentorIcon = pygame.image.load(r"{}/Images/Game/sr/soldier6.png".format(dirPath))
                mentorIcon = pygame.transform.scale(mentorIcon, [int(size_w/12),int(size_h/6)]) #[int(size_w/10.6),int(size_h/6)]
            except:
                errorInit("Failed to load mentor icon!",fontSize=1.8)
            language = getLang()
            if courseLvl == 1:
                course.dialogStandard(2.6,"What's up private? I'm leutienant Davies","from NAVY SEALs and I made a nice","training course for you, get ready man",fontSize=1.5)   
            elif courseLvl == 2:
                storedItems.clear()
                course.dialogTop(6.41,"But first you have to understand some things","especially about WHILE loop and its dependencies",fontSize=1.3)  
                strs = [
                    "while loop is a control flow statement that",
                    "allows code to be executed repeatedly based", 
                    "on a given Boolean condition"
                ] 
                pygame.draw.rect(screen,color1,[size_w/4.44,size_h/2.98,size_w/1.65,size_h/2.3],0,size_w//250)
                hght = size_h/2.09
                Write(round(size_w//100*2.6),"Definition",red,[size_w/1.92,size_h/2.51])
                for x in strs:
                    Write(round(size_w//100*2),x,color3,[size_w/1.92,hght])
                    hght += size_h/10
            elif courseLvl == 3:
                if isinstance(iterator,int):
                    if iterator < 4:
                        notBlocked = False
                    else:
                        notBlocked = True
                else:
                    notBlocked = True
                    iterator = 1
                course.dialogTop(6.41,"So yeah, shoot those shields to","check out some more facts")
                strs = [
                    "You use while statement in your life daily",
                    "It's often used to keep apps running",
                    "(Syntax) while statement: action"
                ]
                if(len(SR_icons)<1):
                    try:
                        shoot_shield = pygame.image.load(r"{}/Images/Game/sr/shoot_shield.png".format(dirPath))
                        shoot_shield = pygame.transform.scale(shoot_shield, [int(size_w/14.22),int(size_h/8)])
                        SR_icons.append(shoot_shield)
                    except:
                        errorInit("Failed to load shoot_shield") 
                    try:
                        iron_sight = pygame.image.load(r"{}/Images/Game/iron_sight.png".format(dirPath))
                        iron_sight = pygame.transform.scale(iron_sight, [int(size_w/3.90),int(size_h/2.19)])
                        SR_icons.append(iron_sight)
                    except:
                        errorInit("Failed to load iron_sight")

                try:
                    height = size_h/3.11
                    for x in range(3):
                        shield = screen.blit(SR_icons[0],[size_w/4.15,height])
                        if len(storedItems)<3:
                            storedItems.append(shield)
                        height += size_h/6
                except:
                    pass
                
                for item in storedItems:
                    index = storedItems.index(item)
                    if index>iterator-1:
                        pygame.draw.rect(screen,color2,[item[0],item[1],item[2],item[3]])
                    elif index<iterator-1:
                        pygame.draw.rect(screen,color1,[item[0]+size_w/8,item[1],size_w/2.5,item[3]],0,size_w//250)
                        Write(round(size_w//100*1.5),strs[index],color3,[size_w/1.76,item[1]+item[3]/2])
                        
                for cord in storedCords:
                    pygame.draw.circle(screen,dark_gray,cord,size_w//200)

                pygame.mouse.set_visible(True)
                
                if event.type == MOUSEBUTTONDOWN:
                    for item in storedItems:
                        index = storedItems.index(item)
                        if item.collidepoint(mouse_pos) and iterator-1==index and iterator < 4:
                            iterator += 1
                            storedCords.append([mouse_pos[0],mouse_pos[1]])  
                            course.coursorMarked()  
                elif event.type == MOUSEMOTION:
                    for item in storedItems:
                        index = storedItems.index(item)
                        if item.collidepoint(mouse_pos) and iterator-1==index and iterator < 4:
                            pygame.mouse.set_visible(False)
                            pygame.draw.circle(screen, red, mouse_pos, size_w//450, 0)     
                            pygame.draw.circle(screen, red, mouse_pos, size_w//150, size_w//550)     
            elif courseLvl == 4:
                hght = size_h/3.2
                txthght = size_h/2.65
                if language == "ENG":
                    txts = ["Single line syntax",
                    "Multiple line syntax",
                    "While...Else..."]
                    descs = [
                        ["Single line syntax contains both statement and action",
                        "           while statement: action",
                        "Where statement = bool and action is set of instructions",
                        "Also: always remeber about ':' after statement"],
                        [
                            "Multiple line while loop also need tabulations",
                            "while statement:",
                            "                                                               instructions1...instruction2...etc.",
                            "!Remember about [Tab]/[Space] before instruction!"
                        ],
                        [
                            "While is a statetement checking instructions, that",
                            "means statement can be not fulfilled, what then you ask?",
                            "There's possibility to join else to your while loop, but how?",
                            "It's really easy! It works the same way as with IF instruction",
                        ]
                    ]
                    back = "Back"
                else:
                    txts = ["Składnia: jedna linia",
                    "Składnia: wiele liń",
                    "While...Else..."]
                    descs = [
                        ["Single line syntax contains both statement and action",
                        "           while statement: action",
                        "Where statement = bool and action is set of instructions",
                        "Also: always remeber about ':' after statement"],
                        [
                            "Multiple line while loop also need tabulations",
                            "while statement:",
                            "                                                               instructions1...instruction2...etc.",
                            "!Remember about [Tab]/[Space] before instruction!"
                        ],
                        [
                            "While is a statetement checking instructions, that",
                            "means statement can be not fulfilled, what then you ask?",
                            "There's possibility to join else to your while loop, but how?",
                            "It's really easy! It works the same way as with IF instruction",
                        ]
                    ]
                    back = "Powrót"
                rects = []
                txtCords = []
                if activeMain:
                    if language == "ENG":
                        course.dialogTop(6.41,"About syntax there's still few more","things, so let's check them out")
                    else:
                        course.dialogTop(6.41,"Co do składni wciąż jest jeszcze pare","rzeczy, więc sprawdźmy je")
                    for it in range(3):
                        rect = pygame.draw.rect(screen, color1, [size_w/3.25,hght,size_w/2.2,size_h/8], 0,15)
                        rects.append(rect)
                        txt=Write(size_w//100*2,txts[it],color2,[size_w/1.85,txthght])
                        txtCords.append([size_w/1.85,txthght])
                        hght += size_h/6
                        txthght += size_h/6
                else:
                    pygame.draw.rect(screen, color2, [size_w/5,size_h/16,size_w/1.5,size_h/1.1],0,10)
                    backBtn = course.centeredBtn(12.8,dark_red,back)
                    bckgr = pygame.draw.rect(screen, color1, [size_w/4.37,size_h/3.46,size_w/1.65,size_h/2], 0,10)
                    descHght = size_h/2.59
                    for desc in descs[iterator]:
                        pygame.draw.rect(screen, color2, [size_w/4.01,size_h/3.16,size_w/1.8,size_h/2.3], size_w//450,15)
                        pygame.draw.line(screen, color2, [size_w/4.01,size_h/2.3], [size_w/1.248,size_h/2.3], size_w//450)
                        pygame.draw.line(screen, color2, [size_w/4.01,size_h/1.86], [size_w/1.248,size_h/1.86], size_w//450)
                        pygame.draw.line(screen, color2, [size_w/4.01,size_h/1.57], [size_w/1.248,size_h/1.57], size_w//450)
                        if getTheme().lower() == "light":
                            WriteItalic(round(size_w//100*1.5),desc,color3,[size_w/1.91,descHght])
                        else:
                            WriteItalic(round(size_w//100*1.5),desc,dark_gray,[size_w/1.91,descHght])
                        descHght += size_h/10
                if event.type == MOUSEMOTION:
                    for rect in rects:
                        index = rects.index(rect)
                        if rect.collidepoint(mouse_pos):
                            pygame.draw.rect(screen, color3, [rect[0],rect[1],rect[2],rect[3]], size_w//450,15)
                            Write(size_w//100*2,txts[index],color3,txtCords[index])
                    if not activeMain:
                        try:
                            if backBtn.collidepoint(mouse_pos):
                                course.centeredBtn(12.8,red,back)
                        except:
                            pass
                elif event.type == MOUSEBUTTONDOWN:
                    for rect in rects:
                        index = rects.index(rect)
                        if rect.collidepoint(mouse_pos):
                            activeMain = False
                            iterator = index
                    if not activeMain:
                        try:
                            if backBtn.collidepoint(mouse_pos):
                                activeMain = True
                        except:
                            pass
                elif event.type == KEYDOWN:
                    if not activeMain and event.key == K_ESCAPE:
                        activeMain = True                      
            elif courseLvl == 5:
                notBlocked = False
                course.dialogTop(6.41,"Let's talk about next important","thing: infinity loop")
                btn = pygame.draw.rect(screen, purple, [size_w/2.38,size_h/2.92,size_w/5,size_h/12], 0,size_w//250)
                Write(round(size_w//100*2),"Infinity loop?",color1,[size_w/1.91,size_h/2.58])
                if event.type == MOUSEMOTION:
                    if btn.collidepoint(mouse_pos):
                        btn = pygame.draw.rect(screen, logoBlue, [size_w/2.38,size_h/2.92,size_w/5,size_h/12], 0,size_w//250)
                        btn = pygame.draw.rect(screen, dark_blue, [size_w/2.38,size_h/2.92,size_w/5,size_h/12], size_w//200,size_w//250)
                        Write(round(size_w//100*2),"Infinity loop?",color3,[size_w/1.91,size_h/2.58])   
                elif event.type == MOUSEBUTTONDOWN:
                    if btn.collidepoint(mouse_pos):
                        courseLvl += 1 
            elif courseLvl == 6:
                notBlocked = True
                strs = [
                    "Yeah, infinity loops!",
                    "Name is pretty accurate, that's a loop",
                    "with a statement never going to be False",
                    "by itself, so it will simply never end!"
                ]
                course.dialogStandard(2.6,strs[0],strs[1],strs[2],strs[3],fontSize=1.5) 
            elif courseLvl == 7:
                notBlocked = False
                SR_icons.clear()
                course.dialogTop(6.41,"The best way to learn is to","check a way how it's done in practic")
                course.consoleExample("while statement:",left=True,hght=3.37)
                course.consoleExample("spawn_enemy()",hght=2.21)
                btn = pygame.draw.rect(screen, purple, [size_w/2.38,size_h/1.4,size_w/5,size_h/12], 0,size_w//250)
                Write(round(size_w//100*2),"Check it!",color1,[size_w/1.91,size_h/1.32])
                if event.type == MOUSEMOTION:
                    if btn.collidepoint(mouse_pos):
                        btn = pygame.draw.rect(screen, logoBlue, [size_w/2.38,size_h/1.4,size_w/5,size_h/12], 0,size_w//250)
                        btn = pygame.draw.rect(screen, dark_blue, [size_w/2.38,size_h/1.4,size_w/5,size_h/12], size_w//200,size_w//250)
                        Write(round(size_w//100*2),"Check it!",color3,[size_w/1.91,size_h/1.32])   
                elif event.type == MOUSEBUTTONDOWN:
                    if btn.collidepoint(mouse_pos):
                        courseLvl += 1 
            elif courseLvl == 8:
                if not isinstance(chosen,int):
                    notBlocked = False
                else:
                    notBlocked = True

                strs = [
                    "Here you can control statement value to",
                    "see how it works, but rememeber that",
                    "infinity loops statement is always True"
                ]
                course.dialogTop(6.41,strs[0],strs[1],strs[2])

                if(len(SR_icons)) < 1:
                    try:
                        enemy1 = pygame.image.load(f"{dirPath}/Images/Game/sr/enemy1.png")
                        enemy1 = pygame.transform.scale(enemy1, [int(size_w/10.6),int(size_h/6)])
                        SR_icons.append(enemy1)
                        enemy2 = pygame.image.load(f"{dirPath}/Images/Game/sr/enemy2.png")
                        enemy2 = pygame.transform.scale(enemy2, [int(size_w/16),int(size_h/7)])
                        SR_icons.append(enemy2)
                        enemy3 = pygame.image.load(f"{dirPath}/Images/Game/sr/enemy3.png")
                        enemy3 = pygame.transform.scale(enemy3, [int(size_w/10.6),int(size_h/6)])
                        SR_icons.append(enemy3)
                    except:
                        errorInit("Failed to load icons L5.8")

                Write(round(size_w//100*2.5),"Statement",color3,[size_w/2.22,size_h/2.1])

                hght1 = size_h/2.3
                opt1 = pygame.draw.rect(screen, color3, [size_w/1.85,hght1,size_w/50,size_h/30], size_w//500,size_w//300)
                Write(round(size_w//100*1.3),"True",lt_blue,[size_w/1.68,size_h/2.23])
                if(isinstance(chosen,int)):
                    if chosen == 1:
                        pygame.draw.line(screen, lt_blue, [size_w/1.85+size_w/50,hght1], [size_w/1.83,hght1+size_h/30], size_w//400)
                        pygame.draw.line(screen, lt_blue, [size_w/1.83,hght1+size_h/30], [size_w/1.85,size_h/2.24] ,size_w//400)
                
                hght2 = size_h/2.1
                opt2 = pygame.draw.rect(screen, color3, [size_w/1.85,hght2,size_w/50,size_h/30], size_w//500,size_w//300)
                Write(round(size_w//100*1.3),"False",lt_blue,[size_w/1.68,size_h/2.02])
                if(isinstance(chosen,int)):
                    if chosen == 2:
                        pygame.draw.line(screen, lt_blue, [size_w/1.85+size_w/50,hght2], [size_w/1.83,hght2+size_h/30], size_w//400)
                        pygame.draw.line(screen, lt_blue, [size_w/1.83,hght2+size_h/30], [size_w/1.85,size_h/2.02] ,size_w//400)

                try:
                    if chosen == 1:
                        randW = uniform(3.04,1.42)
                        randH = uniform(1.78,1.72)
                        storedCords.append([size_w/randW,size_h/randH])
                except:
                    errorInit("Failed to blit SR_Icons: L5.8",fontSize=1.7)

                try:
                    if chosen == 1:
                        for cord in storedCords:
                            randNr = randint(0,2)
                            screen.blit(SR_icons[randNr],cord)
                        Write(round(size_w//100*1.8),"Move your mouse to see effects",red,[size_w/1.84,size_h/1.2])
                except:
                    pass

                if event.type == MOUSEBUTTONDOWN:
                    if opt1.collidepoint(mouse_pos):
                        chosen = 1
                    elif opt2.collidepoint(mouse_pos):
                        chosen = 2
                        storedCords.clear()
            elif courseLvl == 9:
                SR_icons.clear()
                storedCords.clear()
                chosen = ''
                notBlocked = True
                strs= [
                    "You may be wondering what is use of",
                    "loop like that? Well, it's not like that",
                    "infinity loop can not be stopped, it can!",
                    "There's an instructions for ending loop,",
                    "even infinite one, it's called BREAK"
                ]
                course.dialogStandard(2.5,strs[0],strs[1],strs[2],strs[3],strs[4],fontSize=1.6)
            elif courseLvl == 10:
                if selected == 1 and chosen == 0:
                    course.dialogTop(6.41,"As you see, statement can be","changed whenever you want")
                elif selected == 0 and chosen == 1:
                    course.dialogTop(6.41,"With break you're out of loop,","so you can't control it at the same time",fontSize=1.3)
                else:
                    course.dialogTop(6.41,"Name is pretty accurate because","it makes program break out of the loop")
                
                
                Write(round(size_w/100*2),"Normal while loop",red,[size_w/2.75,size_h/2.99])
                
                WriteItalic(round(size_w/100*1.6),"Statement",lt_blue,[size_w/2.75,size_h/2.5])
                
                pygame.draw.rect(screen, dark_blue, [size_w/3.9,size_h/1.6,size_w/4.5,size_h/50], 0,size_w//150)
                Write(round(size_w/100*1.4),"False",dark_blue,[size_w/3.59,size_h/1.77])
                Write(round(size_w/100*1.4),"True",dark_blue,[size_w/2.18,size_h/1.77])
                if held:
                    mainCirc = pygame.draw.circle(screen, lt_blue, [mouse_pos[0],size_h/1.58], size_w/70, 0)
                    pygame.draw.circle(screen, purple, [mouse_pos[0],size_h/1.58], size_w/90, 0)
                else:
                    if len(storedCords)<1:
                        mainCirc = pygame.draw.circle(screen, lt_blue, [size_w/3.69,size_h/1.58], size_w/70, 0)
                    else:
                        mainCirc = pygame.draw.circle(screen, lt_blue, [storedCords[0],size_h/1.58], size_w/70, 0)

                Write(round(size_w/100*2),"Status:",color3,[size_w/3.7,size_h/1.38])
                
                if event.type == MOUSEMOTION:
                    if mainCirc.collidepoint(mouse_pos) and not held:
                        if len(storedCords) < 1:
                            pygame.draw.circle(screen, purple, [size_w/3.69,size_h/1.58], size_w/90, 0)
                        else:
                            pygame.draw.circle(screen, purple, [storedCords[0],size_h/1.58], size_w/90, 0)
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    if mainCirc.collidepoint(mouse_pos):
                        held = True
                        storedCords.clear()
                elif event.type == MOUSEBUTTONUP and held:
                    held = False #2.73 polowa
                    if mouse_pos[0] < size_w/2.73:
                        storedCords.append(size_w/3.69)
                        selected = 0
                    else:
                        storedCords.append(size_w/2.18) 
                        selected = 1                       

                if mouse_pos[0] < size_w/3.83 or mouse_pos[0] > size_w/2.09:
                    held = False



                pygame.draw.line(screen, color3, [size_w/1.86,size_h/3.4], [size_w/1.86,size_h/1.24], size_w//500)



                Write(round(size_w/100*2),"While loop with break",red,[size_w/1.43,size_h/2.99])

                if chosen == 1:
                    startBtn = pygame.draw.rect(screen, green, [size_w/1.55,size_h/2.55,size_w/10,size_h/14],0,size_w//200)
                else:
                    startBtn = pygame.draw.rect(screen, dark_green, [size_w/1.55,size_h/2.55,size_w/10,size_h/14],0,size_w//200)
                Write(round(size_w//100*1.4),"Start",color1,[size_w/1.44,size_h/2.31])

                if chosen == 0:
                    breakBtn = pygame.draw.rect(screen, red, [size_w/1.55,size_h/1.89,size_w/10,size_h/14],0,size_w//200)
                else:
                    breakBtn = pygame.draw.rect(screen, dark_red, [size_w/1.55,size_h/1.89,size_w/10,size_h/14],0,size_w//200)
                Write(round(size_w//100*1.4),"Break",color1,[size_w/1.44,size_h/1.76])
                
                Write(round(size_w/100*2),"Status:",color3,[size_w/1.63,size_h/1.38])   

                if event.type == MOUSEMOTION:
                    if startBtn.collidepoint(mouse_pos):
                        pygame.draw.rect(screen, green, [size_w/1.55,size_h/2.55,size_w/10,size_h/14],0,size_w//200)
                        Write(round(size_w//100*1.4),"Start",color3,[size_w/1.44,size_h/2.31])      
                    elif breakBtn.collidepoint(mouse_pos):
                        pygame.draw.rect(screen, red, [size_w/1.55,size_h/1.89,size_w/10,size_h/14],0,size_w//200)
                        Write(round(size_w//100*1.4),"Break",color3,[size_w/1.44,size_h/1.76])    
                elif event.type == MOUSEBUTTONDOWN:
                    if startBtn.collidepoint(mouse_pos) and chosen !=0:
                        chosen = 1   
                    elif breakBtn.collidepoint(mouse_pos):
                        chosen = 0                                        
            elif courseLvl == 11:
                storedCords.clear()
                chosen = ''
                selected = ''
                held = False
                txts = [
                    "So if there's an instruction to end loop,",
                    "is there one to restart loop? Sure it is!",
                    "It's called CONTINUE and with use it makes",
                    "loop to return to the begin, let's check it out!"
                ]
                course.dialogStandard(2.6,txts[0],txts[1],txts[2],txts[3],fontSize=1.4)
            elif courseLvl == 12:
                notBlocked = False
                course.dialogTop(6.41,"Statement is True and iterator is 0")
                course.consoleExample("While statement:",left=True,hght=3.61)
                course.consoleExample("print(iterator)",hght=2.3)
                course.consoleExample("iterator += 1",hght=1.7)
                startBtn = course.centeredBtn(1.27,dark_green,"Start")
                if event.type == MOUSEMOTION and startBtn.collidepoint(mouse_pos):
                    course.centeredBtn(1.27,green,"Start")
                    course.centeredBtn(1.27,dark_green,"",border=size_w//250)
                elif event.type == MOUSEBUTTONDOWN and startBtn.collidepoint(mouse_pos):
                    courseLvl += 1
            elif courseLvl == 13:
                if isinstance(selected,int):
                    if selected == 1:
                        notBlocked = True
                        course.dialogTop(6.41,"As you see iterator value restarted to ","value from the beggining",fontSize=1.4)
                        Write(round(size_w//100*3.5),"You can go futher",green,[size_w/1.95,size_h/1.22])
                else:
                    course.dialogTop(6.41,"Iterator will keep counting and button will","trigger continue function, test it!",fontSize=1.4)
                contBtn = course.centeredBtn(2.09,purple,"Continue",adjustToDialog=True)
                if not done:
                    storedTime = round(float(time.process_time()),1)
                    done = True
                if event.type == MOUSEMOTION and contBtn.collidepoint(mouse_pos):
                    course.centeredBtn(2.09,lt_blue,"Continue",adjustToDialog=True)
                    course.centeredBtn(2.09,logoBlue,"",adjustToDialog=True,border=size_w//250)
                elif event.type == MOUSEBUTTONDOWN and contBtn.collidepoint(mouse_pos):
                    storedTime = round(float(time.process_time()),1)
                    selected = 1
            elif courseLvl == 14:
                selected = ''
                done = False
                storedTime = ''
                txts = [
                    "I think it's time to test what you've learned,",
                    "go futher whenever you're ready soldier"
                ]
                course.dialogStandard(2.65,txts[0],txts[1],fontSize=1.4)
            elif courseLvl == 15: #QUIZ
                notBlocked = False
                if not done:
                    if isinstance(SR_holder,str):
                        SR_holder = 0
                    if isinstance(SR_holder2,str) or SR_holder2 == 0:
                        SR_holder2 = 1
                    course.dialogTop(6.41,"Oh right recruit, grab a gun","and show me what you've learned")
                    if len(SR_icons)<1:
                        m4 = pygame.image.load(r"{}/Images/Game/sr/m4.png".format(dirPath))
                        m4 = pygame.transform.scale(m4, [int(size_w/5),int(size_h/5)])
                        SR_icons.append(m4)
                        mp5 = pygame.image.load(r"{}/Images/Game/sr/mp5.png".format(dirPath))
                        mp5 = pygame.transform.scale(mp5, [int(size_w/6),int(size_h/8)])
                        SR_icons.append(mp5)
                        m4m = pygame.image.load(r"{}/Images/Game/sr/m4marked.png".format(dirPath))
                        m4m = pygame.transform.scale(m4m, [int(size_w/5),int(size_h/5)])
                        SR_icons.append(m4m)
                        mp5m = pygame.image.load(r"{}/Images/Game/sr/mp5marked.png".format(dirPath))
                        mp5m = pygame.transform.scale(mp5m, [int(size_w/6),int(size_h/8)])
                        SR_icons.append(mp5m)
                    try:
                        gun1 = screen.blit(SR_icons[SR_holder],[size_w/3.41,size_h/2.54])
                        gun2 = screen.blit(SR_icons[SR_holder2],[size_w/1.74,size_h/2.32])
                    except:
                        pass
                    if isinstance(selected,int):
                        nextBtn = course.centeredBtn(1.37,dark_green,"Go")
                    try:
                        if event.type == MOUSEMOTION and nextBtn.collidepoint(mouse_pos):
                            course.centeredBtn(1.37,green,"Go")
                            course.centeredBtn(1.37,dark_green,"",border=size_w//250)
                    except:
                        pass
                    if event.type == MOUSEBUTTONDOWN and event.button==1:
                        try:
                            if gun1.collidepoint(mouse_pos):
                                SR_holder = 2
                                SR_holder2 = 1
                                selected = 1
                            elif gun2.collidepoint(mouse_pos):
                                SR_holder = 0
                                SR_holder2 = 3
                                selected = 2
                        except:
                            pass    
                        try:
                            if nextBtn.collidepoint(mouse_pos):
                                SR_icons.clear()       
                                SR_holder = 0
                                SR_holder2 = 0
                                iterator = 1
                                done = True
                                storedTimeValue = round(float(time.process_time()),2)
                        except:
                            pass              
                        
                else:
                    questions = [
                        "What is the instruction used to end while loop?",
                        "While loop that runs forever is known as:",
                        "Which is correct syntax?",
                        "Else can be bound to while loop",
                        "Which instruction makes loop return to beginning?",
                        "Why infinite loop is called like that?",
                        "Statement is:",
                        "While loop statement ends with",
                        "Output of while True {print('x')} is:"
                    ]
                    allAnswers = [
                        ["End","Break","Out"],
                        ["Long Loop","Broken Loop","Infinite Loop"],
                        ["While statement: action","While statement() action","While statement do action"],
                        ["True","False","Only if statement is True"],
                        ["Return","Restart","Continue"],
                        ["Because of author's name","Statement is always True","We don't know why"],
                        ["True or False","List","String"],
                        [":","#","+"],
                        ["Infinity of 'x'","Error","Infinity of x"]
                    ]
                    correctAnswers = [1,2,0,0,2,1,0,0,1] #0-A 1-B 2-C

                    course.shooting_range.quiz.start(questions,allAnswers,correctAnswers)
            elif courseLvl == 16:
                notBlocked = False
                course.dialogTop(6.41,"Great job! Do you want to test your reflex","at shooting range?",fontSize=1.4)
                playBtn=pygame.draw.rect(screen, dark_green, [size_w/2.77,size_h/2.16,size_w/8,size_h/10], 0,size_w//150)
                Write(round(size_w//100*1.8),"Play",color1,[size_w/2.36,size_h/1.93])
                skipBtn=pygame.draw.rect(screen, dark_green, [size_w/1.77,size_h/2.16,size_w/8,size_h/10], 0,size_w//150)
                Write(round(size_w//100*1.8),"Skip",color1,[size_w/1.59,size_h/1.93])
                if event.type == MOUSEMOTION:
                    if playBtn.collidepoint(mouse_pos):
                        pygame.draw.rect(screen, green, [size_w/2.77,size_h/2.16,size_w/8,size_h/10], 0,size_w//150)
                        pygame.draw.rect(screen, dark_green, [size_w/2.77,size_h/2.16,size_w/8,size_h/10], size_w//250,size_w//150)
                        Write(round(size_w//100*1.8),"Play",color3,[size_w/2.36,size_h/1.93])
                    elif skipBtn.collidepoint(mouse_pos):
                        pygame.draw.rect(screen, green, [size_w/1.77,size_h/2.16,size_w/8,size_h/10], 0,size_w//150)
                        pygame.draw.rect(screen, dark_green, [size_w/1.77,size_h/2.16,size_w/8,size_h/10], size_w//250,size_w//150)
                        Write(round(size_w//100*1.8),"Skip",color3,[size_w/1.59,size_h/1.93])   
                elif event.type == MOUSEBUTTONDOWN:
                    if playBtn.collidepoint(mouse_pos):
                        courseLvl += 1
                    elif skipBtn.collidepoint(mouse_pos):
                        courseLvl = 20
            elif courseLvl == 17:
                #Single Init
                pygame.event.set_blocked(MOUSEWHEEL)
                notBlocked = False
                storedTime = round(float(time.process_time())-storedTimeValue,1)
                if 30-SR_iterator > 0:
                    ammoColor = green
                    course.dialogTop(6.41,"Shoot the targets!")
                else:
                    ammoColor = red
                    course.dialogTop(6.41,"Mag empty, you need to reload!")
                if len(SR_icons)<1:
                    for x in range(15):
                        pointW = uniform(size_w/3.02,size_w/1.59)
                        pointH = uniform(size_h/2.97,size_h/2.34)
                        SR_cords.append([pointW,pointH])
                    try:
                        iron_sight = pygame.image.load(r"{}/Images/Game/iron_sight.png".format(dirPath))
                        iron_sight = pygame.transform.scale(iron_sight, [int(size_w/3.90),int(size_h/2.19)])
                        SR_icons.append(iron_sight)
                    except:
                        errorInit("Failed to load iron_sight")

                    try:
                        shoot_shield = pygame.image.load(r"{}/Images/Game/sr/shoot_shield.png".format(dirPath))
                        shoot_shield = pygame.transform.scale(shoot_shield, [int(size_w/21.34),int(size_h/12)])
                        SR_icons.append(shoot_shield)
                    except:
                        errorInit("Failed to load shoot_shield")

                    try:
                        iron_sight = pygame.image.load(r"{}/Images/Game/iron_sight_shoot.png".format(dirPath))
                        iron_sight = pygame.transform.scale(iron_sight, [int(size_w/3.90),int(size_h/2.09)])
                        SR_icons.append(iron_sight)
                    except:
                        errorInit("Failed to load 'iron_sight_shoot.png'",fontSize=1.7)

                #Bliting and Writing content
                Write(round(size_w//100*1.5),f"Ammo: {30-SR_iterator}/30",ammoColor,[size_w/1.24,size_h/1.08])
                reloadBtn = pygame.draw.rect(screen, purple, [size_w/2.38,size_h/1.19,size_w/5,size_h/12], 0,size_w//250)
                reloadTxt = Write(round(size_w//100*2),"Reload",color1,[size_w/1.91,size_h/1.13])

                #GUN BLITING
                try:
                    correctH = mouse_pos[1]<size_h/1.75 and mouse_pos[1]>size_h/7.92
                    correctW = mouse_pos[0]<size_w/1.35 and mouse_pos[0]>size_w/3.07
                    sight_rect = SR_icons[0].get_rect()
                    try:
                        shield = screen.blit(SR_icons[1],SR_cords[iterator])
                    except:
                        SR_icons.clear()
                        courseLvl += 1
                    if correctH and correctW:
                        pygame.mouse.set_visible(False)
                        screen.blit(SR_icons[0],[mouse_pos[0]-sight_rect[2]/2.1,mouse_pos[1]-sight_rect[3]/7])
                    else:
                        pygame.mouse.set_visible(True)
                except:
                    pass


                if event.type == MOUSEMOTION:
                    if reloadBtn.collidepoint(mouse_pos):
                        reloadBtn = pygame.draw.rect(screen, logoBlue, [size_w/2.38,size_h/1.19,size_w/5,size_h/12], 0,size_w//250)
                        reloadBtn = pygame.draw.rect(screen, dark_blue, [size_w/2.38,size_h/1.19,size_w/5,size_h/12], size_w//200,size_w//250)
                        reloadTxt = Write(round(size_w//100*2),"Reload",color3,[size_w/1.91,size_h/1.13])                        
                elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                    if 30-SR_iterator > 0:
                        if correctH and correctW:
                            SR_holder += 1
                            try:
                                SR_iterator += 1
                                pygame.mouse.set_visible(False)
                                screen.blit(SR_icons[2],[mouse_pos[0]-sight_rect[2]/2.1,mouse_pos[1]-sight_rect[3]/7])
                            except:
                                pass
                        else:
                            pygame.mouse.set_visible(True)
                        try:
                            if shield.collidepoint(mouse_pos):
                                iterator += 1
                                SR_holder2 += 1
                        except:
                            pass
                    if reloadBtn.collidepoint(mouse_pos):
                        SR_iterator = 0
                elif event.type == KEYDOWN:
                    if event.key == K_r:
                        SR_iterator = 0
            elif courseLvl == 18:
               #Single Init
                notBlocked = False
                if 30-SR_iterator > 0:
                    course.dialogTop(6.41,"Shoot the targets!")
                else:
                    course.dialogTop(6.41,"Mag empty, you need to reload!")
                if len(SR_icons)<1:
                    for x in range(15):
                        pointW = uniform(size_w/3.02,size_w/1.59)
                        pointH = uniform(size_h/2.97,size_h/2.34)
                        SR_cords.append([pointW,pointH])
                    try:
                        iron_sight = pygame.image.load(r"{}/Images/Game/iron_sight2.png".format(dirPath))
                        iron_sight = pygame.transform.scale(iron_sight, [int(size_w/2),int(size_h/2.3)])
                        SR_icons.append(iron_sight)
                    except:
                        errorInit("Failed to load iron_sight")

                    try:
                        shoot_shield = pygame.image.load(r"{}/Images/Game/sr/shoot_shield.png".format(dirPath))
                        shoot_shield = pygame.transform.scale(shoot_shield, [int(size_w/21.34),int(size_h/12)])
                        SR_icons.append(shoot_shield)
                    except:
                        errorInit("Failed to load shoot_shield")

                    try:
                        iron_sight = pygame.image.load(r"{}/Images/Game/iron_sight2_shoot.png".format(dirPath))
                        iron_sight = pygame.transform.scale(iron_sight, [int(size_w/2),int(size_h/2.19)]) 
                        SR_icons.append(iron_sight)  
                    except:
                        errorInit("Failed to load 'iron_sight2_shoot.png'",fontSize=1.7)                   

                #Bliting and Writing content
                Write(round(size_w//100*1.5),f"Ammo: {30-SR_iterator}/30",color3,[size_w/1.24,size_h/1.08])
                reloadBtn = pygame.draw.rect(screen, purple, [size_w/2.38,size_h/1.19,size_w/5,size_h/12], 0,size_w//250)
                reloadTxt = Write(round(size_w//100*2),"Reload",color1,[size_w/1.91,size_h/1.13])

                #GUN BLITING
                try:
                    correctH = mouse_pos[1]<size_h/1.75 and mouse_pos[1]>size_h/7.92
                    correctW = mouse_pos[0]<size_w/1.35 and mouse_pos[0]>size_w/3.07
                    sight_rect = SR_icons[0].get_rect()
                    try:
                        shield = screen.blit(SR_icons[1],SR_cords[iterator])
                    except:
                        SR_icons.clear()
                        courseLvl += 1
                        SR_iterator = 0
                    if correctH and correctW:
                        pygame.mouse.set_visible(False)
                        screen.blit(SR_icons[0],[mouse_pos[0]-sight_rect[2]/2,mouse_pos[1]-sight_rect[3]/12])
                    else:
                        pygame.mouse.set_visible(True)
                except:
                    pass

                if event.type == MOUSEMOTION:
                    if reloadBtn.collidepoint(mouse_pos):
                        reloadBtn = pygame.draw.rect(screen, logoBlue, [size_w/2.38,size_h/1.19,size_w/5,size_h/12], 0,size_w//250)
                        reloadBtn = pygame.draw.rect(screen, dark_blue, [size_w/2.38,size_h/1.19,size_w/5,size_h/12], size_w//200,size_w//250)
                        reloadTxt = Write(round(size_w//100*2),"Reload",color3,[size_w/1.91,size_h/1.13])   
                elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                    if 30-SR_iterator > 0:
                        if correctH and correctW:
                            SR_holder += 1
                            try:
                                SR_iterator += 1
                                pygame.mouse.set_visible(False)
                                screen.blit(SR_icons[2],[mouse_pos[0]-sight_rect[2]/2,mouse_pos[1]-sight_rect[3]/12])
                            except:
                                pass
                        else:
                            pygame.mouse.set_visible(True)
                        try:
                            if shield.collidepoint(mouse_pos):
                                iterator += 1
                                SR_holder2 += 1
                        except:
                            pass      
                    if reloadBtn.collidepoint(mouse_pos):
                        SR_iterator = 0    
                elif event.type == KEYDOWN:
                    if event.key == K_r:
                        SR_iterator = 0     
            elif courseLvl == 19:
                SR_icons.clear()
                pygame.mouse.set_visible(True)
                notBlocked = True
                course.dialogTop(6.41,"Here are your results recruit")
                try:
                    accuracy = round(SR_holder2/SR_holder*100,2)
                except:
                    accuracy = 0
                if accuracy>90.0 and storedTime<20:
                    rank = "Gold"
                    medalColor = gold
                elif accuracy>75.0 and storedTime < 35:
                    rank = "Silver"
                    medalColor  = dark_gray
                else:
                    rank = "Bronze"
                    medalColor  = lt_brown

                Write(round(size_w/100*3),f"Time: {storedTime}s",green,[size_w/1.83,size_h/2.9])
                Write(round(size_w/100*3),f"Accuracy: {accuracy}%",green,[size_w/1.83,size_h/2.23])
                Write(round(size_w/100*3),f"Missed shots: {SR_holder-SR_holder2}",green,[size_w/1.83,size_h/1.86])
                Write(round(size_w/100*3),f"Rank:",green,[size_w/2.01,size_h/1.6])
                Write(round(size_w/100*3),rank,medalColor,[size_w/1.58,size_h/1.6])

                pygame.draw.polygon(screen, dark_red, [(size_w/2.21,size_h/1.37),(size_w/1.8,size_h/1.37),(size_w/1.98,size_h/1.18)], 0)
                pygame.draw.circle(screen, medalColor, [size_w/1.98,size_h/1.18], size_w//25, 0)
            elif courseLvl == 20: 
                pygame.mouse.set_visible(True)
                if len(SR_icons)<1:
                    try:
                        medal = pygame.image.load(r"{}/Images/Game/medal.png".format(dirPath))
                        medal = pygame.transform.scale(medal, [int(size_w/7),int(size_h/3)])
                        SR_icons.append(medal)
                    except:
                        errorInit("Failed to load medal.png")
                txts = [
                    "Congratulations soldier! You've made it",
                    "through my training program, see you at ",
                    "next one, oh and take this as reward"
                ]
                course.dialogTop(6.41,txts[0],txts[1],txts[2],fontSize=1.4)
                screen.blit(SR_icons[0],[size_w/2.03,size_h/2.29])
                finishBtn = course.centeredBtn(1.25,dark_green,"Finish",adjustToDialog=True)

                if event.type == MOUSEMOTION:
                    if finishBtn.collidepoint(mouse_pos):
                        course.centeredBtn(1.25,green,"Finish",adjustToDialog=True)
                        course.centeredBtn(1.25,dark_green,"",border=size_w//250,adjustToDialog=True)
                elif event.type == MOUSEBUTTONDOWN:
                    if finishBtn.collidepoint(mouse_pos):
                        if getCourseLvl() < 6:
                            changeCourselvl(6)
                        activeMenu = True
                        courseLvl = 1  
                        iterator = 1 
                        bckgrMusicPlayed = False  
    def lesson6():
        global mentorIcon,activeMain,held,courseLvl,notBlocked,iterator,activeMenu,done
        global bckgrMusicPlayed,errorShowed,storedItems,storedCords,chosen,selected,storedTime,storedTimeValue
        global SR_icons,SR_cords,SR_iterator,SR_holder,SR_holder2
        if activeMain and not errorShowed:
            course.standardLessonEvents("lesson6",29,condition=notBlocked)
        if activities[0] and not activeMenu and str(activeLesson)[17:-23]=="lesson6" and not errorShowed:
            try:
                mentorIcon = pygame.image.load(r"{}/Images/Game/sr/soldier6.png".format(dirPath))
                mentorIcon = pygame.transform.scale(mentorIcon, [int(size_w/12),int(size_h/6)]) #[int(size_w/10.6),int(size_h/6)]
            except:
                errorInit("Failed to load mentor icon!",fontSize=1.8)
            language = getLang()
            if courseLvl == 1:
                txts = [
                    "Howdy recruit, it's me again!",
                    "I've made another course for you and I'm sure",
                    "you're damn happy about it, let's go"
                ]
                course.dialogTop(6.41,txts[0],txts[1],txts[2],fontSize=1.4)
                pygame.draw.rect(screen, dark_gray, [size_w/3.12,size_h/2.16,size_w/2.3,size_h/5], 0,size_w//150)
                Write(round(size_w//100*8),"For Loop",black,[size_w/1.85,size_h/1.77])
                Write(round(size_w//100*8.5),"For Loop",lt_gray,[size_w/1.85,size_h/1.77])
                storedItems.clear()
                SR_icons.clear()
                SR_cords.clear()
                SR_holder=0
                SR_holder2=0
            elif courseLvl == 2:
                course.dialogTop(6.41,"Let's get some theory at first")
                strs = [
                    "while loop is a control flow statement for",
                    "specifying iteration which allows code to be", 
                    "be executed repeatedly"
                ] 
                pygame.draw.rect(screen,color1,[size_w/4.44,size_h/2.98,size_w/1.65,size_h/2.3],0,size_w//250)
                hght = size_h/2.09
                Write(round(size_w//100*2.6),"Definition",red,[size_w/1.92,size_h/2.51])
                for x in strs:
                    Write(round(size_w//100*2),x,color3,[size_w/1.92,hght])
                    hght += size_h/10
            elif courseLvl == 3:
                notBlocked = False
                txts = [
                    "Important things first, let's check",
                    "how the syntax looks like"
                ]
                course.dialogTop(6.41,txts[0],txts[1])
                course.consoleExample("For x in object:",hght=3,left=True)
                course.consoleExample("instrucions",hght=2.02)
                analiseBtn = course.centeredBtn(1.44,purple,"Analyze")

                if event.type == MOUSEMOTION and analiseBtn.collidepoint(mouse_pos):
                    course.centeredBtn(1.44,lt_blue,"Analyze")
                    course.centeredBtn(1.44,dark_blue,"",border=size_w//250)
                elif event.type == MOUSEBUTTONDOWN and analiseBtn.collidepoint(mouse_pos):
                    courseLvl += 1
            elif courseLvl == 4:
                notBlocked = True
                hght = size_h/4.99
                syntaxList = ['For','x','in','object','instructions']
                desc = [
                    "Main keyword added at the beggining",
                    "iterator holding value from iteration",
                    "keyword to iterate 'x' as objects from object",
                    "Object like function,list or string",
                    "instructions to be made with iteration"
                ]
                for x in range(5):
                    pygame.draw.rect(screen, color1, [size_w/4.45,hght,size_w/11,size_h/11], 0,size_w//150)
                    if x == 4:
                        Write(round(size_w//100*0.9),syntaxList[x],color3,[size_w/4.45+(size_w/11)/2,hght+(size_h/11)/2])
                    else:
                        Write(round(size_w//100*1.1),syntaxList[x],color3,[size_w/4.45+(size_w/11)/2,hght+(size_h/11)/2])
                    WriteItalic(round(size_w//100*2),'-',color3,[size_w/2.94,hght+(size_h/11)/2])
                    Write(round(size_w//100*1.8),desc[x],color3,[size_w/1.7,hght+(size_h/11)/2])
                    hght += size_h/8
            elif courseLvl == 5:
                txts = [
                    "Let's take an 'Object' element to",
                    "check what can it be and how it works"
                ]
                course.dialogTop(6.41,txts[0],txts[1],fontSize=1.6)
                course.consoleExample("Object can be:",3.46)
                course.consoleExample("List/Set/Tupple",2.23,left=True)
                course.consoleExample("String",1.65,left=True)
                course.consoleExample("Range() function",1.31,left=True)
            elif courseLvl == 6:
                notBlocked = False
                course.dialogTop(6.41,"Object as list:")
                course.consoleExample("circles = [green,orange,red,purple]",3.62,fontSize=1.9)
                course.consoleExample("for circle in circles:",2.32,left=True)
                course.consoleExample("draw_circle()",1.69)
                execBtn = course.centeredBtn(1.25,dark_green,"Execute")
                if event.type == MOUSEMOTION and execBtn.collidepoint(mouse_pos):
                    course.centeredBtn(1.25,green,"Execute")
                    course.centeredBtn(1.25,dark_green,"",border=size_w//250)
                elif event.type == MOUSEBUTTONDOWN and execBtn.collidepoint(mouse_pos):
                    courseLvl += 1
                    done = False
            elif courseLvl == 7:
                txts = [
                    "As you can see this for loop will iterate",
                    "through given list with it's every element",
                    "and do given instructions with it"
                ]
                course.dialogTop(6.41,txts[0],txts[1],txts[2],fontSize=1.4)
                if notBlocked:
                    Write(round(size_w//100*2.5),"Done!",green,[size_w/1.93,size_h/1.18])
            elif courseLvl == 8:
                notBlocked = True
                txts = [
                    "So yeah, this is how iterating through lists",
                    "works, every element of the list is taken and",
                    "held as list's iterator until instructions with",
                    "this element are done, then iterator has new value",
                    "from this list which is just next one element of it,",
                    "when all elements have been iterated loop ends"
                ]
                course.dialogStandard(2.6,txts[0],txts[1],txts[2],txts[3],txts[4],txts[5],fontSize=1.3)
            elif courseLvl == 9:
                course.dialogTop(6.41,"So you've learned about lists, time","for next object for iterations which","is string variable")
                Write(round(size_w//100*4),'"Example of string"',orange,[size_w/1.87,size_h/1.71])
            elif courseLvl == 10:
                notBlocked = False
                iterator = 1
                txts = [
                    "Iterating through strings works the same way",
                    "as in lists, but in this situation string is",
                    "treated as list and every character in string",
                    "is treated like an element of a list"
                ]
                course.dialogTop(5.8,txts[0],txts[1],txts[2],txts[3],fontSize=1.4)
                nextBtn = course.centeredBtn(1.76,purple,"Show example",adjustToDialog=True,fontSize=1.4)
                
                if event.type == MOUSEMOTION and nextBtn.collidepoint(mouse_pos):
                    course.centeredBtn(1.76,lt_blue,"Show example",adjustToDialog=True,fontSize=1.4)
                    course.centeredBtn(1.76,dark_blue,"",adjustToDialog=True,fontSize=1.4,border=size_w//250)
                elif event.type == MOUSEBUTTONDOWN and nextBtn.collidepoint(mouse_pos):
                    courseLvl += 1
            elif courseLvl == 11:
                if iterator == 5:
                    notBlocked = True
                word = '"World"'
                course.consoleExample(f'For x in {word}:',10.11,left=True)
                course.consoleExample('print(x)',3.9)
                Write(round(size_w//100*3),"x is:",red,[size_w/1.94,size_h/1.94])
                Write(round(size_w//100*1.6),f"iteration round: {iterator}",red,[size_w/1.38,size_h/1.94])

                Write(round(size_w//100*3),f'"{word[iterator]}"',orange,[size_w/1.94,size_h/1.61])

                next = Write(round(size_w//100*3),f'>',lt_blue,[size_w/1.59,size_h/1.61])
                back = Write(round(size_w//100*3),f'<',lt_blue,[size_w/2.47,size_h/1.61])

                Write(round(size_w//100*2,5),f'"World"[{iterator-1}]',lt_blue,[size_w/1.94,size_h/1.32])

                if event.type == MOUSEMOTION:
                    if next.get_rect().collidepoint(mouse_pos):
                        Write(round(size_w//100*3),f'>',logoBlue,[size_w/1.59,size_h/1.61])
                    elif back.get_rect().collidepoint(mouse_pos):
                        Write(round(size_w//100*3),f'<',logoBlue,[size_w/2.47,size_h/1.61])
                elif event.type == MOUSEBUTTONDOWN:
                    if next.get_rect().collidepoint(mouse_pos):
                        if iterator < 5:
                            iterator += 1
                        else:
                            Write(round(size_w//100*3),f'>',red,[size_w/1.59,size_h/1.61])
                    elif back.get_rect().collidepoint(mouse_pos): 
                        if iterator > 1:
                            iterator -= 1  
                        else:
                            Write(round(size_w//100*3),f'<',red,[size_w/2.47,size_h/1.61])                  
            elif courseLvl == 12:
                notBlocked = True
                done = False
                txts = [
                    "The next object is range() function",
                    "that takes two arguments(range(start,end))",
                    "e.g. range(2,5), but you can also only give one",
                    "argument like range(5), then end is",
                    "5(as given) and start is by default 0,",
                    "so the same as range(0,5)"
                ]
                course.dialogStandard(2.6,txts[0],txts[1],txts[2],txts[3],txts[4],txts[5],fontSize=1.4)
            elif courseLvl == 13:
                if not done:
                    notBlocked = False
                else:
                    notBlocked = True
                txts = [
                    "It's worth to mention that range()",
                    "'end' value is not included to iteration"
                ]
                course.dialogTop(6.41,txts[0],txts[1])
                course.consoleExample("For x in range(2,8):",3.32,left=True)
                course.consoleExample("print(x)",2.18)

                if not done:
                    startBtn = course.centeredBtn(1.5,dark_green,"Check")
                else:
                    Write(round(size_w//100*2,5),"x results:",red,[size_w/1.93,size_h/1.45])
                    Write(round(size_w//100*3),"2    3    4   5   6   7",color3,[size_w/1.93,size_h/1.29])

                try:
                    if event.type == MOUSEMOTION and startBtn.collidepoint(mouse_pos):
                        course.centeredBtn(1.5,green,"Check")
                        course.centeredBtn(1.5,dark_green,"",border=size_w//250)
                    elif event.type == MOUSEBUTTONDOWN and startBtn.collidepoint(mouse_pos):
                        done = True
                        pygame.event.post(pygame.event.Event(pygame.KEYDOWN))
                except:
                    pass
            elif courseLvl == 14:
                notBlocked = False
                txts = [
                    "Okay, let's do something more interesting,",
                    "we will use range() function with",
                    "single argument to accomplish that",
                ]
                course.dialogTop(6.41,txts[0],txts[1],txts[2],fontSize=1.4)
                course.consoleExample("For x in range(5):",2.59,left=True)
                course.consoleExample("spawn_enemy()",1.83)
                execBtn = course.centeredBtn(1.32,purple,"Execute")

                if event.type == MOUSEMOTION and execBtn.collidepoint(mouse_pos):
                    course.centeredBtn(1.32,lt_blue,"Execute")
                    course.centeredBtn(1.32,dark_blue,"",border=size_w//250)
                elif event.type == MOUSEBUTTONDOWN and execBtn.collidepoint(mouse_pos):
                    courseLvl += 1
                    done = False
            elif courseLvl == 15:
                if len(SR_icons) < 1:
                    map = pygame.image.load(r"{}/Images/Game/sr/garage.jpg".format(dirPath))
                    map = pygame.transform.scale(map, [int(size_w/1.6),int(size_h/1.8)])
                    SR_icons.append(map)
                    iron_sight = pygame.image.load(r"{}/Images/Game/iron_sight.png".format(dirPath))
                    iron_sight = pygame.transform.scale(iron_sight, [int(size_w/3.90),int(size_h/2.19)])
                    SR_icons.append(iron_sight)
                    iron_sight_shoot = pygame.image.load(r"{}/Images/Game/iron_sight_shoot.png".format(dirPath))
                    iron_sight_shoot = pygame.transform.scale(iron_sight_shoot, [int(size_w/3.90),int(size_h/2.09)])
                    SR_icons.append(iron_sight_shoot)
                    enemy1 = pygame.image.load(f"{dirPath}/Images/Game/sr/enemy1.png")
                    enemy1 = pygame.transform.scale(enemy1, [int(size_w/12),int(size_h/6)])
                    SR_icons.append(enemy1)
                    enemy2 = pygame.image.load(f"{dirPath}/Images/Game/sr/enemy2.png")
                    enemy2 = pygame.transform.scale(enemy2, [int(size_w/30),int(size_h/14)])
                    SR_icons.append(enemy2)
                    enemy3 = pygame.image.load(f"{dirPath}/Images/Game/sr/enemy3.png")
                    enemy3 = pygame.transform.scale(enemy3, [int(size_w/30),int(size_h/14)])
                    SR_icons.append(enemy3)
                mapJPG = screen.blit(SR_icons[0],[size_w/4.57,size_h/5.57])
                if isinstance(SR_holder2,int):
                    SR_holder2 = []
                if 1 not in SR_holder2:
                    enemy1 = screen.blit(SR_icons[3],[size_w/1.54,size_h/2.27])
                if 2 not in SR_holder2:
                    enemy2 = screen.blit(SR_icons[4],[size_w/2.5,size_h/2])
                if 3 not in SR_holder2:
                    enemy3 = screen.blit(pygame.transform.flip(SR_icons[4], True, False),[size_w/1.58,size_h/2])
                if 4 not in SR_holder2:
                    enemy4 = screen.blit(SR_icons[5],[size_w/2.27,size_h/2.04])
                if 5 not in SR_holder2:
                    enemy5 = screen.blit(pygame.transform.flip(SR_icons[3], True, False),[size_w/1.9,size_h/2.27])
                
                SR_holder2.sort()
                if SR_holder2 == [1,2,3,4,5]:
                    course.dialogTop(6.41,"Good job recruit!","I hope I taught you how","this works, you can go futher",bckgr=True)
                    notBlocked = True
                else:
                    course.dialogTop(6.41,"Oh damn, that was not the best idea!","Shoot them!",bckgr=True)
                    notBlocked = False

                correctH = mouse_pos[1]<size_h/1.74
                correctW = size_w/1.34 > mouse_pos[0] > size_w/3.06                
                if correctW and correctH and SR_holder == 1:
                    pygame.mouse.set_visible(False)
                    sight_rect=SR_icons[1].get_rect()
                    cords = [mouse_pos[0]-sight_rect[2]/2.1,mouse_pos[1]-sight_rect[3]/7]
                    screen.blit(SR_icons[1],cords)
                correctH = size_h/3.25 < mouse_pos[1] < size_h/1.74
                correctW = size_w/1.34 > mouse_pos[0] > size_w/3.06
                if event.type == MOUSEMOTION:
                    if mapJPG.collidepoint(mouse_pos) and correctW and correctH:
                        SR_holder = 1
                    else:
                        pygame.mouse.set_visible(True)
                        SR_holder = 0
                elif event.type == MOUSEBUTTONDOWN and correctH and correctW:
                    sight_rect = SR_icons[1].get_rect()
                    cords = [mouse_pos[0]-sight_rect[2]/2.1,mouse_pos[1]-sight_rect[3]/7]
                    screen.blit(SR_icons[2],cords)
                    pygame.mouse.set_pos([mouse_pos[0], mouse_pos[1]-size_h//100])
                    try:
                        if enemy1.collidepoint(mouse_pos):
                            SR_holder2.append(1)
                    except:
                        pass
                    try:
                        if enemy2.collidepoint(mouse_pos):
                            SR_holder2.append(2)
                    except:
                        pass
                    try:
                        if enemy3.collidepoint(mouse_pos):
                            SR_holder2.append(3)
                    except:
                        pass
                    try:
                        if enemy4.collidepoint(mouse_pos):
                            SR_holder2.append(4)
                    except:
                        pass
                    try:
                        if enemy5.collidepoint(mouse_pos):
                            SR_holder2.append(5)   
                    except:
                        pass
            elif courseLvl == 16:
                if not done:
                    notBlocked = False
                    course.dialogTop(6.41,"That's not end with range() function yet,","but we will try something less dangerous",fontSize=1.4)
                    goBtn = course.centeredBtn(2.81,purple,"Let's try",adjustToDialog=True)

                    if event.type == MOUSEMOTION and goBtn.collidepoint(mouse_pos):
                        course.centeredBtn(2.81,lt_blue,"Let's try",adjustToDialog=True)
                        course.centeredBtn(2.81,dark_blue,"",adjustToDialog=True,border=size_w//250)
                    elif event.type == MOUSEBUTTONDOWN and goBtn.collidepoint(mouse_pos):
                        done = True
                        storedTimeValue = round(float(time.process_time()),1)
                else:
                    course.dialogTop(6.41,"So you can also give third argument which","is jump, let's try it in practic",fontSize=1.4)
                    
                    pygame.draw.line(screen, color3, [size_w/1.8,size_h/3.21], [size_w/1.8,size_h/1.2], size_w//1000)
                    pygame.draw.line(screen, color3, [size_w/2.9,size_h/1.8], [size_w/1.33,size_h/1.8], size_w//1000)
            elif courseLvl == 17:
                notBlocked = False
                course.dialogTop(6.41,"Similar to while, for loop also has","possiblity to attach else keyword")
                course.consoleExample("for x in range(5):",3.49,left=True)
                course.consoleExample("print(x)",2.27)
                course.consoleExample("else:",1.68,left='mega')
                course.consoleExample('print("Ended")',1.34)

                resultBtn = pygame.draw.rect(screen, dark_green, [size_w/1.38,size_h/1.92,size_w/9,size_h/10],0,size_w//250)
                Write(round(size_w//100*1.5),"See results",color1,[size_w/1.28,size_h/1.75])

                if event.type == MOUSEMOTION and resultBtn.collidepoint(mouse_pos):
                    pygame.draw.rect(screen, green, [size_w/1.38,size_h/1.92,size_w/9,size_h/10],0,size_w//250)
                    pygame.draw.rect(screen, dark_green, [size_w/1.38,size_h/1.92,size_w/9,size_h/10],size_w//250,size_w//250)
                    Write(round(size_w//100*1.5),"See results",color3,[size_w/1.28,size_h/1.75])
                elif event.type == MOUSEBUTTONDOWN and resultBtn.collidepoint(mouse_pos):
                    courseLvl += 1
            elif courseLvl == 18:
                notBlocked = True
                course.dialogTop(6.41,"So else is executed only once and","that happens when for loop is done")
                Write(round(size_w//100*3),"Results",red,[size_w/1.83,size_h/3.08])
                results = ["0","1","2","3","4",'"Ended"']
                hght = size_h/2.5
                for result in results:
                    Write(round(size_w//100*3),result,color3,[size_w/1.83,hght])
                    hght += size_h/15
            elif courseLvl == 19:
                notBlocked = False
                course.dialogTop(6.41,"Similar to while loop, there's also a break","instruction - it works the same way",fontSize=1.4)
                checkBtn = course.centeredBtn(2.69,dark_green,"Check",adjustToDialog=True)

                if event.type == MOUSEMOTION and checkBtn.collidepoint(mouse_pos):
                    course.centeredBtn(2.69,green,"Check",adjustToDialog=True)
                    course.centeredBtn(2.69,dark_green,"",adjustToDialog=True,border=size_w//250)
                elif event.type == MOUSEBUTTONDOWN and checkBtn.collidepoint(mouse_pos):
                    courseLvl += 1
                    storedTimeValue = round(float(time.process_time()),1)
                    done = True
            elif courseLvl == 20:
                course.consoleExample("For x in range(50):",12.19,left=True)
                course.consoleExample("print(x)",4.13,left=False)


                if not done:
                    Write(round(size_w//100*2.2),"Ended by break instruction",red,[size_w/1.92,size_h/1.82])
                    Write(round(size_w//100*2.2),"You can go further",green,[size_w/1.91,size_h/1.45])
                    notBlocked = True
                else:
                    breakBtn = course.centeredBtn(1.55,dark_red,"Break")

                try:
                    if event.type == MOUSEMOTION and breakBtn.collidepoint(mouse_pos):
                        course.centeredBtn(1.55,red,"Break")
                        course.centeredBtn(1.55,dark_red,"",border=size_w//250)
                    elif event.type == MOUSEBUTTONDOWN and breakBtn.collidepoint(mouse_pos):
                        done = False
                except:
                    pass
            elif courseLvl == 21:
                notBlocked = False
                course.dialogTop(6.41,"As you can guess there's also continue","instruction that you know from while loops",fontSize=1.4)
                checkBtn = course.centeredBtn(2.69,dark_green,"Check",adjustToDialog=True)

                if event.type == MOUSEMOTION and checkBtn.collidepoint(mouse_pos):
                    course.centeredBtn(2.69,green,"Check",adjustToDialog=True)
                    course.centeredBtn(2.69,dark_green,"",adjustToDialog=True,border=size_w//250)
                elif event.type == MOUSEBUTTONDOWN and checkBtn.collidepoint(mouse_pos):
                    courseLvl += 1
                    storedTimeValue = round(float(time.process_time()),1)
                    done = True
            elif courseLvl == 22:
                course.consoleExample("For x in range(50):",12.19,left=True)
                course.consoleExample("print(x)",4.13,left=False)


                if not done:
                    notBlocked = True
                contBtn = course.centeredBtn(1.55,purple,"Continue")

                try:
                    if event.type == MOUSEMOTION and contBtn.collidepoint(mouse_pos):
                        course.centeredBtn(1.55,lt_blue,"Continue")
                        course.centeredBtn(1.55,dark_blue,"",border=size_w//250)
                    elif event.type == MOUSEBUTTONDOWN and contBtn.collidepoint(mouse_pos):
                        storedTimeValue = round(float(time.process_time()),1)
                        done = False
                        Write(round(size_w//100*5),"Reset!",green,[size_w/1.93,size_h/1.18])
                except:
                    pass                
            elif courseLvl == 23:
                txts = [
                    "Next thing I prepared for you is double for",
                    "loop, which is simply a loop inside a loop,",
                    "but this one have a nice specific use"
                ]
                course.dialogStandard(2.6,txts[0],txts[1],txts[2],fontSize=1.5)
            elif courseLvl == 24:
                if iterator < 2:
                    storedTimeValue = round(float(time.process_time()),1)
                    iterator = 2
                course.consoleExample("for x in range(5):",2.27,left=True)
                course.consoleExample("for x in range(5):",1.68,left=False)
                course.consoleExample("draw_rect()",1.33,left=False)
                skipBtn = pygame.draw.rect(screen, purple, [size_w/1.45,size_h/5.02,size_w/8,size_h/10], 0,15)
                Write(round(size_w//100*2.5),"Skip",color1,[size_w/1.33,size_h/3.96])

                if event.type == MOUSEMOTION and skipBtn.collidepoint(mouse_pos):
                    pygame.draw.rect(screen, lt_blue, [size_w/1.45,size_h/5.02,size_w/8,size_h/10], 0,15)
                    pygame.draw.rect(screen, purple, [size_w/1.45,size_h/5.02,size_w/8,size_h/10], size_w//250,15)
                    Write(round(size_w//100*2.5),"Skip",color3,[size_w/1.33,size_h/3.96])
                elif event.type == MOUSEBUTTONDOWN and skipBtn.collidepoint(mouse_pos):
                    courseLvl += 1
                    notBlocked = True
            elif courseLvl == 25:
                txts = [
                    "Last, but not least is pass instruction - ",
                    "it is a keyword to leave instruction as",
                    "none action, lemme show you an example"
                ]
                course.dialogTop(6.41,txts[0],txts[1],txts[2],fontSize=1.4)
                course.consoleExample("for x in range(10):",2.38,left=True)
                course.consoleExample("pass",1.73)
            elif courseLvl == 26:
                course.dialogTop(6.41,"This will return nothing as pass is a way","to 'cheat' and leave empty instruction",fontSize=1.4)
                strs = [
                    "for loops cannot be empty, but if you for some", 
                    "reason have a for loop with no content, put in", 
                    "the pass statement to avoid getting an error."
                ] 
                pygame.draw.rect(screen,color1,[size_w/4.44,size_h/2.98,size_w/1.65,size_h/2.3],0,size_w//250)
                hght = size_h/2.09
                Write(round(size_w//100*2.6),"Pass ~ W3Schools",red,[size_w/1.92,size_h/2.51])
                for x in strs:
                    Write(round(size_w//100*2),x,color3,[size_w/1.92,hght])
                    hght += size_h/10
                course.shooting_range.clearVars()
            elif courseLvl == 27:
                notBlocked = False
                course.dialogTop(6.41,"Oh right, time to test your","abilities, are you ready recruit?")
                readyBtn = course.centeredBtn(2.83,purple,"Ready",adjustToDialog=True)

                if event.type == MOUSEMOTION and readyBtn.collidepoint(mouse_pos):
                    course.centeredBtn(2.83,lt_blue,"Ready",adjustToDialog=True)
                    course.centeredBtn(2.83,purple,"",adjustToDialog=True,border=size_w//250)
                elif event.type == MOUSEBUTTONDOWN and readyBtn.collidepoint(mouse_pos):
                    courseLvl += 1
            elif courseLvl == 28: #QUIZ
                notBlocked = False
                if isinstance(SR_holder,float):
                    SR_holder = 0
                if not done:
                    if isinstance(SR_holder,str):
                        SR_holder = 0
                    if isinstance(SR_holder2,str) or SR_holder2 == 0:
                        SR_holder2 = 1
                    course.dialogTop(6.41,"Oh right recruit, grab a gun","and show me what you've learned")
                    if len(SR_icons)<1:
                        m4 = pygame.image.load(r"{}/Images/Game/sr/m4.png".format(dirPath))
                        m4 = pygame.transform.scale(m4, [int(size_w/5),int(size_h/5)])
                        SR_icons.append(m4)
                        mp5 = pygame.image.load(r"{}/Images/Game/sr/mp5.png".format(dirPath))
                        mp5 = pygame.transform.scale(mp5, [int(size_w/6),int(size_h/8)])
                        SR_icons.append(mp5)
                        m4m = pygame.image.load(r"{}/Images/Game/sr/m4marked.png".format(dirPath))
                        m4m = pygame.transform.scale(m4m, [int(size_w/5),int(size_h/5)])
                        SR_icons.append(m4m)
                        mp5m = pygame.image.load(r"{}/Images/Game/sr/mp5marked.png".format(dirPath))
                        mp5m = pygame.transform.scale(mp5m, [int(size_w/6),int(size_h/8)])
                        SR_icons.append(mp5m)
                    try:
                        gun1 = screen.blit(SR_icons[SR_holder],[size_w/3.41,size_h/2.54])
                        gun2 = screen.blit(SR_icons[SR_holder2],[size_w/1.74,size_h/2.32])
                    except:
                        pass
                    if isinstance(selected,int):
                        nextBtn = course.centeredBtn(1.37,dark_green,"Go")
                    try:
                        if event.type == MOUSEMOTION and nextBtn.collidepoint(mouse_pos):
                            course.centeredBtn(1.37,green,"Go")
                            course.centeredBtn(1.37,dark_green,"",border=size_w//250)
                    except:
                        pass
                    if event.type == MOUSEBUTTONDOWN and event.button==1:
                        try:
                            if gun1.collidepoint(mouse_pos):
                                SR_holder = 2
                                SR_holder2 = 1
                                selected = 1
                            elif gun2.collidepoint(mouse_pos):
                                SR_holder = 0
                                SR_holder2 = 3
                                selected = 2
                        except:
                            pass    
                        try:
                            if nextBtn.collidepoint(mouse_pos):
                                SR_icons.clear()       
                                SR_holder = 0
                                SR_holder2 = 0
                                iterator = 1
                                done = True
                                storedTimeValue = round(float(time.process_time()),2)
                        except:
                            pass              
                        
                else:
                    questions = [
                        "Which is correct object?",
                        "Which is correct for list iteration?",
                        "At range(1,10,3) 3 is:",
                        "Which one gives output: 0 1 2 3 4",
                        "Else is executed:",
                        "What is break used for?",
                        "Which instruction is used to restart loop:",
                        "Output of for x in range(0,8,2): print(x)",
                        "Double for loop is good for:",
                        "Which one can be iterated by for loop?",
                        "Which is start value for range(10)?",
                        "Which one gives all the numbers from 1 to 10?",
                        "For can iterate through set, tupple and list"
                    ]
                    allAnswers = [
                        ["True/False","15.093","Range(5)"],
                        ["for x at list:","for x in list:","for x by list:"],
                        ["Jump value","End value","Start value"],
                        ["for x in range(4): print(x)","for x in range(5): print(x)","for x in range(0,4): print(x)"],
                        ["Every iteration","There's no else at for loop","Once"],
                        ["Breaking loop","Restarting loop","Leaving none instruction"],
                        ["Restart","Continue","Refresh"],
                        ["Error","1 3 5 7","0 2 4 6"],
                        ["Drawing figures","It has no use","You can't make double for loop"],
                        ["Float","Integer","String"],
                        ["10","0","None"],
                        ["range(1,10)","range(11)","range(1,11)"],
                        ["Yes","No","Only list"]
                    ]
                    correctAnswers = [2,1,0,1,2,0,1,2,0,2,1,2,0] #0-A 1-B 2-C

                    course.shooting_range.quiz.start(questions,allAnswers,correctAnswers)                
            elif courseLvl == 29:
                if len(SR_icons)<1:
                    reward = pygame.image.load(r"{}/Images/Game/sr/dogtag1.png".format(dirPath))
                    reward = pygame.transform.scale(reward, [int(size_w/3.90),int(size_h/2.19)])
                    reward = pygame.transform.rotate(reward, 60.0)
                    SR_icons.append(reward)
                if SR_holder==0:
                    SR_holder = 1
                screen.blit(SR_icons[0],[size_w/3.16,size_h/3])
                name = WriteItalic(round(size_w//100*SR_holder),getName(),darker_gray,[size_w/1.81,size_h/1.63])
                nameRect = name.get_rect()
                if (nameRect[0]+nameRect[2])<size_w/1.66:
                    SR_holder += 2/len(getName())
                    pygame.event.post(pygame.event.Event(pygame.KEYDOWN))
                course.dialogTop(6.41,"You've finished my course recruit!","I'm proud, there's your reward so","you can remember what you achieved",fontSize=1.4)

                finishBtn = course.centeredBtn(1.22,dark_green,"Finish")

                if event.type == MOUSEMOTION and finishBtn.collidepoint(mouse_pos):
                    course.centeredBtn(1.22,green,"Finish")
                    course.centeredBtn(1.22,dark_green,"",border=size_w//250)
                elif event.type == MOUSEBUTTONDOWN:
                    if finishBtn.collidepoint(mouse_pos):
                        if getCourseLvl() < 7:
                            changeCourselvl(7)
                        activeMenu = True
                        courseLvl = 1  
                        iterator = 1 
                        course.shooting_range.clearVars()
                        bckgrMusicPlayed = False
    def lesson7():
        global mentorIcon,activeMain,held,courseLvl,notBlocked,iterator,activeMenu,done
        global bckgrMusicPlayed,errorShowed,storedItems,storedCords,chosen,selected,storedTime,storedTimeValue
        global SR_icons,SR_cords,SR_iterator,SR_holder,SR_holder2
        if activeMain and not errorShowed:
            course.standardLessonEvents("lesson7",29,condition=notBlocked)
        if activities[0] and not activeMenu and str(activeLesson)[17:-23]=="lesson7" and not errorShowed:
            try:
                mentorIcon = pygame.image.load(r"{}/Images/Game/sr/soldier6.png".format(dirPath))
                mentorIcon = pygame.transform.scale(mentorIcon, [int(size_w/12),int(size_h/6)]) #[int(size_w/10.6),int(size_h/6)]
            except:
                errorInit("Failed to load mentor icon!",fontSize=1.8)
            language = getLang()
    def lesson8():
        course.standardLessonEvents("lesson8",99) 
    def lesson9():
        course.standardLessonEvents("lesson9",99)
class LookFor(pygame.sprite.Sprite):
    def startScreen():
        global activeAny,inputBox,searchBox,activeWriting,lookForPhrase,clearBtn,searching
        if activities[1]:
            if pygame.event.get_blocked(MOUSEMOTION):
                pygame.event.set_allowed(MOUSEMOTION)
            bckgr = pygame.draw.rect(screen, color2, [size_w/5,size_h/16,size_w/1.5,size_h/1.1],0,10)
            inputBox = pygame.draw.rect(screen, color1, [size_w/3.1,size_h/4,size_w/2.5,size_h/8],0,10)
            language = getLang()
            if language == "ENG":
                Write(round(size_w//100*2.1),"What are you looking for {}?".format(getName().lower()),color3,[size_w/1.9,size_h/6])
            else:
                Write(round(size_w//100*2.1),"Poszukujesz czegoś {}?".format(getName().lower()),color3,[size_w/1.9,size_h/6]) 
            searchBox = pygame.draw.rect(screen, color1, [size_w/1.35,size_h/4,size_w/12,size_h/8],0,10)
            searchBoxCirc = pygame.draw.circle(screen, color2, [size_w/1.26,size_h/3.3], size_w//60, 2)
            searchBoxLine = pygame.draw.line(screen, color2, [size_w/1.32,size_h/2.9], [size_w/1.283,size_h/3.15], 6)            

            if len(lookForPhrase) >= 1:   
                clearBtn = pygame.draw.rect(screen, dark_red, [size_w/4.28,size_h/4,size_w/15,size_h/8],0,10)
                clearTxt = Write(round(size_w//100*4),"X",color1,[size_w/3.75,size_h/3.13])
            if activeWriting:
                inputBoxBord = pygame.draw.rect(screen, color3, [size_w/3.1,size_h/4,size_w/2.5,size_h/8],1,10)                    
                inputBoxTxt = Write(round(size_w//100*3),lookForPhrase+"|",color3,[size_w/1.9,size_h/3.2])
            else:
                inputBoxBord = pygame.draw.rect(screen, color1, [size_w/3.1,size_h/4,size_w/2.5,size_h/8],1,10) 
                if len(lookForPhrase) < 1:       
                    if language == "ENG":            
                        inputBoxTxt = WriteItalic(round(size_w//100*3.5),"Enter text here...",color2,[size_w/1.9,size_h/3.2])
                    else:
                        inputBoxTxt = WriteItalic(round(size_w//100*3.5),"Wpisz tekst tutaj...",color2,[size_w/1.9,size_h/3.2])
                else:
                    inputBoxTxt = Write(round(size_w//100*3),lookForPhrase,color3,[size_w/1.9,size_h/3.2])
            if searching and len(lookForPhrase)>0:
                if language == "ENG":
                    WriteItalic(round(size_w//100*5),"None results found",color3,[size_w/1.9,size_h/1.6])
                else:
                    WriteItalic(round(size_w//100*5),"Nie znaleziono wyników",color3,[size_w/1.9,size_h/1.6])
            if event.type == MOUSEBUTTONDOWN and activities[1]:
                if activities[1]:   
                    inputBox = pygame.draw.rect(screen, color1, [size_w/3.1,size_h/4,size_w/2.5,size_h/8],0,10)
                    if language == "ENG":            
                        inputBoxTxt = WriteItalic(round(size_w//100*3.5),"Enter text here...",color2,[size_w/1.9,size_h/3.2])
                    else:
                        inputBoxTxt = WriteItalic(round(size_w//100*3.5),"Wpisz tekst tutaj...",color2,[size_w/1.9,size_h/3.2])

                    isCorrectActivity()
                    if inputBox.collidepoint(mouse_pos):
                        inputBox = pygame.draw.rect(screen, color1, [size_w/3.1,size_h/4,size_w/2.5,size_h/8],0,10)
                        inputBoxBord = pygame.draw.rect(screen, color3, [size_w/3.1,size_h/4,size_w/2.5,size_h/8],1,10)                    
                        inputBoxTxt = Write(round(size_w//100*1.7),lookForPhrase+"|",color3,[size_w/1.9,size_h/3.2])
                        activeWriting = True
                    else:
                        inputBox = pygame.draw.rect(screen, color1, [size_w/3.1,size_h/4,size_w/2.5,size_h/8],0,10)
                        inputBoxBord = pygame.draw.rect(screen, color1, [size_w/3.1,size_h/4,size_w/2.5,size_h/8],1,10)                    
                        if len(lookForPhrase) < 1:                   
                            if language == "ENG":            
                                inputBoxTxt = WriteItalic(round(size_w//100*3.5),"Enter text here...",color2,[size_w/1.9,size_h/3.2])
                            else:
                                inputBoxTxt = WriteItalic(round(size_w//100*3.5),"Wpisz tekst tutaj...",color2,[size_w/1.9,size_h/3.2])
                        else:
                            inputBoxTxt = Write(round(size_w//100*3),lookForPhrase,color3,[size_w/1.9,size_h/3.2])
                        activeWriting = False
                    try:
                        if len(lookForPhrase) >= 1:   
                            if clearBtn.collidepoint(mouse_pos):
                                lookForPhrase = ""
                                searching = False
                            else:
                                pygame.draw.rect(screen, dark_red, [size_w/4.28,size_h/4,size_w/15,size_h/8],0,10)
                                Write(round(size_w//100*4),"X",color1,[size_w/3.75,size_h/3.13])                        
                    except:
                        pass
                    if searchBox.collidepoint(mouse_pos) and len(lookForPhrase)>0:
                        searching = True
            if event.type == MOUSEMOTION and activities[1]:
                if searchBox.collidepoint(mouse_pos):
                    searchBox = pygame.draw.rect(screen, color1, [size_w/1.35,size_h/4,size_w/12,size_h/8],0,10)
                    searchBoxCirc = pygame.draw.circle(screen, color3, [size_w/1.26,size_h/3.3], size_w//60, 2)
                    searchBoxLine = pygame.draw.line(screen, color3, [size_w/1.32,size_h/2.9], [size_w/1.283,size_h/3.15], 6)
                try:
                    if clearBtn.collidepoint(mouse_pos) and len(lookForPhrase) >= 1:
                        clearBtn = pygame.draw.rect(screen, red, [size_w/4.28,size_h/4,size_w/15,size_h/8],0,10)
                        clearTxt = Write(round(size_w//100*4),"X",color3,[size_w/3.75,size_h/3.13])
                except:
                    pass
            if event.type == KEYDOWN and activities[1] and activeWriting:
                if event.key == pygame.K_BACKSPACE:
                    try:
                        lookForPhrase = lookForPhrase[:-1]
                    except:
                        pass
                elif event.key == pygame.K_ESCAPE:
                    activeWriting = False
                elif event.key == pygame.K_RETURN:
                    searching = True
                    activeWriting = False
                elif event.key!=K_BACKSPACE and keys[K_LSHIFT] or keys[K_RSHIFT]:
                    if event.key==K_9:
                        lookForPhrase += "("
                    elif event.key==K_8:
                        lookForPhrase += "*"
                    elif event.key==K_7:
                        lookForPhrase += "&"
                    elif event.key==K_6:
                        lookForPhrase += "^"
                    elif event.key==K_5:
                        lookForPhrase += "%"
                    elif event.key==K_4:
                        lookForPhrase += "$"
                    elif event.key==K_2:
                        lookForPhrase += "@"
                    elif event.key==K_1:
                        lookForPhrase += "!"
                    elif event.key==K_0:
                        lookForPhrase += ")"
                    elif event.key==K_LEFTBRACKET:
                        lookForPhrase += "["
                    elif event.key == K_RIGHTBRACKET:
                        lookForPhrase += "]"
                    elif event.key == K_QUOTE:
                        lookForPhrase += "\""
                    elif event.key == K_3:
                        lookForPhrase += "#"
                    elif event.key == K_SEMICOLON:
                        lookForPhrase += ":"
                    elif event.key == K_SLASH:
                        lookForPhrase += "?"
                    elif event.key == K_MINUS:
                        lookForPhrase += "_"
                    else:
                        lookForPhrase += chr(event.key)
                elif event.key!=K_BACKSPACE and keys[K_LSHIFT] or keys[K_RSHIFT]:
                    if event.key == K_z:
                        lookForPhrase += "ż"
                    elif event.key == K_l:
                        lookForPhrase += "ł"
                elif len(lookForPhrase)<14 and event.key!=pygame.K_BACKSPACE:
                    try:
                        lookForPhrase += chr(event.key)
                    except:
                        pass                 
class Settings(pygame.sprite.Sprite):
    def startScreen():
        global activeAny,activeMain
        global size_w,size_h
        if activities[2]:
            language = getLang()
            if pygame.event.get_blocked(MOUSEMOTION):
                pygame.event.set_allowed(MOUSEMOTION)
            bckgr = pygame.draw.rect(screen, color2, [size_w/5,size_h/16,size_w/1.5,size_h/1.1],0,10)
            if language == "ENG":
                Write(size_w//100*2,"Want to change anything {}?".format(getName()),color3,[size_w/1.8,size_h/8])
            else:
                Write(size_w//100*2,"Chcesz coś zmienić {}?".format(getName()),color3,[size_w/1.8,size_h/8])
            isCorrectActivity()                   
    def resizing():
        global size,size_w,size_h,activeAny,TD_circs,selectingDisplay,SR_icons,SR_cords
        global hp1,hp2,rectCenter,TD_wdthStart,TD_hghtStart,DG_icons,TD_icon
        global storedCords,storedItems
        if activities[2]:
            language = getLang()
            if language == "ENG":
                resTxt = Write(size_w//100*2,"Resolution: {}:{}".format(size_w,size_h),color3,[size_w/1.8,size_h/2])
            else:
                resTxt = Write(size_w//100*2,"Rozdzielczość: {}:{}".format(size_w,size_h),color3,[size_w/1.8,size_h/2])
            resLine = pygame.draw.line(screen, color1, [size_w/1.3,size_h/1.7], [size_w/2.9,size_h/1.7], size_w//450)
            resCirc1 = pygame.draw.circle(screen, logoBlue, [size_w/2.5,size_h/1.7], size_w//50, 0)
            resCirc2 = pygame.draw.circle(screen, logoBlue, [size_w/2,size_h/1.7], size_w//50, 0)
            resCirc3 = pygame.draw.circle(screen, logoBlue, [size_w/1.65,size_h/1.7], size_w//50, 0)
            resCirc4 = pygame.draw.circle(screen, logoBlue, [size_w/1.4,size_h/1.7], size_w//50, 0)    

            if not selectingDisplay:
                if event.type == MOUSEMOTION and activeMain:
                    if resCirc1.collidepoint(mouse_pos):
                        pygame.draw.circle(screen, dark_blue, [size_w/2.5,size_h/1.7], size_w//60, 0)
                        Write(size_w//100*2,"1200:700",color3,[size_w/1.8,size_h/1.5])
                    elif resCirc2.collidepoint(mouse_pos):
                        pygame.draw.circle(screen, dark_blue, [size_w/2,size_h/1.7], size_w//60, 0)
                        Write(size_w//100*2,"1600:900",color3,[size_w/1.8,size_h/1.5])
                    elif resCirc3.collidepoint(mouse_pos):
                        pygame.draw.circle(screen, dark_blue, [size_w/1.65,size_h/1.7], size_w//60, 0)
                        Write(size_w//100*2,"X:Y",color3,[size_w/1.8,size_h/1.5])
                    elif resCirc4.collidepoint(mouse_pos):
                        pygame.draw.circle(screen, dark_blue, [size_w/1.4,size_h/1.7], size_w//60, 0)
                        if language == "ENG":
                            Write(size_w//100*2,"Default",color3,[size_w/1.8,size_h/1.5]) 
                        else:
                            Write(size_w//100*2,"Domyślne",color3,[size_w/1.8,size_h/1.5]) 
                elif event.type==MOUSEBUTTONDOWN and activeMain:
                    resCircs = [resCirc1,resCirc2,resCirc3,resCirc4]
                    res = [[1200,700],[1366,768],[1600,900],[displaySize.current_w,displaySize.current_h]]
                    for resCirc in resCircs:
                        if resCirc.collidepoint(mouse_pos):
                            index = resCircs.index(resCirc)
                            size_w = res[index][0]
                            size_h = res[index][1]
                            size = (size_w,size_h)
                            activeAny = False
                            activities[2] = False
                            TD_circs = []
                            DG_icons = []
                            TD_icon = ""
                            SR_icons.clear()
                            SR_cords.clear()
                            storedCords.clear()
                            storedItems.clear()
                            hp1 = size_w/2.66
                            hp2 = size_w/6
                            course.tower_defence.reset()
                            rectCenter = (size_w/1.5)/2 + size_w/5
                            start.useScreenDef()
                            start.welcomeScreen()             
    def theme():
        global size_w,size_h,activeMain,activeAny
        if activities[2]:
            choosing = False
            themeRect = pygame.draw.rect(screen, color1, [size_w/3.8,size_h/4.8,size_w/6,size_h/7], size_w//270,5)
            language = getLang()
            if language == "ENG":
                ThemeTxt = Write(size_w//100*3,"Theme",color1,[size_w/2.9,size_h/3.47])
            else:
                ThemeTxt = Write(size_w//100*3,"Motyw",color1,[size_w/2.9,size_h/3.47])

            activeThemeRect = pygame.draw.rect(screen, color1, [size_w/3.7,size_h/2.88,size_w/6.5,size_h/12], size_w//270,2)
            if language == "ENG":
                activeThemeTxt = Write(size_w//100*3,getTheme().upper(),color1,[size_w/2.9,size_h/2.55]) 
            else:
                if getTheme().upper() == "DARK":
                    activeThemeTxt = Write(size_w//100*3,"Ciemny",color1,[size_w/2.9,size_h/2.55])
                else:
                    activeThemeTxt = Write(size_w//100*3,"Jasny",color1,[size_w/2.9,size_h/2.55])

            if event.type == MOUSEMOTION and activeMain:
                themeChooseBckgr = pygame.draw.rect(screen, color2, [size_w/2.329,size_h/4.8,size_w/3,size_h/7], 0,0)
                if themeRect.collidepoint(mouse_pos) or themeChooseBckgr.collidepoint(mouse_pos):
                    choosing = True
                    themeChooseBckgr = pygame.draw.rect(screen, color1, [size_w/2.34,size_h/4.8,size_w/3,size_h/7], size_w//270,5)
                    opt1 = pygame.draw.rect(screen, color1, [size_w/2.24,size_h/4.6,size_w/8,size_h/8], size_w//270,15)
                    if language == "ENG":
                        opt1txt = Write(size_w//100*2,"Light",color1,[size_w/1.97,size_h/3.5])
                        opt2 = pygame.draw.rect(screen, color1, [size_w/1.65,size_h/4.6,size_w/8,size_h/8], size_w//270,15)
                        opt2txt = Write(size_w//100*2,"Dark",color1,[size_w/1.50,size_h/3.5])
                        if opt1.collidepoint(mouse_pos):
                            Write(size_w//100*2,"Light",color3,[size_w/1.97,size_h/3.5])
                        else:
                            Write(size_w//100*2,"Light",color1,[size_w/1.97,size_h/3.5])
                        if opt2.collidepoint(mouse_pos):
                            Write(size_w//100*2,"Dark",color3,[size_w/1.50,size_h/3.5])
                        else:
                            Write(size_w//100*2,"Dark",color1,[size_w/1.50,size_h/3.5])
                    else:
                        opt1txt = Write(size_w//100*2,"Jasny",color1,[size_w/1.97,size_h/3.5])
                        opt2 = pygame.draw.rect(screen, color1, [size_w/1.65,size_h/4.6,size_w/8,size_h/8], size_w//270,15)
                        opt2txt = Write(size_w//100*2,"Ciemny",color1,[size_w/1.50,size_h/3.5])
                        if opt1.collidepoint(mouse_pos):
                            Write(size_w//100*2,"Jasny",color3,[size_w/1.97,size_h/3.5])
                        else:
                            Write(size_w//100*2,"Jasny",color1,[size_w/1.97,size_h/3.5])
                        if opt2.collidepoint(mouse_pos):
                            Write(size_w//100*2,"Ciemny",color3,[size_w/1.50,size_h/3.5])
                        else:
                            Write(size_w//100*2,"Ciemny",color1,[size_w/1.50,size_h/3.5])
            elif event.type == MOUSEBUTTONDOWN and activeMain:
                opt1 = pygame.draw.rect(screen, color2, [size_w/2.24,size_h/4.6,size_w/8,size_h/8], size_w//270,15)
                opt2 = pygame.draw.rect(screen, color2, [size_w/1.65,size_h/4.6,size_w/8,size_h/8], size_w//270,15)
                if opt1.collidepoint(mouse_pos):
                    changeTheme("light")
                    activeAny = False
                    activities[2] = False
                    start.useScreenDef()
                    start.welcomeScreen()
                elif opt2.collidepoint(mouse_pos):
                    changeTheme("dark")
                    activeAny = False
                    activities[2] = False
                    start.useScreenDef()
                    start.welcomeScreen()
    def resetName():
        global activeMain,activeAny
        if activities[2]:
            nameResetRect = pygame.draw.rect(screen, color1, [size_w/3.8,size_h/1.3,size_w/6,size_h/7], size_w//270,5)
            language = getLang()
            if language == "ENG":
                nameResetTxt = Write(round(size_w//100*3),"Name",color1,[size_w/3.15,size_h/1.18])
            else:
                nameResetTxt = Write(round(size_w//100*3),"Nick",color1,[size_w/3.15,size_h/1.18])
            nameResetCirc = pygame.draw.circle(screen, color1, [size_w/2.55,size_h/1.19], size_w//45, size_w//225)
            nameResetLine = pygame.draw.line(screen, color2, [size_w/2.85,size_h/1.25], [size_w/2.35,size_h/1.15], size_w//135)
            nameResetArrow1_1 = pygame.draw.line(screen, color1, [size_w/2.67,size_h/1.22], [size_w/2.7,size_h/1.25], size_w//225)
            nameResetArrow1_2 = pygame.draw.line(screen, color1, [size_w/2.67,size_h/1.22], [size_w/2.56,size_h/1.22], size_w//225)
            nameResetArrow2_1 = pygame.draw.line(screen, color1, [size_w/2.46,size_h/1.16], [size_w/2.43,size_h/1.13], size_w//225)
            nameResetArrow2_2 = pygame.draw.line(screen, color1, [size_w/2.46,size_h/1.16], [size_w/2.52,size_h/1.17], size_w//225)
            if event.type == MOUSEMOTION and activeMain:
                if nameResetRect.collidepoint(mouse_pos):
                    if language == "ENG":
                        nameResetTxt = Write(round(size_w//100*3),"Name",color3,[size_w/3.15,size_h/1.18])
                    else:
                        nameResetTxt = Write(round(size_w//100*3),"Nick",color3,[size_w/3.15,size_h/1.18])
                    nameResetCirc = pygame.draw.circle(screen, color3, [size_w/2.55,size_h/1.19], size_w//45, size_w//225)
                    nameResetLine = pygame.draw.line(screen, color2, [size_w/2.85,size_h/1.25], [size_w/2.35,size_h/1.15], size_w//135)
                    nameResetArrow1_1 = pygame.draw.line(screen, color3, [size_w/2.67,size_h/1.22], [size_w/2.7,size_h/1.25], size_w//225)
                    nameResetArrow1_2 = pygame.draw.line(screen, color3, [size_w/2.67,size_h/1.22], [size_w/2.56,size_h/1.22], size_w//225)
                    nameResetArrow2_1 = pygame.draw.line(screen, color3, [size_w/2.46,size_h/1.16], [size_w/2.43,size_h/1.13], size_w//225)
                    nameResetArrow2_2 = pygame.draw.line(screen, color3, [size_w/2.46,size_h/1.16], [size_w/2.52,size_h/1.17], size_w//225)
            elif event.type == MOUSEBUTTONDOWN and activeMain:
                if nameResetRect.collidepoint(mouse_pos):
                    clearName()
                    activeAny = False
                    activities[2] = False
    def isAdmin():
        global admin,confirmed,activeMain,text
        if activities[2]:
            if admin:
                adminRect = pygame.draw.rect(screen, dark_gray, [size_w/2.24,size_h/1.3,size_w/6,size_h/7], size_w//270,5)
            else:
                adminRect = pygame.draw.rect(screen, color1, [size_w/2.24,size_h/1.3,size_w/6,size_h/7], size_w//270,5)
                hideOptions = pygame.draw.rect(screen, color1, [size_w/1.14,size_h/2.74,size_w/7,size_h/1.3], 0)
            adminTxt = Write(round(size_w//100*3.5),"Admin",color1,[size_w/1.88,size_h/1.18])

            if not confirmed:
                passwordConfirm(getPsswd())    

            if event.type == MOUSEMOTION and activeMain:
                text = ""
                if adminRect.collidepoint(mouse_pos):
                    adminTxt = Write(round(size_w//100*3.5),"Admin",color3,[size_w/1.88,size_h/1.18])   
            elif event.type == MOUSEBUTTONDOWN and activeMain:
                if adminRect.collidepoint(mouse_pos):
                    if admin:
                        admin = False
                    else:
                        activeMain = False
                        confirmed = False
    def language():
        if activities[2]:
            plBtn = pygame.draw.rect(screen, color2, [size_w/4.63,size_h/11.29,size_w/20,size_h/12], 0,20)
            engBtn = pygame.draw.rect(screen, color2, [size_w/3.76,size_h/11.29,size_w/20,size_h/12], 0,20)
            language = getLang()
            if language == "ENG":
                Write(round(size_w//100*1.8),"ENG",lt_blue,[size_w/3.46,size_h/7.5])
            else:
                Write(round(size_w//100*1.8),"ENG",color1,[size_w/3.46,size_h/7.5])
            if language == "PL":
                Write(round(size_w//100*1.8),"PL",lt_blue,[size_w/4.14,size_h/7.5])
            else:
                Write(round(size_w//100*1.8),"PL",color1,[size_w/4.14,size_h/7.5])
            if event.type == MOUSEMOTION:
                if plBtn.collidepoint(mouse_pos):
                    Write(round(size_w//100*1.8),"PL",dark_gray,[size_w/4.14,size_h/7.5])
                elif engBtn.collidepoint(mouse_pos):
                    Write(round(size_w//100*1.8),"ENG",dark_gray,[size_w/3.46,size_h/7.5])
            elif event.type == MOUSEBUTTONDOWN:
                if plBtn.collidepoint(mouse_pos):
                    changeLang("PL")
                elif engBtn.collidepoint(mouse_pos):
                    changeLang("ENG")                
            pygame.draw.rect(screen, color1, [size_w/4.63,size_h/11.29,size_w/10,size_h/12], size_w//450,20)
            pygame.draw.line(screen, color1, [size_w/3.78,size_h/11.13],[size_w/3.78,size_h/5.97], size_w//450)
    def isSoundEnabled():
        global soundEnabled
        if activities[2]:
            try:
                speaker = pygame.image.load(f"{dirPath}/images/speaker.png")
                speaker = pygame.transform.scale(speaker, [int(size_w/28.29),int(size_h/18.22)])
                if soundEnabled:
                    soundBtn = pygame.draw.rect(screen, lt_blue, [size_w/1.3,size_h/9.6,size_w/13,size_h/13], size_w//250,size_w//200)
                    screen.blit(speaker,[size_w/1.27,size_h/8.5])
                    Write(round(size_w/100*1.4),"ON",lt_blue,[size_w/1.24,size_h/4.89])
                else:
                    soundBtn = pygame.draw.rect(screen,color1, [size_w/1.3,size_h/9.6,size_w/13,size_h/13], size_w//250,size_w//200)
                    screen.blit(speaker,[size_w/1.27,size_h/8.5])
                    pygame.draw.line(screen, color1, [size_w/1.28,size_h/6.1], [size_w/1.21,size_h/8.35], size_w//250)
                    Write(round(size_w/100*1.4),"OFF",color1,[size_w/1.24,size_h/4.89])
            except:
                errorInit(["Failed to load 'speaker.png'","at settings.isSoundEnabled()"])
            if event.type == MOUSEBUTTONDOWN:
                if soundBtn.collidepoint(mouse_pos):
                    if soundEnabled:
                        soundEnabled = False
                    else:
                        soundEnabled = True
                        music.init()
    def displayStyle(): #NOT WORKING CORRECTLY YET
        global size,size_w,size_h,activeAny,TD_circs,selectingDisplay,running
        global hp1,hp2,rectCenter,TD_wdthStart,TD_hghtStart,DG_icons,TD_icon,exiting
        if activities[2]:
            if selectingDisplay:
                pygame.draw.rect(screen, color1, [size_w/1.59,size_h/1.86,size_w/6,size_h/4.2], 0,size_w//450)
                pygame.draw.line(screen, color3, [size_w/1.58,size_h/1.53], [size_w/1.27,size_h/1.53], size_w//650)
                
                fullScreenBtn = pygame.draw.rect(screen, color1, [size_w/1.57,size_h/1.79,size_w/6.7,size_h/12], width=0)
                if getDisplayStyle() == "fullscreen":
                    Write(round(size_w//100*2),"Fullscreen",lt_blue,[size_w/1.41,size_h/1.67])
                else:
                    Write(round(size_w//100*2),"Fullscreen",color3,[size_w/1.41,size_h/1.67])
                
                windowBtn = pygame.draw.rect(screen, color1, [size_w/1.57,size_h/1.5,size_w/6.7,size_h/12], width=0)
                if getDisplayStyle() == "window":
                    Write(round(size_w//100*2),"Window",lt_blue,[size_w/1.41,size_h/1.41])
                else:
                    Write(round(size_w//100*2),"Window",color3,[size_w/1.41,size_h/1.41])

                displayBtn = pygame.draw.rect(screen, color3, [size_w/1.59,size_h/1.3,size_w/6,size_h/7], size_w//270,5)
            else:
                displayBtn = pygame.draw.rect(screen, color1, [size_w/1.59,size_h/1.3,size_w/6,size_h/7], size_w//270,5)
            Write(round(size_w//100*3),"Display",color1,[size_w/1.4,size_h/1.18])

            if event.type == MOUSEMOTION:
                if displayBtn.collidepoint(mouse_pos):
                    Write(round(size_w//100*3),"Display",color3,[size_w/1.4,size_h/1.18])
                try:
                    if fullScreenBtn.collidepoint(mouse_pos):
                        pygame.draw.rect(screen, color1, [size_w/1.57,size_h/1.79,size_w/6.7,size_h/12], width=0)
                        Write(round(size_w//100*2),"Fullscreen",logoBlue,[size_w/1.41,size_h/1.67])
                    elif windowBtn.collidepoint(mouse_pos):
                        pygame.draw.rect(screen, color1, [size_w/1.57,size_h/1.5,size_w/6.7,size_h/12], width=0)
                        Write(round(size_w//100*2),"Window",logoBlue,[size_w/1.41,size_h/1.41])
                except:
                    pass  
            elif event.type == MOUSEBUTTONDOWN:
                if displayBtn.collidepoint(mouse_pos):
                    if selectingDisplay:
                        selectingDisplay = False
                    else:
                        selectingDisplay = True    
                try:
                    if fullScreenBtn.collidepoint(mouse_pos):
                        changeDisplayStyle("fullscreen")   
                        selectingDisplay = False
                        if len(dirPath) == 50: 
                            os.system(f"start {dirPath}/Code/main.py")
                            pygame.quit()
                            sys.exit()
                        try:
                            if len(dirPath) == 40:
                                os.system(f"start {dirPath}/Code/dist/main/main.exe")
                                pygame.quit()
                                sys.exit()
                        except:
                            print(len(dirPath))     
                            print(f"start {dirPath}/Code/dist/main/main.exe") 
                    elif windowBtn.collidepoint(mouse_pos):
                        changeDisplayStyle("window")
                        selectingDisplay = False
                        print(len(dirPath))
                        if len(dirPath) == 50:
                            os.system(f"start {dirPath}/Code/main.py")
                            pygame.quit()
                            sys.exit()
                        try:
                            if len(dirPath) == 40:
                                os.system(f"start {dirPath}/Code/dist/main/main.exe")
                                pygame.quit()
                                sys.exit()
                        except:
                            print(len(dirPath))     
                            print(f"start {dirPath}/Code/dist/main/main.exe") 
                except:
                    pass       
class Prize(pygame.sprite.Sprite):
    def startScreen():
        global activeAny,name
        if activities[3]:
            global iconsUnlock,iconsLocked
            language = getLang()
            if pygame.event.get_blocked(MOUSEMOTION):
                pygame.event.set_allowed(MOUSEMOTION)

            bckgr = pygame.draw.rect(screen, color2, [size_w/5,size_h/16,size_w/1.5,size_h/1.1],0,10)
            if getTheme() == "DARK":
                pygame.draw.rect(screen, lt_brown, [size_w/4.11,size_h/16,size_w/1.7,size_h/1.1],0,0)
                pygame.draw.rect(screen, dark_brown, [size_w/3.03,size_h/16,size_w/2.44,size_h/1.1],0,0)
            else:
                pygame.draw.rect(screen, dark_brown, [size_w/4.11,size_h/16,size_w/1.7,size_h/1.1],0,0)
                pygame.draw.rect(screen, lt_brown, [size_w/3.03,size_h/16,size_w/2.44,size_h/1.1],0,0)
            
            if language == "ENG":
                Write(round(size_w//100*2.5),f"Checking your collection {getName()}?",color3,[size_w/1.8,size_h/8.83])
            else:
                Write(round(size_w//100*2.5),f"Jak tam twoja kolekcja {getName()}?",color3,[size_w/1.8,size_h/8.83])
            
            try:
                table = pygame.image.load(r"{}/Images/Game/table.png".format(dirPath))
                table = pygame.transform.scale(table, [int(size_w/1.7),int(size_h/4)])
                screen.blit(table,[size_w/4.11,size_h/2.86])
                screen.blit(table,[size_w/4.11,size_h/1.4])
            except:
                errorInit("Failed to load 'table.png'")

            if language == "ENG":
                names = [
                    "Beginner's cup",
                    "Romo's axe",
                    "Magic potion",
                    "Book of spells",
                    "Graduate's medal",
                    "Dogtag",
                    "None",
                    "None",
                ]
            else:
                names = [
                    "Puchar nowicjusza",
                    "Topór Romo",
                    "Magiczny eliksir",
                    "Księga zaklęć",
                    "Medal ukończenia",
                    "Nieśmiertelnik",
                    "None",
                    "None",
                ]
            
            try:
                if len(iconsLocked) < 1:
                    cupL = pygame.image.load(r"{}/Images/install/cup_locked.png".format(dirPath))
                    cupL = pygame.transform.scale(cupL, [int(size_w/10.6),int(size_h/6)])  
                    axeL = pygame.image.load(r"{}/Images/Game/romosaxe_locked.png".format(dirPath))
                    axeL = pygame.transform.scale(axeL, [int(size_w/10.6),int(size_h/6)]) 
                    potionL = pygame.image.load(r"{}/Images/Game/potion_locked.png".format(dirPath))
                    potionL = pygame.transform.scale(potionL, [int(size_w/14.6),int(size_h/6)]) 
                    bookL = pygame.image.load(r"{}/Images/Game/book_locked.png".format(dirPath))
                    bookL = pygame.transform.scale(bookL, [int(size_w/10.6),int(size_h/6)]) 
                    medalL = pygame.image.load(r"{}/Images/Game/medal_locked.png".format(dirPath))
                    medalL = pygame.transform.scale(medalL, [int(size_w/12),int(size_h/6)]) 
                    dogtagL = pygame.image.load(r"{}/Images/Game/sr/dogtag1_locked.png".format(dirPath))
                    dogtagL = pygame.transform.scale(dogtagL, [int(size_w/10.6),int(size_h/6)]) 
                    iconsLocked = [cupL,axeL,potionL,bookL,medalL,dogtagL]

                if len(iconsUnlock) < 1:
                    cup = pygame.image.load(r"{}/Images/install/cup.png".format(dirPath))
                    cup = pygame.transform.scale(cup, [int(size_w/10.6),int(size_h/6)])  
                    axe = pygame.image.load(r"{}/Images/Game/romosaxe.png".format(dirPath))
                    axe = pygame.transform.scale(axe, [int(size_w/10.6),int(size_h/6)]) 
                    potion = pygame.image.load(r"{}/Images/Game/potion.png".format(dirPath))
                    potion = pygame.transform.scale(potion, [int(size_w/14.6),int(size_h/6)]) 
                    book = pygame.image.load(r"{}/Images/Game/book.png".format(dirPath))
                    book = pygame.transform.scale(book, [int(size_w/10.6),int(size_h/6)]) 
                    medal = pygame.image.load(r"{}/Images/Game/medal.png".format(dirPath))
                    medal = pygame.transform.scale(medal, [int(size_w/12),int(size_h/6)]) 
                    dogtag = pygame.image.load(r"{}/Images/Game/sr/dogtag1.png".format(dirPath))
                    dogtag = pygame.transform.scale(dogtag, [int(size_w/10.6),int(size_h/6)])
                    iconsUnlock = [cup,axe,potion,book,medal,dogtag]
            except:
                errorInit("Failed to load icons at prize.startScreen()",fontSize=1.7)

            wdth = size_w/3.34
            hght = size_h/2.13
            lvl = getCourseLvl() - 2
            iterator = 0

            for it in range(2):
                for it2 in range(4):
                    pygame.draw.rect(screen, gold, [wdth,hght,size_w/12,size_h/15], 0,size_w//450)
                    try:
                        if iterator<=lvl:
                            Write(round(size_w//100*0.7),names[iterator],color1,[wdth+(size_w/12)/2,hght+(size_h/15)/2])
                            screen.blit(iconsUnlock[iterator],[wdth,hght-size_h/4.7])
                        else:
                            Write(round(size_w//100*1.2),"?",color1,[wdth+(size_w/12)/2,hght+(size_h/15)/2])
                            try:
                                screen.blit(iconsLocked[iterator],[wdth,hght-size_h/5])
                            except:
                                pass
                    except:
                        pass
                    wdth += size_w/8
                    iterator += 1
                wdth = size_w/3.34
                hght += size_h/2.7
            isCorrectActivity()
class Contacts(pygame.sprite.Sprite):
    def startScreen():
        global activeAny
        if activities[4]:
            if pygame.event.get_blocked(MOUSEMOTION):
                pygame.event.set_allowed(MOUSEMOTION)
            bckgr = pygame.draw.rect(screen, color2, [size_w/5,size_h/16,size_w/1.5,size_h/1.1],0,10)
            Write(size_w//100*3,"CONTACTS OPTION",color3,[size_w/1.8,size_h/5])
            isCorrectActivity()
class Music():
    def init():
        global soundEnabled
        if soundEnabled:
            global soundFantasy1,soundMagic1
            global fantasyChannel,fantasyChannelSounds,magicChannel
            print("Loading sounds...")
            try:
                soundFantasy1 = pygame.mixer.Sound(r"{}\Music\Ale-and-Anecdotes-by-Darren-Curtis.ogg".format(dirPath))
            except:
                errorInit(["Failed to load sounds: music.init()[1]","You can turn off sounds in settings"],fontSize=1.6)
            try:
                soundMagic1 = pygame.mixer.Sound(f"{dirPath}/Music/Wizardtorium.ogg")
            except:
                errorInit(["Failed to load sounds: music.init()[2]","You can turn off sounds in settings"],fontSize=1.6)
            print("Sounds loaded!")
            
        fantasyChannel = pygame.mixer.Channel(1)
        fantasyChannel.set_volume(0.2)
        fantasyChannelSounds = pygame.mixer.Channel(2)
        fantasyChannelSounds.set_volume(0.4)

        magicChannel = pygame.mixer.Channel(3)
    def playBackground():
        global soundFantasy1,bckgrMusicPlayed,soundEnabled
        if soundEnabled and activities[0]:
            if bckgrMusicPlayed: 
                lessonNr = str(activeLesson)[17:-23]
                if not activeMenu:
                    try:
                        if lessonNr in ["lesson1","lesson2"]:
                            if not fantasyChannel.get_busy():
                                fantasyChannel.play(soundFantasy1)
                        elif lessonNr in ["lesson3","lesson4"]:
                            if not magicChannel.get_busy():
                                magicChannel.play(soundMagic1)
                    except:
                        errorInit(["Failed to play sounds: music.playBackground()","You can turn off sounds in settings"],fontSize=1.6)
            else:
                fantasyChannel.stop()
                magicChannel.stop()
        else:
            fantasyChannel.stop()
            magicChannel.stop()


running = True
start=Start
course=Course
lookFor = LookFor
settings = Settings
contacts = Contacts
prize = Prize
music = Music
start.useScreenDef()
music.init()
print("Init_End_Time: ",str(datetime.now())[10:])
while running:
    try:
        keys = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos() 
    except:
        pass
    start.adminTools.counterCords()
    start.adminTools.counterFPS()
    course.tower_defence.loadingBar(storedTime)
    music.playBackground()
    for event in pygame.event.get():
        errorHandling()
        start.sideBarEvents()
        start.setNameScreen()
        start.welcomeScreen()
        start.adminTools.iterators()
        start.adminTools.changingLvl()
        if len(getName()) > 0:
            course.startScreen()
            lookFor.startScreen()
            settings.startScreen()
            contacts.startScreen()
            course.lesson1()
            course.lesson2()
            course.lesson3()
            course.lesson4()
            course.lesson5()
            course.lesson6()
            course.lesson7()
            course.lesson8()
            course.lesson9()
            settings.theme()
            settings.resizing()
            settings.resetName()
            settings.isAdmin()
            settings.language()
            #settings.displayStyle()
            settings.isSoundEnabled()
            prize.startScreen()
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    #EVENTS THAT NEED TO BE REFRESHED FASTER THAN EVENT LOOP
    course.tower_defence.enemiesPath(storedTime)
    course.tower_defence.targeting()
    course.tower_defence.handlingFinalLvl()
    course.shooting_range.loopExample()
    course.shooting_range.continueTimer()
    course.shooting_range.drawingCircles()
    course.shooting_range.rangeOfRects()
    course.shooting_range.counting()
    course.shooting_range.doubleForRectDraw()
    start.finishBar()
    start.courseLvlBar()
    if pygame.display.get_init():
        pygame.display.update()
