<script setup lang="ts">
import { inject, useTemplateRef, watch } from "vue";

const attachment = defineModel<File | null>();
interface ErrorsInterface {
  fileErrors: string[];
  cleanFileErrors: Function;
}
const defalutErrors: ErrorsInterface = {
  fileErrors: [],
  cleanFileErrors: () => {},
};
const { fileErrors, cleanFileErrors } =
  inject<ErrorsInterface>("fileErrors") || defalutErrors;

watch(attachment, (newValue, oldValue) => {
  if (oldValue != null && !newValue) {
    cleanFile();
  }
});

function cleanFile() {
  if (fileInput.value?.files) {
    fileInput.value.value = "";
    attachment.value = null;
    cleanFileErrors();
  }
}

function changeFile() {
  attachment.value = fileInput.value?.files?.[0] || null;
  cleanFileErrors();
}
const fileInput = useTemplateRef("input");
</script>

<template>
  <div class="join">
    <input
      name="attachment"
      type="file"
      class="file-input join-item w-full"
      :class="{ 'input-error': fileErrors }"
      ref="input"
      @change="changeFile"
      accept="image/png, image/jpeg, image/gif, text/plain"
    />
    <button
      type="button"
      class="btn join-item btn-error btn-soft"
      @click="cleanFile"
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        width="24"
        height="24"
        viewBox="0 0 24 24"
      >
        <path
          fill="none"
          stroke="currentColor"
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="m18 18l-6-6m0 0L6 6m6 6l6-6m-6 6l-6 6"
        />
      </svg>
    </button>
  </div>
  <p v-if="fileErrors" class="text-error block mt-2 text-xs">
    <template v-for="error in fileErrors">
      {{ error }}
      <br />
    </template>
  </p>
</template>
