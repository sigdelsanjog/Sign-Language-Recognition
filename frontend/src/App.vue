<template>
  <div id="app" class="container mt-4">
    <h1>Sign Language Recognition</h1>
    <WebcamCapture @imageCaptured="processImage" />
    <div class="messages-container mt-3">
      <div v-for="(msg, index) in messages" :key="index" class="alert alert-info">
        <p>{{ msg }}</p>
      </div>
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
      messages: [], // Array to hold interaction messages
    };
  },
  methods: {
    async processImage(imageBlob) {
      const formData = new FormData();
      formData.append('file', imageBlob, 'sign.png');

      try {
        const response = await axios.post('http://localhost:8000/predict', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });

        const sign = response.data.sign || null;
        if (sign) {
          this.addMessage(`Captured an image for prediction. Predicted character: ${sign}`);
        } else {
          this.addMessage(`Captured an image for prediction. Error: ${response.data.error}`);
        }
      } catch (error) {
        console.error('Error in prediction:', error);
        this.addMessage('An error occurred while predicting. Please try again.');
      }
    },
    addMessage(msg) {
      this.messages.unshift(msg); // Add new message at the top
      if (this.messages.length > 10) this.messages.pop(); // Keep the last 10 messages
    },
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  text-align: center;
}

.messages-container {
  max-height: 300px;
  overflow-y: auto;
  margin-top: 20px;
  border: 1px solid #ccc;
  padding: 10px;
}

/* Make messages appear more prominent with Bootstrap styling */
.alert {
  margin: 5px 0; /* Margin for spacing between messages */
}
</style>
