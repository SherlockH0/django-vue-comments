<script setup lang="ts">
import { useTemplateRef, nextTick, ref } from "vue";

let text = ref("");
const textarea = ref(null);

function insertTag(tag: String, extra: String = "") {
  const el = textarea.value;
  const start = el.selectionStart;
  const end = el.selectionEnd;

  const before = text.value.substring(0, start);
  const selected = text.value.substring(start, end);
  const after = text.value.substring(end);

  const opening = `<${tag}${extra}>`;
  const closing = `</${tag}>`;

  text.value = before + opening + selected + closing + after;

  // Reselect the inserted text
  nextTick(() => {
    el.focus();
    el.setSelectionRange(start + opening.length, end + opening.length);
  });
}
</script>
<template>
  <div class="join">
    <button type="button" @click="insertTag('i')" class="btn btn-sm join-item">
      <svg
        xmlns="http://www.w3.org/2000/svg"
        width="1rem"
        height="1rem"
        viewBox="0 0 24 24"
      >
        <path
          fill="none"
          stroke="currentColor"
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M8 19h2m0 0h2m-2 0l4-14m-2 0h2m0 0h2"
        />
      </svg>
    </button>
    <button
      type="button"
      @click="insertTag('strong')"
      class="btn btn-sm join-item"
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        width="1rem"
        height="1rem"
        viewBox="0 0 24 24"
      >
        <path
          fill="none"
          stroke="currentColor"
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M8 12h4.5M8 12V5h4.5a3.5 3.5 0 1 1 0 7M8 12v7h5.5a3.5 3.5 0 1 0 0-7h-1"
        />
      </svg>
    </button>
    <button
      type="button"
      @click="insertTag('code')"
      class="btn btn-sm join-item"
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        width="1rem"
        height="1rem"
        viewBox="0 0 24 24"
      >
        <path
          fill="none"
          stroke="currentColor"
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="m15 7l5 5l-5 5m-6 0l-5-5l5-5"
        />
      </svg>
    </button>
    <button
      type="button"
      @click="insertTag('a', ' href=\'\' title=\'\'')"
      class="btn btn-sm join-item"
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        width="1rem"
        height="1rem"
        viewBox="0 0 24 24"
      >
        <path
          fill="none"
          stroke="currentColor"
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M8 12h8m-1-4h2a4 4 0 0 1 0 8h-2M9 8H7a4 4 0 1 0 0 8h2"
        />
      </svg>
    </button>
  </div>
  <textarea
    class="join-item textarea w-full"
    name="text"
    placeholder="Start typing..."
    required
    ref="textarea"
    v-model="text"
  ></textarea>
</template>
