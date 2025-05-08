<template>
  <button @click="handleClick">
    <slot></slot>
  </button>
</template>
<script setup lang="ts">
import { emitter } from "../scripts/events";
import type { CommentObject } from "../scripts/interfaces";

const props = defineProps<{
  parent?: CommentObject;
}>();

function handleClick() {
  emitter.emit("new_comment", { parent: props.parent });
}
</script>
