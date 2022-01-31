import pygame
from random import randint
 
class Peli:
    def __init__(self):
        pygame.init()
    
        self.kello = pygame.time.Clock()
 
        self.leveys = 640
        self.korkeus = 480
 
        self.naytto = pygame.display.set_mode((self.leveys, self.korkeus))
        pygame.display.set_caption("Kolikko peli")
        self.fontti = pygame.font.SysFont("Arial", 24)
 
        self.robo = pygame.image.load("robo.png")
        self.robo_y = self.korkeus - self.robo.get_height()
        self.robo_x = self.leveys/2-self.robo.get_width()/2
 
        self.kolikko = pygame.image.load("kolikko.png")
        self.kolikko_x = 0          #kolikon sijainti x alussa
        self.kolikko_y = 0 - self.kolikko.get_height() #kolikon sijainti y alussa
 
        self.hirvio = pygame.image.load("hirvio.png")      
        self.hirvio_x = 0           #hirvion sijanti alussa
        self.hirvio_y = 0 - self.hirvio.get_height() #        
 
        self.nopeus = 1             #pelin nopeuden nosto, ehkä jos lisätään tasoja yms?
        self.oikealle = False       #robon liikken tila
        self.vasemmalle = False     #robon liikken tila
#        self.alas = False
#        self.ylos = False
        self.suojaus = False
        self.pisteet = 0
        self.kolikot = []
        self.hirviot = []
        self.peli_run = 0           # 0=peli alkaa,1=peli käy,2= peli ohi
        self.txt = ["Kerää kolikoita: ",  
                    "osumasta saa +1 pistettä, hudista -1 pistettä",
                    "peli päättyy jos pisteet on >0 tai osut hirviöön", 
                    "robo liikkuu nuolinäppäimillla oikealle ja vasemmalle",
                    "SPACE = suoja yhdeltä hirviön osumalta, pisteet -10", 
                    "Esc = sulje peli", 
                    "F2 = uusi peli",
                    "RETURN = ALOITA PELI"
                    ]
        self.silmukka()
 
    def silmukka(self):
        while True:
            self.tutki_tapahtumat()  #tarkista näppäin komennot
            self.piirra_naytto()
            self.kello.tick(60)
 
    def arvonta(self):  #arvotaan uudet kolikot ja hirviot
        if len(self.kolikot) < 7: #kolikkojen max määrä
            uusi = randint(0,50)
            if uusi == 1: 
                self.kolikko_x = randint(0, self.leveys-self.kolikko.get_width())
                self.kolikot.append([self.kolikko_x,self.kolikko_y])
        
        if len(self.hirviot) <= self.pisteet//10 and len(self.hirviot) < 6:
            uusi = randint(0,100)
            if uusi == 1:
                self.hirvio_x = randint(0, self.leveys-self.hirvio.get_width())
                self.hirviot.append([self.hirvio_x,self.hirvio_y])
 
    def tutki_tapahtumat(self):
        for tapahtuma in pygame.event.get():
            if tapahtuma.type == pygame.QUIT:
                exit()
            if tapahtuma.type == pygame.KEYDOWN:
                if tapahtuma.key == pygame.K_LEFT:
                    self.vasemmalle = True
                if tapahtuma.key == pygame.K_RIGHT:
                    self.oikealle = True
#                if tapahtuma.key == pygame.K_UP:
#                    self.ylos = True
#                if tapahtuma.key == pygame.K_DOWN:
#                    self.alas = True
                if tapahtuma.key == pygame.K_F2:
                    Peli()
                if tapahtuma.key == pygame.K_ESCAPE:
                    exit()
                if tapahtuma.key == pygame.K_SPACE and self.peli_run == 1:
                    self.suojukset()
                if tapahtuma.key == pygame.K_RETURN and self.peli_run == 0:
                                        #jos peli ei käynnissä
                    self.peli_run = 1   #alota peli
 
            if tapahtuma.type == pygame.KEYUP:  
                if tapahtuma.key == pygame.K_LEFT:
                    self.vasemmalle = False
                if tapahtuma.key == pygame.K_RIGHT:
                    self.oikealle = False
#                if tapahtuma.key == pygame.K_UP:
#                    self.ylos = False
#                if tapahtuma.key == pygame.K_DOWN:
#                    self.alas = False
 
        if self.peli_run == 1:  #robo liikku vain jos peli käynnissä
            if self.oikealle and self.robo_x+self.robo.get_width() <= self.leveys:
                self.robo_x += self.nopeus* 6
            if self.vasemmalle and self.robo_x >= 0:
                self.robo_x -= self.nopeus* 6   
