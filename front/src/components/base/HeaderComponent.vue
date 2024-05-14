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
      <div class="flex align-items-center gap-2">
        <Button label="Изменить профиль" severity="secondary" size="small" text/>
        <Avatar image="https://primefaces.org/cdn/primevue/images/avatar/amyelsner.png"
                style="width: 32px; height: 32px"/>
      </div>
    </template>
  </Toolbar>
</template>

<script setup lang="ts">
const navLinks = [
  { label: 'Главная', url: '/' },
  { label: 'О нас', url: '/about' }
]
</script>