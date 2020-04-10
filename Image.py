import pygame
import pathlib
import os
from pygame.locals import *


class LoadImage:
    # 画像データを格納するリスト
    image_list = None

    def __init__(self):
        self.image_list = {'title': pygame.image.load("res/title.png").convert()}
        folder_list = ['player', 'enemy', 'bg', 'item', 'block']

        # 画像データを読み込む
        for folder in folder_list:
            file_list = pathlib.Path(f'res/{folder}/').glob('*.png')

            for file in file_list:
                image_name = os.path.splitext(file.name)[0]
                image = pygame.image.load(f"res/{folder}/{file.name}").convert()
                if image_name == 'goal_pole':
                    image.set_colorkey((160, 180, 250), RLEACCEL)

                self.image_list[image_name] = image

        # 画像の透過
        for image in self.image_list.values():
            image.set_colorkey((153, 255, 255), RLEACCEL)

        LoadImage.image_list = self.image_list


class Sprite(pygame.sprite.Sprite):
    def __init__(self, screen, player, img_name, x, y, tweak_x=0, tweak_y=0):
        pygame.sprite.Sprite.__init__(self)

        # インスタンスオブジェクトを格納
        self.screen = screen
        self.player = player

        # 画像の読み込み
        self.name = img_name  # スプライトの名前
        self.image = LoadImage.image_list[img_name]

        # 画面内の座標
        self.x = x * 29 + tweak_x
        self.y = y * 29 - 12 + tweak_y

        # スプライトのサイズ
        self.width = self.image.get_width()
        self.height = self.image.get_height()

        # 初期位置に描画
        self.rect = Rect(int(self.x), int(self.y), self.width, self.height)
        screen.blit(self.image, self.rect)

    def update(self):
        # 画面スクロール
        if self.rect.left > -150:
            self.rect.left -= self.player.scroll
            # 画面内の領域のみ描画
            if self.rect.left < 480:
                self.screen.blit(self.image, self.rect)


class SpriteEnemy(Sprite):
    def __init__(self, screen, player, img_name, x, y, tweak_x=0, tweak_y=0):
        super().__init__(screen, player, img_name, x, y, tweak_x, tweak_y)

        # 画像を格納
        self.img_left = self.load_image()
        self.img_right = [pygame.transform.flip(img, True, False) for img in self.img_left]

        self.x_speed = 0.5  # 移動速度
        self.y_speed = 0.0  # 落下速度
        self.direction = 1  # 向き （1 or -1）

    # 画像の読み込み
    def load_image(self):
        img = [self.image]

        # 画像が複数ある場合はリストに追加
        if "1" in self.name:
            for i in range(1, 5):
                name = self.name[:-1] + str(i)
                if name in LoadImage.image_list:
                    img.append(LoadImage.image_list[name])
        return img

    def update(self, list_number=0):
        # 画面スクロール
        if self.rect.left > -150:
            self.rect.left -= self.player.scroll

            # 画面内の領域のみ描画
            if self.rect.left < 550:
                self.rect.left = round(self.x) - self.player.scroll_sum
                self.rect.top = round(self.y)

                # 向きによって画像を変更
                if self.direction == 1:
                    self.screen.blit(self.img_left[list_number], self.rect)
                else:
                    self.screen.blit(self.img_right[list_number], self.rect)