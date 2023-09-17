<template>
    <div>
        <h1>Probando Page</h1>
    </div>
</template>

<script>
import axios from 'axios';
export default {

    beforeMount() {
        this.getData();
    },

    methods: {

        async getData() {
            setTimeout(() => {
                const url = "http://127.0.0.1:5000/api/get_data";
                const response = axios.get(url);
                console.log(response);
            }, 3000);
        }
    }
}
</script>