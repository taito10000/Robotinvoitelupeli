# TEE PELI TÄHÄN

# MOOC Ohjelmoinnin jatkokurssi : lopun harjoitustehtävä.
# Peli pygame kirjastoa sekä kolmea elementtiä käyttäen - 
# robotti, kolikko ja hirviö - Palautus yhtenä tiedostona. 



import pygame
# import math
from random import randint



class Pelilauta:

    def __init__(self):

        pygame.init()
        self.naytto = pygame.display.set_mode((800,576))
        self.naytto.fill((0,0,0))
        
        self.oljykuva = pygame.image.load("hirvio.png")
        self.oljykuva = pygame.transform.scale(self.oljykuva, (25,28))
        self.ruutualat = {}
        
        self.moottori = Pelimoottori(self)
        self.alusta()
        
    
        
    
    def alusta(self):
        
        
        
        pygame.display.set_caption("RobOil!")
        
        self.leveys = 3
        self.korkeus = 3
        self.ruudunsivu = 500 / 4
        self.ruudut = []
        
        self.gui_elements = []
        self.x_marginaali = (800 - self.ruudunsivu*self.leveys)/2
        self.y_marginaali = 80


        i = 1
        for y in range(0, self.korkeus):
            tmp = []
            for x in range(0, self.leveys):
                x_ = x*self.ruudunsivu+self.x_marginaali
                y_ = y*self.ruudunsivu+self.y_marginaali
                tmp.append((x_, y_))
                self.ruutualat[i] = pygame.Rect(x_,y_, self.ruudunsivu, self.ruudunsivu)
                i += 1
            self.ruudut.append(tmp)
        
        self.gui_elements.append(Nappi(self, (700,90), "+1 ALL"))
        self.gui_elements.append(Nappi(self, (700,175), "AVG !"))
        self.gui_elements.append(Nappi(self, (700,260), "POW"))
        self.gui_elements.append(Nappi(self, (700,345), "START"))

        self.looppi()
        
    def levelUp(self):
        
        i = 1
        self.ruutualat = {}
        self.ruudut = []
        if self.leveys < 6:
            self.leveys += 1
        
        if self.leveys % 2 != 0 and self.korkeus < 4:
            self.korkeus += 1
        if self.moottori.taso == 3:
            self.ruudunsivu -= 20
        
        
        
        self.x_marginaali = (800 - self.ruudunsivu*self.leveys)/2
        for y in range(0, self.korkeus):
            tmp = []
            for x in range(0, self.leveys):
                x_ = x*self.ruudunsivu+self.x_marginaali
                y_ = y*self.ruudunsivu+self.y_marginaali
                tmp.append((x_, y_))
                self.ruutualat[i] = pygame.Rect(x_, y_, self.ruudunsivu, self.ruudunsivu)
                i += 1
            self.ruudut.append(tmp)
        
        print("LEVEL UP !")
        

    def piirra_ruudut(self):
        
        col1 = (39, 40, 41)
        col2 = (45, 47, 49)
        col3 = (144, 148, 153)
        col4 = (84, 103, 122)
        i = 0
        j = 0
        kulma = 1
        
        for y in self.ruudut:
            
            for x in y:
                if j % 2 == 0 and i % 2 == 0:
                    col = col1
                elif j % 2 == 0 and i%2 != 0:
                    col = col2
                elif j%2 !=0 and i%2 ==0:
                    col = col2
                elif j%2 !=0 and i%2 !=0:
                    col = col1
                
                pygame.draw.rect(self.naytto, col, (x[0],x[1], self.ruudunsivu,self.ruudunsivu))
                
                i +=1
            j += 1
            i = 0
            i2 = 0
            j2 = 0
            for y in self.ruudut:
                
                if i2 > 0:
                
                    pygame.draw.line(self.naytto, col4, (y[0][0]-5, y[0][1]+4), (y[0][0]+self.leveys*self.ruudunsivu+10, y[0][1]-4), 5)
    
                i2 +=1

            for x in self.ruudut[0]:
                if j2 > 0:
                    pygame.draw.line(self.naytto, col4, (x[0]+3, x[1]-4), (x[0]-3, x[1]+self.korkeus*self.ruudunsivu+8), 5)
                    
                j2 += 1
        
        
    def piirra_gui(self):
        
        pistecol = (214, 140, 28)
        alacol = (145, 98, 26)
        alacol2 = (47,47,47)
        oljylkmcol = (214, 140, 28)
        circcol1 = (145, 98, 26)
        circcol2 = (72, 38, 6)
        
        
        for e in self.gui_elements:
            e.piirra()
        
        for r in self.moottori.robot:
            
            r.piirra_robo()
        
        for p in self.moottori.powerups:

            p.piirra_powerup()
        
        pointfontti = pygame.font.SysFont("Arial", 40)
        levelfontti = pygame.font.SysFont("Arial", 60)
        aikafontti = pygame.font.SysFont("Arial", 20)
        lvllabelfontti = pygame.font.SysFont("Arial", 10)
        aikatext = aikafontti.render(str(f":{self.moottori.aika:02d}"), True, pistecol)
        pointText = pointfontti.render(str(f"{self.moottori.pisteet:03d}"), True, pistecol)
        oljytxt = pointfontti.render(str(f": {self.moottori.oljymaara}"), True, oljylkmcol)
        leveltxt = levelfontti.render(str(f"{self.moottori.taso}"), True, pistecol)
        levellabeltxt = lvllabelfontti.render("LEVEL:", True, pistecol)
        pygame.draw.rect(self.naytto, alacol, (250, 490, 300, 110))
        pygame.draw.rect(self.naytto, alacol2, (258, 498, 284, 102))
        pygame.draw.circle(self.naytto, circcol1, (800, 623), 150)
        pygame.draw.circle(self.naytto, circcol2, (800, 623), 143)
        pygame.draw.circle(self.naytto, circcol1, (20, -45), 150)
        pygame.draw.circle(self.naytto, circcol2, (20, -45), 143)
        
        self.naytto.blit(self.oljykuva, (340, 510))
        self.naytto.blit(self.oljykuva, (350, 535))
        self.naytto.blit(self.oljykuva, (320, 525))
        self.naytto.blit(pointText, (720, 519))
        self.naytto.blit(oljytxt, (410, 515))
        self.naytto.blit(aikatext, (390, 22))
        self.naytto.blit(levellabeltxt, (25, 10))
        self.naytto.blit(leveltxt, (25, 15))


    def gameover(self):

        fontti = pygame.font.SysFont("Arial", 40)
        fontti2 = pygame.font.SysFont("Arial", 15)
        teksti = fontti.render("GAME OVER", True, (0,0,0))
        teksti2 = fontti2.render(f"Sait {self.moottori.pisteet} pistettä. Resetoi painamalla ruutua", True, (0,0,0))
        pygame.draw.rect(self.naytto, (250,70,70), (100,130,600,200))
        self.naytto.blit(teksti, (295, 185))
        self.naytto.blit(teksti2, (265, 235))
        
    def ohje(self):
        
        fontti = pygame.font.SysFont("Arial", 30)
        fontti2 = pygame.font.SysFont("Arial", 14)
        ohjetxt1 = "RobOil!"
        ohjetxt = ["Tehtäväsi on voidella robotteja. Voitelyöljyä on niukalti.", " ",
                    "Klikkaamalla Robotin päällä, lisäät 1 mitallisen öljyä.", 
                    "Robotin vatsassa näkyy luku joka pienenee. Luku ei saa päästä nollaan.",
                    "Käytettyäsi voiteluöljyn loppuun, määrä palautuu muutaman hetken kuluessa."
                    " ", "Saat pisteitä jokaisesta voitelusta ja jokaisesta onnistuneesta 10 sekunnista."," ",
                    "Laudalle ilmestyy erilaisia power up kolikoita. Lisäksi oikeassa reunassa on joka tasolle", 
                    "1 kpl '1 annos öljyä jokaiselle robotille' ja 'AVG' - eli solidaarisuusnappi, jolla robotit", 
                    "jakavat öljyn tasan keskenään. 'POW' nappi antaa ylimääräisen power upin", " ", "       Klikkaa hiirellä Ohje pois. Aloita klikkaamalla Start"]
        
        teksti = fontti.render(ohjetxt1, True, (250,250,250))
        

        pygame.draw.rect(self.naytto, (47, 55, 77), (100,50,600,450))
        self.naytto.blit(teksti, (310, 90))
        
        rivikork = 13
        for line in ohjetxt:
            
            teksti2 = fontti2.render(line, True, (250,250,250))
            self.naytto.blit(teksti2, (140, 138+rivikork))
            rivikork += 22





    def looppi(self):
        
        while True:
            
            self.moottori.tutki_tapahtumat()
            
            if self.moottori.gameover == False:
                
                self.naytto.fill((0,0,0))
                self.piirra_ruudut()
                self.piirra_gui()
            if self.moottori.gameover == True:
                self.gameover() 
            if self.moottori.ohjetxt == True:
                self.ohje()
            pygame.display.flip()
            self.moottori.clock.tick(60)









