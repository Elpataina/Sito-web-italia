# Iportiamo le librerie che abbiamo installato

import os

import sounddevice              # permette di registra l'audio

import speech_recognition       # permette di riconoscere il vocale e crea la trascrizione

import scipy.io.wavfile as wav  # permette di salvare il file

from google import genai

from google.genai import types

from dotenv import load_dotenv

import random



load_dotenv()

 

 

def registra_e_trascrivi():

    numero_segmenti_al_secondo = 44100

    durata_registrazione=3

    # Registra l'audio

    registrazione = sounddevice.rec(

        frames=(durata_registrazione * numero_segmenti_al_secondo),

        samplerate=numero_segmenti_al_secondo,

        channels=1,

        dtype='int16'

    )

    sounddevice.wait()
    # Salva il file WAV

    wav.write('registrazione_del_vocale.wav', numero_segmenti_al_secondo, registrazione)

    

    # Trascrive l'audio

    trascrittore = speech_recognition.Recognizer()

    with speech_recognition.AudioFile('registrazione_del_vocale.wav') as source:

        audio = trascrittore.record(source)

    

    trascrizione = trascrittore.recognize_google(audio, language='it-IT')

    return trascrizione


def traduci_con_gemini(testo: str, lingua_partenza: str, lingua_destinazione: str) -> str:

    client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

    # Rendiamo le istruzioni di sistema dinamiche basandoci sulle lingue passate

    system_prompt = (

        f"Sei un traduttore bilingue professionista ed esperto in {lingua_partenza} e {lingua_destinazione}. "

        f"Il testo inserito è in {lingua_partenza} (che potrebbe contenere espressioni gergali, dialettali o trascrizioni fonetiche). "

        f"Il tuo compito è tradurlo fedelmente in {lingua_destinazione}, mantenendo intatto il significato originale, "

        f"il tono e le sfumature culturali. Trova gli equivalenti idiomatici corretti invece di fare una traduzione letterale. "

        f"Restituisci ESCLUSIVAMENTE la traduzione pulita, senza introduzioni, note, spiegazioni o virgolette."

    )
        

    response = client.models.generate_content(

        model='gemini-2.5-flash',

        contents=system_prompt,

    )

    

    return response.text.strip()


def traduci_parole_con_gemini(testo: str, lingua_partenza: str, lingua_destinazione: str, parola: str):


    client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

    # Rendiamo le istruzioni di sistema dinamiche basandoci sulle lingue passate

    word_prompt = (

        f"Sei un traduttore bilingue professionista ed esperto in {lingua_partenza} e {lingua_destinazione}. "

        f"Il tuo compito è quello di generare una parola casuale in {lingua_partenza} e tradurla fedelmente in {lingua_destinazione}, mantenendo intatto il significato originale."

        f"Dovrai essere PRECISISSIMO E ESTREMAMENTE FEDELE, non accettare sinonimi o parole simili: la parola da tradurre in questione è {parola}"
    )


        
    responseword = client.models.generate_content(

        model='gemini-2.5-flash',

        contents=word_prompt,
    )

    parola = responseword.text.strip()


    system_prompt = (

        f"Sei un traduttore bilingue professionista ed esperto in {lingua_partenza} e {lingua_destinazione}. "

        f"Il tuo compito è il seguente: tradurre esattamente la parola {parola} da {lingua_partenza} a {lingua_destinazione}, mantenendo intatto il significato originale"

        f"Dovrai essere PRECISISSIMO E ESTREMAMENTE FEDELE, non accettare sinonimi o parole simili: la parola da tradurre in questione è {parola}"

        f"esegui una traduzione letterale senza spazi, virgolette o alcun segno di puntegiatura: restituisci solamente la parola richiesta"

        f"Restituisci ESCLUSIVAMENTE la traduzione pulita, senza introduzioni, note, spiegazioni o virgolette."

    )




    response = client.models.generate_content(

        model='gemini-2.5-flash',

        contents=system_prompt,

    )

    return response.text.strip()