#            if self.ylos and self.robo_y >= 0:# 
#                self.robo_y -= 4
#            if self.alas and self.robo_y+self.robo.get_height() <= self.korkeus:
#                self.robo_y += 4  
#             
    def kolikko_liikkuu(self):
        for self.alkio in self.kolikot:
            poista_alkio = False #poista kolikko listalta
            self.alkio[1] += self.nopeus
            if self.alkio[1] + self.kolikko.get_height() >= self.korkeus + self.kolikko.get_height():
                poista_alkio = True                  #self.kolikot.remove(self.alkio)
                self.laske_pisteet(-1)        
 
            if self.osuma(self.alkio, self.kolikko):
                poista_alkio = True                 #self.kolikot.remove(self.alkio)
                self.laske_pisteet(1)               #jos osuma pisteet +1 
 
            if  poista_alkio:
                self.kolikot.remove(self.alkio)           
 
    def hirvio_liikkuu(self):
        for self.alkio in self.hirviot:
            self.alkio[1] += self.nopeus
            if self.alkio[1] > 100:                 #self.korkeus/2:
                if self.alkio[0] > self.robo_x:
                    self.alkio[0] -= 0.5
                if self.alkio[0] < self.robo_x:
                    self.alkio[0] += 0.5 
 
            if self.osuma(self.alkio, self.hirvio): #jos osuma = True
                if self.suojaus:                    #jos suojaus = True
                    self.hirviot.remove(self.alkio)
                    self.suojaus = False
                else:
                    self.peli_run = 2               #peli päättyy
 
            if self.alkio[1] + self.hirvio.get_height() >= self.korkeus + self.hirvio.get_height():
                self.hirviot.remove(self.alkio)
 
    def osuma(self, alkio, muuttuja):           #tarkistetaan alkion osuma roboon
        if alkio[1] + muuttuja.get_height() >= self.korkeus - self.robo.get_height():
            robon_leveys_keskikohta = self.robo_x +self.robo.get_width()/2
            alkion_leveys_keskikohta = alkio[0]+muuttuja.get_width()/2
            keskikohtien_etaisyys = abs(robon_leveys_keskikohta - alkion_leveys_keskikohta)
            leveys_yht = (self.robo.get_width()+muuttuja.get_width())/2
            if keskikohtien_etaisyys <= leveys_yht:
                return True
        return False
 
    def suojukset(self):
        if self.suojaus == False:
            self.laske_pisteet(-10)
            self.suojaus = True
 
    def laske_pisteet(self, pisteet):
        self.pisteet += pisteet
        if self.pisteet < 0:        #jos pisteet < 0 peli päättyy
            self.peli_run = 2
 
    def piirra_naytto(self):
 
        self.naytto.fill((20, 20, 20))
 
        for kolikko in self.kolikot:            #pirrä kolikot
            self.naytto.blit(self.kolikko, (kolikko[0], kolikko[1]))
        
        for hirvio in self.hirviot:             #piirrä hirviot
            self.naytto.blit(self.hirvio, (hirvio[0], hirvio[1]))
 
        if self.suojaus:
            pygame.draw.rect(self.naytto, (0, 0, 200), (self.robo_x, self.robo_y, self.robo.get_width(), self.robo.get_height()))            
 
        self.naytto.blit(self.robo, (self.robo_x, self.robo_y))
 
        if self.peli_run == 1:                  #peli käynnissä
            self.kolikko_liikkuu()
            self.hirvio_liikkuu()
            self.arvonta()         
 
            teksti = self.fontti.render("Pisteet: "+str(self.pisteet), True, (120, 255, 0))
            self.naytto.blit(teksti, (self.leveys-150, 20))
 
        if self.peli_run == 0:                  #pelin alotus
            rivivali =  40
            for t in self.txt:
                teksti = self.fontti.render(t, True, (120, 255, 0))
                self.naytto.blit(teksti, (40, rivivali))
                rivivali += 40
         
        if self.peli_run == 2:                  #peli ohi
            fontti = pygame.font.SysFont("Arial", 50)
            teksti1 = fontti.render("PELI OHI", True, (255, 0, 0))
            pisteet = self.pisteet
            if pisteet < 0:
                pisteet = 0
            teksti2 = fontti.render("Sait "+str(pisteet)+" pistettä", True, (255, 0, 0))
            teksti4 = self.fontti.render("Esc = sulje peli", True, (120, 255, 0))
            teksti5 = self.fontti.render("F2 = uusi peli", True, (120, 255, 0))
            self.naytto.blit(teksti1, (self.leveys/2-teksti1.get_width() /2, 60))
            self.naytto.blit(teksti2, (self.leveys/2-teksti2.get_width() /2, 120))
            self.naytto.blit(teksti4, (40, self.korkeus-100)) 
            self.naytto.blit(teksti5, (40, self.korkeus-60))
 
        pygame.display.flip()
 
if __name__ == "__main__":
    Peli()
