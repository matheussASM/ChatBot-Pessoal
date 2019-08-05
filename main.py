# -*- coding: utf-8 -*-
#Bibliotecas do Spin3
from chatterbot import ChatBot

from datetime import datetime

import os
import speech_recognition as sr
import pyttsx3
import wikipedia
import time

#Configurações do Spin3
speaker = pyttsx3.init()#Inicia a sintese de voz
chatbot = ChatBot("Spin3")#Escolhe o nome da IA
wikipedia.set_lang('pt-BR')#Escolhe a linguagem dos artigos pesquisados pela IA

def speak(text):
    speaker.say(text)
    speaker.runAndWait()

r = sr.Recognizer()

#Selecionado a voz para o Brasil
voices = speaker.getProperty('voices')

for voice in voices:
    if voice.name == 'brazil':
        speaker.setProperty('voice', voice.id)

#Dicionario de comandos
dic_cmds = {}

def load_cmds():#Abre e lê os comandos
    lines = open('cmd.txt', 'r').readlines()

    for line in lines:
        parts = line.split('***')
        dic_cmds.update({ parts[0] : parts[1] })

#Controle de comandos do Spin3
def evaluate (text):#Realiza a validação dos comandos
    result = None

    try:
        result = dic_cmds[text]
    except:
        result = None
    return result

def run_cmd(cmd_type):#Realiza a execução dos comandos
    result =None

    if cmd_type == 'asktime\n':
        now = datetime.now()
        result = 'São ' + str(now.hour) + ' horas e ' + str(now.minute) + ' minutos.'
    elif cmd_type == 'lerarq':
        arq = open('Log.txt', 'r')
        result = arq.read()
        arq.close()
    else:
        result = None
    return result

#Resposta informativas, com base na wikipedia
keywords = ['o que é', 'quem foi', 'descubra', 'me informe', 'defina', 'definição']

def get_answer(text):
    result = None

    if text is not None:
        for key in keywords:
            if text.startswith(key):
                result = text.replace(key,'')

    if result is not None:
        results = wikipedia.search(result)
        result = wikipedia.summary(results[0], sentences=1)
    return result

#Resposta do Spin3
load_cmds()
with sr.Microphone() as s:
    r.adjust_for_ambient_noise(s)
    while True:
            audio = r.listen(s)
            speech = r.recognize_google(audio, language='pt-BR').lower()
            response = run_cmd(evaluate(speech))
            if response == None:
                response = chatbot.get_response(speech)

            print(speech)
            print(response)
            speak(response)
