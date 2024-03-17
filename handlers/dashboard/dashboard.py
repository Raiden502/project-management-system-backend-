from sqlalchemy import text
from myapp.db import db
from utils.dict_fetchall import dictfetchall

class Dashboard:
    def __init__(self, request):
        self.request = request
        self.data = request.json

    def get_counts(self):
        try:
            counts_query = f'''
            select 
                count(DISTINCT pu.user_id) as users,
                count(DISTINCT pu.team_id) as teams,
                count(DISTINCT t.task_id) as tasks,
                count(DISTINCT ty.type_id) as stages
            from 
                project_user_association pu
                left join tasks t on pu.project_id = t.project_id
                left join task_types ty on pu.project_id = ty.project_id
                where pu.project_id = :project_id and pu.department_id = :department_id group by ty.name
                '''
            result = db.session.execute(
                    text(counts_query), {"department_id":self.data['department_id'],"project_id":self.data['project_id'] }).fetchone()
            if result:
                return {
                    "status": True,
                    "message": "query successfull",
                    "errorcode": 0,
                    "data": {
                        "total_users":result[0],
                        "total_teams":result[1],
                        "total_tasks":result[2],
                        "total_stages":result[3]
                    }
                }
            return {
                "status": False,
                "message": "query unsuccessful",
                "errorcode": 1,
                "data": {
                }
            }
        except Exception as e:
            print(e)
            return {
                "status": False,
                "message": "query unsuccessful",
                "errorcode": 2,
                "data": {
                }
            }

    def get_stage_counts(self):
        try:
            counts_query = f'''
                select 
                    ty.name as label,
                    count(t.type_id) as value
                from task_types ty 
                left join tasks t on ty.type_id = t.type_id 
                where ty.project_id =:project_id group by ty.name
                '''
            result = dictfetchall(
                db.session.execute(
                    text(counts_query),
                    {
                        "department_id":self.data['department_id'],
                        "project_id":self.data['project_id']
                    })) 
            if result:
                return {
                    "status": True,
                    "message": "query successfull",
                    "errorcode": 0,
                    "data": result
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

    def get_priority_counts(self):
        try:
            counts_query = f'''
                SELECT
                    pt.enumlabel as label,
                    COUNT(t.task_id) AS value
                FROM
                    pg_enum pt
                LEFT JOIN
                    tasks t ON pt.enumlabel = t.priority::text AND t.project_id = :project_id
                WHERE
                    pt.enumtypid = 'priorities'::regtype
                GROUP BY
                    pt.enumlabel;
                '''
            result = dictfetchall(
                db.session.execute(
                    text(counts_query),
                    {
                        "department_id":self.data['department_id'],
                        "project_id":self.data['project_id']
                    })) 
            if result:
                return {
                    "status": True,
                    "message": "query successfull",
                    "errorcode": 0,
                    "data": result
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
    
    def get_tasks_list(self):
        try:
            order_query = f'''
                select task_order from projects_info where project_id = :project_id
            '''
            order_result = db.session.execute(
                    text(order_query),
                    {
                        "department_id":self.data['department_id'],
                        "project_id":self.data['project_id']
                    }).fetchone()
            
            if not order_result:
                return {
                    "status": False,
                    "message": "query unsuccessful",
                    "errorcode": 1,
                    "data": []
                }
            
            tasks_query = f'''
                with performance_metrics as (
                    select 
                        t.task_id as id, 
                        ty.type_id as typeid,
                        t.name,
                        t.priority, 
                        ty.name as status,
                        TO_CHAR(t.start_date, 'DD-MM-YYYY') AS start_date,
                        TO_CHAR(t.due_date, 'DD-MM-YYYY') AS due_date,
                        COUNT(DISTINCT tu.user_id) AS users,
                        COUNT(DISTINCT tu.team_id) AS teams,
                        COALESCE(
                            json_build_object(
                                'id', cu.user_id,
                                'name', cu.user_name,
                                'avatar', cu.avatar
                            ),
                            json_build_object()
                        ) AS reporter
                    from tasks t
                    left join task_types ty on t.type_id=ty.type_id
                    left join task_user_association tu on tu.task_id = t.task_id
                    left join user_info cu on cu.user_id = t.reporter
                    where t.project_id =:project_id and t.department_id = :department_id
                    group by id, typeid, t.name, t.start_date, t.due_date,  t.priority, status, cu.user_id
                )
                select * from performance_metrics where id is not null;
                '''
            result = dictfetchall(
                db.session.execute(
                    text(tasks_query),
                    {
                        "department_id":self.data['department_id'],
                        "project_id":self.data['project_id']
                    })) 
            
            if not result:
                return {
                    "status": False,
                    "message": "query unsuccessful",
                    "errorcode": 1,
                    "data": []
                }
            
            order_result = order_result[0]
            for item in result:
                item['progress'] = int(order_result.index(item['typeid'])/len(order_result) *100) if(item['status']!='Done') else 100 if(item['typeid']) else 0
            
            if result:
                return {
                    "status": True,
                    "message": "query successfull",
                    "errorcode": 0,
                    "data": result,
                }
        except Exception as e:
            print(e)
            return {
                "status": False,
                "message": "query unsuccessful",
                "errorcode": 2,
                "data": []
            }
    
    def get_user_lists(self):
        try:
            user_query = f'''
                with performance_metrics as (
                    SELECT 
                        COALESCE(NULLIF(u.user_id, ''), NULLIF(te.user_id, '')) AS user_id,
                        COALESCE(NULLIF(u.email_addrs, ''), NULLIF(pe.email_addrs, '')) AS email,
                        COUNT(DISTINCT t.task_id) AS tasks,
                        COUNT(DISTINCT CASE WHEN t.priority = 'medium' THEN t.task_id END) AS medium,
                        COUNT(DISTINCT CASE WHEN t.priority = 'low' THEN t.task_id END) AS low,
                        COUNT(DISTINCT CASE WHEN t.priority = 'high' THEN t.task_id END) AS high,
                        COUNT(DISTINCT CASE WHEN ty.name = 'Done' THEN t.task_id END) AS done,
                        COUNT(DISTINCT CASE WHEN ty.name != 'Done' THEN t.task_id END) AS inprogress,
                        COALESCE(
                            json_build_object(
                                'id', COALESCE(NULLIF(u.user_id, ''), NULLIF(te.user_id, '')),
                                'name', COALESCE(NULLIF(u.user_name, ''), NULLIF(pe.user_name, '')),
                                'avatar', COALESCE(NULLIF(u.avatar, ''), NULLIF(pe.avatar, ''))
                            ),
                            json_build_object()
                        ) AS details
                    FROM tasks t
                    LEFT JOIN task_user_association pu ON pu.task_id = t.task_id
                    LEFT JOIN task_types ty ON ty.type_id = t.type_id
                    LEFT JOIN user_info u ON pu.user_id = u.user_id
                    LEFT JOIN team_user_associaton te ON te.team_id = pu.team_id
                    LEFT JOIN user_info pe ON pe.user_id = te.user_id
                    WHERE t.project_id = :project_id
                    GROUP BY u.user_id, te.user_id, email, pe.user_name, pe.avatar
                )
                select * from performance_metrics where user_id is not null;
                '''
            result = dictfetchall(
                db.session.execute(
                    text(user_query),
                    {
                        "department_id":self.data['department_id'],
                        "project_id":self.data['project_id']
                    })) 
            if result:
                return {
                    "status": True,
                    "message": "query successfull",
                    "errorcode": 0,
                    "data": result
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

    def get_timeline(self):
        try:
            counts_query = f'''
                select 
                    TO_CHAR(created_at, 'DD-MM-YYYY') as time, name as stage
                from task_types ty where project_id =:project_id
                '''
            result = dictfetchall(
                db.session.execute(
                    text(counts_query),
                    {
                        "project_id":self.data['project_id']
                    })) 
            if result:
                return {
                    "status": True,
                    "message": "query successfull",
                    "errorcode": 0,
                    "data": result
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
    
    def get_performance(self):
        try:
            counts_query = f'''
                with performance_metrics as (
                    SELECT 
                        COALESCE(NULLIF(u.user_id, ''), NULLIF(te.user_id, '')) AS user_id,
                        COALESCE(NULLIF(u.email_addrs, ''), NULLIF(pe.email_addrs, '')) AS email,
                        COUNT(DISTINCT t.task_id) AS tasks,
                        COUNT(DISTINCT CASE WHEN t.priority = 'high' THEN t.task_id END) AS high,
                        COUNT(DISTINCT CASE WHEN t.priority = 'medium' THEN t.task_id END) AS medium,
                        COUNT(DISTINCT CASE WHEN t.priority = 'low' THEN t.task_id END) AS low,
                        COUNT(DISTINCT CASE WHEN ty.name = 'Done' and t.priority = 'high' THEN t.task_id END) AS done_high,
                        COUNT(DISTINCT CASE WHEN ty.name = 'Done' and t.priority = 'low' THEN t.task_id END) AS done_low,
                        COUNT(DISTINCT CASE WHEN ty.name = 'Done' and t.priority = 'medium' THEN t.task_id END) AS done_medium,
                        COUNT(CASE WHEN t.due_date < CURRENT_TIMESTAMP THEN 1 END) AS tasks_due_before,
                        COUNT(CASE WHEN t.due_date > CURRENT_TIMESTAMP THEN 1 END) AS tasks_due_after,
                        COALESCE(
                            json_build_object(
                                'id', COALESCE(NULLIF(u.user_id, ''), NULLIF(te.user_id, '')),
                                'name', COALESCE(NULLIF(u.user_name, ''), NULLIF(pe.user_name, '')),
                                'avatar', COALESCE(NULLIF(u.avatar, ''), NULLIF(pe.avatar, ''))
                            ),
                            json_build_object()
                        ) AS details
                    FROM tasks t
                    LEFT JOIN task_user_association pu ON pu.task_id = t.task_id
                    LEFT JOIN task_types ty ON ty.type_id = t.type_id
                    LEFT JOIN user_info u ON pu.user_id = u.user_id
                    LEFT JOIN team_user_associaton te ON te.team_id = pu.team_id
                    LEFT JOIN user_info pe ON pe.user_id = te.user_id
                    WHERE t.project_id = :project_id
                    GROUP BY u.user_id, te.user_id, email, pe.user_name, pe.avatar
                )
                SELECT *
                FROM performance_metrics
                where user_id is not null
                order by tasks DESC, high DESC, done_high DESC, 
                medium DESC, done_medium DESC, low DESC, 
                done_low DESC, tasks_due_after desc, tasks_due_before asc
                limit 10;
                '''
            result = dictfetchall(
                db.session.execute(
                    text(counts_query),
                    {
                        "project_id":self.data['project_id']
                    })) 
            if result:
                return {
                    "status": True,
                    "message": "query successfull",
                    "errorcode": 0,
                    "data": result
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
''''



'''