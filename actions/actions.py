# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

import csv
from typing import Any, List, Dict, Text
from rasa_sdk import Action
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.interfaces import Tracker
import random
from rasa_sdk.forms import FormValidationAction
from rasa_sdk.types import DomainDict
from rasa_sdk.events import EventType
from rasa_sdk.events import SlotSet

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
        dispatcher.utter_message(text=f"Ecco i servizi disponibili: {                                 service_list}. Vuoi maggiori dettagli su uno di questi servizi?")
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
            dispatcher.utter_message(
                text="Non ho capito quale servizio ti interessa. Puoi ripetere?")
            return []

        # Normalizes the service name from the slot (lowercase and strip whitespace)
        service_name = service_name.lower().strip()

        service_detail = None
        possible_locations = []
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

        # Opens the CSV file containing location data
        with open('data/csv/luoghiAncona.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            # Iterates over each row in the CSV file
            for row in reader:
                if row['tipo'].lower() == service_name:
                    possible_locations.append(
                        f"{row['nome']} - {row['indirizzo']} - {row['orario']}")

        # Sends the service details and possible locations to the user if found
        if service_detail:
            locations_text = "\n".join(possible_locations)
            dispatcher.utter_message(text=f"Ecco i dettagli del servizio '{service_name}': {                                     service_detail}.\n\nPossibili luoghi:\n{locations_text}")
        else:
            # Informs the user if the service was not found
            dispatcher.utter_message(
                text=f"Mi dispiace, non ho trovato dettagli per il servizio '{service_name}'.")
        return []


class AskForServiceAction(Action):
    def name(self) -> Text:
        return "action_ask_service"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict) -> List[EventType]:
        dispatcher.utter_message(text="Quale servizio vuoi prenotare?")
        return []


class AskForLocationAction(Action):
    def name(self) -> Text:
        return "action_ask_location"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict) -> List[EventType]:
        dispatcher.utter_message(text="Per favore, specifica una località.")
        return []


class AskForTimeAction(Action):
    def name(self) -> Text:
        return "action_ask_time"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict) -> List[EventType]:
        dispatcher.utter_message(
            text="Per favore, specifica un orario nel formato HH:MM-HH:MM.")
        return []


class AskForCarAction(Action):
    def name(self) -> Text:
        return "action_ask_car"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict) -> List[EventType]:
        dispatcher.utter_message(
            text="Hai bisogno di trasporto?",
            buttons=[
                {"title": "si", "payload": "/affirm"},
                {"title": "no", "payload": "/deny"},
            ],
        )
        return []


class AskForMedAction(Action):
    def name(self) -> Text:
        return "action_ask_med"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict) -> List[EventType]:
        dispatcher.utter_message(
            text="Hai bisogno di assistenza medica?",
            buttons=[
                {"title": "si", "payload": "/affirm"},
                {"title": "no", "payload": "/deny"},
            ],
        )
        return []


class ValidateBookingForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_booking_form"

    def validate_service(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `service` value."""
        allowed_services = []
        with open('data/csv/servizi.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                allowed_services.append(row['nome'].lower())

        if slot_value.lower() not in allowed_services:
            dispatcher.utter_message(text=f"Il servizio '{                                     slot_value}' non è disponibile. I servizi disponibili sono: {', '.join(allowed_services)}.")
            return {"service": None}
        dispatcher.utter_message(
            text=f"OK! Hai scelto il servizio {slot_value}.")
        return {"service": slot_value}

    def validate_location(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `location` value."""
        service = tracker.get_slot('service')
        if service:
            with open('data/csv/servizi.csv', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    if row['nome'].lower() == service.lower() and row['luogo'].lower() == 'casa':
                        dispatcher.utter_message(
                            text="Il servizio scelto è a casa, quindi la località sarà impostata su 'casa'.")
                        return {"location": "casa"}

        possible_locations = []
        with open('data/csv/luoghiAncona.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['tipo'].lower() == service.lower():
                    possible_locations.append(row['nome'].lower())

        if slot_value.lower() not in possible_locations:
            dispatcher.utter_message(text=f"Il luogo '{slot_value}' non è valido per il servizio '{                                     service}'. I luoghi disponibili sono: {', '.join(possible_locations)}.")
            return {"location": None}

        dispatcher.utter_message(
            text=f"OK! La località scelta è {slot_value}.")
        return {"location": slot_value}

    def validate_time(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `time` value."""
        import re
        time_pattern = re.compile(r'^\d{2}:\d{2}-\d{2}:\d{2}$')
        if not time_pattern.match(slot_value):
            dispatcher.utter_message(
                text="Per favore, specifica un orario nel formato HH:MM-HH:MM.")
            return {"time": None}
        dispatcher.utter_message(text=f"OK! L'orario scelto è {slot_value}.")
        return {"time": slot_value}

    def validate_car(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `car` value."""
        intent = tracker.latest_message['intent'].get('name')
        if intent == "affirm":
            dispatcher.utter_message(text="Hai bisogno di trasporto.")
            return {"car": True}
        elif intent == "deny":
            dispatcher.utter_message(text="Non hai bisogno di trasporto.")
            return {"car": False}
        else:
            dispatcher.utter_message(
                text="Non ho capito. Hai bisogno di trasporto?")
            return {"car": None}

    def validate_med(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `med` value."""
        intent = tracker.latest_message['intent'].get('name')
        if intent == "affirm":
            dispatcher.utter_message(text="Hai bisogno di assistenza medica.")
            return {"med": True}
        elif intent == "deny":
            dispatcher.utter_message(
                text="Non hai bisogno di assistenza medica.")
            return {"med": False}
        else:
            dispatcher.utter_message(
                text="Non ho capito. Hai bisogno di assistenza medica?")
            return {"med": None}

    def validate(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> List[Dict]:
        """Validate all slots."""
        slots = super().validate(dispatcher, tracker, domain)

        # Call ActionAssignOperator to assign an operator
        action_assign_operator = ActionAssignOperator()
        events = action_assign_operator.run(dispatcher, tracker, domain)
        for event in events:
            if isinstance(event, SlotSet) and event.key == "operator":
                slots.append({"operator": event.value})
                break

        return slots


class ActionAssignOperator(Action):
    def name(self) -> Text:
        return "action_assign_operator"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict) -> List[EventType]:
        time_slot = tracker.get_slot('time')
        car_needed = tracker.get_slot('car')
        med_needed = tracker.get_slot('med')

        if not time_slot:
            return []

        available_operators = []
        with open('data/csv/operatori.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if car_needed and row['automunito'].lower() != 'si':
                    continue
                if med_needed and row['competenze_mediche'].lower() != 'si':
                    continue
                operator_time = row['fascia_oraria']
                if self.is_time_overlap(time_slot, operator_time):
                    available_operators.append(
                        f"{row['nome']} {row['cognome']}")

        if not available_operators:
            dispatcher.utter_message(
                text="Mi dispiace, non ci sono operatori disponibili per l'orario e i requisiti selezionati. Puoi provare a cambiare i requisiti.")
            return [SlotSet("operator", "nessuno")]

        selected_operator = random.choice(available_operators)
        dispatcher.utter_message(text=f"Operatore assegnato: {                                 selected_operator}.")
        return [SlotSet("operator", selected_operator)]

    def is_time_overlap(self, time1: str, time2: str) -> bool:
        """Check if two time ranges overlap."""
        start1, end1 = time1.split('-')
        start2, end2 = time2.split('-')
        return max(start1, start2) < min(end1, end2)
