# -*- coding: utf-8 -*-
"""
Created on Thu Oct 23 21:13:40 2014

@author: yuanchang

"""

import os
import random
import time
from copy import deepcopy

import numpy as np

from utils.te import cmidd

os.system('cls')
NO = '0225'


def parseTime(date):

    '''
    将时间转换为毫秒数
    输入：要转换的时间列表timeList
    返回：转换完的列表strTotime[date] = timeStamp
    '''

    timeArray = time.strptime(date,"%Y/%m/%d")
    timeStamp = int(time.mktime(timeArray))
    return timeStamp

def getBlog(txtdir,user,timestart,timeend):

    '''读取某个用户所有的微博,剔除转发的微博，移除URL和Mention'''

    rootFile = open('D:/YC/'+txtdir)
    blogs = rootFile.read().splitlines() #获得该用户的所有微博
    rootFile.close()
    temp_blogs = np.array([])
    for blog in blogs:
        temp_blog = blog.split("\t")
        mtime = temp_blog[3][:-3]
        if mtime.isdigit():
             if (int(mtime) > timestart) and (int(mtime) < timeend):
                 temp_blogs = np.append(temp_blogs,int(mtime))
    return temp_blogs

def getWeibo(userList):

    '''读取用户的微博'''
    timestart = parseTime('2013/1/1')
    timeend = parseTime('2014/1/1')
    bins = int(float(timeend - timestart)/3600)
    users = []
    for user in userList: #获取每个用户的所有微博
        if not user:
            continue
        dirc = 'D:/YC/dataset/index/' + user + ".txt" #读取该用户所有微博的文件地址
        userdir = open(dirc)
        dirclist = userdir.read().split("\n")
        userdir.close()
        temp_blogs = np.array([])
        for txtdir in dirclist: #读取该用户所有微博
            if txtdir:
                temp_blogs = np.concatenate((temp_blogs,getBlog(txtdir,user,timestart,timeend)))
        if len(temp_blogs) >= 290:
            dist1, x1 = np.histogram(temp_blogs, bins=bins, range=(temp_blogs.min(),temp_blogs.max()))
            dist1 = np.array(dist1)
            dist1[dist1>0] = 1
            try:
                sample = np.vstack((sample,[dist1]))
            except:
                sample = np.array([dist1])
            users.append(user)
    if users:
        return users,sample
    else:
        return [],[]

def getsample():
    data = np.loadtxt('data1.txt',dtype='S')
    puserts = np.array(['1640601392'])
    childs = np.array([])
    pusert,psample = getWeibo(puserts)
    plist = puserts

    while len(plist):
        for parent in plist:
            child = data[data[:,1] == parent][:,0]
            child = np.unique(child)

            child = child[np.in1d(child,childs)==False]
            child = child[np.in1d(child,puserts)==False]
            cusers,csample = getWeibo(child)
            if len(cusers):
                childs = np.append(childs,cusers)
        plist = cusers

    graphuser = np.append(puserts,childs)
    graphuser = np.unique(graphuser)
    graph = np.zeros((len(graphuser),len(graphuser)))
    cusers,sample = getWeibo(graphuser)

    print('p:',len(puserts),'c:',len(childs))

    for c in range(len(graphuser)):
        for p in range(len(graphuser)):
            d = data==[graphuser[c], graphuser[p]]
            if len(d[d.all(True)]):
                graph[c,p] = 1

    print('graph over !')
    print('sample over !')
    return sample,graph,graphuser

