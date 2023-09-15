<template>
  <div>
    <div style="position: relative;">
      <fondo-video />
      <div style="display: flex; justify-content: center; align-items: center; min-height: 100vh; border: 2px solid red;">
        <div style="text-align: center;">
          <h2>Automatiza tus Retro-Calculos con nuestra herramientas para que tus pavimentos queden como los de Chile</h2>
          <br>
          <b-button pill variant="warning">Ingrese tu archivo</b-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import fondo_video from '../components/fondo_video.vue';
export default {
  components: { fondo_video },
  data() {
    return {
      videoURL: 'https://www.youtube.com/clip/UgkxQD_tEI6PzfTMQtWvJYN1zRD0LJNuDPvO.mp4',
    };
  },
};
</script>





