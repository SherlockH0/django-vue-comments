<script setup lang="ts">
import Filter from "./Filter.vue";
import { ref } from "vue";

const filter_reverse = ref<boolean>(false);
const filter_on = ref<boolean>(false);

const filter = ref<"username" | "email" | "date" | null>("username");
// let filters = [{ name, active, reversed }];
</script>
<template>
  <div class="flex w-full gap-4">
    <div class="flex items-center font-bold">Filters:</div>
    <Filter :name="'username'" />
    <Filter :name="'email'" />
    <Filter :name="'date'" />
  </div>
</template>