class Nappi:

    def __init__(self, lauta: Pelilauta, paikka:tuple, teksti:str):
        
        self.aktiivinen = True
        self.lauta = lauta
        self.x = paikka[0]
        self.y = paikka[1]
        self.label = teksti
        self.nappicol1 = (148, 81, 15)
        self.textCol1 = (240, 188, 129)
        self.nappicol2 = (38, 27, 15)
        self.textCol2 = (66, 34, 0)
        self.reunacol1 = (180, 120, 30)
        self.reunaCol2 = (51, 43, 35)

        self.nappicol = self.nappicol1
        self.textCol = self.textCol1
        self.reunacol = self.reunacol1

        self.fontti = pygame.font.SysFont("Arial", 20)
        self.teksti = self.fontti.render(teksti, True, self.textCol1)
        self.naytto = lauta.naytto


        self.rect = pygame.draw.rect(self.naytto, self.reunacol, (paikka[0]-3, paikka[1]-3, 84, 54))
        self.rect = pygame.draw.rect(self.naytto, self.nappicol, (paikka[0], paikka[1], 78, 48))
        self.naytto.blit(self.teksti, (self.x+12, self.y+13))

    def aktivoi(self):
        self.aktiivinen = True
        self.nappicol = self.nappicol1
        self.textCol = self.textCol1
        self.reunacol = self.reunacol1
        self.teksti = self.fontti.render(self.label, True, self.textCol)

    def deaktivoi(self):
        self.aktiivinen = False
        self.nappicol = self.nappicol2
        self.textCol = self.textCol2
        self.reunacol = self.reunaCol2
        self.teksti = self.fontti.render(self.label, True, self.textCol)

    def piirra(self):
        self.rect = pygame.draw.rect(self.naytto, self.reunacol, (self.x-3, self.y-3, 84, 54))
        self.rect = pygame.draw.rect(self.naytto, self.nappicol, (self.x, self.y, 78, 48))
        self.naytto.blit(self.teksti, (self.x+12, self.y+13))

    def kerropaikka(self):
            return pygame.Rect(self.x, self.y, 84, 54)

    def paina(self):

            print("NAPPIA: ", self.label, "painettu")
            if self.aktiivinen == True:
                self.lauta.moottori.painettunappia(self.label)
                self.deaktivoi()







