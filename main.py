import subprocess
from numpy.core.fromnumeric import size
import time
import numpy as np
import sys
import cv2 as cv
print("Installing extra Libraries")
subprocess.check_call([sys.executable, '-m', 'pip', 'install',
                       'keyboard'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install',
                       'Pillow'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install',
                       'pyserial'])
print('Succesfully installed')
from PIL import ImageGrab
import serial
import keyboard

time_threshold = 0.5  # global space time variable
colour = (0, 0, 0)  # global colour variable
cursour_colour = (255, 255, 255)  # global cursor colour varialble
cnt = 0  # used to keep save count
btn = 1  # global button value
num_line = 1  # fot out pallet
nm_line = 1  # for final image
in_break=1
occupied_pixels = [0, 0]  # global; values of pixels which are used in output panel
occu_pixels_final = [0, 0]
text_size = 2  # global text size variable
try:
    ser = serial.Serial('COM4', 9600, timeout=1)
except:
    print('Device not connected')
x = 100
y = 300
clr = 0
cl = 0

prevx, prevy = 100, 300

bounding_coordinates = [99999, 99999, 0, 0]


def vconcat_resize_min(im_list, interpolation=cv.INTER_CUBIC):
    w_min = min(im.shape[1] for im in im_list)
    im_list_resize = [cv.resize(im, (w_min, int(im.shape[0] * w_min / im.shape[1])), interpolation=interpolation)
                      for im in im_list]
    return cv.vconcat(im_list_resize)


def handel_key_press():
    global colour, cnt, text_size, time_threshold, img_out, prevy, prevx, x, y, occu_pixels_final, nm_line, num_line, bounding_coordinates, occupied_pixels, img_out_palette, img_final_out, in_break
    try:
        if keyboard.is_pressed('1'):
            print('You Pressed Red!')
            colour = (0, 0, 255)
        elif keyboard.is_pressed('2'):
            print('You Pressed Blue!')
            colour = (255, 0, 0)
        elif keyboard.is_pressed('3'):
            print('You Pressed Green!')
            colour = (0, 255, 0)
        elif keyboard.is_pressed('4'):
            print('You Pressed Yellow!')
            colour = (0, 255, 255)
        elif keyboard.is_pressed('5'):
            print('You Pressed Pink!')
            colour = (221, 218, 250)
        elif keyboard.is_pressed('6'):
            print('You Pressed Grey!')
            colour = (128, 128, 128)
        elif keyboard.is_pressed('7'):
            print('You Pressed Brown!')
            colour = (0, 75, 175)
        elif keyboard.is_pressed('8'):
            print('You Pressed Black!')
            colour = (0, 0, 0)
        elif keyboard.is_pressed('9'):
            print('You Pressed Purple!')
            colour = (128, 0, 128)
        elif keyboard.is_pressed('s'):
            print('You Pressed Save!')
            screen = np.array(ImageGrab.grab(bbox=(0, 200, 1050, 1050)))
            cnt += 1
            prevx = 100
            prevy = 300
            name = 'image_' + str(cnt) + '.png'
            cv.imwrite('Save/' + name, screen)
        elif keyboard.is_pressed('d'):
            img_out = cv.resize(cv.imread('resource/main_plt.png'), (1050, 600))
            img_out = cv.line(img_out, (50, 300), (1000, 300), (255, 0, 255), 1)
            prevx = 100
            prevy = 300
            x = 100
            bounding_coordinates = [99999, 99999, 0, 0]
            y = 300
            print('You Pressed Delete!')
        elif keyboard.is_pressed('+'):
            print('You Pressed +')
            text_size = text_size + 0.01
        elif keyboard.is_pressed('-'):
            print('You Pressed -')
            text_size = text_size - 0.01
        elif keyboard.is_pressed('/'):
            print('You Pressed time increase')
            time_threshold += 0.1
        elif keyboard.is_pressed('*'):
            print('You Pressed time decrase')
            time_threshold -= 0.1
        elif keyboard.is_pressed('q'):
            print('You Pressed quit')
            img_final_out= img_final_out[0:nm_line*50,:,:]
            cv.imwrite('Save/Final_out.png', img_final_out)
            in_break=0
            sys.exit()
        elif keyboard.is_pressed('r'):
            print('You Pressed reset')
            img_out = cv.resize(cv.imread('resource/main_plt.png'), (1050, 600))
            img_out = cv.line(img_out, (50, 300), (1000, 300), (255, 0, 255), 1)
            prevx = 100
            prevy = 300
            x = 100
            bounding_coordinates = [99999, 99999, 0, 0]
            num_line = 1
            img_out_palette = cv.resize(cv.imread('resource/img_plt_out.png'), (1050, 150))
            img_final_out = np.ones((1100, 4000, 3)) * 255
            occupied_pixels = [0, 0]
            occu_pixels_final = [0, 0]
            nm_line = 1
            y = 300
    except:
        print('nothing pressed')


