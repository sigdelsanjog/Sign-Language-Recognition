<template>
   <div>
     <video ref="video" width="640" height="480" autoplay></video>
     <button @click="captureImage">Capture Image</button>
   </div>
 </template>
 
 <script>
 export default {
   mounted() {
     const video = this.$refs.video;
     if (navigator.mediaDevices.getUserMedia) {
       navigator.mediaDevices.getUserMedia({ video: true }).then((stream) => {
         video.srcObject = stream;
       });
     }
   },
   methods: {
     captureImage() {
       const video = this.$refs.video;
       const canvas = document.createElement('canvas');
       canvas.width = video.width;
       canvas.height = video.height;
       const context = canvas.getContext('2d');
       context.drawImage(video, 0, 0, canvas.width, canvas.height);
 
       canvas.toBlob((blob) => {
         this.$emit('imageCaptured', blob);
       });
     },
   },
 };
 </script>
 
 <style scoped>
 button {
   margin-top: 20px;
 }
 </style>
 