class Robo:
    id = 0
    def __init__(self, pelilauta:Pelilauta, pelipaikka:int, alkupointsit:int):
        self.pisteet = alkupointsit
        self.kuva = pygame.image.load("robo.png")
        self.rect = self.kuva.get_rect()
        self.leveys = self.kuva.get_width()
        self.korkeus = self.kuva.get_height()
        self.lauta = pelilauta
        self.pelipaikka = pelipaikka
        self.x = self.lauta.ruutualat[self.pelipaikka][0]
        self.y = self.lauta.ruutualat[self.pelipaikka][1]
        self.rect.x = self.x
        self.rect.y = self.y
        self.fontti = pygame.font.SysFont("Arial", 23)
        self.teksti = self.fontti.render(str(self.pisteet), True, (255,255,255))
        
        
        self.id = Robo.id
        Robo.id += 1
        
    def aseta_piste(self, piste:int):
        self.pisteet = piste


    def lisaa_piste(self, piste:int = 1):
        self.pisteet += piste

    def poista_piste(self, piste:int = 1):
        if self.pisteet > 0:
            self.pisteet -= piste
        else:
            self.lauta.moottori.game_over()

    def piirra_robo(self):
        self.x = self.lauta.ruutualat[self.pelipaikka][0]
        self.y = self.lauta.ruutualat[self.pelipaikka][1]
        self.x_ = self.x + self.lauta.ruutualat[self.pelipaikka][2]/2 - self.leveys/2
        self.y_ = self.y + self.lauta.ruutualat[self.pelipaikka][3]/2 - self.korkeus/2
        self.rect.x = self.x_
        self.rect.y = self.y_
        self.teksti = self.fontti.render(str(self.pisteet), True, (255,15,34))
        self.lauta.naytto.blit(self.kuva, (self.x_, self.y_))
        self.lauta.naytto.blit(self.teksti, (self.x_+self.leveys/2-11, self.y_+self.korkeus/2-4))

    def klikkaa_robo(self):
            if self.lauta.moottori.oljymaara > 0:
                self.lauta.moottori.oljymaara -= 1
                self.lisaa_piste()
                self.lauta.moottori.pisteet += 1

            if self.lauta.moottori.oljymaara == 0 and self.lauta.moottori.oljypalautus_kaynnissa == False:
                self.lauta.moottori.palauta_oljya()





