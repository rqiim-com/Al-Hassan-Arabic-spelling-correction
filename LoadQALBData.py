import codecs
def generateTargetsentence(sentence,changesList):
    splited=sentence.split()
    idstoDelte=[]
    shift=0
    for change in changesList:
        changeSplited=change.split("|||")
        changeType=changeSplited[1]
        changeType=str(changeType).lower()
        if changeType=="edit":
            ids=changeSplited[0].split()
            idsTOchange=int(ids[1])+shift
            splited[idsTOchange]=changeSplited[2]

        elif changeType=="merge":
            ids = changeSplited[0].split()
            idsTOchange=int(ids[1])+shift
            mergeSwap=splited[idsTOchange]
            splited[idsTOchange+1]=mergeSwap+splited[idsTOchange+1]
            # idstoDelte.append(idsTOchange)
            del splited[idsTOchange]
            shift-=1

        elif changeType == "delete_token" or changeType == "delete":
            ids = changeSplited[0].split()
            idsTOchange=int(ids[1])+shift
            del splited[idsTOchange]
            shift-=1
            # idstoDelte.append(idsTOchange)

        elif changeType == "split" :
            ids = changeSplited[0].split()
            idsTOchange=int(ids[1])+shift
            splited[idsTOchange]=changeSplited[2]

        elif changeType=="move" or changeType=="move_before":
            ids = changeSplited[0].split()
            idsTOchange=int(ids[1])+shift
            idsTOchange2=int(ids[2])+shift
            splited.insert(idsTOchange2,changeSplited[2])
            shift+=1
            c=0
            for i in range(idsTOchange ,idsTOchange2):

                del splited[idsTOchange]
                shift-=1

        elif changeType=="add_before" or changeType=="add_token_before":
            ids = changeSplited[0].split()
            idsTOchange = int(ids[1]) + shift
            splited.insert(idsTOchange,changeSplited[2])
            shift+=1

        elif changeType == "add_after" or changeType == "add_token_after":
            ids = changeSplited[0].split()
            idsTOchange = int(ids[1]) + shift
            splited.insert(idsTOchange +1, changeSplited[2])
            shift+=1
        else:
                print changeType
                return ""

    str1 = ''.join(e+" " for e in splited)
    return str1.strip()

m2File = codecs.open("/home/razzaz/Desktop/Data/QALB-0.8.0-April08-2015-SharedTask/all.m2", "r", encoding="utf-8")

newFIle=codecs.open("/home/razzaz/Desktop/Data/QALB-0.8.0-April08-2015-SharedTask/all.m2.new",'w',encoding='utf-8')
lines=m2File.readlines()
i=0
while True:
    if not i < len(lines):
        break
    changes = []
    sentence = lines[i].strip("S").strip()
    i+=1
    while True:
        line = lines[i]
        i += 1
        if line == "":
            break

        newLine = ''
        if not line.strip() == "":
            changes.append(line)
        else:
            newLine=generateTargetsentence(sentence,changes)
            newFIle.write(newLine)
            newFIle.write('\n')
            newFIle.flush()
            break
newFIle.close()
m2File.close()