<template>
  <div class="card flex justify-content-center">
    <Button label="Войти" @click="visible = true" outlined/>
    <Dialog v-model:visible="visible" modal header="Вход" :style="{ width: '25rem' }">
      <TabView>
        <TabPanel header="Войти">
          <LoginComponent :visible="visible"/>
        </TabPanel>
        <TabPanel header="Зарегистрироваться">
          <RegisterComponent :visible="visible"/>
        </TabPanel>
      </TabView>
    </Dialog>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import LoginComponent from './LoginComponent.vue'
import RegisterComponent from './RegisterComponent.vue'

const visible = ref(false)
</script>

