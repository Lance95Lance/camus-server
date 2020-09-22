import os
from datetime import datetime
from random import randint

import cv2
import numpy as np
import PIL.Image as PImage
import logging
from PIL import ImageFont, ImageDraw
from camus.settings.base import BASE_ID_CARD_DIR, BASE_MEDIA_CARD_DIR

logger = logging.getLogger('camus.common')


class IdCardUtil:
    def __init__(self):
        pass

    # if getattr(sys, 'frozen', None):
    #     base_dir = os.path.join(sys._MEIPASS, 'usedres')
    # else:
    #     base_dir = os.path.join(os.path.dirname(__file__), 'usedres')

    def changeBackground(self, img, img_back, zoom_size, center):
        # 缩放
        img = cv2.resize(img, zoom_size)
        rows, cols, channels = img.shape

        # 转换hsv
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        # 获取mask
        # lower_blue = np.array([78, 43, 46])
        # upper_blue = np.array([110, 255, 255])
        diff = [5, 30, 30]
        gb = hsv[0, 0]
        lower_blue = np.array(gb - diff)
        upper_blue = np.array(gb + diff)
        mask = cv2.inRange(hsv, lower_blue, upper_blue)
        # cv2.imshow('Mask', mask)

        # 腐蚀膨胀
        erode = cv2.erode(mask, None, iterations=1)
        dilate = cv2.dilate(erode, None, iterations=1)

        # 粘贴
        for i in range(rows):
            for j in range(cols):
                if dilate[i, j] == 0:  # 0代表黑色的点
                    img_back[center[0] + i, center[1] + j] = img[i, j]  # 此处替换颜色，为BGR通道

        return img_back

    def paste(self, avatar, bg, zoom_size, center):
        avatar = cv2.resize(avatar, zoom_size)
        rows, cols, channels = avatar.shape
        for i in range(rows):
            for j in range(cols):
                bg[center[0] + i, center[1] + j] = avatar[i, j]
        return bg

    def generator(self, name, sex, nation, year, mon, day, addr, idn, org, life, ebgvar=True):
        logger.info(">>>>>>>开始生成身份证图片...")

        # 头像
        fname = os.path.join(BASE_ID_CARD_DIR, 'photo.jpg')
        # print fname
        im = PImage.open(os.path.join(BASE_ID_CARD_DIR, 'empty.png'))
        avatar = PImage.open(fname)  # 500x670

        name_font = ImageFont.truetype(os.path.join(BASE_ID_CARD_DIR, 'hei.ttf'), 72)
        other_font = ImageFont.truetype(os.path.join(BASE_ID_CARD_DIR, 'hei.ttf'), 60)
        bdate_font = ImageFont.truetype(os.path.join(BASE_ID_CARD_DIR, 'fzhei.ttf'), 60)
        id_font = ImageFont.truetype(os.path.join(BASE_ID_CARD_DIR, 'ocrb10bt.ttf'), 72)

        draw = ImageDraw.Draw(im)
        draw.text((630, 690), name, fill=(0, 0, 0), font=name_font)
        draw.text((630, 840), sex, fill=(0, 0, 0), font=other_font)
        draw.text((1030, 840), nation, fill=(0, 0, 0), font=other_font)
        draw.text((630, 980), year, fill=(0, 0, 0), font=bdate_font)
        draw.text((950, 980), mon, fill=(0, 0, 0), font=bdate_font)
        draw.text((1150, 980), day, fill=(0, 0, 0), font=bdate_font)
        start = 0
        loc = 1120
        while start + 11 < len(addr):
            draw.text((630, loc), addr[start:start + 11], fill=(0, 0, 0), font=other_font)
            start += 11
            loc += 100
        draw.text((630, loc), addr[start:], fill=(0, 0, 0), font=other_font)
        draw.text((950, 1475), idn, fill=(0, 0, 0), font=id_font)
        draw.text((1050, 2750), org, fill=(0, 0, 0), font=other_font)
        draw.text((1050, 2895), life, fill=(0, 0, 0), font=other_font)

        if ebgvar:
            avatar = cv2.cvtColor(np.asarray(avatar), cv2.COLOR_RGBA2BGRA)
            im = cv2.cvtColor(np.asarray(im), cv2.COLOR_RGBA2BGRA)
            im = self.changeBackground(avatar, im, (500, 670), (690, 1500))
            im = PImage.fromarray(cv2.cvtColor(im, cv2.COLOR_BGRA2RGBA))
        else:
            avatar = avatar.resize((500, 670))
            avatar = avatar.convert('RGBA')
            im.paste(avatar, (1500, 690), mask=avatar)
            # im = paste(avatar, im, (500, 670), (690, 1500))

        timestamp_random = datetime.now().strftime('%Y%m%d%H%M%S') + str(
            randint(10000, 99999))
        path = os.path.join(BASE_MEDIA_CARD_DIR, f'{timestamp_random}.png')

        im.save(path)

        # 转换黑白
        # im.convert('L').save('bw.png')

        logger.info(f'身份证图片生成成功: {timestamp_random}.png')

        return True, f'{timestamp_random}.png'


if __name__ == '__main__':
    IdCardUtil().generator(
        '张三', '男', '汉', '2001', '5', '4', '世纪大道1168号', '320102200105049804',
        '123', '123'
    )
