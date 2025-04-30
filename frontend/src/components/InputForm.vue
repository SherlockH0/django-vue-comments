<script setup lang="ts">
import Textarea from "./Textarea.vue";
function sendMessage() {
  console.log("send");
}
</script>

<template>
  <button class="btn" onclick="my_modal_1.showModal()">open modal</button>
  <dialog id="my_modal_1" class="modal">
    <div class="modal-box">
      <form @submit.prevent="sendMessage">
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
            required
          />

          <label for="homepage" class="label">Homepage</label>
          <input
            type="url"
            placeholder="example.com"
            class="input validator"
            name="homepage"
          />

          <label class="label" for="text">Text</label>
          <Textarea />

          <label for="attachment" class="label">Attachment</label>
          <input
            name="attachment"
            type="file"
            class="file-input"
            accept="image/png, image/jpeg, image/gif, text/plain"
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
