# parsing APK file to get methods and the APIs they call
from androguard.misc import AnalyzeAPK
from androguard.core.analysis.analysis import ExternalMethod
import xlrd
import xlsxwriter

def get_source_call(a, d, dx):
    exclassname = []
    i = 0
    for method in dx.get_methods():
        orig_method = method.get_method()
        orig_descriptor = method.descriptor
        orig_class_name = orig_method.get_class_name()
        orig_method_name = orig_method.get_name()

        for other_class, callee, offset in method.get_xref_to():
            if isinstance(callee,ExternalMethod):
                call_class_name = callee.get_class_name()
                exclassname.append(call_class_name)
            else:
                pass
    exclassname = list(set(exclassname))
    return exclassname

def select_api(exclassname):
    workbook1 = xlrd.open_workbook("E:/Code/apislashversion.xlsx")
    worksheet1 = workbook1.sheet_by_index(0)
    nrows1 = worksheet1.nrows
    api_slash = []
    for i in range(nrows1):
        api_slash.append(''.join(worksheet1.row_values(i)))
    exclasses = exclassname
    api_classes = []
    for i in range(len(exclasses)):
        for j in range(len(api_slash)):
            if api_slash[j] in exclasses[i]:
                api_classes.append(exclasses[i])
            else:
                pass
    api_classes = list(set(api_classes))
    return  api_classes

def build_methodnameapi_relationship(a, d, dx, api_classes):
    workbook = xlsxwriter.Workbook("APK1funcallapi.xlsx")
    worksheet = workbook.add_worksheet()
    exapiname = api_classes
    funcname = []
    funcnameapi = []
    for i in range(len(exapiname)):
        for meth in dx.classes[exapiname[i]].get_methods():
            for _, call,_ in meth.get_xref_from():
                funcname.append(call.name)
                funcnameapi.append(([call.name, exapiname[i]]))
    funcname = list(set(funcname))
    k = 0
    funcallapi = []
    for i in range(len(funcname)):
        for j in range(len(funcnameapi)):
            if funcname[i] == funcnameapi[j][0]:
                funcallapi.append(funcnameapi[j][1])
                funcallapi = list(set(funcallapi))
        worksheet.write(i, 0, funcname[i])
        for k in range(len(funcallapi)):
            worksheet.write(i, k+1, funcallapi[k])
        funcallapi = []
    workbook.close()

if __name__ == "__main__":
    a, d, dx = AnalyzeAPK("E:/Code/APK1.apk")
    exclassname = get_source_call(a, d, dx)
    apiClass = select_api(exclassname)
    build_methodnameapi_relationship(a, d, dx, apiClass)
