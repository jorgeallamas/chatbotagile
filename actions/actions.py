# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import json
import os

bartle_slots = [
            "preg1", "preg2", "preg3", "preg4", "preg5",
            "preg6", "preg7", "preg8", "preg9", "preg10",
            "preg11", "preg12", "preg13", "preg14", "preg15",
            #"preg16", "preg17", "preg18", "preg19", "preg20",
            #"preg21", "preg22", "preg23", "preg24", "preg25",
            #"preg26", "preg27", "preg28", "preg29", "preg30", 
        ]

bartle_answer_points = {
        "preg1": {
            "a": "S",
            "b": "A"
        },
        "preg2": {
            "a": "S",
            "b": "A"
        },
        "preg3": {
            "a": "A",
            "b": "S"
        },
        "preg4": {
            "a": "S",
            "b": "A"
        },
        "preg5": {
            "a": "S",
            "b": "A"
        },
        "preg6": {
            "a": "S",
            "b": "E"
        },
        "preg7": {
            "a": "S",
            "b": "E"
        },
        "preg8": {
            "a": "S",
            "b": "E"
        },
        "preg9": {
            "a": "S",
            "b": "E"
        },
        "preg10": {
            "a": "S",
            "b": "E"
        },
        "preg11": {
            "a": "S",
            "b": "K"
        },
        "preg12": {
            "a": "S",
            "b": "K"
        },
        "preg13": {
            "a": "K",
            "b": "S"
        },
        "preg14": {
            "a": "K",
            "b": "S"
        },
        "preg15": {
            "a": "S",
            "b": "K"
        },
        "preg16": {
            "a": "E",
            "b": "A"
        },
        "preg17": {
            "a": "E",
            "b": "A"
        },
        "preg18": {
            "a": "A",
            "b": "E"
        },
        "preg19": {
            "a": "E",
            "b": "A"
        },
        "preg20": {
            "a": "E",
            "b": "A"
        },
        "preg21": {
            "a": "E",
            "b": "K"
        },
        "preg22": {
            "a": "E",
            "b": "K"
        },
        "preg23": {
            "a": "E",
            "b": "K"
        },
        "preg24": {
            "a": "E",
            "b": "K"
        },
        "preg25": {
            "a": "E",
            "b": "K"
        },
        "preg26": {
            "a": "A",
            "b": "K"
        },
        "preg27": {
            "a": "K",
            "b": "A"
        },
        "preg28": {
            "a": "K",
            "b": "A"
        },
        "preg29": {
            "a": "A",
            "b": "K"
        },
        "preg30": {
            "a": "A",
            "b": "K"
        }
    }

# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

class ActionResetBartleSlots(Action):

    def name(self) -> Text:
        return "action_reset_bartle_slots"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        slots_to_none = []

        for bartle_slot in bartle_slots:
            slots_to_none.append(SlotSet(bartle_slot, None))

        return slots_to_none

class ActionSayBartleProfile(Action):

    def name(self) -> Text:
        return "action_say_bartle_profile"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:


        profiles = {
            "killer": 0,
            "achiever": 0,
            "socialiser": 0,
            "explorer": 0
        }

        for answer in bartle_slots:
            current_answer = bartle_answer_points[answer][tracker.get_slot(answer)]
            if (current_answer == "K"):
                profiles["killer"] += 1
            elif (current_answer == "A"):
                profiles["achiever"] += 1
            elif (current_answer == "S"):
                profiles["socialiser"] += 1
            elif (current_answer == "E"):
                profiles["explorer"] += 1
        
        profile = max(profiles, key=profiles.get)
        msg = "Según el test de Bartle, tu perfil de jugador es: " + profile
        self.addProfile("profiles.json",tracker.current_state()['sender_id'],profile)

        dispatcher.utter_message(text=msg)

        self.insert_profile("perfiles.txt", profile, tracker)

        return []

    def insert_profile(self, path, profile, tracker):
        file = open(path,'a')
        file.write("ID user: " + tracker.current_state()['sender_id'] + '\n' + "Profile user: " + profile + '\n' + '\n')
        file.close()
    
    def addProfile (self,file,sendID,profile):
        try:
            file = open(file,'r+')#Intento abrir el archivo de lectura y escritura, si existe
        except:
            file = open(file , 'w+')#Salta al catch y crea un archivo de escritura/lectura
            file.write("{\n \t \"Profiles\": [ \n \t ] \n }" )#Escribo la cabecera del JSON
        finally:
            file.seek(0,0) #Reseteo el archivo para que lea todo el contenido, ya que si viene del except ya se generó contenido
            contentFile = file.read() #Vuelco el contenido del archivo en una variable
            decodedJSON = json.loads(contentFile) #decodedJSON obtiene en formato JSON lo de contentFile
            newProfile = "{\"ID\" : " + (str)(sendID) + "\n \"Profile\" : " + "\"" + profile + "\" " + "\n }"#newProfile posee el contenido del perfil ingresado (en formato JSON)
            if(len(decodedJSON["Profiles"]) == 0): #Se hace este chequeo para que el primer perfil no tenga una coma de prefijo
                decodedJSON["Profiles"].append(newProfile)
            else:
                decodedJSON["Profiles"].append(", \n" + newProfile)

            encodedJSON = json.dumps(decodedJSON) #Transforma el JSON en String para que se guarde en el archivo
            file.seek(0,0) #Reseteo el archivo para que se reescriba desde el principio
            file.write(encodedJSON) #Escribo en el archivo el StringfyJSON
            file.close() #Se cierra el archivo    

        