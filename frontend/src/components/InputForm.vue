<script setup>
import { ref, defineModel, reactive } from "vue";
import Textarea from "./Textarea.vue";

const emit = defineEmits(["send"]);

const model = reactive({
  username: "sherlock",
  email: "dd@ff.com",
  homepage: "https://",
  text: "hi!",
});

function send() {
  console.log(attachment);
  emit("send", [{ ...model }, attachment]);

  model.text = "";
  fileInput.value.value = null;
}

let attachment = null;
const fileInput = ref();
</script>

<template>
  <dialog id="comment_modal" class="modal">
    <div class="modal-box">
      <form @submit.prevent="send">
        <fieldset class="fieldset [&>*]:w-full">
          <legend class="fieldset-legend text-lg">Add comment</legend>

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
            v-model="model.username"
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
            v-model="model.email"
            required
          />

          <label for="homepage" class="label">Homepage</label>
          <input
            type="url"
            placeholder="example.com"
            value="https://"
            class="input validator"
            v-model="model.homepage"
            name="homepage"
          />

          <label class="label" for="text">Text</label>
          <Textarea v-model="model.text" />

          <label for="attachment" class="label">Attachment</label>
          <input
            name="attachment"
            type="file"
            class="file-input"
            ref="fileInput"
            @change="attachment = fileInput.files[0] || null"
            accept="image/png, image/jpeg, image/gif, text/plain"
            title="Must be an image or a txt file under 100KB"
          />

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
