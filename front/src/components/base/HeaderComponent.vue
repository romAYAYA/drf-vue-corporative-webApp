<template>
  <Toolbar style="border-radius: 3rem; padding: 1rem 1rem 1rem 1.5rem">
    <template #start>
      <div v-for="link in navLinks" :key="link.url" class="flex align-items-center gap-2">
        <RouterLink activeClass="text-[--button-dark] border-b-2 border-[--button-dark]" class="ml-3" :to="link.url">
          {{ link.label }}
        </RouterLink>
      </div>
    </template>

    <template #end>
      <div v-if="userStore.isUserLoaded" class="flex align-items-center gap-2">
        <UserSettingsModal/>
        <Avatar image="https://primefaces.org/cdn/primevue/images/avatar/amyelsner.png"
                style="width: 32px; height: 32px"/>
      </div>
      <div v-else>
        <ModalComponent/>
      </div>
    </template>
  </Toolbar>
</template>

<script setup lang="ts">
import { useUserStore } from '../../stores/user.ts'
import ModalComponent from '../authModal/ModalComponent.vue'
import UserSettingsModal from '../UserSettingsModal.vue'

const userStore = useUserStore()

const navLinks = [
  { label: 'Главная', url: '/' },
  { label: 'О нас', url: '/about' }
]
</script>