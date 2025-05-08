<template>
  <div class="toast">
    <div
      v-for="toast in toasts"
      class="alert"
      :class="`alert-${toast.event.type}`"
      @click="removeToast(toast.id)"
    >
      <span>{{ toast.event.message }}</span>
    </div>
  </div>
</template>
<script setup lang="ts">
import { emitter } from "../scripts/events";
import type { ToastEvent } from "../scripts/interfaces";
import { ref } from "vue";

const toasts = ref<Array<{ id: number; event: ToastEvent }>>([]);

emitter.on("toast", (event) => {
  const id = Math.random() * 1000;
  toasts.value.push({ id, event });
  setTimeout(() => {
    removeToast(id);
  }, 5000);
});
function removeToast(id: number) {
  toasts.value = toasts.value.filter((t) => t.id !== id);
}
</script>
