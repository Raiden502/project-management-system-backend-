from sqlalchemy import text
from myapp.db import db
from utils.dict_fetchall import dictfetchall

class DepartmentFilter:
    def __init__(self, request):
        self.request = request
        self.data = request.json
    
    def get_filter_list(self):
        try:
            dept_query = f''' 
                select 
                    d.department_id, d.name 
                from department_info d left join dept_user_associaton du
                on d.department_id = du.department_id
                where d.organization_id = :org_id and du.user_id =:user_id
            '''    
            with db.session() as session:
                result = session.execute(
                    text(dept_query), 
                    {"org_id":self.data['org_id'], "user_id": self.data["user_id"]})
                
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
