<script setup lang="ts">
import { BACKEND_URL } from "../scripts/config";
import { emitter } from "../scripts/events";
import type { CommentObject, CommentRequest } from "../scripts/interfaces";
import FileInput from "./FileInput.vue";
import Textarea from "./Textarea.vue";
import { inject, reactive, ref, useTemplateRef, watch } from "vue";

const emit = defineEmits(["send"]);
const commentModal = useTemplateRef<HTMLDialogElement>("modal");
const parent = ref<CommentObject | null>(null);
const captcha = ref<{ key: string; image_url: string }>();

const data = reactive<CommentRequest>({
  username: "Gandalf",
  email: "gandalf@gmail.com",
  text: "You shall not pass!!!",
  attachment: null,
  captcha_code: "",
  captcha_hashkey: "",
});

function send() {
  emit("send");
}

const formError = inject<string | null>("formError") || null;

watch(parent, (newValue) => {
  data.parent = newValue?.id;
});

emitter.on("new_comment", (event) => {
  parent.value = event.parent || null;
  commentModal.value?.showModal();
});

emitter.on("clean_form", async () => {
  commentModal.value?.close();
  data.text = "";
  data.attachment = null;
  data.captcha_code = "";
  await getCaptcha();
});

defineExpose({
  data,
});

async function getCaptcha() {
  const response = await fetch(`${BACKEND_URL}/comments/captcha`);
  const json = await response.json();
  captcha.value = json;
  data.captcha_hashkey = json.key;
}
getCaptcha();
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

          <label for="captcha" class="label">CAPTCHA</label>
          <div class="flex gap-2">
            <img :src="captcha?.image_url" class="rounded-lg" />
            <div class="join grow">
              <input
                type="text"
                name="captcha"
                placeholder="Enter text you see on the image"
                v-model="data.captcha_code"
                required
                class="input join-item"
              />
              <button @click="getCaptcha" class="btn join-item" type="button">
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
                    d="M10 16H5v5m9-13h5V3M4.583 9.003a8 8 0 0 1 14.331-1.027m.504 7.021a8 8 0 0 1-14.332 1.027"
                  />
                </svg>
              </button>
            </div>
          </div>
          <p v-if="formError" class="text-error">{{ formError }}</p>

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
