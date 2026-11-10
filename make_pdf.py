# -*- coding: utf-8 -*-
"""视频号视频内容整理报告 PDF 生成（PyMuPDF）"""
import fitz

W, H = 595, 842  # A4 pt
M = 50           # 边距

doc = fitz.open()
page = doc.new_page(width=W, height=H)
PAGES = [page]

def new_page():
    global page
    page = doc.new_page(width=W, height=H)
    page.insert_font(fontname="msyh", fontfile=r"C:\Windows\Fonts\msyh.ttc")
    page.insert_font(fontname="msyhbd", fontfile=r"C:\Windows\Fonts\msyhbd.ttc")
    PAGES.append(page)

def footer(p):
    p.draw_line(fitz.Point(M, H-40), fitz.Point(W-M, H-40), color=LINE, width=0.8)
    p.insert_text((M, H-24), "整理：小周末 · WorkBuddy | 生成时间：2026-11-10 | 成果已同步 GitHub 仓库",
                  fontsize=8.5, fontname="msyh", color=GRAY)

def ensure(y, need):
    """剩余空间不足则换页"""
    if y + need > H - 60:
        footer(page)
        new_page()
        return 70
    return y

# 注册中文黑体/宋体
page.insert_font(fontname="msyh", fontfile=r"C:\Windows\Fonts\msyh.ttc")
page.insert_font(fontname="msyhbd", fontfile=r"C:\Windows\Fonts\msyhbd.ttc")

INK = (0.13, 0.15, 0.18)
BLUE = (0.05, 0.35, 0.65)
GRAY = (0.45, 0.48, 0.52)
LINE = (0.8, 0.83, 0.87)

def text(x, y, s, size=10.5, font="msyh", color=INK):
    page.insert_text((x, y), s, fontsize=size, fontname=font, color=color)

FONT_OBJ = fitz.Font(fontfile=r"C:\Windows\Fonts\msyh.ttc")

def wrap(s, size, width, font="msyh"):
    lines, cur, w = [], "", 0
    for ch in s:
        cw = FONT_OBJ.text_length(ch, fontsize=size)
        if w + cw > width and cur:
            lines.append(cur); cur, w = ch, cw
        else:
            cur += ch; w += cw
    if cur: lines.append(cur)
    return lines

def para(x, y, s, size=10.5, width=None, lh=1.6, color=INK, font="msyh"):
    width = width or (W - 2*M)
    for ln in wrap(s, size, width, font):
        text(x, y, ln, size, font, color)
        y += size * lh
    return y

def section(y, title):
    y = ensure(y, 120)
    y += 10
    page.draw_line(fitz.Point(M, y), fitz.Point(W-M, y), color=LINE, width=0.8)
    y += 24
    text(M, y, title, 13.5, "msyhbd", BLUE)
    return y + 10

y = 0
# ===== 页眉 =====
page.draw_rect(fitz.Rect(0, 0, W, 64), color=None, fill=BLUE)
text(M, 38, "视频号视频内容整理报告", 20, "msyhbd", (1, 1, 1))
text(W-150, 26, "Report · 视频号分享页", 8.5, "msyh", (0.85, 0.9, 0.97))
text(W-150, 40, "https://weixin.qq.com/sph/AIMyt4qMff", 7.5, "msyh", (0.85, 0.9, 0.97))
y = 92

# ===== 一、视频基本信息 =====
y = section(y, "一、视频基本信息")
info = [
    ("视频标题", "2026哈市69中七年级上数学期中试卷解析"),
    ("话题标签", "#哈尔滨 #初中数学 #七年级 #期中 #试卷"),
    ("发布作者", "初高数学李盼（视频号）"),
    ("发布时间", "2026年11月6日"),
    ("视频链接", "https://weixin.qq.com/sph/AIMyt4qMff"),
    ("互动数据", "点赞 14 · 转发 90 · 喜欢 9 · 评论 7（截至抓取时）"),
    ("画面页数", "共 6 页（右下角页码指示 1/6）"),
]
tw = 80
for k, v in info:
    text(M+8, y+14, k, 10.5, "msyhbd", BLUE)
    yy = y + 14
    for ln in wrap(v, 10.5, W-2*M-tw-24):
        text(M+tw+8, yy, ln, 10.5)
        yy += 16.5
    page.draw_line(fitz.Point(M+8, yy+2), fitz.Point(W-M-8, yy+2), color=LINE, width=0.5)
    y = yy + 6

