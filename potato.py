# -*- coding: UTF-8 -*-
# i_path = ipath[count]
import pygame
from random import *
from pygame.locals import *

arquivo_config = open("config", "r")
arquivo_config = arquivo_config.read().split("\n")
novo = {}
for i in arquivo_config:
	if i == "" or i.count(":") == 0:
		continue
	i = i.split(":")
	novo[i[0]] = i[1]


perdeu = False
nojogo = 0
placar = 0
paraLado = 1
fase = 0
pontos = 0
vidas = 3
creditos = int(novo["creditos_inicial"])

pygame.font.init()
fontePress = pygame.font.SysFont('Comic Sans MS', 50)

#Tela Configs
pygame.init()
screen = pygame.display.set_mode((1280,720))
pygame.display.set_caption(novo["nome_display"])
clock = pygame.time.Clock()
screenIcone = pygame.image.load(novo["local_icon"]).convert_alpha()
pygame.display.set_icon(screenIcone)

#Bala configs
tempo_sec = 35
pos_bala = []
bala_desenho = pygame.Surface((14,35))
bala_desenho.fill((255,189,6))
velocidade_tiro = 10
balas = []

#Inimigo configs
pos_inimigo = (int(novo["spawn_inimigox"]),int(novo["spawn_inimigoy"]))
inimigo_sprite=pygame.image.load('Sprites/inimigo.png').convert_alpha()
inimigo_sprite=pygame.transform.scale(inimigo_sprite, (80,80))
direcao_inimigo = 1
direcao_inimigoy = 1
hit_inimigo = ((60,60))
velocidade_inimigo = 6
velocidade_inimigoy = 3
randomInimigo = 5000

#Balas Inimigo configs
liberado_inimigo = True
bala_inimigo = [pos_inimigo[0],pos_inimigo[1]]
bala_inimigo_desenho = pygame.Surface((15,40))
bala_inimigo_desenho.fill((255,255,255))
tempo_tiro_inimigo = 100
sorte = 300
velocidade_bala_inimigo = 10

#Escudo
escudo_sprite = pygame.image.load(novo["local_escudo"]).convert_alpha()
escudo_sprite = pygame.transform.scale(escudo_sprite, (100,120))
escudo_liberado = True
delay_escudo = 600
tempo_dur_escudo = int(novo["duracao_escudo"])
escudo = False

#Vidas Sprite
pos_vidas = [(720, 10),(780, 10),(840, 10)]
vidas_spriteVivo = pygame.image.load(novo["local_vidas"]).convert_alpha()
vidas_spriteVivo = pygame.transform.scale(vidas_spriteVivo, (50,50))
vidas_spriteMorto = pygame.image.load(novo["local_vidaspb"]).convert_alpha()
vidas_spriteMorto = pygame.transform.scale(vidas_spriteMorto, (50,50))

#Chao configs
pos_chao = ((0,475))
chao_sprite = pygame.image.load(novo["local_ground"]).convert_alpha()
chao_sprite = pygame.transform.scale(chao_sprite, (1280,245))
chao_sprite.blit(chao_sprite, pos_chao)


#Batata configs
tamanho_batata = (80,90)
pos_batata = ((640, 515))
batata_sprite1 = pygame.image.load(novo["local_potatoSprite1"]).convert_alpha()
batata_sprite1 = pygame.transform.scale(batata_sprite1, tamanho_batata)
batata_sprite2 = pygame.image.load(novo["local_potatoSprite2"]).convert_alpha()
batata_sprite2 = pygame.transform.scale(batata_sprite2, tamanho_batata)
hit_batata = (80,90)
velocidade_batata = 10

#Music
musica_tudo = pygame.mixer.music.load(novo["local_musica"])
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(float(novo["volume_musica"]))

#Ups
ups_velocidade_bala = 5
ups_cadencia_bala = 5
ups_velocidade_batata = 5
ups_tempo_shield = 5
dollar_sprite = pygame.image.load(novo["local_dollar"]).convert_alpha()
dollar_sprite = pygame.transform.scale(dollar_sprite, (60,60))

frames = 0
frames_inimigo = 0
frames_escudo = 0
frames_dur_escudo = 0
liberado = True
atualplano = int(novo["plano_inicial"])
qualultimo = 0

