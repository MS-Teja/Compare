from flask import Flask, request, jsonify, Response
from parsera import Parsera
import os
from dotenv import load_dotenv
import logging
from flask_cors import CORS
import time
from queue import Queue

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

status_queue = Queue()

def status_producer():
    while True:
        message = status_queue.get()
        if message == "DONE":
            break
        yield f"data: {message}\n\n"
    yield "data: DONE\n\n"

@app.route('/status')
def status():
    return Response(status_producer(), content_type='text/event-stream')

def send_status(message):
    status_queue.put(message)

def scrape_data(url, source):
    logger.debug(f"Scraping data from URL: {url}")
    send_status(f"Searching on {source}...")

    elements = {
        "Title": "Product title",
        "Price": "Product price",
        "Availability": "Product availability",
        "Url": "Product URL"
    }

    try:
        scraper = Parsera()
        data = scraper.run(url=url, elements=elements)

        for item in data:
            if "Price" in item and item["Price"]:
                item["Price"] = f"₹{item['Price'].replace(',', '').replace('₹', '')}"
            if "Availability" not in item:
                item["Availability"] = "Unavailable"
            if "Url" in item and item["Url"]:
                if source == "Amazon":
                    if not item["Url"].startswith("http"):
                        item["Url"] = f"https://www.amazon.in{item['Url']}"
                elif source == "Flipkart":
                    if not item["Url"].startswith("http"):
                        item["Url"] = f"https://www.flipkart.com{item['Url']}"

        send_status(f"Found {len(data)} items on {source}")
        return data
    except Exception as e:
        logger.error(f"Error scraping data: {e}")
        send_status(f"Error occurred while searching on {source}")
        return []

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    keywords = request.args.get('keywords', '').split(',')
    logger.debug(f"Received search query: {query}, keywords: {keywords}")

    if not query:
        logger.error("Query parameter is missing")
        return jsonify({"error": "Query parameter is required"}), 400

    send_status(f"Starting search for: {query}")

    amazon_url = f"https://www.amazon.in/s?k={query}"
    flipkart_url = f"https://www.flipkart.com/search?q={query}"

    amazon_data = scrape_data(amazon_url, "Amazon")
    flipkart_data = scrape_data(flipkart_url, "Flipkart")

    send_status("Filtering products based on keywords")
    # Filter products based on keywords and exact match
    def filter_products(products, keywords):
        filtered = []
        for product in products:
            if all(keyword.lower() in product['Title'].lower() for keyword in keywords):
                filtered.append(product)
        return filtered

    amazon_products = filter_products(amazon_data, keywords)
    flipkart_products = filter_products(flipkart_data, keywords)

    send_status(f"Found {len(amazon_products)} matching products on Amazon")
    send_status(f"Found {len(flipkart_products)} matching products on Flipkart")

    logger.debug(f"Amazon products: {amazon_products}")
    logger.debug(f"Flipkart products: {flipkart_products}")

    # Ensure single currency symbol
    for product in amazon_products + flipkart_products:
        product["Price"] = product.get("Price", "").replace("₹₹", "₹")

    send_status("DONE")
    return jsonify({
        "amazon": amazon_products if amazon_products else [{"Title": "Unavailable", "Price": None, "Availability": "Unavailable", "Url": None}],
        "flipkart": flipkart_products if flipkart_products else [{"Title": "Unavailable", "Price": None, "Availability": "Unavailable", "Url": None}]
    })

if __name__ == "__main__":
    logger.debug("Starting Flask server")
    app.run(port=5000)

