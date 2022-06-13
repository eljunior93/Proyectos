from cgitb import handler
from hashlib import new
from multiprocessing.connection import wait
from sys import exit
import sys
import re 
import calendar
import time
import os
import random
import platform
import pickle
from warnings import catch_warnings
import selenium.webdriver
import speech_recognition as sr
import ffmpy
import requests
import urllib
from pydub import AudioSegment
AudioSegment.converter = "ffmpeg.exe"
AudioSegment.ffmpeg = "ffmpeg.exe"
AudioSegment.ffprobe = "ffprobe.exe"
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import UnexpectedAlertPresentException 
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.proxy import Proxy, ProxyType
from SriDescarga import *

audioFile = "\\sample.mp3"
SpeechToTextURL = "https://speech-to-text-demo.ng.bluemix.net/"
def delay ():
    time.sleep(random.randint(2, 3))

def audioToText(audioFile, driver):
    
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])
    driver.get(SpeechToTextURL)
    time.sleep(3)
    driver.find_element(By.XPATH, '//*[@id="root"]/div/div[5]/div[1]/p[1]/select').send_keys("Spanish broadband model  (16KHz)")
    driver.find_element(By.XPATH, '//*[@id="root"]/div/div[5]/div[1]/p[2]/label').click()
    audioInput = driver.find_element(By.XPATH, '//*[@id="root"]/div/input')
    audioInput.send_keys(audioFile)
    time.sleep(3)

    text = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[7]/div/div/div/span')
    while text is None:
        text = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[7]/div/div/div/span')
    result = text.text
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    return result


def resolver(ruc, clave, Anio, Mes, Dia, Tipo):
    
    options = Options()
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument("window-size=1280,800")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-infobars")
    options.add_argument("--mute-audio")
    options.add_argument("--headless")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_extension (os.path.expanduser("D:/SriTkinter/Buster--Captcha-Solver-for-Humans.crx"))
    options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(r"C:\SRIdesc\chromedriver.exe", options=options) 
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    #driver.minimize_window()
    driver.get("https://srienlinea.sri.gob.ec/tuportal-internet/accederAplicacion.jspa?redireccion=57&idGrupo=55")
    time.sleep(1)
    driver.minimize_window()

    #print ("Número de parámetros: ", sys.argv)

    ruc = str(ruc)
    clave = clave
    Anio = Anio
    Mes = Mes
    Dia = Dia
    Tipo = Tipo

    #####INICIA PROCESO DE CONSULTA###############         
    driver.find_element(By.XPATH, "//input[contains(@id,'usuario')]").send_keys(ruc)
    time.sleep(1)
    driver.find_element(By.XPATH, "//input[contains(@id,'password')]").send_keys(clave)
    time.sleep(1)
    driver.find_element(By.XPATH, "//input[contains(@id,'kc-login')]").click()
    time.sleep(1)
    driver.maximize_window() 
    time.sleep(1)
    driver.find_element(By.XPATH, "//select[contains(@id,'frmPrincipal:ano')]").send_keys(Anio)
    time.sleep(1)
    driver.find_element(By.XPATH, "//select[contains(@id,'frmPrincipal:mes')]").send_keys(Mes)
    time.sleep(1)
    driver.find_element(By.XPATH, "//select[contains(@id,'frmPrincipal:dia')]").send_keys(Dia)
    time.sleep(1)
    driver.find_element(By.XPATH, "//select[contains(@id,'frmPrincipal:cmbTipoComprobante')]").send_keys(Tipo)
    time.sleep(1)
    driver.find_element(By.XPATH, "//button[contains(@id,'btnRecaptcha')]").click()
    time.sleep(1)
    #driver.maximize_window() 
    ########CAPTCHA#########
    try:
        frame = driver.find_element_by_xpath("//iframe[@title='El reCAPTCHA caduca dentro de dos minutos']")
        driver.switch_to.frame(frame)
        time.sleep(1)
        audiobutton = driver.find_element_by_xpath("/html/body/div/div/div[3]/div[2]/div[1]/div[1]/div[2]/button")
        audiobutton = driver.find_element_by_id("recaptcha-audio-button")
        time.sleep(1)  
        audiobutton.click()  
        driver.switch_to.default_content()
        frame = driver.find_elements_by_tag_name("iframe")
        driver.switch_to.frame(frame[-1])
        delay()
        #driver.maximize_window()
        driver.find_element_by_xpath("/html/body/div/div/div[3]/div/button").click()
        #driver.minimize_window()
        time.sleep(2)
        src = driver.find_element_by_id("audio-source").get_attribute("src")
        print("[INFO] Audio src: %s"%src)
        time.sleep(2)
        urllib.request.urlretrieve(src, os.getcwd() + audioFile)
        key = audioToText(os.getcwd() + audioFile, driver)
        #sound = AudioSegment.from_mp3(os.getcwd()+audioFile)
        #sound.export(os.getcwd()+"\\sample.wav", format="wav")
        #sample_audio = sr.AudioFile(os.getcwd()+"\\sample.wav")
        #r = sr.Recognizer()
        #with sample_audio as source:
        #    audio = r.record(source)
        #key = r.recognize_google(audio, language="es-ES")
        print("[INFO] Recaptcha Passcode: %s"%key)
        driver.switch_to.default_content()
        time.sleep(2)
        frame = driver.find_element_by_xpath("//iframe[@title='El reCAPTCHA caduca dentro de dos minutos']")
        driver.switch_to.frame(frame)
        driver.find_element(By.XPATH, '//*[@id="audio-response"]').send_keys(key)
        #driver.find_element_by_id("audio-response").send_keys(key.lower())
        time.sleep(1)
        driver.find_element_by_id("audio-response").send_keys(Keys.ENTER)
        time.sleep(1)
    except NoSuchElementException:
        pass      
    except Exception as e:
        driver.quit()
        resolver(ruc, clave, Anio, Mes, Dia, Tipo)

    driver.find_element(By.XPATH,"//a[contains(@id,'frmPrincipal:lnkTxtlistado')]").click()
    ban = True
    #print('descargo')
    time.sleep(1)
    driver.quit()
