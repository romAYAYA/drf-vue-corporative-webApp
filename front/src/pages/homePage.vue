<template>
  <div>
    {{ products }}sdf
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import axios from 'axios'

const products = ref([])


const getData = async () => {
  const { data } = await axios.get('https://fakestoreapi.com/products')
  products.value = data
}
getData()
</script>

