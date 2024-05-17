<template>
  <div>Status: {{ usersDataStatus }}</div>
  <div v-if="usersData">Users: {{ usersData }}</div>
  <div v-else-if="!isUserLoaded">Login to see this</div>
  <div v-else>Loading...</div>
</template>

<script setup lang="ts">
import { useQuery } from '@tanstack/vue-query'
import axios from 'axios'
import { useUserStore } from '../stores/user.ts'
import { computed } from 'vue'


const userStore = useUserStore()

const isUserLoaded = computed(() => userStore.isUserLoaded)

const { data: usersData, status: usersDataStatus } = useQuery({
  queryKey: ['users'],
  queryFn: async () => await axios.get('/users'),
  select: ({ data }) => data,
  enabled: isUserLoaded
})

</script>
