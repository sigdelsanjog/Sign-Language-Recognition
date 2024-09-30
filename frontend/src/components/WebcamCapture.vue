<template>
  <div class="row">
    <div class="col-md-6">
      <video ref="video" autoplay></video>
    </div>
    <div class="col-md-6">
      <button @click="toggleDetection" class="btn" :class="isDetecting ? 'btn-danger' : 'btn-primary'">
        {{ isDetecting ? 'Stop Detection' : 'Start Detection' }}
      </button>
      <div class="message-container">
        <div v-for="(message, index) in messages" :key="index" class="message">
          {{ message }}
        </div>
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
      isDetecting: false, // Track detection state
    };
  },
  methods: {
    async toggleDetection() {
      if (this.isDetecting) {
        await this.stopDetection();
      } else {
        await this.startDetection();
      }
    },
    async startDetection() {
      this.addMessage("Detection started.");
      this.isDetecting = true;
      this.intervalId = setInterval(this.captureAndSendImage, 4000); // Adjust the interval as needed

      // Send a request to start detection on the backend
      try {
        await axios.post('http://localhost:8000/start_detection');
        this.addMessage('Started detection on the backend.');
      } catch (error) {
        console.error('Error starting detection:', error);
        this.addMessage('Error: Could not start detection on the backend.');
        this.isDetecting = false; // Reset state on error
      }
    },
    async stopDetection() {
      clearInterval(this.intervalId);
      this.intervalId = null;
      this.addMessage("Detection stopped.");
      this.isDetecting = false;

      // Send a request to stop detection on the backend
      try {
        await axios.post('http://localhost:8000/stop_detection');
        this.addMessage('Stopped detection on the backend.');
      } catch (error) {
        console.error('Error stopping detection:', error);
        this.addMessage('Error: Could not stop detection on the backend.');
      }
    },
    async captureAndSendImage() {
      const video = this.$refs.video;

      // Check if the video reference is valid
      if (!video || !video.videoWidth || !video.videoHeight) {
        console.error('Video element is not available or has no dimensions.');
        this.addMessage('Error: Video element is not available.');
        return;
      }

      const canvas = document.createElement('canvas');
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      const context = canvas.getContext('2d');

      context.drawImage(video, 0, 0);

      canvas.toBlob(async (blob) => {
        if (!blob) {
          console.error('Error: Blob creation failed.');
          this.addMessage('An error occurred while capturing the image.');
          return;
        }

        const formData = new FormData();
        formData.append('file', blob, 'sign.png');

        try {
          const response = await axios.post('http://localhost:8000/predict', formData, {
            headers: {
              'Content-Type': 'multipart/form-data',
            },
          });

          const sign = response.data.sign || null;
          if (sign) {
            this.addMessage(`Captured Image for prediction. Predicted character: ${sign}`);
          } else {
            this.addMessage(`Error: ${response.data.error}`);
          }
        } catch (error) {
          console.error('Error in prediction:', error);
          this.addMessage('An error occurred while predicting.');
        }
      }, 'image/png');
    },
    addMessage(message) {
      this.messages.unshift(message); // Add new messages at the beginning
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
