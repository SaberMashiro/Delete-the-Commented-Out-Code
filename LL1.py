#coding:utf-8
'''
e代表空串
'''
import pandas
import copy
grammer = {}
first = {}
follow = {}
select = {}
check = {}
table = {}
empty = []
#setGrammer,初始化各个字典
with open('grammer.txt','r+') as f:
    contents = f.read().split('\n')
for line in contents:
    grammer[line[0]] = line[1:].replace('->','').split('|')
    first[line[0]] = ""
    follow[line[0]] = ""
    check[line[0]] = set()
    table[line[0]] = []

for key in grammer.keys():
    for value in grammer[key]:
        select[key+"->"+value] = []


def SetFirst(first):
    for key in first.keys():
        firstList = grammer[key]
        result = []
        for value in firstList:
            counter = 0
            if value[counter].islower():
                result.append(value[counter])#第一个是终结符
            else:#第一个是非终结符
                while(''.join(grammer[value[counter]]).find('e') >= 0):#如果该非终结符中有空串
                    if not result.count('e'):
                        result.append('e')
                    result+=[n[0] for n in grammer[key] if n[0].islower() and n[0]  is not 'e']
                    counter += 1
        result = list(set(result))
        first[key] = result


def SetFollow(follow):
    flag = 1
    for key in ['S'] + [x for x in follow.keys() if x is not 'S']:#对每个元素  
        result = []
        if flag:
            result+=['#']
            flag = 0
        for word in ['S'] + [x for x in follow.keys() if x is not 'S']:#按顺序遍历 
            for value in grammer[word]:#遍历value列表
                length = value.__len__()
                position = value.find(key) + 1
                if position and position < length:
                    if value[position].islower():
                        result.append(value[position])#如果找到的位置后面是终结符
                    else:
                        while(position is True and ''.join(first[value[position]]).find('e') >= 0):#如果该非终结符中有空串
                            temp = copy.deepcopy(first)[value[position]]#first集
                            if temp.count('e'):
                                temp.remove('e')
                            result+=temp
                            result+=follow[word]
                            if position < length-1:
                                position += 1
                            else:
                                position = -1
                        temp = copy.deepcopy(first)[value[position]]#最后一个或者没有空串
                        if temp.count('e'):
                            temp.remove('e')
                        result+=temp
                elif position and position >= length:
                    result += follow[word]
        result = list(set(result))
        follow[key] = result



def SetSelect(select):
    for key in select.keys():
        #S->aBc,S->bAB.......
        flag = 1
        result = []
        counter = 0
        value = key[1:].replace('->','')
        parameter = key[counter]
        if value[counter].islower() and value[counter] is not 'e':
            result.append(value[counter])
        elif value[counter] is 'e':
            result += follow[parameter]
        else:
            while(value[counter].isupper()):
                temp = first[value[counter]]
                if not temp.count('e'):
                    flag = 0
                result += temp
            if flag:
                result += follow[parameter]
        select[key] = result

def CheckLL1():
    for key in select.keys():
        value = key[0]
        check[value] &= set(select[key])
    flag = 1
    for temp in check.values():
        if len(temp):
            flag = 0
    return flag

def Table():
    top = list(set(sum(select.values(),[])))
    left = grammer.keys()
    for key in table.keys():
        for i in xrange(top.__len__()):
            table[key[0]].append('')
    for key in select.keys():
        parameter = key[0]
        value = key[1:]
        for each in top:
            counter = top.index(each)
            if select[key].count(each):
                table[parameter][counter] = value
    #data = pandas.DataFrame(table,columns=top,index=left)
    print table
    data = pandas.DataFrame(table,index=top)#绘制图形
    print data

def SetEmpty():
    for key in first.keys():
        parameter = key[0]
        if first[parameter].count('e'):
            empty.append(parameter)

    

if __name__ == '__main__':
    SetFirst(first)
    SetFollow(follow)
    SetSelect(select)
    print 'first is---',first
    print 'follow is ---',follow
    print 'select is ---',select
    is_ll = CheckLL1()
    if is_ll:
        print u'是LL1文法'
        Table()
    else:
        print u'不是LL1文法'
    SetEmpty()
    print u'能推导出空串的非终结符为'+''.join(empty)


