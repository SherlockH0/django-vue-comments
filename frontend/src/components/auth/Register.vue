<template>
  <form @submit.prevent="submit">
    <fieldset
      class="fieldset bg-base-200 border-base-300 rounded-box border p-4"
    >
      <p class="label text-error" v-if="errors.detail">{{ errors.detail }}</p>
      <Input
        type="text"
        required
        placeholder="Username"
        v-model="username"
        name="username"
        :errors="errors.username || []"
      />
      <Input
        type="email"
        required
        class="validator"
        placeholder="Email"
        v-model="email"
        name="email"
        :errors="errors.email || []"
      />

      <Input
        type="password"
        required
        placeholder="Password"
        v-model="password"
        name="password"
        :errors="errors.password || []"
      />

      <button class="btn btn-neutral mt-4">Register</button>
    </fieldset>
  </form>
</template>

<script setup lang="ts">
import Input from "../Input.vue";
import { isAuthenticated } from "@/scripts/api.ts";
import { BACKEND_URL, REFRESH_TOKEN, ACCESS_TOKEN } from "@/scripts/config.ts";
import { loading } from "@/scripts/events.ts";
import axios from "axios";
import { ref } from "vue";

const username = ref("");
const email = ref("");
const password = ref("");

const errors = ref();

function submit() {
  loading.value = true;
  axios
    .post(`${BACKEND_URL}/api/auth/register/`, {
      username: username.value,
      email: email.value,
      password: password.value,
    })
    .then(() => {
      axios
        .post(`${BACKEND_URL}/api/token/`, {
          username: username.value,
          password: password.value,
        })
        .then((response) => {
          errors.value = {};
          password.value = "";
          email.value = "";
          username.value = "";

          localStorage.setItem(ACCESS_TOKEN, response.data.access);
          localStorage.setItem(REFRESH_TOKEN, response.data.refresh);

          isAuthenticated.value = true;
        });
    })
    .catch((error) => {
      errors.value = error.response.data;
    })
    .finally(() => {
      loading.value = false;
    });
}
</script>