# ===== 二、封面关键画面 =====
y = section(y, "二、封面关键画面")
img_y = y + 4
img_h = 300
img_w = img_h * 698 / 922  # 保持比例
page.insert_image(fitz.Rect(M, img_y, M+img_w, img_y+img_h), filename=r"cover.png")
bx = M + img_w + 20
by = img_y + 6
desc = [
    "封面主体：蓝色大字横幅",
    "“26 哈市69中 七上数学期中”",
    "“试卷解析”，居中压在试卷图上。",
    "",
    "背景画面：试卷第 1 页扫描件，",
    "页眉带“李盼数学【微信 lipan1993924】”",
    "水印，卷面标题为“2026 哈西 69",
    "七上数学期中”。",
    "",
    "可见内容：选择题部分（每题 3 分，",
    "共 30 分），涉及有理数概念、",
    "近似数、单项式、去括号、正负数",
    "（算筹表示）等七年级上学期考点，",
    "卷面带红色手写批注答案。",
]
for ln in desc:
    text(bx, by, ln, 9.5, "msyh", (0.25, 0.28, 0.32))
    by += 15
y = img_y + img_h + 24

# ===== 三、内容概述 =====
y = section(y, "三、内容概述")
y = para(M, y+8,
    "该视频为初中数学教辅类解析视频：作者针对 2026 年哈尔滨市第 69 中学七年级上学期数学期中试卷，"
    "逐题讲解共 6 页试卷内容。封面显示为试卷第 1 页（选择题部分），讲解考点包括："
    "有理数的识别、近似数与精确度、单项式次数、整式去括号化简、用算筹/正负数表示意义等。"
    "视频形式为“静态试卷页面 + 语音讲解 + 手写标注”的常见解析风格。", size=10.5)
for ln_i in range(2): pass
y += 8
y = ensure(y, 60)
page.draw_rect(fitz.Rect(M, y, W-M, y+30), color=None, fill=(0.93, 0.96, 1.0))
text(M+10, y+20, "说明：以上概述基于封面帧画面、标题与话题标签整理；正片播放受微信登录限制，未能逐页截图。",
     9.5, "msyh", (0.2, 0.35, 0.55))
y += 42

# ===== 四、下载限制与替代方案 =====
y = section(y, "四、视频文件下载限制与替代方案")
y = para(M, y+8,
    "网页分享页仅提供“扫码前往微信观看”的受限预览：播放、视频流地址均需微信登录态与加密签名接口，"
    "因此无法在浏览器直接获取视频文件。可行的替代方案：", size=10.5)
alts = [
    "① 手机微信扫码观看后，使用手机录屏功能保存画面与声音；",
    "② 在电脑微信客户端打开该视频，配合本地抓包工具（如 GitHub 开源的 Fiddler / mitmproxy + WeChat 视频号解析脚本）截取视频流；",
    "③ 直接向作者“初高数学李盼”索取视频原文件或试卷电子版；",
    "④ 将原始视频文件发给小周末，可直接完成下载归档与逐帧解析。",
]
y += 6
for a in alts:
    y = ensure(y, 40)
    for ln in wrap(a, 10.5, W-2*M-16):
        text(M+14, y+14, ln, 10.5)
        y += 17
    y += 4

for i in range(doc.page_count):
    footer(doc[i])

doc.save(r"视频内容整理报告.pdf")
print("PDF saved")
