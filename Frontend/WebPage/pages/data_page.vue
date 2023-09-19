<template>
    <div class="page">
        <!-- Sidebar fijo -->
        <aside class="sidebar">
            <NuxtLogo />
            <div class="menu">
                <li @click="cambiarContenido('boton1')" class="button">
                    <span class="text">
                        Pagina 1
                    </span>
                </li>
                <li @click="cambiarContenido('boton2')" class="button">
                    <span class="text">
                        Pagina 2
                    </span>
                </li>
            </div>

        </aside>

        <!-- Contenido principal -->
        <div class="content">
            <div v-if="contenido == 'boton1'">
                <h1>Contenido de la Pagina 1</h1>
            </div>
            <div v-if="contenido == 'boton2'">
                <h1>Contenido de la Pagina 2</h1>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import NuxtLogo from '~/components/NuxtLogo.vue';
export default {

    data() {
        return {
            contenido: null,
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
            setTimeout(() => {
                const url = "http://127.0.0.1:5000/api/get_data";
                const response = axios.get(url);
                console.log(response);
            }, 3000);
        }
    },
    components: { NuxtLogo }
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