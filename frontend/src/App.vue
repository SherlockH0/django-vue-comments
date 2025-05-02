<script setup>
import { ref } from "vue";
import InputForm from "./components/InputForm.vue";
import Comment from "./components/Comment.vue";
import CommentButton from "./components/CommentButton.vue";
import { BACKEND_URL, WEBSOCKET_URL } from "./scripts/config.js";

const attachment = ref(null);

async function uploadFile(file) {
  console.log(file);
  try {
    const response = await fetch(`${BACKEND_URL}/attachments/upload/`, {
      method: "PUT",
      headers: {
        "Content-Disposition": `attachment; filename="${file.name}`,
      },
      body: file,
    });
    if (!response.ok) {
      throw new Error(`Response status: ${response.status}`);
    }

    const json = await response.json();
    // attachment.value.files = null;
    return json.id;
  } catch (error) {
    console.error(error.message);
  }
}
const socket = new WebSocket(`${WEBSOCKET_URL}/comments`);

socket.addEventListener("open", (event) => {
  console.log("WebSocket connected!");
});

socket.addEventListener("message", (event) => {
  console.log(event.data);
  comments.value = [JSON.parse(event.data), ...comments.value];
});

async function handleMessage(data) {
  let attachment_id = null;
  console.log(data[1]);
  if (data[1]) {
    attachment_id = await uploadFile(data[1]);
  }
  socket.send(
    JSON.stringify({ comment: { ...data[0], attachment: attachment_id } }),
  );
}

async function loadComments(page) {
  try {
    const response = await fetch(`${BACKEND_URL}/comments/?page=${page}`);
    if (!response.ok) {
      throw new Error(`Response status: ${response.status}`);
    }

    const json = await response.json();

    comments.value = json.results;
    pages.value = json.total_pages;
    currentPage.value = page;
  } catch (error) {
    console.error(error.message);
  }
}

const pages = ref(0);
const currentPage = ref(1);

loadComments(1);
let comments = ref([]);
</script>

<template>
  <main class="flex max-h-svh flex-col">
    <div class="bg-base-200 grid place-items-center p-4">
      <CommentButton>Add Comment</CommentButton>
    </div>
    <InputForm @send="handleMessage" />
    <div class="overflow-x-auto">
      <ul class="list bg-base-100 rounded-box shadow-md">
        <Comment v-for="comment in comments" :data="comment" />
      </ul>
    </div>
    <div class="bg-base-200 grid place-items-center p-4">
      <div class="join" v-if="pages > 1">
        <button
          class="join-item btn"
          @click="loadComments(page)"
          :class="{ 'btn-primary': page == currentPage }"
          v-for="page in pages"
        >
          {{ page }}
        </button>
      </div>
    </div>
  </main>
</template>