class PowerUp:

    def __init__(self, pelilauta:Pelilauta, pelipaikka:int, aika:int, tyyppi:str):
        
        self.kuva = pygame.image.load("kolikko.png")
        self.rect = self.kuva.get_rect()
        self.leveys = self.kuva.get_width()
        self.korkeus = self.kuva.get_height()
        self.tyyppi = tyyppi
        self.lauta = pelilauta
        self.pelipaikka = pelipaikka
        self.aika = aika
        self.fontti = pygame.font.SysFont("Arial", 20)
    
    
    def piirra_powerup(self):

        self.x = self.lauta.ruutualat[self.pelipaikka][0]
        self.y = self.lauta.ruutualat[self.pelipaikka][1]
        self.x_ = self.x + self.lauta.ruutualat[self.pelipaikka][2]/2 - self.leveys/2
        self.y_ = self.y + self.lauta.ruutualat[self.pelipaikka][3]/2 - self.korkeus/2
        self.rect.x = self.x_
        self.rect.y = self.y_
        self.teksti = self.fontti.render(str(self.tyyppi), True, (150,150,34))
        self.lauta.naytto.blit(self.kuva, (self.x_, self.y_))
        self.lauta.naytto.blit(self.teksti, (self.x_+self.leveys/2-21, self.y_+self.korkeus))

    def klikkaa_powo(self):

        if self.tyyppi == "+5 ölj":
            self.lauta.moottori.oljymaara += 5
        elif self.tyyppi == "-ROBO":
            self.lauta.moottori.robot.pop(-1)
        
        elif self.tyyppi == "+5All":
            for r in self.lauta.moottori.robot:
                piste = r.pisteet
                r.aseta_piste(piste+5)        
        
        
        elif self.tyyppi == "+10":
            lkm = len(self.lauta.moottori.robot)
            arvottu = randint(0, lkm-1)
            self.lauta.moottori.robot[arvottu].pisteet += 10


        elif self.tyyppi == "PTS!!":
            self.lauta.moottori.pisteet += 10
        
        elif self.tyyppi == "PTS--":
            self.lauta.moottori.pisteet -= 20

        self.lauta.moottori.powerups.remove(self)
        self.lauta.moottori.pow_arvonta_sallittu = False
        pygame.time.set_timer(self.lauta.moottori.pow_cooldown_event, 5000, True)
        pygame.time.set_timer(self.lauta.moottori.powerup_timer_event, 0)
    
    
    def poista(self):
        self.lauta.moottori.powerups.remove(self)
        pygame.time.set_timer(self.lauta.moottori.pow_cooldown_event, 3000, True)





