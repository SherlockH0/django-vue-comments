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
    if (file.type == "text/plain" && file.size >= 1000 * 100) {
      throw new Error("Text file too large");
    }
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
  comments.value.push(JSON.parse(event.data));
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
    const response = await fetch(`${BACKEND_URL}/comments/`);
    if (!response.ok) {
      throw new Error(`Response status: ${response.status}`);
    }

    const json = await response.json();
    comments.value = comments.value.concat(json.results);

    comments.value.forEach((element) => {
      console.log(element.email);
    });
  } catch (error) {
    console.error(error.message);
  }
}
loadComments();
let comments = ref([]);
</script>

<template>
  <CommentButton>New Comment</CommentButton>
  <InputForm @send="handleMessage" />
  <ul
    class="bg-base-100 rounded-box mx-auto mt-6 flex max-w-2xl flex-col shadow"
  >
    <Comment v-for="comment in comments" :data="comment" />
  </ul>
  <div class="flex w-full items-center">
    <div class="join mx-auto">
      <button class="join-item btn">1</button>
      <button class="join-item btn btn-active">2</button>
      <button class="join-item btn">3</button>
      <button class="join-item btn">4</button>
    </div>
  </div>
</template>
