<template>
  <div id="container">
    <input v-model="query" placeholder="Enter product name" />
    <input v-model="keywords" placeholder="Enter features like color, storage (comma-separated)" />
    <button @click="searchProducts">Search</button>

    <!-- Loading animation -->
    <div v-if="isLoading" class="loader"></div>

    <div v-if="results">
      <h2>Amazon</h2>
      <ul class="product-list">
        <li v-for="product in results.amazon" :key="product.Title" class="product-item">
          <span class="product-name">{{ product.Title }}</span>
          <span class="product-price">
            <a :href="product.Url" target="_blank" class="product-link">{{ product.Price }} <i class="fas fa-external-link-alt icon"></i></a>
          </span>
        </li>
        <li v-if="results.amazon.length === 0">No products found</li>
      </ul>

      <h2>Flipkart</h2>
      <ul class="product-list">
        <li v-for="product in results.flipkart" :key="product.Title" class="product-item">
          <span class="product-name">{{ product.Title }}</span>
          <span class="product-price">
            <a :href="product.Url" target="_blank" class="product-link">{{ product.Price }} <i class="fas fa-external-link-alt icon"></i></a>
          </span>
        </li>
        <li v-if="results.flipkart.length === 0">No products found</li>
      </ul>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      query: '',
      keywords: '',
      results: null,
      isLoading: false,
      eventSource: null,
    };
  },
  methods: {
    async searchProducts() {
      this.results = null; // Clear previous results
      this.isLoading = true; // Show loading animation

      // Setup SSE to listen for status updates
      this.eventSource = new EventSource('http://127.0.0.1:5000/status');
      this.eventSource.onmessage = (event) => {
        console.log('Received SSE:', event.data);
        // Here you can display the status update to the user if needed
      };

      try {
        const response = await axios.get('http://127.0.0.1:5000/search', {
          params: { query: this.query, keywords: this.keywords }
        });
        console.log('Response Data:', response.data); // Debugging line
        this.results = response.data;
        console.log('Amazon Products:', this.results.amazon); // Debugging line
        console.log('Flipkart Products:', this.results.flipkart); // Debugging line
      } catch (error) {
        console.error('Error fetching data from backend:', error);
      } finally {
        this.isLoading = false; // Hide loading animation
        if (this.eventSource) {
          this.eventSource.close(); // Close SSE connection
        }
      }
    }
  }
};
</script>

<style scoped>
/* General styles for the container */
#container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start; /* Adjusted to start from the top */
  height: 100vh;
  text-align: center;
  padding-top: 20px; /* Add some padding to the top */
}

/* Styles for input elements */
/*input {
  margin: 10px 0;
  padding: 10px;
  width: 300px;
  box-sizing: border-box;
}

input:focus {
  border-color: white;
}

/* Styles for input elements */
input {
  font-size: 13px;
  margin: 10px 0;
  padding: 10px;
  width: 300px;
  box-sizing: border-box;
  border: 2px solid #959494; /* Set a consistent border color */
  border-radius: 4px;
  outline: none; /* Remove the default outline */
  transition: border-color 0.3s ease, /* Smooth transition for border color */
              transform 0.2s ease; /* Smooth transition for the movement */
}

/* Maintain the border color when focused */
input:focus {
  border-color: #cfcdcd; /* Set to your preferred focus border color */
  box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.2); /* Bottom and left outer shadow */
  transform: translate(0px, -1px); /* Moves the input box */
}

/* Styles for the results section */
#container > div:last-child {
  margin-top: 20px;
}

/* Styles for the loader */
.loader {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100px;
}

.loader::after {
  content: "";
  width: 40px;
  height: 40px;
  border: 4px solid #ccc;
  border-top-color: #444;
  border-radius: 50%;
  animation: spin 1s ease-in-out infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* Styling for the columns of the list */
.product-list {
  list-style: none;
  padding: 0;
}

.product-item {
  display: flex;
  justify-content: space-between;
  padding: 10px 0;
  border-bottom: 1px solid #ccc; /* Optional: Add a divider between items */
}

.product-name {
  flex: 3; /* Adjust this value to control the width of the name column */
}

.product-price {
  flex: 1; /* Adjust this value to control the width of the price column */
  text-align: right;
}

.product-link {
  text-decoration: none;
  color: #000;
}

.product-link:hover {
  text-decoration: underline;
}

/* Styles for the button */
button {
    font-size: 13px;
    padding: 10px 20px;
    margin: 10px 0;
    cursor: pointer;
    color: #959494; /* Default text color */
    border: 2px solid #959494;
    transition: background-color 0.3s ease, transform 0.1s ease; /* Smooth transition for background color and transform */
}

/* Hover effect */
button:hover {
    background-color: #959494; /* Darker background color on hover */
    color: #f0f0f0;
    border-radius: 3px;
    border-color: #959494;
}

/* Click effect */
button:active {
    transform: scale(0.95); /* Slightly shrink the button when clicked */
}

/* Styles for the list elements */
li {
    text-align: left; /* Left-align the text inside the list items */
    margin: 5px 0;
    padding: 5px;
    border-bottom: 1px solid #ccc; /* Optional: Add a border for better visibility */
}

/* Styles for the product links */
.product-link {
    text-decoration: none;
    color: inherit;
    transition: text-decoration 0.3s ease;
}

/* Styles for the icon */
.icon {
      margin-left: 5px;
      font-size: 0.8em;
}
</style>