def get_input():
    global tm_list
    try:
        text = ser.readline()
        var = time.time()
    except:
        text = ''
        print('No input recieved exiting')
    for word in text.split():
        if word.isdigit():
            tm_list.append(int(word))


def crop_image():
    global prevx, prevy, chk_time, cheked_time, bounding_coordinates, occupied_pixels, num_line, x, y, ranges, img_final_out, nm_line, occu_pixels_final
    print('prev pixels', occupied_pixels)
    print('soi', ranges)

    img_out_palette[(occupied_pixels[0] + 5):(occupied_pixels[0] + 5 + ranges[0]), occupied_pixels[1]+5:(ranges[1] + 5+occupied_pixels[1]), :] = im_tmp_out
    occupied_pixels = [(num_line - 1) * 50, occupied_pixels[1] + ranges[1] + 5]
    occu_pixels_final = [(nm_line - 1) * 50, occupied_pixels[1] + ranges[1] + 5]
    print('giving space')
    img_out[bounding_coordinates[1] - 15:bounding_coordinates[2] + 15, bounding_coordinates[0] - 10:bounding_coordinates[3] + 15, :] = 255
    img_final_out[(occu_pixels_final[0] + 5):(occu_pixels_final[0] + 5 + ranges[0]),  occu_pixels_final[1]+5:(ranges[1] + 5+occu_pixels_final[1]), :] = im_tmp_out
    x += 30
    y = 300

    prevx=x
    prevy=y

    bounding_coordinates[0] = x
    bounding_coordinates[1] = 99999
    bounding_coordinates[2] = 0
    bounding_coordinates[3] = x
    cheked_time = 0
    chk_time = 0


pallete = cv.resize(cv.imread('resource/plt.png'), (150, 755))
clr = cv.resize(cv.imread('resource/current_colour.png'), (150, 50))
instructions = cv.resize(cv.imread('resource/instructions.png'), (1050, 50))
img_out = cv.resize(cv.imread('resource/main_plt.png'), (1050, 600))
img_out = cv.line(img_out, (50, 300), (1000, 300), (255, 0, 255), 1)
img_out_palette = cv.resize(cv.imread('resource/img_plt_out.png'), (1050, 150))
img_pad1 = cv.resize(cv.imread('resource/padding_colour.png'), (1050, 5))
img_pad2 = cv.resize(cv.imread('resource/padding_colour.png'), (1215, 5))
img_pad3 = cv.resize(cv.imread('resource/padding_colour.png'), (5, 810))
img_final_out = np.ones((1100, 4000, 3)) * 255
img_pad4 = cv.resize(cv.imread('resource/padding_colour.png'), (150, 5))

chk_time = 0
cheked_time = 0

