# -*- coding: utf-8 -*-
from chatterbot.trainers import ListTrainer
from chatterbot import ChatBot

import os

chatbot = ChatBot("Spin3")

#Treino do Spin3
for arq in os.listdir('chat'):
    lines = open('chat/'+ arq, 'r').readlines()
    trainer = ListTrainer(chatbot)
    trainer.train(lines)
