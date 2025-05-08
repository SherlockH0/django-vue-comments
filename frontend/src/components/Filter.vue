<template>
  <div class="join">
    <button
      class="btn flex items-center gap-2 join-item"
      @click="changeState()"
      :class="{ 'btn-neutral': active }"
    >
      <div>{{ display }}</div>
      <template v-if="active">
        <Icon v-if="reversed" icon="ci:caret-up-md" width="24" height="24" />
        <Icon v-else icon="ci:caret-down-md" width="24" height="24" />
      </template>
    </button>
    <button
      class="btn join-item btn-square btn-neutral"
      v-if="active"
      @click="active = false"
    >
      <Icon icon="ci:filter-off" width="16" height="16" />
    </button>
  </div>
</template>
<script setup lang="ts">
import { Icon } from "@iconify/vue";

defineProps<{
  display: string;
}>();
const emit = defineEmits(["activate"]);

const active = defineModel<boolean>("active", { default: false });
const reversed = defineModel<boolean>("reversed", { default: false });

function changeState() {
  if (!active.value) {
    emit("activate");
    active.value = true;
  } else if (!reversed.value) {
    reversed.value = true;
  } else {
    active.value = false;
    reversed.value = false;
  }
}
</script>
