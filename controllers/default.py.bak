# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------
import webbrowser
import gtk.gdk
import datetime
import time
import os, shutil
import glob
import pygeoip
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import json
import requests
import os
import time
import threading
from os import path
from os import walk
import hashlib
#from gluon.debug import dbg



def index():
    return dict(form=auth())

@auth.requires_login()
def source():
    src = get_airport_code()
    if not src:
        form = display_code_form()
    else:
        form = ''
        redirect(URL('home'))

    return dict(form=form, src=src)


@auth.requires_login()
def home():
    src = str(get_airport_code())
    unique_path = str(get_user_id())
    dest = ''
    full_dest =''
    if request.args==[]:
        if(db((db.user_dest.created_by==auth.user.id)).select()):
                if(db((db.user_request_images.created_by==auth.user.id)).select()):
                    dest = db((db.user_request_images.created_by==auth.user.id)).select(db.user_request_images.destination_code, orderby=~db.user_request_images.created_on, limitby=(0,1)).first().destination_code
                    full_dest = str(get_city_from_code(dest))
                else:
                    dest= ''
                    full_dest = ''
        else:
          redirect(URL('destinations'), client_side=True)      

    else:
        if request.args[0] == 'refresh':
            process_screenshots()
        dest = request.args[1]
    path = request.env.web2py_path +'/applications/' +request.application + '/static/images/user_images/' + unique_path + '/' + src + '/' + dest + '/'
    files= {}
    image_rows = db((db.user_request_images.destination_code == dest) & (db.user_request_images.depart_date > datetime.date.today())).select(db.user_request_images.image_path, db.user_request_images.link_to)
    for i in image_rows:
        files[i.image_path] = i.link_to
    dir_path = request.env.web2py_path +'/applications/' +request.application + '/static/images/user_images/' + unique_path + '/' + src + '/'
    dirs = [x[0] for x in os.walk(dir_path)]
    dirs = [d.replace('/home/www-data/web2py/applications/travel/static/images/user_images/' + unique_path, '') for d in dirs]
    if image_rows:
        last_refreshed = db((db.user_request_images.destination_code == dest) & (db.user_request_images.created_by==auth.user.id)).select(db.user_request_images.created_on, orderby=~db.user_request_images.created_on, limitby=(0,1)).first().created_on
        last_refreshed = last_refreshed.strftime("%m/%d/%Y %I:%M:%p")
    else:
        last_refreshed = ''
    dest_picks = db((db.user_dest.created_by==auth.user.id)).select()
    full_dest = str(get_city_from_code(dest))
    return dict(files=files, dest=dest, dirs=dirs, src=src, last_refreshed=last_refreshed, dest_picks=dest_picks, unique_path=unique_path, full_dest=full_dest)

def images():
    src = db((db.user_airport_code.created_by==auth.user.id)).select(db.user_request_images.image_path)
    return dict(src=src)

def get_city_from_code(three_letter_code):
    if(three_letter_code):
        dest = db((db.airport_info.three_letter_code==three_letter_code)).select(db.airport_info.city).first().city
    else:
        dest = ''
    return dest

def display_code_form():
    form = SQLFORM(db.user_airport_code)
    if form.process().accepted:
        response.flash = 'form accepted'
        redirect(URL('home'))
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'
    return form

def location():
    ip = request.client
    rawdata = pygeoip.GeoIP(request.env.web2py_path +'/applications/' +request.application + '/static/GeoLiteCity.dat')
    data = rawdata.record_by_name(ip)
    if data:
        longi = data['longitude']
        lat = data['latitude']
    else:
        lat = 100000
        longi = -10000
    return dict(lat=lat, longi=longi)

def get_airport_code():
    src = db((db.user_airport_code.created_by==auth.user.id)).select(db.user_airport_code.three_letter_code)
    if not src:
        src = ''
    else:
        src = src.first().three_letter_code
    return src

def image(): # http://.../image/where/ever/it/is.jpeg
    filename = os.path.join(BASEDIR,'/'.join(request.args))
    return response.stream(open(filename,'rb'))

