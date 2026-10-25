from PIL import Image
from pathlib import Path
p=Path(r'C:/Users/andre/Documents/ChatGPT/Burque Events Designs/burque-pocket/qa')
a=Image.open(p/'list.png').convert('RGB'); b=Image.open(p/'detail.png').convert('RGB')
out=Image.new('RGB',(a.width+b.width+16,max(a.height,b.height)),'#fff');out.paste(a,(0,0));out.paste(b,(a.width+16,0));out.save(p/'pocket-preview.png')