def defineLimites():
	o = randrange(0,randomInimigo)
	if not o > 10:
		direcao_inimigo = direcao_inimigo * -1
	if pos_inimigo[0] < 10:
		direcao_inimigo = 1
	if pos_inimigo[0] > 1210:
		direcao_inimigo = -1
	if pos_inimigo[1] < 50:
		direcao_inimigoy = 1
	if pos_inimigo[1] > 200:
		direcao_inimigoy = -1

plano = pygame.image.load(novo["local_b1"]).convert()
while True:
	if not perdeu:
		#Executar a cada frame
		while True:
			#Presets
			clock.tick(int(novo["velocidade_fps"]))
			
			#Liberar tiro
			if not liberado:
				if frames >= tempo_sec:
					frames = 0
					liberado = True
				else:
					frames += 1
					liberado = False
					
			#Liberar escuro
			if not escudo_liberado:
				if frames_escudo >= delay_escudo:
					frames_escudo = 0
					escudo_liberado = True
				else:
					frames_escudo += 1
					escudo_liberado = False
					
			if escudo == True:
				if frames_dur_escudo >= tempo_dur_escudo:
					frames_dur_escudo = 0
					escudo = False
				else:
					frames_dur_escudo += 1
					escudo = True
				
			#Liberar Tiro inimigo
			if not liberado_inimigo:
				if frames_inimigo >= tempo_tiro_inimigo:
					frames_inimigo = 0
					liberado_inimigo = True
				else:
					c = randrange(1,500)
					if randrange(1,500) > sorte:
						frames_inimigo += 1
					else:
						frames_inimigo += 0.5
			
			#Mudar fundo
			if atualplano == 1 and qualultimo != 1:
				 plano = pygame.image.load(novo["local_b1"]).convert()
				 qualultimo = 1
			elif atualplano == 2 and qualultimo != 2:
				 plano = pygame.image.load(novo["local_b2"]).convert()
				 qualultimo = 2
			elif atualplano == 3 and qualultimo != 3:
				 plano = pygame.image.load(novo["local_b3"]).convert()
				 qualultimo = 3
			screen.blit(plano, (0,0))
			
			if vidas == 3:
				screen.blit(vidas_spriteVivo, pos_vidas[2])
				screen.blit(vidas_spriteVivo, pos_vidas[1])
				screen.blit(vidas_spriteVivo, pos_vidas[0])
			if vidas == 2:
				screen.blit(vidas_spriteMorto, pos_vidas[2])
				screen.blit(vidas_spriteVivo, pos_vidas[1])
				screen.blit(vidas_spriteVivo, pos_vidas[0])
			if vidas == 1:
				screen.blit(vidas_spriteMorto, pos_vidas[2])
				screen.blit(vidas_spriteMorto, pos_vidas[1])
				screen.blit(vidas_spriteVivo, pos_vidas[0])
			
			#Placar spawner
			textPlacar = str("Placar: "+str(placar))
			textoPress = fontePress.render((textPlacar), 1, ((255,0,0)))
			screen.blit(textoPress, (10,10))
			#Fase spawner
			textFase = str("Fase: "+str(fase))
			textoFase = fontePress.render((textFase), 1, ((255,255,255)))
			screen.blit(textoFase, (1000,10))
			#Creditos spawner
			textoCreditos =str(creditos)
			spawnCreditos = fontePress.render((textoCreditos), 1, ((210,105,30)))
			screen.blit(spawnCreditos, (330,10))
			screen.blit(dollar_sprite, (250,18))
			
			
			fonteUps = pygame.font.SysFont('Arial', 20)
			#Spawner ups
			#Velocidade tiro
			textup1 = str("[1] Velocidade Tiro "+str(5-ups_velocidade_bala))
			if ups_velocidade_bala == 0:
				textup1 = str("[1] Velocidade Tiro MAX")
				spawnTextup1 = fonteUps.render((textup1), 1, ((255,0,0)))
			else:
				spawnTextup1 = fonteUps.render((textup1), 1, ((0,0,0)))
			screen.blit(spawnTextup1, ((400,10)))
			
			#Velocidade batata
			textup1 = str("[2] Velocidade Batata "+str(5-ups_velocidade_batata))
			if ups_velocidade_batata == 0:
				textup1 = str("[2] Velocidade Batata MAX")
				spawnTextup1 = fonteUps.render((textup1), 1, ((255,0,0)))
			else:
				spawnTextup1 = fonteUps.render((textup1), 1, ((0,0,0)))
			screen.blit(spawnTextup1, ((400,30)))
			
			#Cadencia bala
			textup1 = str("[3] Cadencia Bala "+str(5-ups_cadencia_bala))
			if ups_cadencia_bala == 0:
				textup1 = str("[3] Cadencia Bala MAX")
				spawnTextup1 = fonteUps.render((textup1), 1, ((255,0,0)))
			else:
				spawnTextup1 = fonteUps.render((textup1), 1, ((0,0,0)))
			screen.blit(spawnTextup1, ((400,50)))
			
			#Delay escudo
			textup1 = str("[4] Delay Escudo "+str(5-ups_tempo_shield))
			if ups_tempo_shield == 0:
				textup1 = str("[4] Delay Escudo MAX")
				spawnTextup1 = fonteUps.render((textup1), 1, ((255,0,0)))
			else:
				spawnTextup1 = fonteUps.render((textup1), 1, ((0,0,0)))
			screen.blit(spawnTextup1, ((400,70)))
			#Comprar vida
			textup1 = str("[5] Comprar uma vida ")
			if vidas == 3:
				spawnTextup1 = fonteUps.render((textup1), 1, ((255,0,0)))
			else:
				spawnTextup1 = fonteUps.render((textup1), 1, ((0,0,0)))
			screen.blit(spawnTextup1, ((400,90)))
			
			#Events
			for event in pygame.event.get():
				if event.type == QUIT:
					continuar_jogo = False
					quit()
				if event.type == KEYDOWN:
					if event.key == K_UP and liberado:
						screen.blit(bala_desenho, pos_bala)
						balas.append((pos_bala))
						liberado = False
					if event.key == K_g:
						if atualplano == 1:
							atualplano = 3
						else:
							atualplano = atualplano - 1
					if event.key == K_h:
						if atualplano == 3:
							atualplano = 1
						else:
							atualplano += 1
					if event.key == K_ESCAPE:
						pygame.quit()
						quit()
					#ups
					if event.key == K_1:
						if creditos >= int(novo["custo_1"]) and ups_velocidade_bala != 0:
							ups_velocidade_bala -= 1
							velocidade_tiro += 1
							creditos -= 1
					if event.key == K_2:
						if creditos >= int(novo["custo_2"]) and ups_velocidade_batata != 0:
							ups_velocidade_batata -= 1
							velocidade_batata += 1
							creditos -= 1
					if event.key == K_3:
						if creditos >= int(novo["custo_3"]) and ups_cadencia_bala != 0:
							ups_cadencia_bala -= 1
							tempo_sec -= 5
							creditos -= 1
					if event.key == K_4:
						if creditos >= int(novo["custo_4"]) and ups_tempo_shield != 0:
							delay_escudo += 50
							ups_tempo_shield -= 1
							creditos -= 1
					if event.key == K_5:
						if creditos >= int(novo["custo_5"]) and vidas < 3 and vidas > 0:
							vidas += 1
							creditos -= 5
			#Escudo
					if event.key == K_DOWN and escudo_liberado and not escudo:
						escudo_liberado = False
						escudo = True
					else:
						if not escudo:
							tempo_sec = 35-5*(5-ups_cadencia_bala)
							velocidade_batata = 10+1*(5-ups_velocidade_batata)
							velocidade_tiro = 10+1*(5-ups_velocidade_bala)
							
			#Movimento Batata
			teclado = pygame.key.get_pressed()
			if teclado[K_RIGHT] and pos_batata[0] + velocidade_batata < 1210:
				pos_batata = ((pos_batata[0] + velocidade_batata, pos_batata[1]))
				if not paraLado == 1:
					paraLado = 1
			if teclado[K_LEFT] and pos_batata[0] - velocidade_batata > 10:
				pos_batata = ((pos_batata[0] - velocidade_batata, pos_batata[1]))
				if not paraLado == -1:
					paraLado = -1
					
			#Atirar a bala
			pos_bala = ((pos_batata[0] + 15, pos_batata[1] - 50))
			for i in balas:
				balas.remove(i)
				if i[1] < 50:
					break
				balas.append((i[0], i[1]-velocidade_tiro))
				screen.blit(bala_desenho, i)
				
			#limites inimigo
			defineLimites()
			
			
			#Inimigo mexer
			pos_inimigo = ((pos_inimigo[0] + velocidade_inimigo*direcao_inimigo, pos_inimigo[1]))
			pos_inimigo = ((pos_inimigo[0], pos_inimigo[1] + velocidade_inimigoy*direcao_inimigoy*2))
			screen.blit(inimigo_sprite, pos_inimigo)
			
			#Atirar Balas Inimigo
			if liberado_inimigo:
					liberado_inimigo = False
					bala_inimigo = [pos_inimigo[0]+30,pos_inimigo[1]+60]
			bala_inimigo[1] = bala_inimigo[1]+velocidade_bala_inimigo
			screen.blit(bala_inimigo_desenho, (bala_inimigo[0],bala_inimigo[1]))
			
			#Spawna tudo
			if paraLado == 1:
				screen.blit(batata_sprite2, pos_batata)
			if paraLado == -1:
				screen.blit(batata_sprite1, pos_batata)
			
			#Colisor bala>inimigo
			for j in balas:
				if j[0]-10 < pos_inimigo[0]+hit_inimigo[0] and j[0]+7 > pos_inimigo[0]-10 and j[1] < pos_inimigo[1]+hit_inimigo[1] and j[1] > pos_inimigo[1]-30:
					placar += 1
					balas.remove(j)
					if placar == 6:
						fase += 1
						creditos += 1
						placar = 0
						if randomInimigo > 1000:
							randomInimigo -= 100
						if velocidade_bala_inimigo < 90:
							velocidade_bala_inimigo += 1
						if tempo_tiro_inimigo > 40:
							tempo_tiro_inimigo -= 10
						if sorte >= 0:
							sorte -= 10
			
			#Colisor bala>batata
			if bala_inimigo[1] > pos_batata[1] and bala_inimigo[1] < pos_batata[1]+hit_batata[1] and bala_inimigo[0]+12 > pos_batata[0] and bala_inimigo[0]-12 < pos_batata[0]+hit_batata[0]:
				if not escudo:
					if vidas == 1:
						liberado = True
						liberado_inimigo = True
						pontos = fase*6+placar
						placar = 0
						fase = 0
						sorte = 300
						tempo_tiro_inimigo = 100
						velocidade_inimigo = 6
						velocidade_inimigoy = 3
						velocidade_bala_inimigo = 10
						tempo_tiro_inimigo = 100
						ups_velocidade_bala = 5
						ups_velocidade_batata = 5
						ups_tempo_shield = 5
						ups_cadencia_bala = 5
						delay_escudo = 600
						perdeu = True
						pos_batata = ((640, 515))
						vidas = 0
						creditos = int(novo["creditos_inicial"])
						bala_inimigo = [-120,-120]
						break
					elif vidas > 1:
						vidas -= 1
						bala_inimigo = [-120,-120]
				else:
					escudo = False
					bala_inimigo = [-120,-120]
					
			if escudo:
				screen.blit(escudo_sprite, (pos_batata[0]-10,pos_batata[1]-10))
				velocidade_batata = 5
				tempo_sec = 180
				velocidade_tiro = 5
			if novo["modo_teste"] == "True":
				velocidade_inimigo = 0
				velocidade_inimigoy = 0
				creditos = 1000
			#Spawn Objetos
			screen.blit(chao_sprite, pos_chao)
			pygame.display.update()
	else:
		screen.blit(plano, (0,0))
		fontePontuacao = pygame.font.SysFont('Arial', 100)
		fontePressione = pygame.font.SysFont('Arial', 50)
		textPerdeu = str("Pontuacao: "+str(pontos))
		textoPerdeu = fontePontuacao.render((textPerdeu), 1, ((255,255,255)))
		screen.blit(textoPerdeu, (200,200))
		textinAperteV = fontePressione.render(("Pressione 'v' para tentar novamente"), 1, ((0,0,0)))
		screen.blit(textinAperteV, (300, 350))
		pygame.display.update()
		abacate = 0
		balas = []
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
			if event.type == KEYDOWN:
				if event.key == K_v:
					abacate = 1
					perdeu = False
		if abacate == 1:
			vidas = 3
			continue
