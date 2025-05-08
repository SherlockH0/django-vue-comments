<template>
  <label for="attachment" class="label">Attachment</label>
  <div class="join">
    <input
      name="attachment"
      type="file"
      class="file-input join-item w-full"
      :class="{ 'input-error': formErrors?.attachment }"
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
  <p v-if="formErrors?.attachment" class="text-error label">
    <template v-for="error in formErrors.attachment">
      {{ error }}
      <br />
    </template>
  </p>
</template>
<script setup lang="ts">
import type { FormErrors } from "../scripts/interfaces.ts";
import { inject, useTemplateRef, watch } from "vue";

const attachment = defineModel<File | null>();

const formErrors = inject<FormErrors>("formErrors") || {};

watch(attachment, (newValue, oldValue) => {
  if (oldValue != null && !newValue) {
    cleanFile();
  }
});

function cleanFile() {
  if (fileInput.value?.files) {
    fileInput.value.value = "";
    attachment.value = null;
  }
}

function changeFile() {
  attachment.value = fileInput.value?.files?.[0] || null;
}
const fileInput = useTemplateRef("input");
</script>
