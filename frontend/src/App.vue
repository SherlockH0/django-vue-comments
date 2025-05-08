<template>
  <Transition>
    <div
      class="absolute inset-0 h-svh grid place-items-center bg-black/30 z-50"
      v-if="loading"
    >
      <span class="loading loading-spinner loading-xl"></span>
    </div>
  </Transition>
  <main class="flex max-h-svh flex-col">
    <Auth>
      <Comments />
    </Auth>
    <Toasts />
  </main>
</template>
<script setup lang="ts">
import Comments from "./components/Comments.vue";
import Toasts from "./components/Toasts.vue";
import Auth from "./components/auth/Auth.vue";
import { loading } from "./scripts/events";
</script>
<style>
.v-enter-active,
.v-leave-active {
  transition: opacity 0.5s ease;
}

.v-enter-from,
.v-leave-to {
  opacity: 0;
}
</style>
