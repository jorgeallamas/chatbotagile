# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher

class ActionSayBartleProfile(Action):

    bartle_answer_points = {
        "preg1": {
            "a": "S",
            "b": "A"
        },
        "preg2": {
            "a": "A",
            "b": "S"
        },
        "preg3": {
            "a": "S",
            "b": "A"
        },
        "preg4": {
            "a": "A",
            "b": "S"
        },
        "preg5": {
            "a": "S",
            "b": "A"
        },
        "preg6": {
            "a": "S",
            "b": "A"
        },
        "preg7": {
            "a": "S",
            "b": "A"
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
            "b": "E"
        },
        "preg12": {
            "a": "S",
            "b": "E"
        },
        "preg13": {
            "a": "S",
            "b": "E"
        },
        "preg14": {
            "a": "K",
            "b": "S"
        },
        "preg15": {
            "a": "S",
            "b": "K"
        }
    }

    def name(self) -> Text:
        return "action_say_bartle_profile"

    @staticmethod
    def answers_slots() -> List[Text]:
        return [
            "preg1", "preg2", "preg3", "preg4", "preg5",
            "preg6", "preg7", "preg8", "preg9", "preg10",
            "preg11", "preg12", "preg13", "preg14", "preg15",
            #"preg16", "preg17", "preg18", "preg19", "preg20",
            #"preg21", "preg22", "preg23", "preg24", "preg25",
            #"preg26", "preg27", "preg28", "preg29", "preg30", 
        ]

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:


        profiles = {
            "killer": 0,
            "achiever": 0,
            "socialiser": 0,
            "explorer": 0
        }

        for answer in self.answers_slots():
            current_answer = self.bartle_answer_points[answer][tracker.get_slot(answer)]
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

        dispatcher.utter_message(text=msg)

        return []
