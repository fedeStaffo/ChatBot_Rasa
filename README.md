# ChatBot_Rasa

## Instructions for Collaborators

### Setting up a Virtual Environment

1. Ensure you have Python 3.9.13 installed. You can download it from [python.org](https://www.python.org/).
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

### Rasa Project Structure

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
