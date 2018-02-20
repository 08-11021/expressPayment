# coding=utf-8


import time
import datos
import re
from selenium import webdriver
from datetime import datetime

def send_email(user, pwd, recipient, subject, body):
    import smtplib

    FROM = user
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(user, pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        print 'successfully sent the mail'
    except:
        print "failed to send mail"
        refreshIp()

def login():
    connected = False
    while not connected:
        try:
            browser.get('https://tramites.saime.gob.ve/index.php?r=site/login')
            user = browser.find_element_by_name("LoginForm[username]")
            user.send_keys(datos.user)
            password = browser.find_element_by_name("LoginForm[password]")
            password.send_keys(datos.pwd)
            password.submit()
            browser.get('https://tramites.saime.gob.ve/index.php?r=inicio/inicio/agilizacion')
            connected = True
        except:
            time.sleep(15)
            try:
                browser.get('http://www.google.com')
                q = browser.find_element_by_name("q")
                q.send_keys("checking connection")
            except:
                refreshIp()
                time.sleep(90)
            print 'reconnecting'
            connected = False

def refreshIp():
    browser.get("http://192.168.1.1/login_security.html")
    try:
        user = browser.find_element_by_name("Login_Name")
        user.send_keys("admin")
        pwd = browser.find_element_by_name("Login_Pwd")
        pwd.send_keys("admin")
        submit = browser.find_element_by_name("texttpLoginBtn")
        submit.click()
    except:
        print "error iniciando sesion en el router"
    browser.get('http://192.168.1.1/wizard/wizardConfigured.html')
    for i in xrange(0,3):
        next=browser.find_element_by_name("NextBtn")
        next.click()
    next = browser.find_element_by_name("WizardWlanNextBtn")
    next.click()
    save = browser.find_element_by_name("SaveBtn")
    save.click()

browser = webdriver.Chrome(executable_path='C:/Users/Gabriel/PycharmProjects/selenium test/chromedriver.exe')
#browser.set_page_load_timeout(90)
login()

element = browser.find_elements_by_css_selector('h1')
while True:
    try:
        browser.find_element_by_name('Pago[tipotramiteprocesoagilizacion]').submit()
        #time.sleep(30)
        if browser.current_url == 'https://tramites.saime.gob.ve/index.php?r=inicio/inicio/agilizacion':
            print datetime.now().strftime('%H:%M:%S')
        elif browser.current_url == 'https://tramites.saime.gob.ve/index.php?r=pago/pago/formpago':
            src = browser.page_source
            text_found = re.search(r'502 Bad Gateway', src)
            if text_found is None:
                bodyText = browser.find_element_by_tag_name('body').text.strip()
                if bodyText != '':
                    text_found = re.search(r'No se puede acceder a este sitio web',src)
                    if text_found is None:
                        send_email(datos.fromMail, datos.mailpwd, datos.to, datos.successSubject, datos.successBody+datetime.now().strftime('%H:%M:%S'))
                        break
            browser.get('https://tramites.saime.gob.ve/index.php?r=inicio/inicio/agilizacion')
        else:
            login()
    except:
        #send_email('globerusso@gmail.com', 'bartholomeo$$4Gg1', 'globerusso@gmail.com', 'Algo salio mal', 'ocurrio una excepcion')
        login()

