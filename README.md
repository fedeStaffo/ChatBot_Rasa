# ElderCare Chatbot

ElderCare is a chatbot designed to assist elderly users or their caregivers by providing information about various services, making bookings, and consulting the history of requested services. The primary goal of ElderCare is to offer a user-friendly interface that helps elderly individuals access essential services and information with ease.

## How to run the chatbot


1. Train a Rasa model containing the Rasa NLU and Rasa Core models by running:
    ```bash
    rasa train
    ```
    The model will be stored in the `/models` directory as a zipped file.

1. Run an instance of [duckling](https://rasa.com/docs/rasa/nlu/components/#ducklingentityextractor)
   on port 8000 by either running the docker command
    ```bash
    docker run -p 8000:8000 rasa/duckling
    ```
   or [installing duckling](https://github.com/facebook/duckling#requirements) directly on your machine and starting the server.

1. Test the assistant by running:
    ```bash
    rasa run actions
    python load_env.py && rasa run -m models --endpoints endpoints.yml
    ```
    This will load the assistant in your command line for you to chat.

1. *Start the ngrok gateway [Optional]*: in another terminal run
    ```bash
    ngrok http 5005 
    ```
    This will assign you a public ngrok https URL. Put it inside [`credentials.yml`](credentials.yml) in the `webhook_url` field. Then update the Telegram's bot webhook URL running in your terminal
    ```bash
    curl -X POST "https://api.telegram.org/bot<TOKEN>/setWebhook" -d "<YOUR_NGROK_URL>"
    ```
    The `TOKEN` can be read in the `access_token` field in the [`credentials.yml`](credentials.yml) file.

Once the chatbot is ready, you can use it accessing the [@ElderCare_bot](https://web.telegram.org/k/#@ElderCare_bot) bot.



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

## Training the Model

To train the Rasa model, run the following command:
```bash
rasa train
```

## Custom Actions

The custom actions are defined in `actions/actions.py`. These actions are used to fetch information from external sources, such as a CSV file, and provide detailed responses to the user.

### Booking Form and Actions

The booking process is managed using a form and several custom actions. The form collects necessary information from the user, such as the service they want to book, the location, time, and any additional requirements like transportation or medical assistance.

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
```
