#Импортирование библиотек
import time
from sprite import *

#Создание функции, отвечающий за диалоги
def dialogue_mode(sprite, text):
    #Обновление
    sprite.update()

    #отрисовка
    screen.blit(space, (0, 0))
    screen.blit(sprite.image, sprite.rect)

    #рендер текста
    text1 = f1.render(text[text_number], True, pg.Color("white"))

    #отрисовка текста
    screen.blit(text1, (280, 450))

    #отрисовка второй строчки текста
    if text_number < len(text) - 1:
        text2 = f1.render(text[text_number + 1], True, pg.Color("white"))
        screen.blit(text2, (280, 470))

#иницилизация библиотек
pg.init()
pg.mixer.init()

#переменая отвечающая за размер окна
size = (800, 600)

#установка размера окна
screen = pg.display.set_mode(size)

#добавление названия окна
pg.display.set_caption("Космические коты")

#пременная хранящая количество кадров
FPS = 120
clock = pg.time.Clock()

#переменная для продолжения цикла
is_running = True

#режим игры
mode = "start_scene"

#создание групп спрайтов
meteorites = pg.sprite.Group()
mice = pg.sprite.Group()
lasers = pg.sprite.Group()

#создание спрайтов
captain = Captain()
alien = Alien()
starship = Starship()

#загрузка фона и его трансформация
space = pg.image.load("space.png").convert()
space = pg.transform.scale(space, size).convert_alpha()

#загрузка сердца и его трансформация
heart = pg.image.load("heart.png")
heart = pg.transform.scale(heart, (30, 30)).convert_alpha()

#пременная хранящая количество сердец
heart_count = 3

#списоки хранящие фразы
start_text = ["Мы засекли сигнал с планеты Мур.",
              "",
              "Наши друзья, инопланетные коты,",
              "нуждаются в помощи.",
              "Космические мыши хотят съесть их луну,",
              "потому что она похожа на сыр.",
              "Как долго наш народ страдал от них, ",
              "теперь и муряне в беде...",
              "Мы должны помочь им.",
              "Вылетаем прямо сейчас.",
              "Спасибо, что починил звездолёт, штурман. ",
              "Наконец-то функция автопилота работает.",
              "Поехали!"]

alien_text = ["СПАСИТЕ! МЫ ЕЛЕ ДЕРЖИМСЯ!",
              "",
              "Мыши уже начали грызть луну...",
              "Скоро куски луны будут падать на нас.",
              "Спасите муриан!", ]

final_text = ["Огромное вам спасибо,",
              "друзья с планеты Мяу!",
              "Как вас называть? Мяуанцы? Мяуриане?",
              "В любом случае, ",
              "теперь наша планета спасена!",
              "Мы хотим отблагодарить вас.",
              "Капитан Василий и его штурман получают",
              "орден Визита.",
              "А также несколько бутылок нашей",
              "лучшей валерьянки.",
              "",
              ""]

text_number = 0

#шрифт
f1 = pg.font.Font("FRACTAL.otf", 25)

#загрузка, настройка и запуск музыки
pg.mixer.music.load("Tense Intro.wav")
pg.mixer.music.set_volume(0.2)
pg.mixer.music.play()

#загрузка звуков
laser_sound = pg.mixer.Sound("11377 ice cannon shot.wav")
win_sound = pg.mixer.Sound("Victory Screen Appear 01.wav")

#основной цикл игры
while is_running:

    # СОБЫТИЯ
    for event in pg.event.get():
        #прекращение цикла игры по нажатию на крестик
        if event.type == pg.QUIT:
            is_running = False
        #пролистование диалогов
        if event.type == pg.KEYDOWN:
            if mode == "start_scene":
                text_number += 2
                if text_number > len(start_text):
                    mode = "meteorites"
                    text_number = 0
                    start_time = time.time()
            if mode == "alien_scene":
                text_number += 2
                if text_number > len(alien_text):
                    mode = "moon"
                    starship.switch_mode()
                    text_number = 0
                    start_time = time.time()
            if mode == "moon":
                #добавление и отрисовка лазеров
                if event.key == pg.K_SPACE:
                    lasers.add(Laser(starship.rect.midtop))
                    laser_sound.play()
            if mode == "final_scene":
                text_number += 2
                if text_number >= len(final_text):
                    mode = "end"
                    text_number = 0
                    start_time = time.time()
                    is_running = False

    if mode == "start_scene":
        #добавление диалога
        dialogue_mode(captain, start_text)

    if mode == "meteorites":
        #установка таймера для игры 1
        if time.time() - start_time > 20.0:
            mode = "alien_scene"

        #установка кол-во метеоритов
        if random.randint(1, 30) == 1:
            meteorites.add(Meteorite())

        #обновление спрайтов
        starship.update()
        meteorites.update()

        #сталкивания корабля и метеоритов
        hits = pg.sprite.spritecollide(starship, meteorites, True)
        for hit in hits:
            heart_count -= 1
            if heart_count <= 0:
                is_running = False

        # ОТРИСОВКA
        screen.blit(space, (0, 0))
        screen.blit(starship.image, starship.rect)
        meteorites.draw(screen)
        for i in range(heart_count):
            screen.blit(heart, (i * 30, 0))


    if mode == "alien_scene":
        #добавление диалога
        dialogue_mode(alien, alien_text)

    if mode == "moon":
        #установка таймера для игры 2
        if time.time() - start_time > 20.0:
            mode = "final_scene"

            #плавное завершение музыки
            pg.mixer.music.fadeout(3)

            #проигрование звука
            win_sound.play()

        if random.randint(1, 30) == 1:
            mice.add(Mouse_starship())

        starship.update()
        mice.update()
        lasers.update()

        hits = pg.sprite.spritecollide(starship, mice, True)
        for hit in hits:
            heart_count -= 1
            if heart_count <= 0:
                is_running = False

        hits = pg.sprite.groupcollide(lasers, mice, True, True)

        #отрисовка
        screen.blit(space, (0, 0))
        screen.blit(starship.image, starship.rect)
        mice.draw(screen)
        lasers.draw(screen)

        for i in range(heart_count):
            screen.blit(heart, (i * 30, 0))

    if mode == "final_scene":
        #добавление диалога
        dialogue_mode(alien, final_text)


    pg.display.flip()

    #добавление кол-во кадров
    clock.tick(FPS)
