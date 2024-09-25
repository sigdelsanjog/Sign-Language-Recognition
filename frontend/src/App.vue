<template>
  <div id="app">
    <h1>Sign Language Recognition</h1>
    <WebcamCapture @imageCaptured="processImage" />
    <div v-if="sign">
      <h2>Detected Sign: {{ sign }}</h2>
    </div>
    <div v-if="error" class="error-message">
      <h3>Error: {{ error }}</h3>
    </div>
  </div>
</template>

<script>
import WebcamCapture from './components/WebcamCapture.vue';
import axios from 'axios';

export default {
  components: {
    WebcamCapture,
  },
  data() {
    return {
      sign: null,
      error: null, // Added for error handling
    };
  },
  methods: {
    async processImage(imageBlob) {
      const formData = new FormData();
      formData.append('file', imageBlob, 'sign.png');

      try {
        const response = await axios.post('http://localhost:8000/predict', formData, {
          headers: {
            'Content-Type': 'multipart/form-data', // Specify content type
          },
        });
        this.sign = response.data.sign || null;
        this.error = response.data.error || null; // Handle error messages
      } catch (error) {
        console.error('Error in prediction:', error);
        this.error = 'An error occurred while predicting. Please try again.'; // User-friendly error message
        this.sign = null; // Clear sign on error
      }
    },
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  text-align: center;
}

.error-message {
  color: red; /* Style for error message */
}
</style>
