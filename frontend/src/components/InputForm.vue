<script setup lang="ts">
import { emitter } from "../scripts/events";
import type { CommentObject, CommentRequest } from "../scripts/interfaces";
import FileInput from "./FileInput.vue";
import Textarea from "./Textarea.vue";
import { reactive, ref, useTemplateRef, watch } from "vue";

const emit = defineEmits(["send"]);
const comment_modal = useTemplateRef<HTMLDialogElement>("modal");
const parent = ref<CommentObject | null>(null);

const data = reactive<CommentRequest>({
  username: "Gandalf",
  email: "gandalf@gmail.com",
  text: "You shall not pass!!!",
  attachment: null,
});

function send() {
  emit("send");
}

watch(parent, (newValue) => {
  data.parent = newValue?.id;
});

emitter.on("new_comment", (event) => {
  parent.value = event.parent || null;
  comment_modal.value?.showModal();
});

emitter.on("clean_form", () => {
  comment_modal.value?.close();
  data.text = "";
  data.attachment = null;
});

defineExpose({
  data,
});
</script>

<template>
  <dialog ref="modal" class="modal">
    <div class="modal-box">
      <form @submit.prevent="send">
        <fieldset class="fieldset [&>*]:w-full">
          <legend class="fieldset-legend text-lg" v-if="!parent">
            Add comment
          </legend>
          <legend class="fieldset-legend text-lg" v-else>
            <span>
              Reply to <i>{{ parent.username }}</i>
            </span>
          </legend>
          <p v-if="parent" v-html="parent.text" class="truncate"></p>

          <label class="label" for="username">Username</label>
          <input
            type="text"
            name="username"
            placeholder="Your username"
            class="input validator"
            required
            pattern="[A-Za-z][A-Za-z0-9\-]*"
            minlength="3"
            maxlength="30"
            title="Only letters, numbers or dash"
            v-model="data.username"
          />
          <p class="validator-hint hidden">
            Must be 3 to 30 characters
            <br />containing only letters, numbers or dash
          </p>

          <label for="email" class="label">Email</label>
          <input
            type="email"
            placeholder="example@example.com"
            class="input validator"
            name="email"
            v-model="data.email"
            required
          />

          <label for="homepage" class="label">Homepage</label>
          <input
            type="url"
            placeholder="https://"
            class="input validator"
            v-model="data.homepage"
            name="homepage"
          />

          <label class="label" for="text">Text</label>
          <Textarea v-model="data.text" />

          <label for="attachment" class="label">Attachment</label>
          <FileInput v-model="data.attachment" />

          <div class="modal-action">
            <button class="btn" type="submit">Send</button>
            <form method="dialog">
              <button class="btn btn-soft btn-error">Cancel</button>
            </form>
          </div>
        </fieldset>
      </form>
    </div>
    <form method="dialog" class="modal-backdrop">
      <button>close</button>
    </form>
  </dialog>
</template>
