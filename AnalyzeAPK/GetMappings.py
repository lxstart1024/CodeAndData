# build mappings between features and methods
import xlrd
import xlsxwriter
import re
import nltk
from gensim.models import word2vec

def trans_funcname(str):
    p = re.compile(r'([a-z]|\d)([A-Z])')
    sub = re.sub(p, r'\1 \2', str).lower()
    return sub

def split_funcname():
    workbook = xlrd.open_workbook("C:/Users/DELL/PycharmProjects/paper1Code/APK2funcallapi.xlsx")
    worksheet = workbook.sheet_by_index(0)
    nrows = worksheet.nrows
    funcname = []
    funcnamesplit = []

    for i in range(nrows):
        funcname.append(''.join(worksheet.cell_value(i, 0)))
    for i in range(len(funcname)):
        funcnamesplit.append([funcname[i],trans_funcname(funcname[i]).split()])
    return funcnamesplit


def funcnameFilter():
    funcnamesplit = split_funcname()#funcnamesplit1保存函数名分词
    funcnamefiltered = []
    # print(funcnamesplit[1])
    for i in range(len(funcnamesplit)):
        if funcnamesplit[i][0].startswith('<') or funcnamesplit[i][0].startswith('_'):
            pass
        else:
            funcnamefiltered.append(funcnamesplit[i])
    return funcnamefiltered

#方法名词性标注
def MethodNamePos():
    funcnamefiltered = funcnameFilter()
    methodPOS = []
    # 函数名分词词性标注
    for i in range(len(funcnamefiltered)):
        funcname_split = trans_funcname(funcnamefiltered[i][0]).split()
        funcname_postag = nltk.pos_tag(funcname_split)
        methodPOS.append([funcnamefiltered[i], funcname_postag])
    return methodPOS

#训练word2vec,计算方法名和特征的相似度，得到mapping
def getMapping_level2():
    experimentalfeature_level2 = ["text","message","video","image","color","Facebook"]
    sentences = word2vec.Text8Corpus(u"E:/Code/photographyDescription.txt")
    model = word2vec.Word2Vec(sentences, size=100, min_count=1)
    #建表保存特征和方法名的对应关系
    workbook = xlsxwriter.Workbook("APK2FeatureAPIMapping_level2.xlsx")
    worksheet = workbook.add_worksheet()

    workbook1 = xlrd.open_workbook("C:/Users/DELL/PycharmProjects/paper1Code/APK2funcallapi.xlsx")
    worksheet1 = workbook1.sheet_by_index(0)
    nrows1 = worksheet1.nrows

    methodPoslist = MethodNamePos()

    mappinglist = []
    for i in range(len(experimentalfeature_level2)):
        for j in range(len(methodPoslist)):
            for k in range(len(methodPoslist[j][1])):
                if methodPoslist[j][1][k][1].startswith('N') and model.similarity(experimentalfeature_level2[i], methodPoslist[j][1][k][0])>0.7:
                    mappinglist.append([experimentalfeature_level2[i],methodPoslist[j][0][0]])

    for i in range(len(mappinglist)):
        for j in range(nrows1):
            m = 2
            n = 1
            if worksheet1.cell_value(j,0) == mappinglist[i][1]:
                worksheet.write(i,0,mappinglist[i][0])
                worksheet.write(i,1,mappinglist[i][1])
                while worksheet1.cell_value(j,n)!='':
                    worksheet.write(i,m,worksheet1.cell_value(j,n))
                    m = m+1
                    n = n+1
    workbook.close()



    #建立feature和method name的mapping
    # for i in range(len(mappinglist)):
    #     worksheet.write(i, 0, mappinglist[i][0])
    #     worksheet.write(i, 1, mappinglist[i][1])
    # workbook.close()

#训练word2vec,计算方法名和特征的相似度，得到mapping
def getMapping_level3():
    #第三层的实验特征
    experimentalfeature_level3 = [[["text"],["find","get","set","add"]],[["image"],["copy","open","load","get","find"]],
                                  [["video"],["take","create","make","get","find","remove","set","preview","mode"]],
                                  [["message"],["get","find","create","make"]],[["color"],["add"]],[["Facebook"],["set"]]]
    #训练模型
    sentences = word2vec.Text8Corpus(u"E:/Code/photographyDescription.txt")
    model = word2vec.Word2Vec(sentences, size=100, min_count=1)
    #建表保存特征和方法名的对应关系
    workbook = xlsxwriter.Workbook("APK2FeatureAPIMapping_level3.xlsx")
    worksheet = workbook.add_worksheet()

    workbook1 = xlrd.open_workbook("C:/Users/DELL/PycharmProjects/paper1Code/APK2funcallapi.xlsx")
    worksheet1 = workbook1.sheet_by_index(0)
    nrows1 = worksheet1.nrows

    methodPoslist = MethodNamePos()
    # print(methodPoslist)
    # print(experimentalfeature_level3[0])
    # print(experimentalfeature_level3[0][0])
    # print(experimentalfeature_level3[0][1])
    # print(experimentalfeature_level3[0][1][1])

    mappinglist = []

    for i in range(len(experimentalfeature_level3)):
        for j in range(len(methodPoslist)):
            for k in range(len(methodPoslist[j][1])):
                if methodPoslist[j][1][k][1].startswith('N') and model.similarity(experimentalfeature_level3[i][0][0], methodPoslist[j][1][k][0])>0.7:
                    for m in range(len(experimentalfeature_level3[i][1])):
                        for n in range(len(methodPoslist[j][1])):
                            if methodPoslist[j][1][n][1].startswith('V') and model.similarity(experimentalfeature_level3[i][1][m],methodPoslist[j][1][n][0])>0.7:
                                mappinglist.append([experimentalfeature_level3[i][1][m]+experimentalfeature_level3[i][0][0], methodPoslist[j][0][0]])
    for i in range(len(mappinglist)):
        for j in range(nrows1):
            m = 2
            n = 1
            if worksheet1.cell_value(j,0) == mappinglist[i][1]:
                worksheet.write(i,0,mappinglist[i][0])
                worksheet.write(i,1,mappinglist[i][1])
                while worksheet1.cell_value(j,n)!='':
                    worksheet.write(i,m,worksheet1.cell_value(j,n))
                    m = m+1
                    n = n+1
    workbook.close()








if __name__ == "__main__":
    # getMapping_level3()
    getMapping_level2()