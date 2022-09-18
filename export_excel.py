import io
import xlwt

def excel_file(headers,data):
     #output in bytes
    output = io.BytesIO()
    #create WorkBook object
    workbook = xlwt.Workbook()
    #add a sheet
    sh = workbook.add_sheet('Employee Report')

    #add headers
    head = 0
    for header in headers:
        sh.write(0, head, header)
        head += 1
    idx = 0
    #     keys=list(result[0].keys())
    for row in data:
        head = 0
        for header in headers:
            sh.write(idx+1, head, row[header])
            head += 1
        idx += 1

    workbook.save(output)
    
    return output.seek(0)