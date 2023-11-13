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
                <li @click="cambiarContenido('boton2'), getImage()" class="button">
                    <span class="text">
                        Graficas
                    </span>
                </li>
            </div>

        </aside>

        <!-- Contenido principal -->
        <div class="content">
            <div class="mt-4" v-if="contenido == 'boton1' && boton1_contenido == 0" style="margin: 10%;">
                <h4>Ingrese la distancia de cada geofono en pulgadas</h4>
                <b-card img-src="https://picsum.photos/id/182/600/600" img-alt="Card image" img-right class="mb-3">
                    <div class="input-field" v-for="(input, index) in distancia_D" :key="index + 2">
                        <b-form-input type="text" v-model="inputValues[index]" :name="`input_${index + 2}`"
                            :placeholder="`Geofono ${index + 2}`"></b-form-input><br>
                    </div>
                    <br>
                    <b-button variant="warning" @click="guardarValores('boton3')">Guardar Valores</b-button>
                </b-card>
            </div>
            <div v-else-if="contenido == 'boton3'">
                <b-table responsive striped hover :items="tabla_necesaria"></b-table>
            </div>
            <div v-if="contenido == 'boton2'">
                <div v-if="loadedImage == true">
                    <img class="imagen-redimensionada" :src="imageSrc[0]" alt="Imagen" />
                    <img class="imagen-redimensionada" :src="imageSrc[1]" alt="Imagen" />
                    <img class="imagen-redimensionada" :src="imageSrc[2]" alt="Imagen" />
                    <img class="imagen-redimensionada" :src="imageSrc[3]" alt="Imagen" />
                    <img class="imagen-redimensionada" :src="imageSrc[4]" alt="Imagen" />
                    <img class="imagen-redimensionada" :src="imageSrc[5]" alt="Imagen" />
                </div>
                <div v-else>Cargando Imagen...</div>
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
            imageSrc: [],
            loadedImage: false,

        }
    },

    beforeMount() {
        this.getData();
    },
    methods: {

        async getImage() {
            const imagenes = [];
            if (this.loadedImage != false) {
                try {
                    for (let i = 1; i < 7; i++) {
                        // Realizar la solicitud HTTP a la ruta de la imagen en Flask
                        const response = await this.$axios.get(`http://127.0.0.1:5000/api/get_image${i}`, {
                            responseType: 'arraybuffer',  // Indicar que esperamos datos binarios
                        });

                        // Convertir la respuesta a una URL de datos (data URL)
                        const imageDataUrl = `data:image/jpeg;base64,${btoa(
                            new Uint8Array(response.data).reduce((data, byte) => data + String.fromCharCode(byte), '')
                        )}`;

                        // Actualizar el estado para mostrar la imagen
                        imagenes.push(imageDataUrl);

                    }
                } catch (error) {
                    console.error('Error al obtener la imagen:', error);
                    alert("Error al obtener la imagen");
                }
            } else {
                this.$swal({
                    icon: 'error',
                    title: 'Oops...',
                    text: 'Ingrese las distancias primero!',
                })
            }
            this.imageSrc = imagenes

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
                    //console.log(response.data);
                    this.tabla_necesaria = response.data
                    this.contenido = valor
                    this.loadedImage = true
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
                //console.log(response.data);
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


.imagen-redimensionada{
    width: 725px; /* Ancho deseado */
    height: auto;
}
</style>