while True and in_break==1:
    var = time.time()
    try:
        text = ser.readline()
        var = time.time()
    except:
        text = ''
        print('No input recieved exiting')
        break

    if btn:
        img_out = cv.circle(img_out, (prevx, prevy), 1, (0,0,0), 1)


    numbers = []
    tm_list = []
    im_v_resize = vconcat_resize_min([clr, img_pad4, pallete])
    im_v_resize = cv.hconcat([img_pad3, im_v_resize, img_pad3])
    img_concat = vconcat_resize_min([instructions, img_pad1, img_out_palette, img_pad1, img_out])
    img_concat = cv.hconcat([img_pad3, img_concat])
    img_final = cv.hconcat([img_concat, im_v_resize])
    img_final = cv.vconcat([img_final, img_pad2])
    cv.imshow('Smart Pen', img_final)
    handel_key_press()
    clr[:, :, 0] = colour[0]
    clr[:, :, 1] = colour[1]
    clr[:, :, 2] = colour[2]
    for word in text.split():
        if word.isdigit():
            numbers.append(int(word))
    try:
        numbers[0] -= 128
        numbers[1] -= 128
    except:
        print('Pen not activated')

    if numbers[2] == 111:
        print('clear')

        if cl == 3:
            btn = not btn
            if (not btn):
                print('pen up')
            else:
                print('pen down')
            cl = 0

        cl += 1

    var1 = time.time() - var
    x += int(var1 * numbers[0] * 30)
    y -= int(var1 * numbers[1] * 20)

    img_out = cv.circle(img_out, (x, y), 1, (255, 255, 255))
    bounding_coordinates[0] = min(bounding_coordinates[0], abs(x))
    bounding_coordinates[1] = min(bounding_coordinates[1], abs(y))
    bounding_coordinates[2] = max(bounding_coordinates[2], abs(y))
    bounding_coordinates[3] = max(bounding_coordinates[3], abs(x))
    # # code for giving space
    if numbers[0] == 0 and numbers[1] == 0:
        chk_time = 1
        print('detected 0 movement')
    else:
        chk_time = 0
        cheked_time = 0
    if (chk_time == 1 and cheked_time == 0):
        cheked_time = time.time()
        print('timer start')

    if (not (cheked_time == 0) and (time.time() - cheked_time > time_threshold)):
        print('timer exceeded')

        if (x == 100 and y == 300):
            cheked_time = 0
            chk_time = 0
            print("Cancelling timer due to origin")
        else:
            print('bounding bx', bounding_coordinates)
            print('x y', x, ' ', y)
            im = img_out[bounding_coordinates[1] - 15:bounding_coordinates[2] + 15,
                 bounding_coordinates[0] - 10:bounding_coordinates[3] + 15, :]
            im_tmp_out = cv.resize(im, ((bounding_coordinates[3] - bounding_coordinates[0] + 30) // 5, 40))
            ranges = im_tmp_out.shape
            print("shape of resized cutout = ", ranges)
            if ranges[1] >= 15:
                for i in range(ranges[0]):
                    for k in range(ranges[1]):
                        if  im_tmp_out[i, k, 1] == 0 :
                            im_tmp_out[i, k, 1] = 255
                if (1050 - occupied_pixels[1] - 10) >= 2 * ranges[1]:
                    print('occupied pix', occupied_pixels)
                    print('if 1')
                    crop_image()
                elif (not ((1050 - occupied_pixels[1] - 10) >= 2 * ranges[1])) and num_line == 1:
                    num_line += 1
                    print('nl')
                    nm_line += 1
                    occupied_pixels[1] = 0
                    occu_pixels_final[1] = 0
                    crop_image()
                elif (not ((1050 - occupied_pixels[1] - 10) >= 2 * ranges[1])) and num_line == 2:
                    print('Cleaning workspace and allocating')
                    num_line = 1
                    nm_line += 1
                    occupied_pixels = [0, 0]
                    occu_pixels_final[1] = 0
                    img_out_palette = cv.resize(cv.imread('resource/img_plt_out.png'), (1050, 150))
                    crop_image()
            else:
                print("cancelling timer due to very small character")
                cheked_time = 0
                chk_time = 0
    #####################################
    if x > 1000:
        x = 100
        img_out = cv.resize(cv.imread('resource/main_plt.png'), (1050, 600))
        img_out = cv.line(img_out, (50, 300), (1000, 300), (255, 0, 255), 1)
        prevx = 100
        prevy = 300
        bounding_coordinates = [99999, 99999, 0, 0]
        y = 300

    elif x < 0:
        x = 0


    if y > 600:
        y = 300
        img_out = cv.resize(cv.imread('resource/main_plt.png'), (1050, 600))
        img_out = cv.line(img_out, (50, 300), (1000, 300), (255, 0, 255), 1)
        prevx = 100
        prevy = 300
        x = 100
        bounding_coordinates = [99999, 99999, 0, 0]

    elif y < 0:
        y = 0


    if (btn):
        cv.line(img_out, (prevx, prevy), (x, y), colour, text_size)

    if not btn:
        #img_out = cv.circle(img_out, (prevx, prevy), 1, (0, 255, 0), 1)
    prevx = x
    prevy = y
    img_out = cv.line(img_out, (50, 300), (1000, 300), (255, 0, 255), 1)

    print(x, y)

    cv.waitKey(1)