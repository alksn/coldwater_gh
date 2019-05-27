



import re
import json
import sys
import getopt
import os



inputfile = ''
outputfile = './data.json'


def help():
    print('app v.1.0.19.0517')
    print('coldwater.py -i <inputfile> -o <outputfile>')



# проверка наличия параметров
if len(sys.argv) == 1:
    help()
    sys.exit()

# получение параметров
try:
    options, remainder = getopt.getopt(sys.argv[1:], "hi:o:", [])
except getopt.GetoptError:
    help()
    sys.exit(2)

# чтение параметров
for opt, arg in options:
    if opt in ('-h', '-?', '--help'):
        help()
        sys.exit()
    elif opt == '-s':
        text = arg
    elif opt == '-i':
        inputfile = arg
    elif opt == '-o':
        outputfile = arg


# чтение строки из файла
if inputfile != '':
    if os.path.isfile(inputfile):
        with open(inputfile, 'r') as file:
            text = file.read()


root = {}
list = []

#with open('mart2019.txt', 'r') as file:
#    text = file.read()


objs = re.findall(r'\n..\.[\s\S]*?%\n-{89}', text)

for obj in objs:

    name = re.findall(r'..\.\s(.+)', obj)                       # до конца строки после пробела
    vidv = re.findall(r'-{40}\n.+\n.+-(.+)', obj)               # через две строки после -{40}
    valv = re.findall(r'Расход\(м3\)\s+(-*\d+.\d+).+%', obj)    # расход(м3) пробелы шаблон любые символы и символ % в конце строки
    tarv = re.findall(r'Расход.+?Тариф.+?(-*\d+.\d+).+%', obj)
    sumv = re.findall(r'Расход.+?Сумма.+?(-*\d+.\d+).+%', obj)
    vidk = re.findall(r'-{40}\n.+-(.+)', obj)
    valk = re.findall(r'Сброс\(м3\)\s+(-*\d+.\d+).+%', obj)
    tark = re.findall(r'Сброс.+?Тариф.+?(-*\d+.\d+).+%', obj)
    sumk = re.findall(r'Сброс.+?Сумма.+?(-*\d+.\d+).+%', obj)

    elem = {}

    i = 0
    for el in list:
        if el["name"].upper() == name[0].upper():
            i = el["line"]

    elem["line"] = i + 1
    elem["name"] = name[0]
    elem["values"] = {}
    elem["values"]["vidv"] = vidv[0].strip().lower()
    elem["values"]["vidk"] = vidk[0].strip().lower()
    elem["values"]["valv"] = float(valv[len(valv)-1])
    elem["values"]["tarv"] = float(tarv[len(tarv)-1])
    elem["values"]["sumv"] = float(sumv[len(sumv)-1])
    elem["values"]["valk"] = float(valk[len(valk)-1])
    elem["values"]["tark"] = float(tark[len(tark)-1])
    elem["values"]["sumk"] = float(sumk[len(sumk)-1])

    list.append(elem)


root["root"] = list
with open(outputfile, 'w', encoding='utf8') as file:
    dumps = json.dumps(root, ensure_ascii=False)  # type(dumps) = string
    file.write(dumps + '\n')


print(list)


print("len(list)="+str(len(list)))
print("len(objs)="+str(len(objs)))




