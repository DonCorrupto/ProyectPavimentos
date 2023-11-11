<template>
    <div class="page">
        <!-- Sidebar fijo -->
        <aside class="sidebar">
            <NuxtLogo />
            <div class="menu">
                <h5>Cantidad de Geofonos: {{ geofonos }}</h5>
                <li @click="cambiarContenido('boton1')" class="button">
                    <span class="text">
                        Retro-Calculo
                    </span>
                </li>
                <li @click="cambiarContenido('boton2'), fetchImage()" class="button">
                    <span class="text">
                        Graficas
                    </span>
                </li>
            </div>

        </aside>

        <!-- Contenido principal -->
        <div class="content">
            <div v-if="contenido == 'boton1' && boton1_contenido == 0">
                <h2>Ingrese la distancia de cada geofono en pulgadas</h2>
                <div v-for="(input, index) in distancia_D" :key="index + 2">
                    <input type="text" v-model="inputValues[index]" :name="`input_${index + 2}`"
                        :placeholder="`Geofono ${index + 2}`">
                </div>
                <br>
                <button @click="guardarValores(1)">Guardar Valores</button>
            </div>
            <div v-else-if="boton1_contenido == 1">
                <b-table responsive :items="tabla_necesaria"></b-table>
            </div>
            <div v-if="contenido == 'boton2'">
                <img v-if="imageLoaded" :src="imageSrc" alt="Imagen" />
                <div v-else>Cargando imagen...</div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';

export default {

    data() {
        return {
            contenido: null,
            boton1_contenido: 0,
            tabla_necesaria: [],
            generatedInputs: [],
            geofonos: null,
            currentPage: 1,
            inputValues: [],
            rows: null,
            imageSrc: null,
            imageLoaded: false,

        }
    },

    beforeMount() {
        this.getData();
        this.fetchImage();
    },
    methods: {

        async fetchImage() {
            try {
                // Realizar la solicitud HTTP a la ruta de la imagen en Flask
                const response = await this.$axios.get('http://127.0.0.1:5000/api/get_image', {
                    responseType: 'arraybuffer', // Configurar el tipo de respuesta como arraybuffer
                });

                // Convertir la respuesta a una URL de datos (data URL)
                const imageSrc = `data:image/png;base64,${btoa(
                    new Uint8Array(response.data).reduce((data, byte) => data + String.fromCharCode(byte), '')
                )}`;

                // Actualizar el estado para mostrar la imagen
                this.imageSrc = imageSrc;
                this.imageLoaded = true;
            } catch (error) {
                console.error('Error al obtener la imagen:', error);
            }
        },

        async guardarValores(valor) {
            //console.log(this.inputValues);
            const formData = new FormData();
            formData.append('distancia_D', this.inputValues);
            try {
                // Realiza la solicitud POST para enviar el archivo CSV a la API Flask
                await axios.post('http://127.0.0.1:5000/api/distancia_geofono', formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    }
                });
                this.$swal(
                    'Excelente!',
                    'Archivo CSV enviado correctamente.',
                    'success'
                )
                try {
                    const url = "http://127.0.0.1:5000/api/get_tabla";
                    const response = await axios.get(url);
                    console.log(response.data);
                    this.tabla_necesaria = response.data
                    this.boton1_contenido = valor
                } catch (error) {
                    console.error(error);
                }
            } catch (error) {
                console.error('Error al enviar el archivo CSV:', error);
                this.$swal({
                    icon: 'error',
                    title: 'Oops...',
                    text: 'Error al enviar el archivo CSV!',
                })
            }

        },

        cambiarContenido(boton) {
            this.contenido = boton;
        },

        async getData() {
            try {
                const url = "http://127.0.0.1:5000/api/get_data";
                const response = await axios.get(url);
                console.log(response.data);
                this.geofonos = response.data.geofonos;
                this.distancia_D = response.data.geofonos - 1;
            } catch (error) {
                console.error(error);
            }
        }
    },
}
</script>

<style scoped>
/* Estilos para el sidebar fijo */
.sidebar {
    position: fixed;
    left: 0;
    top: 0;
    bottom: 0;
    width: 250px;
    background-color: black;
    color: white;
    /* Otros estilos personalizados */
}

/* Estilos para el contenido principal */
.content {
    margin-left: 270px;
    /* Ajusta el margen según el ancho de tu sidebar */
    /* Otros estilos personalizados */
}

.menu {
    margin-top: 35%;
}

/* Estilos para los botones */
.button {
    display: flex;
    align-items: center;
    text-decoration: none;

    padding: 0.5rem 1rem;
    transition: 0.2s ease-out;
    cursor: pointer;
}

.text {
    color: white;
    transition: 0.2s ease-out;
    cursor: pointer;
}

.button:hover {
    background-color: darkcyan;
}
</style>