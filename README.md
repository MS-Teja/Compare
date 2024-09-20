# Price Comparison

## Description
Compare prices between Flipkart and Amazon using Parsera library.

## Requirements
You will need an OpenAI API key.
You will have to install Node.js and Python on your device.

## Installation
Step-by-step instructions on how to get the development environment running.

1. Clone the repository:
    ```sh
    git clone https://github.com/MS-Teja/compare.git
    ```
2. Navigate to the project directory:
    ```sh
    cd compare
    ```
3. Install dependencies for frontend:
    ```sh
    npm install
    ```
4. Create and activate a virtual environment for backend:
    On Mac, use:
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```
    On Windows, use:
    ```
    python3 -m venv venv
    .venv\Scripts\activate
    ```

5. Install dependencies for backend:
    ```sh
    pip install -r requirements.txt
    ```
6. Install Playwright browsers:
    ```sh
    playwright install
    ```
7. Create a `.env` file in the backend directory and add your OpenAI API key:
    ```sh
    echo "OPENAI_API_KEY=your_openai_api_key" > Backend/.env
    ```
    Replace your_openai_api_key with your OpenAI API key.

## Usage
Instructions and examples for using the project.

1. For Backend
    ```
    cd Backend
    python app.py
    ```
    or
    ```
    cd Backend
    python3 app.py
    ```
    Make sure the virtual environment is activated

2. For Frontend
    ```sh
    npm run dev
    ```

## License
This project is licensed under the MIT License - see the LICENSE file for details.

