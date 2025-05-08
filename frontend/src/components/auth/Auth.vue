<template>
  <slot v-if="isAuthenticated"> </slot>
  <div class="grid place-items-center h-svh" v-else>
    <div class="tabs tabs-lift w-md">
      <input type="radio" name="tabs" class="tab" aria-label="Login" checked />
      <div class="tab-content bg-base-100 border-base-300 p-6">
        <Login />
      </div>

      <input type="radio" name="tabs" class="tab" aria-label="Register" />
      <div class="tab-content bg-base-100 border-base-300 p-6">
        <Register />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import Login from "./Login.vue";
import Register from "./Register.vue";
import { isAuthenticated, refreshToken } from "@/scripts/api.ts";
import { ACCESS_TOKEN } from "@/scripts/config.ts";
import { jwtDecode } from "jwt-decode";

auth().catch(() => {
  isAuthenticated.value = false;
});

async function auth() {
  const token = localStorage.getItem(ACCESS_TOKEN);
  if (!token) {
    isAuthenticated.value = false;
    return;
  }
  const decoded = jwtDecode(token);
  const tokenExpiration = decoded.exp;
  const now = Date.now() / 1000;

  if (tokenExpiration && tokenExpiration < now) {
    await refreshToken();
  } else {
    isAuthenticated.value = true;
  }
}
</script>
