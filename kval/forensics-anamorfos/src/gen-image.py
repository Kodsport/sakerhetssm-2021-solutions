from  PIL import Image, ImageDraw, ImageFont
fontsize = 250  
pad_left = 50
pad_up = 70
per_line = 6
text = "SSM{SP1N_M3_R1GH7_ROUND}"
text = f"{text[:per_line]}\n{text[per_line:2*per_line]}\n{text[2*per_line:-per_line]}\n{text[-per_line:]}"

colorText = "black"
colorBackground = "white"

font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf", fontsize, encoding="unic")

width, height = 1024, 1024
img = Image.new('RGB', (width, height), colorBackground)
d = ImageDraw.Draw(img)
d.text((pad_left, pad_up), text, fill=colorText, font=font)
d.rectangle((0, 0, width, height))
img.save("image.png")
