from ssl import Options
from time import time
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pydub import AudioSegment
from cgitb import handler
from multiprocessing.connection import wait
from sys import exit
from selenium.webdriver.common.keys import Keys
import time
import os
import random
import speech_recognition as sr
import ffmpy
import urllib
AudioSegment.converter = "ffmpeg.exe"
AudioSegment.ffmpeg = "ffmpeg.exe"
AudioSegment.ffprobe = "ffprobe.exe"

audioFile = "\\sample.mp3"
SpeechToTextURL = "https://speech-to-text-demo.ng.bluemix.net/"
def delay ():
    time.sleep(random.randint(2, 3))

def audioToText(audioFile, driver):
    
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])
    driver.get(SpeechToTextURL)
    print('Abrio Watson')
    time.sleep(3)
    driver.find_element_by_name('model').send_keys("Spanish broadband model  (16KHz)")
    print('Cambio audio')
    time.sleep(2)  
    driver.find_element_by_xpath("/html/body/div[3]/div/div[5]/div[1]/p[2]/label").click()
    print('dio click')
    time.sleep(2)  
    #time.sleep(2)
    audioInput = driver.find_element(By.XPATH, '//*[@id="root"]/div/input')
    audioInput.send_keys(audioFile)
    print('carga el audio')
    time.sleep(3)
    print('Escribira texto')
    text = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[7]/div/div/div/span[1]')
    print('Escribe texto')
    while text is None:
        text = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[7]/div/div/div/span[1]')
    result = text.text
    print(result)
    time.sleep(3)
    driver.close()
    print('cerro watson')
    driver.switch_to.window(driver.window_handles[0])
    return result


def resolver(ruc, clave, Anio, Mes, Dia, Tipo):
    options = FirefoxOptions()
    #options.add_argument("--headless")
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-infobars")
    driver = webdriver.Firefox(options=options, executable_path=GeckoDriverManager().install())
    driver.get("https://srienlinea.sri.gob.ec/tuportal-internet/accederAplicacion.jspa?redireccion=57&idGrupo=55")
    print('Abre la Pagina')

    ruc = str(ruc)
    clave = clave
    Anio = Anio
    Mes = Mes
    Dia = Dia
    Tipo = Tipo

    #####INICIA PROCESO DE CONSULTA###############         
    driver.find_element(By.XPATH, "//input[contains(@id,'usuario')]").send_keys(ruc)
    print('escribio el ruc')
    time.sleep(1)
    driver.find_element(By.XPATH, "//input[contains(@id,'password')]").send_keys(clave)
    print('escribio la clave')
    time.sleep(1)
    driver.find_element(By.XPATH, "//input[contains(@id,'kc-login')]").click()
    print('dio click')
    time.sleep(1)
    #driver.maximize_window() 
    time.sleep(2)
    driver.find_element_by_name("frmPrincipal:ano").send_keys(Anio)
    print('cambio el año')
    time.sleep(2)
    driver.find_element_by_name("frmPrincipal:mes").send_keys(Mes)
    print('cambio el mes')
    time.sleep(2)
    driver.find_element_by_name("frmPrincipal:dia").send_keys(Dia)
    print('cambio el dia')
    time.sleep(2)
    driver.find_element_by_name("frmPrincipal:cmbTipoComprobante").send_keys(Tipo)
    print('cambio el comprobante')
    time.sleep(1)
    driver.find_element(By.XPATH, "//button[contains(@id,'btnRecaptcha')]").click()
    print('dio click')
    time.sleep(1)
    options.preferences.update({'javascript.enabled': False})
    #driver.maximize_window() 
    ########CAPTCHA#########
    try:
        print('Inicia Captcha')
        frame = driver.find_element_by_xpath("//iframe[@title='El reCAPTCHA caduca dentro de dos minutos']")
        driver.switch_to.frame(frame)
        print('Abrio el captcha')
        time.sleep(1)
        audiobutton = driver.find_element_by_xpath("/html/body/div/div/div[3]/div[2]/div[1]/div[1]/div[2]/button")
        audiobutton = driver.find_element_by_id("recaptcha-audio-button")
        time.sleep(1)  
        audiobutton.click()
        print('dio click')  
        driver.switch_to.default_content()
        frame = driver.find_elements_by_tag_name("iframe")
        driver.switch_to.frame(frame[-1])
        delay()
        #driver.maximize_window()
        driver.find_element_by_xpath("/html/body/div/div/div[3]/div/button").click()
        #driver.minimize_window()
        print('dio click')
        time.sleep(2)
        src = driver.find_element_by_id("audio-source").get_attribute("src")
        print("[INFO] Audio src: %s"%src)
        print('bajo el archivo de audio')
        time.sleep(2)
        urllib.request.urlretrieve(src, os.getcwd() + audioFile)
        key = audioToText(os.getcwd() + audioFile, driver)
        print('Escribira Captcha')
        #sound = AudioSegment.from_mp3(os.getcwd()+audioFile)
        #sound.export(os.getcwd()+"\\sample.wav", format="wav")
        #sample_audio = sr.AudioFile(os.getcwd()+"\\sample.wav")
        #r = sr.Recognizer()
        #with sample_audio as source:
        #    audio = r.record(source)
        #key = r.recognize_google(audio, language="es-ES")
        time.sleep(2)
        print("[INFO] Recaptcha Passcode: %s"%key)
        driver.switch_to.default_content()
        time.sleep(2)
        frame = driver.find_element_by_xpath("//iframe[@title='El reCAPTCHA caduca dentro de dos minutos']")
        driver.switch_to.frame(frame)
        driver.find_element(By.XPATH, '//*[@id="audio-response"]').send_keys(key)
        print('escribio captcha')
        #driver.find_element_by_id("audio-response").send_keys(key.lower())
        time.sleep(1)
        driver.find_element_by_id("audio-response").send_keys(Keys.ENTER)
        print('dio click')
        time.sleep(5)
    except NoSuchElementException:
        pass      
    except Exception as e:
        driver.quit()
        resolver(ruc, clave, Anio, Mes, Dia, Tipo)

    driver.find_element_by_id("frmPrincipal:lnkTxtlistado").click()
    ban = True
    #print('descargo')
    time.sleep(1)
    driver.quit()    