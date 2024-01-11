from app import app
from model.user_model import user_model
from model.auth_model import auth_model
from flask import request, send_file
from datetime import datetime

obj=user_model()
auth = auth_model()

@app.route("/user/getall")
# @auth.token_auth()
def user_getall_controller():
    return obj.user_getall_model()

@app.route("/user/addone", methods=["POST"])
def user_addone_controller():
    return obj.user_addone_model(request.form)

@app.route("/user/update", methods=["PUT"])
def user_update_controller():
    return obj.user_update_model(request.form)

@app.route("/user/delete/<id>", methods=["DELETE"])
def user_delete_controller(id):
    return obj.user_delete_model(id)

@app.route("/user/patch/<id>", methods=["PATCH"])
def user_patch_controller(id):
    return obj.user_patch_model(request.form, id)

@app.route("/user/getall/limit/<limit>/page/<page>", methods=["GET"])
def user_pagination_controller(limit, page):
    return obj.user_pagination_model(limit, page)

@app.route("/user/<uid>/avatar/upload", methods=["PATCH"])
def user_upload_avatar_controller(uid):
    file = request.files['avatar']
    new_filename =  str(datetime.now().timestamp()).replace(".", "") # Generating unique name for the file
    split_filename = file.filename.split(".") # Spliting ORIGINAL filename to seperate extenstion
    ext_pos = len(split_filename)-1 # Canlculating last index of the list got by splitting the filname
    ext = split_filename[ext_pos] # Using last index to get the file extension
    db_path = f"uploads/{new_filename}.{ext}"
    file.save(db_path)
    return obj.user_upload_avatar_model(uid, db_path)

@app.route("/uploads/<filename>")
def user_getavatar_controller(filename):
    return send_file(f"uploads/{filename}")

@app.route("/user/login")
def user_login():
    auth_data = request.authorization
    return obj.user_login_model(auth_data['username'], auth_data['password'])