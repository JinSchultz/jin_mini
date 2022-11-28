# -*- coding: utf-8 -*-
import json
import requests
import math
from PIL import Image,ImageFont,ImageDraw
import numpy as np
import uuid
# 16进制颜色格式颜色转换为RGB格式

def Hex_to_RGBA(hex):
    r = int(hex[1:3],16)
    g = int(hex[3:5],16)
    b = int(hex[5:7], 16)
    rgba = [r,g,b,255]
    return tuple(rgba)

bg_conf = {
    'rgba':tuple([255,255,255,0])
}
def CreateMutiLinesPic(text):
    margin=10

    line_size = int(math.sqrt(len(text)))
    line_count=math.ceil(len(text)/line_size)
    # pic_size=[margin*2+fwidth+owidth,margin*2+(fheight+oheight)*line_count]
    pic_size = [400,400]
    font_size = pic_size[0]//line_size-margin
    # create new picture
    pic = Image.new('RGBA', pic_size,bg_conf['rgba'])
    draw = ImageDraw.Draw(pic)
    font = ImageFont.truetype('方正粗黑宋简体.TTF',font_size)
    f_weight,f_height = draw.textsize('中',font)
    pic_size[1] = f_height*line_count+margin*2
    pic = Image.new('RGBA', pic_size,bg_conf['rgba'])
    draw = ImageDraw.Draw(pic)
   # font_size = find_font_size(text,font_conf['type'],pic,width_ratio)
    fwidth,fheight = font.getsize('中'*line_size)
    # owidth,oheight = font.getoffset('中'*line_size) 

    for i in range(line_count):
        # draw lines
        draw.text((margin,(fheight)*i), text[i*line_size:(i+1)*line_size], tuple([1,1,1,1]), font,)
                    # stroke_width=5,stroke_fill='black')
        draw.text((margin,(fheight)*i), text[i*line_size:(i+1)*line_size], tuple([1,1,1,1]), font,)
                    # stroke_width=5,stroke_fill='black')
    return np.array(pic,dtype=np.uint8)

def draw_back(width,height,c_from,c_to):
    if c_from==c_to:
        pic = Image.new(mode = 'RGBA',size = (height,width),color = Hex_to_RGBA(c_from))
        draw = ImageDraw.Draw(pic)
        return np.array(pic,np.uint8)
    bg_1 = Hex_to_RGBA(c_from)
    bg_2 = Hex_to_RGBA(c_to)
    pic = Image.new(mode = 'RGBA',size = (height,width),color = 'white')
    draw = ImageDraw.Draw(pic)
    step_r = (bg_2[0] - bg_1[0]) / 500
    step_g = (bg_2[1] - bg_1[1]) / 500
    step_b = (bg_2[2] - bg_1[2]) / 500
    for y in range(0,height+1):
        bg_r = round(bg_1[0] + step_r * y)
        bg_g = round(bg_1[1] + step_g * y)
        bg_b = round(bg_1[2] + step_b * y)
        for x in range(0,height):
            draw.point((x,y),fill = (bg_r,bg_g,bg_b,255))
    return np.array(pic,dtype=np.uint8)

text='草'


def get_word_by_pic(text,pic):
    words = CreateMutiLinesPic(text)
    wid = words.shape[1]
    hei = words.shape[0]
    back = Image.open(pic).resize((wid,hei))
    new_ = words * back
    im = Image.fromarray(new_)
    return  im


def get_word_by_gradient(text,c_from,c_to):
    words = CreateMutiLinesPic(text)
    wid = words.shape[0]
    hei = words.shape[1]
    back = draw_back(wid,hei,c_from,c_to)
    new_ = words * back
    im = Image.fromarray(new_)
    return im

def get_word_by_custom(text,arr):
    words = CreateMutiLinesPic(text)
    wid = words.shape[1]
    hei = words.shape[0]
    back = Image.fromarray(arr).resize((wid,hei))
    new_ = words * back
    im = Image.fromarray(new_)
    return im

def words_to_gif(text,conf):
    frames = []
    if conf is None:
        return ''
    if conf['type'] == 1:
        word = get_word_by_gradient(text,conf['c_from'],conf['c_to'])
        file_name = hash(text+conf['c_from']+conf['c_to'])
    elif conf['type'] == 2:
        word = get_word_by_pic(text,conf['img'])
        file_name = hash(text+conf['img'].split('/')[-1])
    else:
        word = get_word_by_custom(text,conf['arr'])
        file_name = uuid.uuid1().hex
    
    star = Image.open('wxcloudrun/img/star1.png').resize((word.width,word.height))
    
    for i in range(5):
        star = star.rotate(45*i)
        out = Image.alpha_composite(word,star)
        out = np.array(out)
        black_pixels = np.where(
            (out[:, :, 0] == 0) & 
            (out[:, :, 1] == 0) & 
            (out[:, :, 2] == 0))
        out[black_pixels] = [255, 255, 255,255]
        out = Image.fromarray(out)
        frames.append(out)
    frames[0].save('gif/'+str(file_name)+'.gif',save_all=True,append_images=frames[1:],duration=200,loop=0,disposal=2)
    return 'gif/'+str(file_name)+'.gif'
# conf1 = {'type':1,'c_from':'#f2c3c8','c_to':'#942632'}
# conf2 = {'type':2,'img':'wxcloudrun/img/g.png'}
# conf3 = {'type':3,'url':'https://s1.aigei.com/src/img/png/47/47c61edadb5b49d1acc48167443efe41.png?imageMogr2/auto-orient/thumbnail/!99x132r/gravity/Center/crop/99x132/quality/85/%7Cwatermark/3/image/aHR0cHM6Ly9zMS5haWdlaS5jb20vd2F0ZXJtYXJrLzYwLTIucG5nP2U9MTczNTQ4ODAwMCZ0b2tlbj1QN1MyWHB6ZnoxMXZBa0FTTFRrZkhON0Z3LW9PWkJlY3FlSmF4eXBMOnpYaVVCU1Y3SmNxRUUtUTZmTkdGOHVLZ3l2bz0=/dissolve/20/gravity/NorthWest/dx/32/dy/64/ws/0.0/wst/0&e=1735488000&token=P7S2Xpzfz11vAkASLTkfHN7Fw-oOZBecqeJaxypL:Bd_4vzfGPn1TN0Z0gcJ8gcDmvCg='}
# im_b = words_to_gif(text,conf3)

def upload(filepath):
    #获取token
    response = requests.get('https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=wx484701511103dbf8&secret=8ab936eeccce423e034949485ea7fe61',)
    data ={
        "env": "prod-5gncem3b66a1ee31",
        "path": filepath
    }#需填入env和path
    #转json
    data = json.dumps(data)
    response = requests.post("https://api.weixin.qq.com/tcb/uploadfile?access_token="+response.json()['access_token'],data)

    data2={
        "Content-Type":(None,".jpg"), #此处为上传文件类型
        "key": (None,filepath), #需填入path
        "Signature": (None,response.json()['authorization']),
        'x-cos-security-token': (None,response.json()['token']),
        'x-cos-meta-fileid': (None,response.json()['cos_file_id']),
        'file': ('filename.jpg',open(filepath,"rb")) #需填入本地文件路径
        }
    response2 = requests.post(response.json()['url'], files=data2) #此处files提交的为表单数据，不为json数据，json数据或其他数据会报错

    return response.json()['url']

# a = upload("gif/-505346995794605208.gif")
# print(a)