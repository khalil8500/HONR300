from flask import Flask, render_template, request, session, json, redirect, url_for, Response
import pymongo
import bson
import datetime

# establish database
client = pymongo.MongoClient('mongodb://heroku_01zv0lqq:c7tgn1ik3i8va9ql5kpmttisve@ds115340.mlab.com:15340/heroku_01zv0lqq')

# database of user accounts
userdb = client.heroku_01zv0lqq.users
postdb = client.heroku_01zv0lqq.posts
commentdb = client.heroku_01zv0lqq.comments
tagdb = client.heroku_01zv0lqq.tags

app = Flask(__name__)
app.secret_key = "change this string"