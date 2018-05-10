"""
    This is the main file, where template rendering takes place.
"""
from flask import Flask, render_template, request, session, json, redirect, url_for, Response
import pymongo
import bson
from datetime import datetime as dt

from user_calls import *
from post_calls import *
from __init__ import *

@app.route("/")
@app.route("/home")
@app.route("/index")
def homepage():
    if "username" in session:
        return redirect(url_for("dashboard", username=session["username"]))

    return render_template("homepage.html")


@app.route("/register", methods=["GET"])
def register_page():
    return render_template("register.html")


@app.route("/login", methods=["GET"])
def login_page():
    return render_template("login.html")


@app.route("/post", methods=["GET"])
def make_post():
    if "username" not in session:
        return redirect(url_for("login_page"))

    return render_template("post.html")


@app.route("/tag", methods=["GET"])
def make_tag():
    if "username" not in session:
        return redirect(url_for("login_page"))

    return render_template("tag.html")


@app.route("/comment", methods=["GET"])
def make_comment():
    return render_template("comment.html")


@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "username" not in session:
        return redirect(url_for("login_page"))
        
    if request.method == "POST":
        form = dict(request.form)
    
        text = form["text"][0]
        anonymous = request.form.get('anonymous')
        conf = "good"
        if text != "":
            for c in text:
                if ord(c) > 127:
                    conf = "bad"
                
            if conf == "good":
                postdb.insert_one({
                    "user_id": session["user_id"],
                    "text": text,
                    "date_posted": dt.now(),
                    "anonymous": anonymous
                })
	
    # asdasd
    # get the most recent 10 posts
    posts = []
    result = postdb.find().limit(10).sort('date_posted', pymongo.ASCENDING)
    if result:
        for post in result:
            post_entry = {
                "post": post,
                "tags": list(tagdb.find({"post_id": post["id"]}).limit(10)),
                "comments": list(commentdb.find({"post_id": post["id"]}).limit(10))
            }
            # add in tags for those comments
            if post_entry["comments"]:
                for comment in post_entry["comments"]:
                    result = tagdb.find({"comment_id": comment["id"]}).limit(10)
                    if result:
                        post_entry["tags"] += list(result)
            posts.append(post_entry)

    return render_template("dashboard.html", posts=posts)
	

if __name__ == "__main__":
    userdb.remove()
    postdb.remove()
    commentdb.remove()
    tagdb.remove()
    app.run(port=80, debug=True)
    '''
    print(userdb.insert_one({"potato": 1}))
    print(userdb.find_one({"potato":1}))
    print(list(userdb.find()))
    userdb.remove()
    print(userdb.find_one({"potato":1}))
    '''
