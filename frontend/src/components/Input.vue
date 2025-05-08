<template>
  <label class="label capitalize" :for="attrs.name">{{ attrs.name }}</label>
  <input
    class="input"
    v-bind="attrs"
    v-model="value"
    :class="{ 'input-error': errors.length }"
  />
  <p v-if="errors.length" class="label text-error">
    <template v-for="error in errors"> {{ error }}<br /> </template>
  </p>
</template>
<script setup lang="ts">
import { useAttrs } from "vue";

const props = defineProps<{
  errors: string[];
}>();

const attrs = useAttrs();
const value = defineModel<string>();
</script>
