import mysql.connector
import json
from flask import make_response
from datetime import datetime, timedelta
import jwt
from config.config import dbconfig

class user_model():
    def __init__(self):
        # Connection establishment code
        try:
            self.con=mysql.connector.connect(host=dbconfig['hostname'], user=dbconfig['username'], password=dbconfig['password'],database=dbconfig['database'])
            self.con.autocommit=True
            self.cur=self.con.cursor(dictionary=True)
            print("Connection Successful")
        except:
            print("Some error")
            
    def user_getall_model(self):
        self.cur.execute("SELECT * FROM users")
        result = self.cur.fetchall()
        if len(result)>0:
            res = make_response({"payload":result},200)
            res.headers['Access-Control-Allow-Origin'] = "*"
            return res
        else:
            return make_response({"message":"No Data Found"}, 204)
        
    def user_addone_model(self,data):
        self.cur.execute(f"INSERT INTO users(name, email, phone, role_id, password) VALUES('{data['name']}','{data['email']}','{data['phone']}','{data['role_id']}','{data['password']}')")
        return make_response({"message":"User Created Successfully"}, 201)
    
    def user_update_model(self,data):
        self.cur.execute(f"UPDATE users SET name='{data['name']}', email='{data['email']}', phone='{data['phone']}', role_id='{data['role_id']}', password='{data['password']}' WHERE id={data['id']}")
        if self.cur.rowcount>0:
            return make_response({"message":"User Updated Successfully"}, 201)
        else:
            return make_response({"mesaage":"Nothing to Update"}, 202)
        
    def user_delete_model(self,id):
        self.cur.execute(f"DELETE FROM users WHERE id={id}")
        if self.cur.rowcount>0:
            return make_response({"message":"User Deleted Successfully"}, 200)
        else:
            return make_response({"mesaage":"Nothing to Delete"}, 202)
        
    def user_patch_model(self, data, id):
        qry = "UPDATE users SET "
        for key in data:
            qry += f"{key} = '{data[key]}',"

        qry = qry[:-1] + f" WHERE id={id}"

        self.cur.execute(qry)
        
        if self.cur.rowcount>0:
            return make_response({"message":"User Updated Successfully"}, 201)
        else:
            return make_response({"mesaage":"Nothing to Update"}, 202)
        
    def user_pagination_model(self, limit, page):
        limit=int(limit)
        page=int(page)
        start = (page*limit)-limit
        qry = f"SELECT * FROM users LIMIT {start}, {limit}"
        self.cur.execute(qry)
        result = self.cur.fetchall()
        if len(result)>0:
            res=make_response({"payload":result, "page_no":page, "limit":limit}, 200)
            return res
        else:
            return make_response({"message":"No Data Found"}, 204)
        
    def user_upload_avatar_model(self, uid, filepath):
        self.cur.execute(f"UPDATE users SET avatar='{filepath}' WHERE id={uid}")
        if self.cur.rowcount>0:
            return make_response({"message":"FILE_UPLOADED_SUCCESSFULLY", "path":filepath},201)
        else:
            return make_response({"message":"NOTHING_TO_UPDATE"},204)
        
    def user_login_model(self, username, password):
        self.cur.execute(f"SELECT id, role_id, avatar, email, name, phone from users WHERE email='{username}' and password='{password}'")
        result = self.cur.fetchall()
        if len(result)==1:
            exptime = datetime.now() + timedelta(minutes=15)
            exp_epoc_time = exptime.timestamp()
            data = {
                "payload":result[0],
                "exp":int(exp_epoc_time)
            }
            print(int(exp_epoc_time))
            jwt_token = jwt.encode(data, "Sagar@123", algorithm="HS256")
            return make_response({"token":jwt_token}, 200)
        else:
            return make_response({"message":"NO SUCH USER"}, 204)