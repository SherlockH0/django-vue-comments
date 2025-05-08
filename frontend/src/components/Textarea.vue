<template>
  <div class="join">
    <button type="button" @click="insertTag('i')" class="btn btn-sm join-item">
      <Icon icon="ci:italic" width="1rem" height="1rem" />
    </button>
    <button
      type="button"
      @click="insertTag('strong')"
      class="btn btn-sm join-item"
    >
      <Icon icon="ci:bold" width="1rem" height="1rem" />
    </button>
    <button
      type="button"
      @click="insertTag('code')"
      class="btn btn-sm join-item"
    >
      <Icon icon="ci:code" width="1rem" height="1rem" />
    </button>
    <button
      type="button"
      @click="insertTag('a', ' href=\'\' title=\'\'')"
      class="btn btn-sm join-item"
    >
      <Icon icon="ci:link" width="1rem" height="1rem" />
    </button>
  </div>
  <textarea
    class="join-item textarea w-full"
    :class="{ 'input-error': errors.length }"
    name="text"
    placeholder="Start typing..."
    required
    ref="textarea"
    v-model="text"
  ></textarea>
</template>
<script setup lang="ts">
import { Icon } from "@iconify/vue";
import { useTemplateRef, nextTick } from "vue";

defineProps<{
  errors: string[];
}>();

const text = defineModel({ default: "" });
const textarea = useTemplateRef("textarea");

function insertTag(tag: string, extra: string = "") {
  const el = textarea.value;

  if (!el) return;

  const start = el.selectionStart;
  const end = el.selectionEnd;

  const before = text.value.substring(0, start);
  const selected = text.value.substring(start, end);
  const after = text.value.substring(end);

  const opening = `<${tag}${extra}>`;
  const closing = `</${tag}>`;

  text.value = before + opening + selected + closing + after;

  nextTick(() => {
    el.focus();
    el.setSelectionRange(start + opening.length, end + opening.length);
  });
}
</script>