# 等于testMNR
def getGraph(sample,graph,graphuser,nnodes,tmax):

    # np.savetxt('real/graph/'+str(NO)+'.txt',graph,fmt='%i')
    # np.savetxt('real/graph/'+str(NO)+'_user.txt',graphuser,fmt='%s')
    # np.savetxt('real/sample/'+str(NO)+'.txt',sample.T,fmt='%i')

    print(str(nnodes)+'_'+str(tmax)+'.txt')

    length = tmax - lagmax-1
    lag_max_pre = np.eye(nnodes, dtype=int)
    lag_max_late = np.zeros((nnodes,nnodes),dtype=np.int)
    lag_te = np.zeros((nnodes,nnodes))
    for n in range(nnodes):
        con = {}
        con[(n,1)] = sample[n,lagmax:tmax-1]
        x = sample[n,lagmax+1:tmax]
        nodeset = list(range(nnodes))

        for j in range(lagmax):
            n_teList = []

            ####find pc & lag####
            for i in nodeset:
                if n==i:
                    temp_te = cmidd(x,sample[i,(lagmax-j-1):(tmax-j-2)],con)
                    if temp_te > 0:
                        temp_te_2 = np.array([cmidd(x,random.sample(list(sample[i,(lagmax-j-1):(tmax-j-2)]),length),con) for m in range(100)])
                        if len(temp_te_2[temp_te_2 > temp_te])/100.00 < 0.05:
                            n_teList.append(i)
                            con[(i,j+2)] = sample[i,(lagmax-j-1):(tmax-j-2)]
                else:
                    temp_te = cmidd(x,sample[i,(lagmax-j+1):(tmax-j)],con)
                    if temp_te > 0:
                        temp_te_2 = np.array([cmidd(x,random.sample(list(sample[i,(lagmax-j+1):(tmax-j)]),length),con) for m in range(100)])
                        if len(temp_te_2[temp_te_2 > temp_te])/100.00 < 0.05:
                            n_teList.append(i)
                            con[(i,j+1)] = sample[i,(lagmax-j+1):(tmax-j)]

            lag_max_pre[n,n_teList] += 1

            if len(n_teList):
                nodeset = n_teList[:]
            else:
                break
        ####remove pc & lag####
        nodeindex = lag_max_pre[n].nonzero()[0]
        for i in nodeindex:
            tem_con = deepcopy(con)
            j = lag_max_pre[n,i]
            while (j > 0) and bool(len(con)):
                tem_con = deepcopy(con)
                y_next = tem_con.pop((i,j))
                temp_te = cmidd(x,y_next,tem_con)
                if temp_te > 0:
                    temp_te_2 = np.array([cmidd(x,random.sample(list(y_next),length),tem_con) for m in range(100)])
                    if len(temp_te_2[temp_te_2 > temp_te])/100.00 < 0.01:
                        break
                con = tem_con
                j -= 1

            if j and len(con):
                for l in range(1,j+1):
                    tem_con = deepcopy(con)
                    lag_te[n,i] += cmidd(x,tem_con.pop((i,l)),tem_con)
                lag_max_late[n,i] = j

    np.savetxt('Results/real/lag_pre/lag_pre_'+str(tmax)+'_'+str(nnodes)+'.txt',lag_max_late,fmt='%i',delimiter=',')

    for n in range(nnodes):
        for i in range(nnodes):
            if n != i :
                if (lag_te[n,i]>=lag_te[i,n]):
                    lag_max_late[i,n] = 0
                elif lag_te[i,n]:
                    lag_max_late[n,i] = 0
            else:
                break

    np.savetxt('Results/real/lag_late/lag_late_'+str(tmax)+'_'+str(nnodes)+'.txt',lag_max_late,fmt='%i',delimiter=',')
    np.savetxt('Results/real/lag_te/lag_te_'+str(tmax)+'_'+str(nnodes)+'.txt',lag_te,delimiter=',')

    return lag_max_late

def getuserName(userList):

    name = np.array([])
    '''读取用户的微博'''

    for user in userList: #获取每个用户的所有微博
        if not user:
            continue
        dirc = 'D:/YC/dataset/index/' + str(user) + ".txt" #读取该用户所有微博的文件地址
        userdir = open(dirc)
        dirclist = userdir.readline().split("\n")
        userdir.close()

        rootFile = open('D:/YC/'+dirclist[0])
        blogs = rootFile.readline().split("\t")#获得该用户的所有微博
        rootFile.close()
        name = np.append(name,blogs[1])
    return name

lagmax = 3
if __name__ == '__main__':
    from pandas import DataFrame


    sample,graph,graphuser = getsample()

    graph1 = graph.T
    a = graph1.nonzero()
    name = getuserName(graphuser)
    b = DataFrame({'Source':name[a[0]],'Target':name[a[1]]})
    b.to_csv('real/graph/name_'+str(NO)+'.csv',index=False)

    nnodes,tmax = sample.shape
    lag_max_late = getGraph(sample,graph,graphuser,nnodes,tmax)


    lag_max_late1 = lag_max_late.T
    a = lag_max_late1.nonzero()
    name = getuserName(graphuser)
    b = DataFrame({'Source':name[a[0]],'Target':name[a[1]]})
    c = DataFrame({'Source':graphuser,'Target':name})
    b.to_csv('real/result/name_'+str(NO)+'.csv',index=False)
    c.to_csv('real/result/id_'+str(NO)+'.csv',index=False)