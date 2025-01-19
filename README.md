# ElderCare Chatbot

ElderCare is a chatbot designed to assist elderly users or their caregivers by providing information about various services, making bookings, and consulting the history of requested services. The primary goal of ElderCare is to offer a user-friendly interface that helps elderly individuals access essential services and information with ease.

## Functionalities

- **Greet Users**: The chatbot can greet users and provide a friendly introduction.
- **Service Information**: Users can inquire about the various services offered, and the chatbot will provide detailed information.
- **Service Details**: Users can request detailed information about a specific service, including possible locations and timings.
- **Booking Services**: The chatbot can assist users in booking services by collecting necessary information and confirming the booking.
- **Stop Booking**: Users can stop the booking process at any time, and the chatbot will handle the interruption gracefully.
- **App Information**: The chatbot can provide information about the ElderCare app, its history, and the operators.
- **Security Information**: Users can inquire about the security measures in place to ensure their safety.
- **Mood Handling**: The chatbot can respond to users' moods, providing cheerful responses or comforting messages as needed.
- **Goodbye Messages**: The chatbot can say goodbye to users, ensuring a polite end to the conversation.
- **Bot Challenge**: Users can ask if they are talking to a bot, and the chatbot will confirm its identity.

## Project Setup

### Setting up a Virtual Environment

1. Ensure you have Python 3.9.13 installed. You can download it from [python.org](https://www.python.org/downloads/release/python-3913/).
2. Verify the installed versions:
    ```sh
    py -0
    ```
    This will list all the Python versions installed on your system.
3. Navigate to the project directory:
    ```sh
    cd /path/to/Chatbot_Rasa
    ```
4. Create a virtual environment using a compatible Python version:
    ```sh
    py -3.9 -m venv rasa_env
    ```
5. Activate the virtual environment:
    - On Windows:
        ```sh
        rasa_env\Scripts\activate
        ```
    - On macOS/Linux:
        ```sh
        source rasa_env/bin/activate
        ```

### Installing Rasa

1. Ensure the virtual environment is activated.
2. Install Rasa:
    ```sh
    pip install rasa
    ```
3. Verify the installation:
    ```sh
    rasa --version
    ```

### Required Versions

- Rasa Version: 3.6.20
- Minimum Compatible Version: 3.5.0
- Rasa SDK Version: 3.6.2
- Python Version: 3.9.13

### Installing Dependencies

You can also install all required dependencies using the `requirements.txt` file:
1. Ensure the virtual environment is activated.
2. Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```

### Updating `requirements.txt`

If you add new dependencies or update existing ones, you should update the `requirements.txt` file:
1. Ensure the virtual environment is activated.
2. Install or update the required packages.
3. Freeze the current environment's packages to `requirements.txt`:
    ```sh
    pip freeze > requirements.txt
    ```

## Rasa Project Structure

- `actions/`: Contains custom action code.
- `data/`: Contains training data for NLU and Core.
  - `nlu.yml`: Contains NLU training data.
  - `stories.yml`: Contains training stories for Rasa Core.
  - `rules.yml`: Contains rules for Rasa Core.
- `models/`: Contains trained models.
- `config.yml`: Configuration file for Rasa NLU and Core.
- `credentials.yml`: Contains credentials for external services.
- `domain.yml`: Defines the domain of the assistant including intents, entities, slots, and responses.
- `endpoints.yml`: Configuration for connecting to external services.

## Training the Model

To train the Rasa model, run the following command:
```bash
rasa train
```

## Running the Chatbot

### Start the Action Server

First, start the action server in one terminal:
```bash
rasa run actions
```

### Start the Rasa Server

In another terminal, start the Rasa server:
```bash
rasa run --endpoints endpoints.yml
```

### Using the Rasa Shell

To interact with the chatbot using the Rasa shell, run:
```bash
rasa shell
```

This will allow you to test the chatbot and see how it responds to various inputs.

## Custom Actions

The custom actions are defined in `actions/actions.py`. These actions are used to fetch information from external sources, such as a CSV file, and provide detailed responses to the user.

### Booking Form and Actions

The booking process is managed using a form and several custom actions. The form collects necessary information from the user, such as the service they want to book, the location, time, and any additional requirements like transportation or medical assistance.

#### Form Definition

The form is defined in the `domain.yml` file under the `forms` section:

```yaml
forms:
  booking_form:
    required_slots:
    - service
    - location
    - time
    - car
    - med
    - operator
```

#### Custom Actions

Several custom actions are used to handle different parts of the booking process. These actions are defined in `actions/actions.py`.

1. **AskForServiceAction**: This action asks the user which service they want to book.

```python
class AskForServiceAction(Action):
    def name(self) -> Text:
        return "action_ask_service"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict) -> List[EventType]:
        dispatcher.utter_message(text="Quale servizio vuoi prenotare?")
        return []
```

2. **AskForLocationAction**: This action asks the user for the location.

3. **AskForTimeAction**: This action asks the user for the time.

4. **AskForCarAction**: This action asks the user if they need transportation using buttons for saving boolean values.

```python
class AskForCarAction(Action):
    def name(self) -> Text:
        return "action_ask_car"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict) -> List[EventType]:
        dispatcher.utter_message(
            text="Hai bisogno di trasporto?",
            buttons=[
                {"title": "sì", "payload": "/affirm"},
                {"title": "no", "payload": "/deny"},
            ],
        )
        return []
```

5. **AskForMedAction**: This action asks the user if they need medical assistance in the same way of ask for car.

6. **AskForOperatorAction**: This action assigns an operator and asks the user to confirm the assigned operator.

```python
class AskForOperatorAction(Action):
    def name(self) -> Text:
        return "action_ask_operator"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict) -> List[EventType]:
        operator = tracker.get_slot('operator')
        if operator is None:
            operator = self.assign_operator(dispatcher, tracker, domain)
        dispatcher.utter_message(
            text=f"L'operatore assegnato è {operator}. Confermi?",
            buttons=[
                {"title": "sì", "payload": "/affirm"},
                {"title": "no", "payload": "/deny"},
            ],
        )
        return []

    def assign_operator(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> str:
        """Assign a random available operator based on the selected time, car, and med slots."""
        time_slot = tracker.get_slot('time')
        car_needed = tracker.get_slot('car')
        med_needed = tracker.get_slot('med')

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
                    available_operators.append(f"{row['nome']} {row['cognome']}")

        if not available_operators:
            dispatcher.utter_message(text="Mi dispiace, non ci sono operatori disponibili per l'orario e i requisiti selezionati.")
            return None

        selected_operator = random.choice(available_operators)
        dispatcher.utter_message(text=f"L'operatore assegnato è {selected_operator}.")
        return selected_operator

    def is_time_overlap(self, time1: str, time2: str) -> bool:
        """Check if two time ranges overlap."""
        start1, end1 = time1.split('-')
        start2, end2 = time2.split('-')
        return max(start1, start2) < min(end1, end2)
```

7. **ValidateBookingForm**: This action validates the slots once all slots are filled.