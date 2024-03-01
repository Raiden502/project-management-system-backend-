from sqlalchemy import text
from myapp.db import db
from utils.dict_fetchall import dictfetchall

class ProjectList:
    def __init__(self, request):
        self.request = request
        self.data = request.json
    
    def get_proj_list(self):
        try:
            proj_query = f''' 
                select * from projects_info where department_id = :dept_id
            '''    
            with db.session() as session:
                result = session.execute(
                    text(proj_query), {"dept_id":self.data['dept_id']})
                
                data =  dictfetchall(result)
                if len(data):
                    return {
                        "status": True,
                        "message": "query successful",
                        "errorcode": 0,
                        "data": data
                    }
                return {
                    "status": False,
                    "message": "query unsuccessful",
                    "errorcode": 1,
                    "data": []
                }
        except Exception as e:
            print(e)
            return {
                    "status": False,
                    "message": "query unsuccessful",
                    "errorcode": 2,
                    "data": []
                }
