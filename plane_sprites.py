"""
    1.  游戏子程序:
        1)  封装游戏中 所有 需要使用的 精灵子类
        2)  提供游戏的 相关工具

    2.  如果一个类的父类不是 object
        在重写初始化方法时,一定要先 super() 一下父类的 __init 方法
        从而保证父类中实现的 __init__ 代码能够被正常执行

    3.  精灵:
        1)  封装图像 image 、位置 rect 和速度 speed
        2)  提供 update() 方法,根据游戏需求,更新位置 rect

    4.  精灵组:
        1)  包含多个精灵对象
        2)  update 方法,让精灵组中所有的精灵调用 update 方法更新位置
        3)  draw(screen) 方法,在screen上绘制精灵组中所有的精灵
"""

import random
import pygame

# 屏幕大小常量: 字母大写,且之间用下划线连接
SCREEN_RECT = pygame.Rect(0, 0, 480, 700)
# 刷新的帧率
FRAME_PER_SEC = 60
# 创建敌机的定时器常量
# pygame 提供了 USEREVENT 常量
# 为了更好理解常量,所以重新定义了一个
CREATE_ENEMY_EVENT = pygame.USEREVENT
# 英雄发射子弹事件
HERO_FIRE_EVENT = pygame.USEREVENT + 1


class GameSprite(pygame.sprite.Sprite):
    """ 飞机大战游戏精灵 """

    def __init__(self, image_name, speed=1):

        # 调用父类的初始化方法
        super().__init__()

        # 定义对象的属性
        self.image = pygame.image.load(image_name)
        self.rect = self.image.get_rect()
        self.speed = speed

    def update(self):

        # 在屏幕垂直方向上移动
        self.rect.y += self.speed


class Background(GameSprite):
    """ 游戏背景精灵 """

    def __init__(self, is_alt=False):

        # 1. 调用父类方法实现精灵的创建(image/rect/speed)
        super().__init__("./images/background.png")

        # 2. 判断是否是交替图像,如果是,需要设置初始位置
        if is_alt:
            self.rect.y = -self.rect.height

    def update(self):
        # 1. 调用父类方法实现
        super().update()

        # 2. 判断是否移出屏幕,如果移出屏幕,将图像设置到图像上方
        if self.rect.y >= SCREEN_RECT.height:
            self.rect.y = -self.rect.height


class Enemy(GameSprite):
    """ 敌机精灵 """

    def __init__(self):

        # 1. 调用父类方法,创建敌机精灵,同时指定敌机图片
        super().__init__("./images/enemy0.png")

        # 2. 指定敌机的初始随机速度
        self.speed = random.randint(1, 3)

        # 实现飞机从屏幕上方慢慢进入效果
        self.rect.y = -self.rect.height

        # 3. 指定敌机的初始随机位置
        self.rect.x = random.randint(0, 8) * 51

    def update(self):
        # 1.调用父类方法,保持垂直方向飞行
        super().update()
        # 2.判断是否飞出屏幕,如果是,需要从精灵组中删除敌机
        if self.rect.y >= SCREEN_RECT.height:
            print("飞出屏幕,需要从精灵组删除...")

            # 将精灵从精灵组移出,一旦移出,精灵就会被自动销毁
            self.kill()

    # 对象被删除后,会自动调用的内置方法
    def __del__(self):
        print("敌机挂了 %s" % self.rect)


class Hero(GameSprite):
    """ 英雄精灵 """

    def __init__(self):

        # 1. 调用父类方法,设置 image 和 speed
        super().__init__("./images/hero.gif", 0)

        # 2. 设置英雄初始位置
        # 设置 飞机 在屏幕水平方向中央
        self.rect.centerx = SCREEN_RECT.centerx
        # 设置 飞机距离底部 120
        # bottom是图像底部的坐标     y =bottom - height
        self.rect.bottom = SCREEN_RECT.bottom - 120

        # 创建子弹的精灵组
        self.bullets = pygame.sprite.Group()

    def update(self):
        # 英雄在水平方向移动
        self.rect.x += self.speed

        # 控制英雄不能移出屏幕
        if self.rect.x < 0:
            self.rect.x = 0

        elif self.rect.right > SCREEN_RECT.right:
            self.rect.right = SCREEN_RECT.right

    def fire(self):
        print("发射子弹")

        for i in (0, 1, 2):
            # 1. 创建子弹精灵
            bullet = Bullet()

            # 2. 设置精灵位置
            bullet.rect.bottom = self.rect.y - 20*i
            bullet.rect.centerx = self.rect.centerx

            # 3. 将精灵添加到精灵组
            self.bullets.add(bullet)


class Bullet(GameSprite):
    """ 子弹精灵 """

    def __init__(self):

        # 调用父类方法,设置子弹图片,设置子弹速度
        super().__init__("./images/bullet1.png", -3)

    def update(self):

        # 调用父类方法,让子弹沿垂直方向飞行
        super().update()

        # 判断子弹是否飞出屏幕
        if self.rect.bottom < 0:
            # 将精灵从精灵组中删除
            self.kill()

    def __del__(self):
        # 对象被删除前自动执行的动作
        print("子弹被销毁")
