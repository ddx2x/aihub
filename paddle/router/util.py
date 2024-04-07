from PIL import Image, ImageEnhance
import os
def resize_photo(photo, choice):
    if choice == 1:
        # 1寸照片，尺寸调整为295x413
        resized_photo = photo.resize((295, 413))
    elif choice == 2:
        # 2寸照片，尺寸调整为413x626
        resized_photo = photo.resize((413, 626))
    elif choice == 3:
        # 小2寸照片，尺寸调整为260x378
        resized_photo = photo.resize((260, 378))
    else:
        return photo  # 如果选择不是 1, 2 或 3，则返回原图

    # 增强图片锐度
    enhancer = ImageEnhance.Sharpness(resized_photo)
    resized_photo = enhancer.enhance(2)
    return resized_photo

def cut_photo(photo, choice):
    width, height = photo.size
    if choice == 1:
        target_aspect = 295 / 413
    elif choice == 2:
        target_aspect = 413 / 626
    elif choice == 3:
        target_aspect = 260 / 378
    else:
        return photo  # 如果选择不是 1, 2 或 3，则返回原图

    # 根据目标尺寸裁剪图片
    photo_aspect = width / height
    if photo_aspect > target_aspect:
        # 图片过宽
        new_width = int(target_aspect * height)
        x = (width - new_width) / 2
        y = 0
    else:
        # 图片过高
        new_height = int(width / target_aspect)
        x = 0
        y = (height - new_height) / 2

    cutted_photo = photo.crop((x, y, x + (new_width if photo_aspect > target_aspect else width),
                               y + (new_height if photo_aspect <= target_aspect else height)))
    return cutted_photo




def idPhoto(photo, choice):
    if choice==1:
        print(os.path.abspath(__file__))
        photo_1 = resize_photo(cut_photo(photo, 1), 1)
        print_bg = Image.open('img/295-413.png')
        print_bg.paste(photo_1, (120, 180))
        print_bg.paste(photo_1, (435, 180))
        print_bg.paste(photo_1, (750, 180))
        print_bg.paste(photo_1, (1065, 180))
        print_bg.paste(photo_1, (1380, 180))
        print_bg.paste(photo_1, (120, 613))
        print_bg.paste(photo_1, (435, 613))
        print_bg.paste(photo_1, (750, 613))
        print_bg.paste(photo_1, (1065, 613))
        print_bg.paste(photo_1, (1380, 613))
        return print_bg
    if choice==2:
        photo_2 = resize_photo(cut_photo(photo, 2), 2)
        rotated_photo = photo_2.rotate(-90, expand=True)
        twoInch = Image.open('img/626-413.png')
        # 定义小二寸照片的起始坐标和间隔
        space_x = 386
        space_y = 55
        start_x = 647 - space_x
        start_y = 234 - space_y
        # 计算每张照片的横坐标
        x_coords_small2inch = [start_x + i * (260 + space_x) for i in range(2)]
        # 粘贴第一行的小二寸照片
        for x in x_coords_small2inch:
            twoInch.paste(rotated_photo, (x, start_y))
        # 粘贴第二行的小二寸照片
        second_row_y_small2inch = start_y + 378 + space_y
        for x in x_coords_small2inch:
            twoInch.paste(rotated_photo, (x, second_row_y_small2inch))
        return twoInch

    if choice==3:
        photo_3 = resize_photo(cut_photo(photo, 3), 3)

        print_bg_small2inch = Image.open('img/260-378.png')
        # 定义小二寸照片的起始坐标和间隔
        space_x = 20
        space_y = 20
        start_x = 227 - space_x
        start_y = 234 - space_y
        # 计算每张照片的横坐标
        x_coords_small2inch = [start_x + i * (260 + space_x) for i in range(5)]
        # 粘贴第一行的小二寸照片
        for x in x_coords_small2inch:
            print_bg_small2inch.paste(photo_3, (x, start_y))
        # 粘贴第二行的小二寸照片
        second_row_y_small2inch = start_y + 378 + space_y
        for x in x_coords_small2inch:
            print_bg_small2inch.paste(photo_3, (x, second_row_y_small2inch))
        return print_bg_small2inch