class Pelimoottori:

    def __init__(self, lauta: Pelilauta):
        

        self.lauta = lauta
        self.lauta.moottori = self
        
        self.oljymaara = 3
        self.plus1lkm = 2
        self.robolkm = 3
        self.aika = 15
        self.pisteet = 0
        self.lisaa_kaikkiin = True
        self.keskiarvo = True
        self.pow_arvonta_sallittu = True
        self.pow_napin_aktivointiaika = 9
        self.taso = 1
        self.robot = []
        self.powerups = []
        self.clock = pygame.time.Clock()
        self.timer_event = pygame.USEREVENT+1
        self.robo_timer_event = pygame.USEREVENT+2
        self.oljy_timer_event = pygame.USEREVENT+3
        self.powerup_timer_event = pygame.USEREVENT+4
        self.pow_cooldown_event = pygame.USEREVENT+5
        self.POW_timer_event = pygame.USEREVENT+6
        self.counter = 0
        self.gameover = False
        self.ohjetxt = True
        self.oljypalautus_kaynnissa = False

    def reset(self):
        self.ohjetxt = False
        self.oljymaara = 3
        self.pisteet = 0
        self.aika = 15
        self.taso = 1
        self.robot = []
        self.powerups = []
        self.counter = 0
        self.gameover = False
        self.lauta.ruutualat = {}
        self.lauta.alusta()
        self.vapaatruudut = []
        self.oljypalautus_kaynnissa = False



    def next_level(self):
        for e in self.lauta.gui_elements:
            if e.label != "START":
                e.aktivoi()
        self.aika = 29
        self.plus1lkm = 2
        self.taso += 1
        self.lauta.levelUp()
        self.robot = []
        if self.taso <=5:    
            self.arvorobopaikat(40-self.taso*4)
        else:
            self.arvorobopaikat(20)
            self.pow_napin_aktivointiaika = 7
        self.powerups = []
        self.pow_arvonta_sallittu = True
        pygame.time.set_timer(self.POW_timer_event, 0)



    def painettunappia(self, label:str):
        if label == "+1 ALL":
            if self.plus1lkm>0:
                for r in self.robot:
                    r.lisaa_piste()
                    self.plus1lkm -= 1
                for e in self.lauta.gui_elements:
                    if e.label == "+1 ALL":
                        e.aktivoi()
        
        elif label == "AVG !":
            pisteet = sum([r.pisteet for r in self.robot])
            ka = int(pisteet / len(self.robot))
            for r in self.robot:
                r.aseta_piste(ka)
            print("KA : ", ka)

        elif label == "POW":
            self.arvo_powerup()
            pygame.time.set_timer(self.POW_timer_event, self.pow_napin_aktivointiaika*1000, True)

        elif label == "START":
            self.arvorobopaikat(25)
            
            
            pygame.time.set_timer(self.timer_event, 1000)
            pygame.time.set_timer(self.robo_timer_event, 1500)
        
    
    
    def arvorobopaikat(self, ylinaika:int):
        robolkm = 2+self.taso
        self.vapaatruudut = [i+1 for i in range(len(self.lauta.ruutualat))]
     
        for i in range(0, robolkm):
            self.robot.append(Robo(self.lauta, self.vapaatruudut.pop(randint(0,len(self.vapaatruudut)-1)) , randint(10,ylinaika)))
    
    
    def arvo_powerup(self):
        aika = 5
        tyypit = ["+5 ölj", "-ROBO", "+5All", "+10", "PTS!!","PTS!!", "PTS--"]
        t_len = len(tyypit)
        self.powerups.append(PowerUp(self.lauta, self.vapaatruudut.pop(randint(0, len(self.vapaatruudut)-1)),aika, tyypit[randint(0,t_len-1)]))
        pygame.time.set_timer(self.powerup_timer_event, 4000, True)
        self.pow_arvonta_sallittu = False

    def timer_sekunti(self):
        self.aika -= 1
        self.counter += 1

        if self.pow_arvonta_sallittu:
            trues = [randint(0,1) for i in range(0,8)]
            print(trues)
            if trues.count(True) >=6:
                self.arvo_powerup()


        if self.counter % 10 == 0:
            self.pisteet += 1
            
        
        if self.aika == 0:
            self.next_level()


    def timer_robotimer(self):
        for r in self.robot:
            r.poista_piste()

    def powerup_timer(self):

        print("POWER UP TIMER - DELETE")
        for p in self.powerups:
            p.poista()


    
    def game_over(self):
        pygame.time.set_timer(self.timer_event, 0)
        pygame.time.set_timer(self.robo_timer_event, 0)
        self.gameover = True
        self.lauta.gameover()


    def ohje(self):
        pygame.time.set_timer(self.timer_event, 0)
        pygame.time.set_timer(self.robo_timer_event, 0)
        self.ohjetxt = True
        self.lauta.ohje()

    def palauta_oljya(self):
        self.oljypalautus_kaynnissa = True
        pygame.time.set_timer(self.oljy_timer_event, 3000, True)

    

    
    def tutki_tapahtumat(self):
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                exit()
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if self.ohjetxt == True:
                    self.reset()
                if self.gameover == True:
                    self.reset()
                
                for e in self.lauta.gui_elements:
                    if e.kerropaikka().collidepoint(ev.pos):
                        e.paina()
                
                for r in self.robot:
                    if r.rect.collidepoint(ev.pos):
                        r.klikkaa_robo()

                for i in range(1, len(self.lauta.ruutualat)):
                    if self.lauta.ruutualat[i].collidepoint(ev.pos):
                        print(f"RUUTU ID: ", i)
                for p in self.powerups:
                    if p.rect.collidepoint(ev.pos):
                        p.klikkaa_powo()


            if ev.type == self.timer_event:
                self.timer_sekunti()
                
            if ev.type == self.robo_timer_event:
                self.timer_robotimer()  
            if ev.type == self.oljy_timer_event:
                if self.oljymaara == 0:
                    self.oljymaara = 3
                    self.oljypalautus_kaynnissa = False
                else:
                    self.oljymaara += 3
                    self.oljypalautus_kaynnissa = False

            if ev.type == self.powerup_timer_event:
                self.powerup_timer()
            if ev.type == self.pow_cooldown_event:
                self.pow_arvonta_sallittu = True

            if ev.type == self.POW_timer_event:
                for e in self.lauta.gui_elements:
                    if e.label == "POW":
                        e.aktivoi()

lauta = Pelilauta()
motor = Pelimoottori(lauta)


