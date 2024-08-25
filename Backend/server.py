from flask import Flask, request, jsonify, Response
from parsera import Parsera
import os
from dotenv import load_dotenv
import logging
from flask_cors import CORS
import time

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

# Generator function to handle Server-Sent Events (SSE)
def generate_status_messages():
    try:
        while True:
            message = yield
            yield f"data: {message}\n\n"
            time.sleep(1)
    except GeneratorExit:
        pass

status_generator = generate_status_messages()
next(status_generator)

def scrape_data(url, source):
    logger.debug(f"Scraping data from URL: {url}")
    try:
        status_generator.send(f"Searching on {source}...")
    except Exception as e:
        logger.error(f"Error sending status message: {e}")

    elements = {
        "Title": "span.a-size-medium",
        "Price": "span.a-price-whole",
        "Availability": "div.a-section.a-spacing-none.a-spacing-top-micro",
        "Url": "a.a-link-normal" if source == "Amazon" else "a._1fQZEK"
    }

    try:
        scraper = Parsera()
        data = scraper.run(url=url, elements=elements)

        for item in data:
            if "Price" in item and item["Price"]:
                item["Price"] = f"₹{item['Price'].replace(',', '')}"
            if "Availability" not in item:
                item["Availability"] = "Unavailable"
            if "Url" in item and item["Url"]:
                item["Url"] = item["Url"].replace("https://www.amazon.inhttps://www.amazon.in", "https://www.amazon.in") if source == "Amazon" else item["Url"].replace("https://www.flipkart.comhttps://www.flipkart.com", "https://www.flipkart.com")

        try:
            status_generator.send(f"Found {len(data)} items on {source}.")
        except Exception as e:
            logger.error(f"Error sending status message: {e}")
        return data
    except Exception as e:
        logger.error(f"Error scraping data: {e}")
        try:
            status_generator.send(f"Error occurred while searching on {source}.")
        except Exception as e:
            logger.error(f"Error sending status message: {e}")
        return []

@app.route('/status')
def status():
    return Response(status_generator, content_type='text/event-stream')

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    keywords = request.args.get('keywords', '').split(',')
    logger.debug(f"Received search query: {query}, keywords: {keywords}")

    if not query:
        logger.error("Query parameter is missing")
        return jsonify({"error": "Query parameter is required"}), 400

    amazon_url = f"https://www.amazon.in/s?k={query}"
    flipkart_url = f"https://www.flipkart.com/search?q={query}"

    amazon_data = scrape_data(amazon_url, "Amazon")
    flipkart_data = scrape_data(flipkart_url, "Flipkart")

    # Filter products based on keywords and exact match
    def filter_products(products, keywords):
        filtered = []
        for product in products:
            if all(keyword.lower() in product['Title'].lower() for keyword in keywords):
                filtered.append(product)
        return filtered

    amazon_products = filter_products(amazon_data, keywords)
    flipkart_products = filter_products(flipkart_data, keywords)

    logger.debug(f"Amazon products: {amazon_products}")
    logger.debug(f"Flipkart products: {flipkart_products}")

    # Ensure single currency symbol
    for product in amazon_products + flipkart_products:
        product["Price"] = product.get("Price", "").replace("₹₹", "₹")

    return jsonify({
        "amazon": amazon_products if amazon_products else [{"Title": "Unavailable", "Price": None, "Availability": "Unavailable", "Url": None}],
        "flipkart": flipkart_products if flipkart_products else [{"Title": "Unavailable", "Price": None, "Availability": "Unavailable", "Url": None}]
    })

if __name__ == "__main__":
    logger.debug("Starting Flask server")
    app.run(port=5000)