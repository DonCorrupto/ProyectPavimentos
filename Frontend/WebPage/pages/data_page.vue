<template>
    <div class="page">
        <!-- Sidebar fijo -->
        <aside class="sidebar">
            <NuxtLogo />
            <div class="menu">
                <h5>Cantidad de Geofonos: {{ geofonos }}</h5>
                <li @click="cambiarContenido('boton1')" class="button">
                    <span class="text">
                        Normalización por unidades
                    </span>
                </li>
                <li @click="cambiarContenido('boton2')" class="button">
                    <span class="text">
                        Normalización por carga
                    </span>
                </li>
                <li @click="cambiarContenido('boton3')" class="button">
                    <span class="text">
                        Normalización por temperatura
                    </span>
                </li>
                <li @click="cambiarContenido('boton4')" class="button">
                    <span class="text">
                        Modulo Resiliente
                    </span>
                </li>
            </div>

        </aside>

        <!-- Contenido principal -->
        <div class="content">
            <div v-if="contenido == 'boton1'">
                <b-table responsive :items="normalizacion_unidades"></b-table>
            </div>
            <div v-if="contenido == 'boton2'">
                <b-table responsive :items="normalizacion_carga"></b-table>
            </div>
            <div v-if="contenido == 'boton3'">
                <b-table responsive :items="normalizacion_temperatura"></b-table>
            </div>
            <div v-if="contenido == 'boton4' && boton4_contenido == 0">
                <h2>Ingrese la distancia de cada geofono en pulgadas</h2>
                <div v-for="(input, index) in distancia_D" :key="index + 2">
                    <input type="text" v-model="inputValues[index]" :name="`input_${index + 2}`"
                        :placeholder="`D${index + 2}`">
                </div>
                <br>
                <button @click="guardarValores(1)">Guardar Valores</button>
            </div>
            <div v-else-if="boton4_contenido == 1">
                <div v-for="(subarray, index) in distancia_D" :key="index">
                    <h2>Geofono {{ index + 2 }}</h2>
                    <b-table responsive :items="subarray" :fields="fields" :per-page="rows"
                        :current-page="currentPage[index]"></b-table>
                    <b-pagination v-model="currentPage[index]" :total-rows="subarray.length" :per-page="rows"
                        aria-controls="my-table"></b-pagination>
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
            contenido: null,
            fields: [
                { key: 'd', label: 'd' },
                { key: 'Mr', label: 'Mr' },
                { key: 'E_solution', label: 'E_solution' },
            ],
            boton4_contenido: 0,
            normalizacion_unidades: [],
            normalizacion_carga: [],
            normalizacion_temperatura: [],
            generatedInputs: [],
            geofonos: null,
            distancia_D: [],
            currentPage: 1,
            inputValues: [],
            rows: null

        }
    },

    beforeMount() {
        this.getData();
    },
    methods: {

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
                    const url = "http://127.0.0.1:5000/api/get_modulo_resiliente";
                    const response = await axios.get(url);
                    //console.log(response.data);
                    var object = response.data;
                    this.distancia_D = Object.values(object)
                    this.rows = this.distancia_D.length;
                    console.log(this.distancia_D);
                    this.currentPage = new Array(this.distancia_D.length).fill(1);
                    this.boton4_contenido = valor
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
                this.normalizacion_unidades = JSON.parse(response.data.normalizacion_unidades)
                this.normalizacion_carga = JSON.parse(response.data.normalizacion_carga)
                this.normalizacion_temperatura = JSON.parse(response.data.normalizacion_temperatura)
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