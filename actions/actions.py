# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
import csv
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Hello World!")

        return []

class ActionServiceListInfo(Action):
    """
    Action to retrieve and list all available services from a CSV file.
    
    @return: A list containing a SlotSet action for 'service_list'.
    """

    def name(self) -> str:
        """
        Defines the name of the action for reference in the Rasa domain.

        @return: The name of the action as a string.
        """
        return "action_service_list_info"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict) -> list:
        """
        Reads service names from a CSV file, formats them into a message, and sends it to the user. 
        Updates the 'service_list' slot with the list of services.

        @param dispatcher: The dispatcher used to send messages back to the user.
        @param tracker: The tracker instance containing the conversation state.
        @param domain: The domain dictionary containing action and intent definitions.
        
        @return: A list containing the SlotSet action with the updated 'service_list'.
        """
        services = []
        # Opens the CSV file containing service data
        with open('data/csv/servizio.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            # Reads each row and appends the service name to the services list
            for row in reader:
                services.append(row['nome'])

        # Joins all service names into a single string
        service_list = ", ".join(services)
        # Sends the list of services to the user
        dispatcher.utter_message(text=f"Ecco i servizi disponibili: {service_list}. Vuoi maggiori dettagli su uno di questi servizi?")
        # Updates the 'service_list' slot with the list of services
        return [SlotSet("service_list", service_list)]


class ActionServiceDetail(Action):
    """
    Action to provide detailed information about a specific service selected by the user.
    
    @return: An empty list if the service is not found or a message is sent to the user.
    """

    def name(self) -> str:
        """
        Defines the name of the action for reference in the Rasa domain.

        @return: The name of the action as a string.
        """
        return "action_service_detail"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict) -> list:
        """
        Retrieves the selected service from the slot, searches for its details in a CSV file, 
        and sends the details to the user. If the service is not found, informs the user.

        @param dispatcher: The dispatcher used to send messages back to the user.
        @param tracker: The tracker instance containing the conversation state.
        @param domain: The domain dictionary containing action and intent definitions.

        @return: An empty list if no service is found or a SlotSet action if details are provided.
        """
        # Retrieves the service name from the slot
        service_name = tracker.get_slot('service')
        if not service_name:
            # If no service is specified, asks the user to repeat
            dispatcher.utter_message(text="Non ho capito quale servizio ti interessa. Puoi ripetere?")
            return []

        # Normalizes the service name from the slot (lowercase and strip whitespace)
        service_name = service_name.lower().strip()

        service_detail = None
        # Opens the CSV file containing service data
        with open('data/csv/servizio.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            # Iterates over each row in the CSV file
            for row in reader:
                # Normalizes the service name from the CSV file
                csv_service_name = row['nome'].lower().strip()
                # Checks for an exact match with the requested service
                if csv_service_name == service_name:
                    service_detail = row['descrizione']
                    break

        # Sends the service details to the user if found
        if service_detail:
            dispatcher.utter_message(text=f"Ecco i dettagli del servizio '{service_name}': {service_detail}")
        else:
            # Informs the user if the service was not found
            dispatcher.utter_message(text=f"Mi dispiace, non ho trovato dettagli per il servizio '{service_name}'.")
        return []
