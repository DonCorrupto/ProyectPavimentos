<template>
    <div class="page">
        <!-- Sidebar fijo -->
        <aside class="sidebar">
            <NuxtLogo />
            <div class="menu">
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
        </div>
    </div>
</template>

<script>
import axios from 'axios';

export default {

    data() {
        return {
            contenido: null,
            normalizacion_unidades: [],
            normalizacion_carga: [],
            normalizacion_temperatura: [],
        }
    },

    beforeMount() {
        this.getData();
    },
    methods: {

        cambiarContenido(boton) {
            this.contenido = boton;
        },

        async getData() {
            try {
                const url = "http://127.0.0.1:5000/api/get_data";
                const response = await axios.get(url);
                console.log(response.data);
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