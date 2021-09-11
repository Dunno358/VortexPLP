from typing import Type
import pygame
from pygame import Surface, rect
from pygame.event import get_blocked, post
from pygame.locals import *
import os
from datetime import datetime
from random import randint
import sys
import os
import time
pygInit = pygame.init()
pygame.key.set_repeat(500, 100)
print("\nPygame init: {}/7 Succed and {} failed".format(pygInit[0],pygInit[1]))
print("Init_Start_Time: ",str(datetime.now())[10:])
print("Witaj {}!".format(os.getlogin()))# - RETURNS NAME OF CURRENT USER

#01.09.2021

#COLORS
darkThemeMainCol = (30,30,30)
darkThemeSubCol = (45,45,45)
lightThemeMainCol = (230,230,230)
lightThemeSubCol = (190,190,190)
lt_gray = (240,240,240)
dark_gray = (120,120,120)
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

#DIR PATH
dirPath = os.path.dirname(os.path.realpath(__file__))
dirPath = dirPath[:-5] #-15 for .exe, -5 for .py
print("Dir Path: ",dirPath)

#DISPLAY
displaySize = pygame.display.Info()
#size_w_minus = displaySize.current_w//91
#size_h_minus = displaySize.current_h//10
size_w=displaySize.current_w#-size_w_minus
size_h=displaySize.current_h#-size_h_minus
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

#LEVELS
courseLvl = 1
iterator = 1

#TEXTS
name=""
lookForPhrase=""
text = ""

#TIME
wait = False
storedTime = ""

#ACTIVE/INACTIVE
activeMenu = True
activeMain = True
notBlocked = True
wrong = False
confirmed = True
activeWriting = False
done = False

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