def populate_weekend_dates(start_index, ttl_duration):
    today = datetime.datetime.today().weekday()
    weekend_dates = []
    start= ''
    if(today==3 or today==4):
        start = datetime.datetime.now() + datetime.timedelta(days=3)
    else:
        start = datetime.datetime.now()
    #3 months into the future
    end =  (start + datetime.timedelta(ttl_duration*365/12))
    begin = start
    delta = datetime.timedelta(days=1)
    diff = 0
    #ONLY CALCULATE FRIDAY SINCE YOU CAN DO THE MATH FOR SUNDAY..
    weekend = ''
    if(start_index==4):
        weekend = set([3])
    elif(start_index==5):
        weekend = set([4])
    else:
        weekend = set([4])
    while(begin<=end):
            if(begin.weekday() in weekend):
                    weekend_dates.append(begin)
                    diff+=1
            begin+=delta
    return weekend_dates

def browser_screenshot(url,start_date,end_date,dest,source):
        unique_path = str(get_user_id())
        browser = driver = webdriver.PhantomJS()
        browser.get(url)
        delay = 0
        wait = WebDriverWait(browser, delay)
        wait.until(EC.presence_of_element_located((By.ID, 'root')))
        time.sleep(1)
        stringtime = str(start_date) + '->' + str(end_date)
        newdir = request.env.web2py_path +'/applications/travel/static/images/user_images/' + unique_path + '/' + source + '/' + dest + "/"
        if not os.path.exists(newdir):
                os.makedirs(newdir)
        filename = request.env.web2py_path +'/applications/travel/static/images/user_images/' + unique_path + '/' + source+ '/' + dest + '/flight' + stringtime + ".png"
        image = 'flight' + stringtime + ".png"
        db.user_request_images.insert(image_path=image, link_to=url, source_code = source, destination_code = dest, depart_date = start_date, return_date = end_date )
        browser.save_screenshot(filename)
        browser.close()


def call_all_destinations(source, weekend_dates, dest, start_index):
        for d in dest:
            for date in weekend_dates:
                start_date = datetime.datetime.strftime(date,'%Y-%m-%d')
                end_date = ''
                if(start_index==4):
                    end_date = datetime.datetime.strftime(date+datetime.timedelta(3),'%Y-%m-%d')
                elif(start_index==5):
                    end_date = datetime.datetime.strftime(date+datetime.timedelta(2),'%Y-%m-%d')
                url = 'https://www.google.com/flights/#search;f='+source+';t='+d+';d='+start_date+';r='+end_date+''
                browser_screenshot(url,start_date, end_date,d,source)


def delete_files(source):
    unique_path = str(get_user_id())
    folder = request.env.web2py_path +'/applications/travel/static/images/user_images/' + unique_path + '/' + source + '/'
    db((db.user_request_images.created_by==auth.user.id)).delete()
    if os.path.isdir(folder):
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path): shutil.rmtree(file_path)
            except Exception as e:
                print(e)

def process_screenshots():
    dest = []
    unique_path = str(get_user_id())
    start_index = request.args[0]
    start_index = start_index.replace('D','')
    ttl_duration = request.args[1]
    ttl_duration = ttl_duration.replace('F','')
    if(len(request.args) > 1):
        for val in request.args[2:]:
            dest.append(val)
    else:
        dest = ['DEN','LAX', 'SFO']
    start_index = int(start_index)
    ttl_duration = int(ttl_duration)
    weekend_dates = populate_weekend_dates(start_index, ttl_duration)
    source = get_airport_code()
    delete_files(source)
    if(source in dest):
        dest.remove(source)
    call_all_destinations(source, weekend_dates,dest, start_index)
    db.commit()
    redirect(URL('home'), client_side=True)


def user_profile():
    form = display_profile_form()
    return dict(form=form)

def display_profile_form():
    record = db.user_airport_code(auth.user.id)
    form = SQLFORM(db.user_airport_code, record)
    if form.process().accepted:
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    return form

def get_user_id():
    user_id = auth.user.id
    return user_id



def destinations():
    return dict(form=display_dest_form().process(),
                dest=db((db.user_dest.created_by==auth.user.id)).select(db.user_dest.three_letter_code))

def display_dest_form():
    form = SQLFORM(db.user_dest)
    if form.process().accepted:
        response.flash = request.args
    elif form.errors:
        response.flash = str(form.errors)
    else:
        response.flash = 'please fill out the form'
    return form


def delete_dest():
    code = request.args[0]
    if code==None:
        output = "Missing parameter"
        return output
    dest = db((db.user_dest.created_by==auth.user.id) & (code ==db.user_dest.three_letter_code))
    if dest==None:
        output = "delete error"
    else:
        dest.delete()

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()
