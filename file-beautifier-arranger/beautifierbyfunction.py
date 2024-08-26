import os
import shutil
import sys
dictionary = {
    "bmp": "BITMAP FILES",
    "rar": "RAR FILES",
    "txt": "TEXT FILES",
    "jpg": "JPG FILES",
    "accdb": "ACCESS FILES",
    "png": "PNG FILES",
    "docx": "WORD FILES",
    "pub": "PUBLISHER FILES",
    "py": "PYTHON FILES",
    "pptx": "POWERPOINT FILES"
}
def arrange(choice):
    for x in os.listdir():
        currentdir=os.getcwd()
        c=os.path.splitext(x)
        a=c[-1]
        if a=='.'+choice:
            origin=os.path.join(currentdir,x)
            if not os.path.exists(dictionary.get(choice)):
                os.mkdir(dictionary.get(choice))
            destination=os.path.join(currentdir,dictionary.get(choice))
            shutil.move(origin,destination)
extension=set()
for x in os.listdir():
    c=os.path.splitext(x)
    extension.add(c[-1])
print(f"There are {extension} extensions")
extension=list(extension)
extension= [ext.lower() for ext in extension]
e=list()
for ext in extension:
    e.append(ext[1:])
extension=e
extension.append("all")
print(f"Which file you want  to sort? ")
for x in extension:
    print(x,end='? ')
choice=input().lower()
if choice  not in extension:
    print(f"{choice} IS NOT THE VALID INPUT PLEASE ENTER WITH IN {extension}")    
    sys.exit()
print(choice)
if choice=='all':
    for x in extension:
        arrange(x)
elif choice=='':
    print("all files are arranged")
    sys.exit()
else:
    arrange(choice)
