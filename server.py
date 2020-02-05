import cherrypy
import xlrd
import xlwt
import json
import os

path   = os.path.abspath(os.path.dirname(__file__))
config = {
  'global' : {
    'server.socket_host' : '127.0.0.1',
    'server.socket_port' : 8080,
    'server.thread_pool' : 1
  },
  '/static' : {
    'tools.staticdir.on'  : True,
    'tools.staticdir.dir' : os.path.join(path, 'static'),
    'tools.expires.on'    : True,
    'tools.expires.secs'  : 1
  }
}



class Handler(object):
    @cherrypy.expose
    def index(self):
        f = open("index.html", "r")
        
        return f.read()
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def run(self):

        result = {"operation": "request", "result": "success"}
        
        input_json = cherrypy.request.json
        print(input_json)
        return result
    
    @cherrypy.expose
    def readfile(self):
        with xlrd.open_workbook('workbook.xls') as f:
            
            
            
            toReturn = {}
            def format(v):
                if type(v) == float:
                    return {'type':'text','title':int(val), 'width':200 }
                else:
                    return {'type':'text','title':v.lower(), 'width':200 }
                
            

            for n in range(0, f.nsheets):
                _sheet=f.sheet_by_index(n)
                _sheet.cell_value(0,0)
                toReturn[_sheet.name] = {'data':[],'columns':[format(val) for val in _sheet.row_values(0)]}
                for row in range(1, _sheet.nrows):
                    row = _sheet.row_values(row)
                    toReturn[_sheet.name]['data'].append(row)
                
        return json.dumps(toReturn)
    
   
    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def writefile(self):

        result = {"operation": "request", "result": "success"}
        wb = xlwt.Workbook()
        input_json = cherrypy.request.json
        for sheet in input_json:
            tab = sheet[0]
            data = sheet[1:]
            
            ws = wb.add_sheet(tab)
            for r, row in enumerate(data):
                for c, v in enumerate(row):
                    ws.write(r,c,v)
        
        wb.save('workbook.xls')
        # Responses are serialized to JSON (because of the json_out decorator)
        return result
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def upload(self, myFile):

        result = {"operation": "request", "result": "success"}

        size = 0
        f = open("workbook.xls", "wb")
        
        
        while True:
            data = myFile.file.read(8192)
            f.write(data)
            if not data:
                f.close()
                break

        # Responses are serialized to JSON (because of the json_out decorator)
        return result
    

def main():
    #DO STUFF HERE
    cherrypy.quickstart(Handler(),'/',config = config)



if __name__ == '__main__':
    main()