#Tower Defense
TD_circs = []
TD_pathCords = []
TD_guards = []
TD_guardRects = []
TD_guardSubRects = []
TD_consoleRects = []
TD_queue = []
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
TD_added = False
TD_added2 = False
TD_Lvls = [3,4,9,10,11]
TD_excludeLvls = 3
TD_subDone = False
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
        screen.blit(self.writeText,self.textRect)

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
def resetEvents():
    events = [MOUSEBUTTONDOWN,MOUSEBUTTONUP,MOUSEMOTION,KEYUP,KEYDOWN]
    for event in events:
        if pygame.event.get_blocked(event):
            pygame.event.set_allowed(event)

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
       
        courseIcon = pygame.image.load(r"{}/Images/python-iconx128.png".format(dirPath))
        magnifierIcon = pygame.image.load(r"{}/Images/magnifier-iconx128.png".format(dirPath))
        settingsIcon = pygame.image.load(r"{}/Images/settings-iconx128.png".format(dirPath))
        prizeIcon = pygame.image.load(r"{}/Images/install/cup.png".format(dirPath))
        contactsIcon = pygame.image.load(r"{}/Images/contacts-iconx128.png".format(dirPath))

        sideBarIcons = [courseIcon,magnifierIcon,settingsIcon,prizeIcon,contactsIcon]
        for icon in sideBarIcons:
            index = sideBarIcons.index(icon)
            icon = pygame.transform.scale(icon,[int(size_w//21.3),int(size_h//12)])
            sideBarIcons[index] = icon

        it =sideBarRctHStart*1.15            
        for icon in sideBarIcons:
            screen.blit(icon,(sideBarRctWStart+size_w/120,it))  #int(size_w/29)
            it+=sideBar_h/5.6        

        Write(size_w//100,"V0.0.0.9",color3,[size_w/1.81,10]) 

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
            Write(size_w//35*3,logoName,color2,[size_w/1.85,size_h/2.2])
           
            logoSize = size_w//50*3
            logoTxt1 = WriteItalic(logoSize,logoName,logoBlue,[size_w/2,size_h/2.3])
            logoTxt1 = WriteItalic(logoSize-logoSize//3,"PLP",red,[size_w/2+(size_w//50*3*len(logoName)/2.65),size_h/2.5])#size_w/1.5
            if event.type == MOUSEMOTION:
                if guideBtn.collidepoint(mouse_pos):
                    guideBtn = pygame.draw.rect(screen, green, [size_w/2.1,size_h/1.35,size_w/6,size_h/8],0,10)
                    guideBtnBrd = pygame.draw.rect(screen, dark_green, [size_w/2.1,size_h/1.35,size_w/6,size_h/8],size_w//675,10)
                    guideBtnTxt = Write(round(size_w//100*2.5),"Start",color3,[size_w/1.78,size_h/1.24])      
                else:
                    guideBtn = pygame.draw.rect(screen, dark_green, [size_w/2.1,size_h/1.35,size_w/6,size_h/8],0,10)
                    guideBtnTxt = Write(round(size_w//100*2.5),"Start",color3,[size_w/1.78,size_h/1.24]) 
    class adminTools(pygame.sprite.Sprite):
        global admin
        def iterators():
            global iterator,courseLvl
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
            global hp1,hp2,courseLvl
            global iterator,inFight,notBlocked,chosen
            if event.type == MOUSEBUTTONDOWN:
                for rect in rects:
                    if rect.collidepoint(mouse_pos) and inFight and activeMain and not hpBarEmpty:
                        hp1 -= size_w/70
                        index = rects.index(rect)
                        screen.blit(icons[1],[wdth,hght])
                        course.coursorMarked()
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

            if trees:
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
    
            course.tower_defence.drawPath()
        def nextBtn(color,text,border=False,colorIfBorder=(0,0,0)):
            okBtn = pygame.draw.rect(screen, color, [size_w/2.05,size_h/2.29,size_w/8,size_h/10], 0,15)
            if border:
                pygame.draw.rect(screen, colorIfBorder, [size_w/2.05,size_h/2.29,size_w/8,size_h/10], size_w//450,15)
            Write(size_w//100*2,text,color1,[size_w/1.82,size_h/2.29+size_h/19])
            return okBtn
        def makingGuards():
            global selected,storedTime,chosen,storedCords,done,circles,loadingBar
            potion = pygame.image.load(r"{}/Images/Game/potion.png".format(dirPath))
            potion = pygame.transform.scale(potion,[int(size_w/42.68),int(size_h/12)])
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


            correctWidth = mouse_pos[0] > size_w/4.93 and mouse_pos[0] < size_w/1.2
            correctHight = mouse_pos[1] > size_h/3.41 and mouse_pos[1] < size_h/1.17
            if not loadingBar:
                if correctWidth and correctHight:
                    screen.blit(potion,[mouse_pos[0]+size_w//400,mouse_pos[1]])
            else:
                try:
                    blitWdth = circles[selected][0] + circles[selected][2]/2
                    blitHght = circles[selected][1] + circles[selected][3]/2
                    screen.blit(potion,[blitWdth,blitHght])
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
            global TD_guardSubRects,TD_enemy,TD_done,admin,TD_circs,TD_pathCords,TD_guards
            global TD_time,TD_active,TD_iterator,TD_hp,TD_consoleShown,TD_friends,TD_enemies
            global TD_actualEnemy,TD_actualEnemy2,TD_wdthStart2,TD_hghtStart2,TD_enemy2,TD_firstDone2
            global TD_hp2,TD_queue,TD_lvlType,TD_Lvls,TD_excludeLvls
            lessonOk = str(activeLesson)[17:-23]=="lesson4"
            lvlOk = courseLvl in TD_Lvls[TD_excludeLvls:]
            if activities[0] and not activeMenu and lessonOk and lvlOk and not TD_consoleShown:
                eventsBlocked = True
                if len(TD_queue)<2:
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
                        guard = pygame.image.load(r"{}/Images/Game/2dmap/guard.png".format(dirPath))
                        guard = pygame.transform.scale(guard, [int(size_w/14.22),int(size_h/8)])
                        course.tower_defence.drawPath()
                        #pygame.draw.rect(screen, TD_darkGreen, TD_guardSubRects[3], width=0)
                        try:
                            guardW = TD_guardRects[3][0]
                            guardH = TD_guardRects[3][1]
                            screen.blit(guard,[guardW,guardH]) 
                        except:
                            print("Line 929 Error occured | TDGUARDS",TD_guardRects)
                        if pygame.event.get_blocked(MOUSEMOTION):
                            pygame.event.set_allowed(MOUSEMOTION)
                        #TD_done = True
                        holdIterator = iterator
                        course.tower_defence.reset()
                        course.tower_defence.drawMap()
                        iterator = holdIterator + 2
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
                            guard = pygame.image.load(r"{}/Images/Game/2dmap/guard.png".format(dirPath))
                            guard = pygame.transform.scale(guard, [int(size_w/14.22),int(size_h/8)])
                            course.tower_defence.drawPath()
                            pygame.draw.rect(screen, TD_darkGreen, TD_guardSubRects[3], width=0)
                            try:
                                guardW = TD_guardRects[3][0]
                                guardH = TD_guardRects[3][1]
                                screen.blit(guard,[guardW,guardH]) 
                            except:
                                print("Line 929 Error occured | TDGUARDS",TD_guardRects)
                            if pygame.event.get_blocked(MOUSEMOTION):
                                pygame.event.set_allowed(MOUSEMOTION)
                            #TD_done = True
                            holdIterator = iterator
                            course.tower_defence.reset()
                            course.tower_defence.drawMap()
                            iterator = holdIterator + 2

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
            global TD_consoleShown,TD_count,TD_Lvls,TD_excludeLvls,courseLvl
            lvlOk = courseLvl in TD_Lvls[TD_excludeLvls:]
            if activities[0] and not activeMenu and str(activeLesson)[17:-23]=="lesson4" and lvlOk and not TD_consoleShown:
                global TD_enemy,TD_enemy2,TD_guardSubRects,TD_circs,TD_guardRects,TD_active,TD_done,TD_eventRects
                global iterator,TD_hp,TD_hp2,TD_round,TD_consoleTxts,TD_friends,TD_enemies,TD_actualEnemy2,TD_actualEnemy
                global TD_added,TD_added2,TD_toDefeat
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
                    guard = pygame.image.load(r"{}/Images/Game/2dmap/guard.png".format(dirPath))
                    guard = pygame.transform.scale(guard, [int(size_w/14.22),int(size_h/8)])

                    cords = [
                        [size_w/5,size_h/5.57,size_w/1.5,size_h/1.5],
                        [size_w/3.29,size_h/15.67,size_w/1.78,size_h/8],
                        [size_w/5,size_h/1.18,size_w/16,size_h/8],
                        [size_w/3.36,size_h/1.18,size_w/1.76,size_h/8],
                        [size_w/3.82,size_h/1.13,size_w/16,size_h/11]
                    ]

                    if len(TD_circs)<1:
                        course.tower_defence.drawMap()

                    for circ in TD_circs:
                        try:
                            index = TD_circs.index(circ)
                            if circ.collidepoint(TD_enemy) and TD_hp>0 and circ not in TD_active:
                                if index not in TD_active:
                                    TD_active.append(index)
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
                                if letEnemy and TD_actualEnemy in TD_enemies or letFriend and TD_actualEnemy in TD_friends:
                                    pass
                                else:
                                    if getActualSecond()%2==0:
                                        if TD_hp > 0:
                                            TD_hp -= size_w/1000*len(TD_active)/1.5
                                            lineColor = lt_blue
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
                                            TD_hp2 -= size_w/700*len(TD_active2)
                                            lineColor = lt_blue
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
                    Write(round(size_w//100*1.7),f"{TD_count}/{TD_toDefeat}",color3,[size_w/1.87,size_h/1.11])
                    if TD_count == TD_toDefeat and TD_lvlType!="onlyfriend":
                        course.dialogTop(6.41,"Great job! Click anywhere","to go to the next level",bckgr=True)
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
            global iterator,TD_wdthStart,TD_hghtStart,TD_firstDone,TD_guardRects,eventsBlocked
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
            course.tower_defence.drawMap()
        def console():
            global TD_consoleShown

            btnColor = TD_darkGray
            txtColor = lt_gray
            if TD_consoleShown:
                global TD_consoleRects,TD_consoleActiveRect,activeWriting,text,TD_consoleTxts,TD_consoleOK
                global iterator
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

        if event.type == MOUSEMOTION and activities[0] and activeMenu:
            permitionsFile = open(r"{}/Metadata/course/permitions.txt".format(dirPath),"r")
            permitionLvl = permitionsFile.read()
            permitionsFile.close()
            permitionLvl = int(decipher(permitionLvl[34:]))
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
        global hp1,hp2,loadingBar,storedCords,storedTime,TD_circs
        actualLesson = str(activeLesson)[17:-23]
        if not activeMenu and activities[0] and actualLesson==lesson:
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
            lvlTxt = Write(round(size_w//100*1.5),"{}/{}".format(courseLvl,maxLvl),color1,[size_w/1.19,size_h/11.53])


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
                    hp1 = size_w/2.66
                    hp2 = size_w/6
                    storedCords = []
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
    def coursorMarked(cords=None):
        if isinstance(cords,None):
            mw = mouse_pos[0]
            mh = mouse_pos[1]
        else:
            mw = cords[0]
            mh = cords[1]            
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
        global activeMain,hp2,iterator,storedTime
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
                    elif index != goodAnswerIndex:
                        hp2 -= size_w/50
                        activeMain = True
                        iterator += 1
            wdth += size_w/8     
    def consoleGame(textToShow,goodAnswer,btnText="Attack",fontSize=2.5,textLen=23,multipleAnswers=False,answersList=[],fontSize2=2):
        global text,activeMain,iterator,keys
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
                else:
                    if text.lower().replace(" ","") == goodAnswer.lower().replace(" ",""):
                        text = ""
                        iterator += 1
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
                        text += chr(event.key)
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
        else:
            WriteItalic(round(size_w//100*fontSize),text, color3, [size_w/2.15,size_h/hght+size_h/11.15])
    def lesson1():
        global activeMenu,courseLvl,mentorIcon,activeLesson,theme,langugage
        course.standardLessonEvents("lesson1",11)   
        if getTheme().lower() == "light":
            mentorIcon = pygame.image.load(r"{}/Images/Game/orcM.png".format(dirPath))
        else:
            mentorIcon = pygame.image.load(r"{}/Images/Game/orc.png".format(dirPath))
        mentorIcon = pygame.transform.scale(mentorIcon, [int(size_w/10.6),int(size_h/6)])
        if activities[0] and not activeMenu and str(activeLesson)[17:-23]=="lesson1":
            language = getLang()
            if courseLvl == 1: #LVL1
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
                course.dialogTop(6.41,"So, Python is:","(Move mouse over question mark)")
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
            elif courseLvl == 4:
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

                pygame.draw.rect(screen, color1, [size_w/2.31,size_h/8.5,size_w/4,size_h/8], size_w//200,30)
                if language == "ENG":
                    WriteItalic(round(size_w//100*2.5),"Python is used for:",color3,[size_w/1.8,size_h/5.5]) 
                else:
                    WriteItalic(round(size_w//100*2.2),"Zastosowania Python:",color3,[size_w/1.8,size_h/5.5])

                rects = []
                colors = [dark_red,dark_green,dark_blue,orange]
                width_Start = size_w/2.82
                if language == "ENG":
                    check = "Check"
                else:
                    check = "Sprawdź"
                for x in range(4):
                    rect = pygame.draw.rect(screen, color1, [width_Start,size_h/3.26,size_w/10,size_h/10], size_w//150,10)
                    Write(round(size_w//100*1.5),check,color1,[width_Start+size_w/20,size_h/2.76])
                    rects.append(rect)
                    width_Start += size_w/9

                if event.type == MOUSEMOTION:
                    width_Start = size_w/2.82
                    for rect in rects:
                        index = rects.index(rect)
                        if rect.collidepoint(mouse_pos):
                            WriteItalic(round(size_w//100*2.5),pythonList[index],colors[index],[size_w/1.83,size_h/1.74])
                            WriteItalic(round(size_w//100*2.5),"({})".format(lang[index]),colors[index],[size_w/1.83,size_h/1.42])
                            Write(round(size_w//100*1.5),check,color3,[width_Start+size_w/20,size_h/2.76])
                            width_Start += size_w/9
                        else:
                            Write(round(size_w//100*1.5),check,color1,[width_Start+size_w/20,size_h/2.76])
                            width_Start += size_w/9
            elif courseLvl==5:
                if language == "ENG":
                    course.dialogStandard(2.6,"Now we will install Python,","just follow my lead!")   
                else:
                    course.dialogStandard(2.6,"Teraz zainstalujemy Pythona,","pokażę ci jak!")    
            elif courseLvl == 6:
                installPng = pygame.image.load(r"{}/Images/Install/1.png".format(dirPath)) 
                installPng = pygame.transform.scale(installPng, [int(size_w/1.95),int(size_h/2.29)])
                screen.blit(installPng,[size_w/3.5,size_h/3.3])  
                screen.blit(mentorIcon,[size_w/3.5,size_h/10])
                if language == "ENG":  
                    strs = [
                        "Go to python.org/downloads",
                        "and click the marked button",
                        "<- Click there"
                    ] 
                else:
                    strs = [
                        "Idź do python.org/downloads, a",
                        "następnie kliknij zaznaczony przycisk",
                        "<- Kliknij tam"
                    ]                     
                link = pygame.draw.rect(screen, color1, [size_w/2.57,size_h/9,size_w/3,size_h/6], size_w//200,30)   
                WriteItalic(round(size_w//100*1.5),strs[0],color3,[size_w/1.82,size_h/6.41]) 
                WriteItalic(round(size_w//100*1.5),strs[1],color3,[size_w/1.82,size_h/4.41]) 
                Write(round(size_w/100*1.5),strs[2],color3,[size_w/1.26,size_h/5.41])
                if event.type == MOUSEBUTTONDOWN:
                    if link.collidepoint(mouse_pos):
                        os.system(r"start https://python.org/downloads")
            elif courseLvl == 7:
                if language == "ENG":
                    course.dialogStandard(2.6,"Don't worry about installation,","it's pretty user friendly!","Just remeber to mark","ADD TO PATH checkbox",big=True)
                else:
                    course.dialogStandard(2.6,"Nie martw się instalacją,","jest bardzo przyjazna dla","użytkownika! Tylko zaznacz","ADD TO PATH opcję",big=True)
                pygame.draw.line(screen, dark_red, [size_w/1.9,size_h/1.75], [size_w/1.5,size_h/1.75], 3)
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
                                Write(round(size_w//100*1.5),"Click to open",color3,[size_w/1.25,size_h/6.23])
                            else:
                                Write(round(size_w//100*1),"Kliknij by otworzyć",color3,[size_w/1.25,size_h/6.23])
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
                cup = pygame.image.load(r"{}/Images/Install/cup.png".format(dirPath))
                cup = pygame.transform.scale(cup, [int(size_w/5.33),int(size_h/3)])
                screen.blit(cup,[size_w/2.33,size_h/2.4])  

                pygame.draw.rect(screen, color1, [size_w/2.24,size_h/7.14,size_w/4,size_h/8], size_w//150,15)
                if language == "ENG":
                    Write(round(size_w//100*1.5),"Romo is proud",color3,[size_w/1.77,size_h/4.9])
                    finish = "Finish"
                else:
                    Write(round(size_w//100*1.5),"Romo jest dumny",color3,[size_w/1.77,size_h/4.9])
                    finish = "Zakończ"

                finishBtn = pygame.draw.rect(screen, dark_green, [size_w/2.3,size_h/1.26,size_w/6,size_h/8], 0,20)
                Write(round(size_w//100*2),finish,color3,[size_w/1.94,size_h/1.17])        

                if event.type == MOUSEMOTION:
                    if finishBtn.collidepoint(mouse_pos):
                        pygame.draw.rect(screen, color1, [size_w/2.3,size_h/1.26,size_w/6,size_h/8], size_w//200,20) 
                    else:
                        pygame.draw.rect(screen, dark_green, [size_w/2.3,size_h/1.26,size_w/6,size_h/8], 0,20) 
                        Write(round(size_w//100*2),finish,color3,[size_w/1.94,size_h/1.17])  
                elif event.type == MOUSEBUTTONDOWN:
                    if finishBtn.collidepoint(mouse_pos):
                        if getCourseLvl() < 2:
                            changeCourselvl(2)
                        activeMenu = True
                        courseLvl = 1
    def lesson2():
        global activeMenu,courseLvl,mentorIcon,wait,storedTime,activeMain,type,chosen,inFight,notBlocked,theme
        global hp1,hp2,iterator,activeMain,rectCenter,langugage
        if activeMain:
            course.standardLessonEvents("lesson2",16,condition=notBlocked)
        if activities[0] and not activeMenu and str(activeLesson)[17:-23]=="lesson2":
            language = getLang()
            if getTheme().lower() == "light":
                mentorIcon = pygame.image.load(r"{}/Images/Game/orcM.png".format(dirPath))
            else:
                mentorIcon = pygame.image.load(r"{}/Images/Game/orc.png".format(dirPath))
            mentorIcon = pygame.transform.scale(mentorIcon, [int(size_w/10.6),int(size_h/6)])
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
                global selected,goBtn
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
                        troll = pygame.image.load(r"{}/Images/Game/troll.png".format(dirPath)) 
                        trollDialog =  pygame.image.load(r"{}/Images/Game/trollDialog.png".format(dirPath))
                        trollM = pygame.image.load(r"{}/Images/Game/trollMarked.png".format(dirPath))  
                        troll = pygame.transform.scale(troll, [int(size_w/4.55),int(size_h/1.64)])  
                        trollM = pygame.transform.scale(trollM, [int(size_w/4.55),int(size_h/1.64)])
                        trollDialog = pygame.transform.scale(trollDialog, [int(size_w/4.55),int(size_h/2.71)]) 
                        icons = [troll,trollM,trollDialog]
                        course.dungeon.singleUnitInit(icons,size_w/2.52,size_h/4.86)
                        tw = troll.get_width()
                        th = troll.get_height()
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
                        hunter = pygame.image.load(r"{}/Images/Game/knight2.png".format(dirPath))
                        hunter = pygame.transform.scale(hunter, [int(size_w/5.26),int(size_h/1.92)])
                        hunterMarked = pygame.image.load(r"{}/Images/Game/knight2M.png".format(dirPath))
                        hunterMarked = pygame.transform.scale(hunterMarked, [int(size_w/5.26),int(size_h/1.92)])
                        hunterDialog = pygame.image.load(r"{}/Images/Game/knight3.png".format(dirPath))
                        hunterDialog = pygame.transform.scale(hunterDialog, [int(size_w/4.55),int(size_h/2.71)])
                        icons = [hunter,hunterMarked,hunterDialog]
                        course.dungeon.singleUnitInit(icons,size_w/2.42,size_h/4.5)
                        hw = hunter.get_width()
                        hh = hunter.get_height()
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
                        knight = pygame.image.load(r"{}/Images/Game/knight1.png".format(dirPath))
                        knightMarked = pygame.image.load(r"{}/Images/Game/knight1M.png".format(dirPath))
                        icons = [knight,knightMarked]
                        for icon in icons:
                            index = icons.index(icon)
                            icon = pygame.transform.scale(icon, [int(size_w/2.985),int(size_h/1.92)])
                            icons[index] = icon
                        course.dungeon.singleUnitInit(icons,size_w/2.69,size_h/4.38)
                        wdth = size_w/2.69
                        hght = size_h/4.38
                        kw = knight.get_width()
                        kh = knight.get_height()
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
    def lesson3():
        global mentorIcon,activeMain,held,courseLvl,notBlocked,iterator,activeMenu,chosen
        if activeMain:
            course.standardLessonEvents("lesson3",28,condition=notBlocked)
        if activities[0] and not activeMenu and str(activeLesson)[17:-23]=="lesson3":
            mentorIcon = pygame.image.load(r"{}/Images/Game/wizard.png".format(dirPath))
            mentorIcon = pygame.transform.scale(mentorIcon, [int(size_w/10.6),int(size_h/6)])
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
    def lesson4():
        global mentorIcon,activeMain,held,courseLvl,notBlocked,iterator,activeMenu,notBlocked
        global storedCords,done,language,chosen,loadingBar,storedTime,TD_lvlType,TD_Lvls
        global TD_count,TD_subDone,TD_toDefeat,TD_done
        language = getLang()
        if activities[0] and not activeMenu and str(activeLesson)[17:-23]=="lesson4":
            mentorIcon = pygame.image.load(r"{}/Images/Game/wizard.png".format(dirPath))
            mentorIcon = pygame.transform.scale(mentorIcon, [int(size_w/10.6),int(size_h/6)])
            if activeMain:
                if courseLvl in TD_Lvls:
                    course.standardLessonEvents("lesson4",99,condition=notBlocked,standard=False,customCol=TD_darkGreen) 
                else:
                    course.standardLessonEvents("lesson4",99,condition=notBlocked) 
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
                startBtn = course.centeredBtn(2.98,purple,"First wave",fontSize=1.6)
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
                        course.tower_defence.showUnit(enemyGhost,"Phantom","First Wave")
                        WriteItalic(round(size_w//100*3),"Press any key to start...",lt_gray,[size_w/1.88,size_h/9.6])
                        unitBeingShowed = True
                if not unitBeingShowed and not TD_subDone:
                    course.dialogTop(6.41,"My beautiful archespors are ready,","time to face evil forces",bckgr=True)

                if event.type == KEYDOWN and TD_subDone:
                    course.tower_defence.reset()
                if event.type == MOUSEMOTION and not unitBeingShowed:
                    if startBtn.collidepoint(mouse_pos):
                        course.centeredBtn(2.98,logoBlue,"",fontSize=1.6)
                        course.centeredBtn(2.98,dark_blue,"First wave",fontSize=1.6,border=size_w//150)
                elif event.type == MOUSEBUTTONDOWN and not unitBeingShowed:
                    if startBtn.collidepoint(mouse_pos):
                        storedTime = getActualSecond()
                        TD_subDone = True
            elif courseLvl == 10:
                storedTime = ""
                TD_lvlType = "onlyenemy"
                TD_toDefeat = 6
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
                storedTime = ""
                TD_lvlType = "onlyfriend"
                TD_toDefeat = 4
                course.tower_defence.drawMap()
                course.tower_defence.adminTools()
                course.tower_defence.console()                         
    def lesson5():
        course.standardLessonEvents("lesson5",99)
    def lesson6():
        course.standardLessonEvents("lesson6",99)  
    def lesson7():
        course.standardLessonEvents("lesson7",99)
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
        global size,size_w,size_h,activeAny,TD_circs
        global hp1,hp2,rectCenter,TD_wdthStart,TD_hghtStart
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
                resCircs = [resCirc1,resCirc2,resCirc4]
                res = [[1200,700],[1600,900],[displaySize.current_w,displaySize.current_h]]
                for resCirc in resCircs:
                    if resCirc.collidepoint(mouse_pos):
                        index = resCircs.index(resCirc)
                        size_w = res[index][0]
                        size_h = res[index][1]
                        size = (size_w,size_h)
                        activeAny = False
                        activities[2] = False
                        TD_circs = []
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
class Prize(pygame.sprite.Sprite):
    def startScreen():
        global activeAny,name
        if activities[3]:
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
            
            table = pygame.image.load(r"{}/Images/Game/table.png".format(dirPath))
            table = pygame.transform.scale(table, [int(size_w/1.7),int(size_h/4)])
            screen.blit(table,[size_w/4.11,size_h/2.86])
            screen.blit(table,[size_w/4.11,size_h/1.4])

            if language == "ENG":
                names = [
                    "Beginner's cup",
                    "Romo's axe",
                    "Magic potion",
                    "None",
                    "None",
                    "None",
                    "None",
                    "None",
                ]
            else:
                names = [
                    "Puchar nowicjusza",
                    "Topór Romo",
                    "Magiczny eliksir",
                    "None",
                    "None",
                    "None",
                    "None",
                    "None",
                ]
            
            cupL = pygame.image.load(r"{}/Images/install/cup_locked.png".format(dirPath))
            cupL = pygame.transform.scale(cupL, [int(size_w/10.6),int(size_h/6)])  
            axeL = pygame.image.load(r"{}/Images/Game/romosaxe_locked.png".format(dirPath))
            axeL = pygame.transform.scale(axeL, [int(size_w/10.6),int(size_h/6)]) 
            potionL = pygame.image.load(r"{}/Images/Game/potion_locked.png".format(dirPath))
            potionL = pygame.transform.scale(potionL, [int(size_w/14.6),int(size_h/6)]) 
            iconsLocked = [cupL,axeL,potionL]

            cup = pygame.image.load(r"{}/Images/install/cup.png".format(dirPath))
            cup = pygame.transform.scale(cup, [int(size_w/10.6),int(size_h/6)])  
            axe = pygame.image.load(r"{}/Images/Game/romosaxe.png".format(dirPath))
            axe = pygame.transform.scale(axe, [int(size_w/10.6),int(size_h/6)]) 
            potion = pygame.image.load(r"{}/Images/Game/potion.png".format(dirPath))
            potion = pygame.transform.scale(potion, [int(size_w/14.6),int(size_h/6)]) 
            iconsUnlock = [cup,axe,potion]

            wdth = size_w/3.34
            hght = size_h/2.13
            lvl = getCourseLvl() - 2
            iterator = 0

            for it in range(2):
                for it2 in range(4):
                    pygame.draw.rect(screen, gold, [wdth,hght,size_w/12,size_h/15], 0,size_w//450)
                    if iterator<=lvl:
                        Write(round(size_w//100*0.7),names[iterator],color1,[wdth+(size_w/12)/2,hght+(size_h/15)/2])
                        screen.blit(iconsUnlock[iterator],[wdth,hght-size_h/4.7])
                    else:
                        Write(round(size_w//100*1.2),"?",color1,[wdth+(size_w/12)/2,hght+(size_h/15)/2])
                        try:
                            screen.blit(iconsLocked[iterator],[wdth,hght-size_h/5])
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

running = True
start=Start
course=Course
lookFor = LookFor
settings = Settings
contacts = Contacts
prize = Prize
start.useScreenDef()
print("Init_End_Time: ",str(datetime.now())[10:])
while running:
    keys = pygame.key.get_pressed()
    mouse_pos = pygame.mouse.get_pos() 
    start.adminTools.counterCords()
    start.adminTools.counterFPS()
    course.tower_defence.loadingBar(storedTime)
    for event in pygame.event.get():
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
            prize.startScreen()
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    #EVENTS THAT NEED TO BE REFRESHED FASTER THAN EVENT LOOP
    course.tower_defence.enemiesPath(storedTime)
    course.tower_defence.targeting()
    pygame.display.update()
