# Google Scholar Scraper and Visualizer

This project is a web application built with Flask that scrapes data from Google Scholar, processes the data, and visualizes trends and co-authorship networks using Plotly and NetworkX.

## Features

- Scrape publication data from Google Scholar based on a search query.
- Clean and process the scraped data.
- Visualize publication trends over time with an interactive line chart.
- Visualize co-authorship networks with an interactive network graph.

## Installation

To run this project locally, follow these steps:

1. **Clone the repository:**

    ```sh
    git clone https://github.com/your-username/google-scholar-scraper.git
    cd google-scholar-scraper
    ```

2. **Set up a virtual environment (optional but recommended):**

    ```sh
    python -m venv venv
    source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
    ```

3. **Install the required packages:**

    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. **Run the Flask application:**

    ```sh
    python app.py
    ```

2. **Open your browser and navigate to:**

    ```
    http://127.0.0.1:5000/
    ```

3. **Enter a search query and submit the form:**

    The application will scrape Google Scholar for the specified search query, process the data, and display visualizations of publication trends and co-authorship networks.

## Project Structure

Here's a sample README file for your GitHub repository. Save this content as README.md in your project directory.

markdown

# Google Scholar Scraper and Visualizer

This project is a web application built with Flask that scrapes data from Google Scholar, processes the data, and visualizes trends and co-authorship networks using Plotly and NetworkX.

## Features

- Scrape publication data from Google Scholar based on a search query.
- Clean and process the scraped data.
- Visualize publication trends over time with an interactive line chart.
- Visualize co-authorship networks with an interactive network graph.

## Installation

To run this project locally, follow these steps:

1. **Clone the repository:**

    ```sh
    git clone https://github.com/your-username/google-scholar-scraper.git
    cd google-scholar-scraper
    ```

2. **Set up a virtual environment (optional but recommended):**

    ```sh
    python -m venv venv
    source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
    ```

3. **Install the required packages:**

    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. **Run the Flask application:**

    ```sh
    python app.py
    ```

2. **Open your browser and navigate to:**

    ```
    http://127.0.0.1:5000/
    ```

3. **Enter a search query and submit the form:**

    The application will scrape Google Scholar for the specified search query, process the data, and display visualizations of publication trends and co-authorship networks.

## Project Structure

google-scholar-scraper/
│
├── templates/
│ ├── index.html # Homepage with search form
│ ├── result.html # Results page with visualizations
│
├── app.py # Main application file
├── requirements.txt # List of required Python packages
└── README.md # Project README file


## Dependencies

- Flask
- pandas
- requests
- BeautifulSoup
- plotly
- networkx

You can install the dependencies using the `requirements.txt` file:

```sh
pip install -r requirements.txt
