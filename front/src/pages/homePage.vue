<template>
  <div>
    <button @click="register">click</button>
  </div>
</template>

<script setup lang="ts">
import axios from 'axios'


const register = async () => {
  await axios.post('http://127.0.0.1:8000/api/register', {
    username: 'test3325322',
    email: 'test223332@te2st.com',
    password: 'Tes3dfghsdfg2t1234!Tes'
  })
}


</script>

