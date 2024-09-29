<template>
  <div>
    <button @click="startDetection">Start Detection</button>
    <button @click="stopDetection">Stop Detection</button>
    <video ref="video" autoplay></video>
    <div class="message-container">
      <div v-for="(message, index) in messages" :key="index" class="message">
        {{ message }}
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      intervalId: null,
      messages: [],  // Store user interaction messages
    };
  },
  methods: {
    startDetection() {
      this.messages.push("Detection started.");
      this.intervalId = setInterval(this.captureAndSendImage, 4000); // Adjust the interval as needed
    },
    stopDetection() {
      clearInterval(this.intervalId);
      this.intervalId = null;
      this.messages.push("Detection stopped.");
    },
    async captureAndSendImage() {
      const video = this.$refs.video;

      // Log video dimensions to ensure it is streaming
      console.log(`Video dimensions: ${video.videoWidth}x${video.videoHeight}`);

      const canvas = document.createElement('canvas');
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      const context = canvas.getContext('2d');

      // Draw the current frame from the video onto the canvas
      context.drawImage(video, 0, 0);

      // Log canvas content for debugging
      console.log("Canvas drawn. Checking for blob...");

      // Create the blob
      canvas.toBlob(async (blob) => {
        // Check if blob was created successfully
        if (!blob) {
          console.error('Error: Blob creation failed. Check if the canvas has valid content.');
          this.messages.push('An error occurred while capturing the image.');
          return;
        }

        // Debug log to check blob properties
        console.log(`Blob created:`, blob);

        const formData = new FormData();
        formData.append('file', blob, 'sign.png');

        try {
          const response = await axios.post('http://localhost:8000/predict', formData, {
            headers: {
              'Content-Type': 'multipart/form-data',
            },
          });

          // Access the predicted sign directly
          const sign = response.data.sign || null;
          if (sign) {
            this.messages.push(`Captured Image for prediction. Predicted character: ${sign}`);
          } else {
            this.messages.push(`Error: ${response.data.error || 'Unknown error occurred'}`);
          }
        } catch (error) {
          console.error('Error in prediction:', error);
          this.messages.push('An error occurred while predicting.');
        }
      }, 'image/png');
    },
  },
  mounted() {
    const video = this.$refs.video;
    navigator.mediaDevices.getUserMedia({ video: true })
      .then(stream => {
        video.srcObject = stream;
      })
      .catch(err => {
        console.error("Error accessing the camera: ", err);
      });
  },
};
</script>

<style scoped>
.message-container {
  max-height: 200px; /* Adjust as needed */
  overflow-y: auto; /* Enable scrolling */
  border: 1px solid #ccc; /* Optional styling */
  margin-top: 10px; /* Space between video and messages */
}
.message {
  padding: 5px;
  border-bottom: 1px solid #eee; /* Optional styling */
}
</style>
