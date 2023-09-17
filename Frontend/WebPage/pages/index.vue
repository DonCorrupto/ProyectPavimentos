<template>
  <div>
    <div
      style="display: flex; justify-content: center; align-items: center; min-height: 100vh; background-image: url('https://excavacionesgrasa.com/wp-content/uploads/2022/02/Pavimentos-rigidos-y-pavimentos-flexibles.jpg'); background-size: cover; background-position: center;">
      <div style="text-align: center;">
        <h2 style="color: white;">Automatiza tus Retro-Calculos con nuestra herramientas para que tus pavimentos queden
          como los de Chile</h2>
        <br>
        <div>
          <b-button id="show-btn" @click="$bvModal.show('bv-modal-example')" pill variant="warning">Ingrese tu
            archivo</b-button>

          <b-modal id="bv-modal-example" hide-footer>
            <template #modal-title>
              Formato CSV
            </template>
            <form @submit.prevent="handleFileUpload">
              <input type="file" ref="fileInput" accept=".csv">
              <b-button style="margin-left: 5%;" v-b-modal.modal-prevent-closing pill variant="info" type="submit">Cargar
                CSV</b-button>
              <br>
              <br>
              <b-button block @click="$bvModal.hide('bv-modal-example')" pill variant="danger">Cerrar</b-button>
            </form>
          </b-modal>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
export default { 

  methods: {
    async handleFileUpload() {
      const fileInput = this.$refs.fileInput;
      const file = fileInput.files[0]; // Obtiene el primer archivo seleccionado

      if (file) {
        // Verifica que se haya seleccionado un archivo
        if (file.type === 'text/csv') {
          // Verifica que sea un archivo CSV
          // Ahora puedes trabajar con el archivo CSV, por ejemplo, leer su contenido
          const formData = new FormData();
          formData.append('archivo_csv', file);

          try {
            // Realiza la solicitud POST para enviar el archivo CSV a la API Flask
            await axios.post('http://127.0.0.1:5000/api/cargar_csv', formData, {
              headers: {
                'Content-Type': 'multipart/form-data'
              }
            });
            this.$swal(
              'Excelente!',
              'Archivo CSV enviado correctamente.',
              'success'
            )
            setTimeout(() => {
              window.open("./data_page", "_self");
            }, 1500);
          } catch (error) {
            console.error('Error al enviar el archivo CSV:', error);
            this.$swal({
              icon: 'error',
              title: 'Oops...',
              text: 'Error al enviar el archivo CSV!',
            })
          }
        } else {
          this.$swal({
            icon: 'info',
            text: 'Selecciona un archivo CSV válido.',
          })
        }
      } else {
        this.$swal({
          icon: 'info',
          text: 'Selecciona un archivo antes de cargarlo.',
        })
      }
    },
  }
}
</script>









  
