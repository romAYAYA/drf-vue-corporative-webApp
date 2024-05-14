<template>
  <div class="mt-3 mx-5 flex flex-col gap-5">
    <nav>
      <HeaderComponent/>
    </nav>
    <main>
      <RouterView/>
    </main>
  </div>
</template>

<script setup lang="ts">
import HeaderComponent from './components/base/HeaderComponent.vue'
</script>
