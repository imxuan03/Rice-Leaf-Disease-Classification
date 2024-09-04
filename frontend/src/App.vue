<template>
  <div id="app">
    <AppHeader />
    <router-view />
    <Chatbot />
  </div>
</template>

<script>
import AppHeader from "@/components/AppHeader.vue";
import Chatbot from './components/Chatbot.vue';

export default {
  components: {
    AppHeader,
    Chatbot,
  },

};
</script>

<style>
</style>
