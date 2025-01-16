# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

import csv
from typing import Any, List, Dict, Text
from rasa_sdk import Action
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.interfaces import Tracker
import random
from datetime import datetime, timedelta

# This is a simple example for a custom action which utters "Hello World!"
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
        """
        services = []
        # Opens the CSV file containing service data
        with open('data/csv/servizi.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            # Reads each row and appends the service name to the services list
            for row in reader:
                services.append(row['nome'])

        # Joins all service names into a single string
        service_list = ", ".join(services)
        # Sends the list of services to the user
        dispatcher.utter_message(text=f"Ecco i servizi disponibili: {service_list}. Vuoi maggiori dettagli su uno di questi servizi?")
        return []


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
        with open('data/csv/servizi.csv', newline='', encoding='utf-8') as csvfile:
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

class ActionSetServiceLocation(Action):
    """
    Action to determine the location type ('home' or 'outside') for a specified service.
    
    This action checks the service name provided by the user and retrieves the associated 
    location information ('home' or specific location) from a CSV file. If the service is 
    found, the slot 'location' is updated with the location type. If the service is outside, 
    it asks the user to choose a specific location from a list.
    
    After the location is provided, the action confirms the booking if the location is 'home'.
    If the location is outside, the user is asked to select a specific location.
    
    @param dispatcher: CollectingDispatcher - Sends messages back to the user.
    @param tracker: Tracker - Tracks the conversation state and slots.
    @param domain: Dict[Text, Any] - Contains the domain configuration.
    
    @return: List[Dict[Text, Any]] - A list of events to update the conversation state.
    """
    def name(self) -> Text:
        """
        Returns the name of the action.

        @return: The name of the action as a string.
        """
        return "action_set_service_location"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Retrieves the service name from the slot
        service_name = tracker.get_slot('service')
        
        # If the service is not provided, ask the user to specify it
        if not service_name:
            dispatcher.utter_message(text="Non ho capito quale servizio desideri. Puoi ripetere?")
            return []

        # Normalize the service name from the slot
        service_name = service_name.lower().strip()
        location = None

        # Open the CSV file and search for the matching service
        with open('data/csv/servizi.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Normalize the service name from the CSV
                csv_service_name = row['nome'].lower().strip()
                if csv_service_name == service_name:
                    location = row['luogo']
                    break

        # If the service is at home, confirm the booking
        if location == "casa":
            dispatcher.utter_message(text=f"Hai selezionato il servizio '{service_name}' a casa. Hai preferenze sul sesso dell'operatore? (m/f)")
            return [SlotSet("location", location)]

        # If the service is outside, ask for the specific location
        elif location:
            locations = []
            with open('data/csv/luoghiAncona.csv', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    if row['tipo'].lower().strip() == service_name:
                        # Append the available locations for the service
                        locations.append(f"{row['nome'].lower()} - {row['indirizzo']} ({row['orario']})")

            # Prepare the list of locations and ask the user to choose one
            location_list = "\n".join(locations)
            dispatcher.utter_message(text=f"Per il servizio '{service_name}', ecco i luoghi disponibili:\n{location_list}\nDove vuoi andare?")
            return []  # Do not set the slot yet, waiting for user input

        else:
            # If no location is found for the service, inform the user
            dispatcher.utter_message(text=f"Mi dispiace, non ho trovato dettagli per il servizio '{service_name}'. Riprova.")
            return []

def is_time_overlap(user_time: str, operator_time: str) -> bool:
    """
    Check if the user's time overlaps with the operator's time.
    @param user_time: Time range chosen by the user (e.g., '14:00-16:30', 'mattina', or 'alle 15')
    @param operator_time: Time range available for the operator (e.g., '14:00-16:30')
    @return: True if the times overlap, False otherwise
    """
    # Define time ranges for generic times
    generic_times = {
        'mattina': ('08:00', '12:00'),
        'pomeriggio': ('12:00', '18:00'),
        'sera': ('18:00', '22:00')
    }

    def time_to_tuple(time_str: str):
        if '-' in time_str:  # Specific time range
            start, end = time_str.split('-')
        elif time_str in generic_times:  # Generic time range (e.g., "mattina")
            start, end = generic_times[time_str]
        else:  # Specific time point (e.g., "alle 15")
            start = time_str
            end = (datetime.strptime(time_str, '%H:%M') + timedelta(hours=1)).strftime('%H:%M')
        return start, end

    user_start, user_end = time_to_tuple(user_time)
    operator_start, operator_end = time_to_tuple(operator_time)

    # Check if the user time range overlaps with the operator's time range
    return not (user_end <= operator_start or user_start >= operator_end)

class ActionFindAvailableOperator(Action):
    def name(self) -> Text:
        return "action_find_available_operator"

    def run(self, dispatcher, tracker, domain) -> List[Dict[Text, Any]]:
        """
        Finds an available operator based on user preferences and time slot.
        """
        # Retrieve user preferences from slots
        sex = tracker.get_slot("sex")  # e.g., 'M' or 'F'
        car = tracker.get_slot("car")  # e.g., 'si' or 'no'
        med = tracker.get_slot("med")  # e.g., 'si' or 'no'
        #language = tracker.get_slot("language")  # e.g., 'inglese'
        language = None
        time = tracker.get_slot("time")  # e.g., '14:00-16:30' or 'mattina'

        available_operators = []

        try:
            # Open and read the CSV file containing operator data
            with open('data/csv/operatori.csv', mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    # Check if operator meets all preferences
                    if (row['sesso'] == sex or sex is None) and \
                            (row['automunito'] == car or car is None) and \
                            (row['linguaggi'] == language or language is None) and \
                            (row['competenze_mediche'] == med or med is None):

                        # Check if the user's time overlaps with the operator's available time
                        if is_time_overlap(time, row['fascia_oraria']):
                            available_operators.append(row)

            if available_operators:
                # Choose a random operator from the available ones
                chosen_operator = random.choice(available_operators)
                name = chosen_operator['nome']
                surname = chosen_operator['cognome']

                # Save the operator in the slot and notify the user
                dispatcher.utter_message(f"Ho trovato un operatore disponibile: {name} {surname}. Conferma se per te va bene.")
                return [SlotSet("operator", f"{name} {surname}")]
            else:
                # If no operator is available, inform the user
                dispatcher.utter_message("Mi dispiace, non sono riuscito a trovare un operatore disponibile che corrisponda alle tue preferenze e all'orario richiesto.")
                return [SlotSet("operator", None)]

        except FileNotFoundError:
            dispatcher.utter_message("Errore: il file degli operatori non è stato trovato.")
            return [SlotSet("operator", None)]

        except Exception as e:
            dispatcher.utter_message(f"Si è verificato un errore: {str(e)}")
            return [SlotSet("operator", None)]
