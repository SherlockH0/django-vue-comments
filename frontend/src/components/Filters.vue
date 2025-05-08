<template>
  <div class="flex gap-4">
    <div class="flex items-center font-bold">Sort by:</div>
    <Filter
      v-for="filter in filters"
      :display="filter.display"
      v-model:active="filter.active"
      v-model:reversed="reversed"
      @activate="toggleFilters(filter)"
    />
  </div>
</template>
<script setup lang="ts">
import type { FilterInterface } from "../scripts/interfaces";
import Filter from "./Filter.vue";
import { ref, watchEffect } from "vue";

const reversed = ref<boolean>(false);
const emit = defineEmits<{
  change: [filter: string | null, reversed: boolean];
}>();

function toggleFilters(f: FilterInterface) {
  filters.value
    .filter((filter) => filter.name !== f.name)
    .forEach((filter) => {
      filter.active = false;
      reversed.value = false;
    });
}

const filters = ref<FilterInterface[]>([
  { display: "Username", name: "user__username", active: false },
  { display: "Email", name: "user__email", active: false },
  { display: "Date", name: "datetime_created", active: false },
]);

watchEffect(() => {
  emit(
    "change",
    filters.value.filter((filter) => filter.active)[0]?.name || null,
    reversed.value,
  );
});
</script>
