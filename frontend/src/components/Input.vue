<template>
  <label class="label capitalize">{{ attrs.name }}</label>
  <input
    class="input w-full"
    v-bind="attrs"
    v-model="value"
    :class="{ 'input-error': errors?.length || false }"
  />
  <p v-if="errors?.length || false" class="label text-error">
    <template v-for="error in errors"> {{ error }}<br /> </template>
  </p>
</template>
<script setup lang="ts">
import { useAttrs } from "vue";

defineProps<{
  errors?: string[];
}>();

const attrs = useAttrs();
const value = defineModel<string>();
</script>
