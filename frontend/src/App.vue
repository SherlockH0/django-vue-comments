<script setup lang="ts">
import Comment from "./components/Comment.vue";
import CommentButton from "./components/CommentButton.vue";
import Filters from "./components/Filters.vue";
import InputForm from "./components/InputForm.vue";
import Toasts from "./components/Toasts.vue";
import { BACKEND_URL, WEBSOCKET_URL } from "./scripts/config";
import { emitter } from "./scripts/events.ts";
import type { CommentObject } from "./scripts/interfaces.ts";
import { onMounted, provide, ref, useTemplateRef } from "vue";

const comments = ref<CommentObject[]>([]);
const pages = ref(0);
const currentPage = ref(1);

const comment = useTemplateRef("comment");

const socket = new WebSocket(`${WEBSOCKET_URL}/comments`);

const fileErrors = ref<any>(null);

socket.addEventListener("open", () => {
  console.log("WebSocket connected!");
});

socket.addEventListener("message", (event) => {
  const comment: CommentObject = JSON.parse(event.data);
  if (comment.parent || currentPage.value == 1) {
    comments.value = [comment, ...comments.value];
  } else {
    emitter.emit("toast", { type: "info", message: "New comment." });
  }
});

async function uploadFile(file: File): Promise<number | null> {
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
      const json = await response.json();
      fileErrors.value = json.detail;
      return null;
    }

    const json = await response.json();
    return json.id;
  } catch (error: any) {
    console.log(error.message);
    return null;
  }
}

async function handleMessage() {
  if (!comment.value) return;

  let attachment_id: number | null = null;
  if (comment.value.data.attachment) {
    attachment_id = await uploadFile(comment.value.data.attachment);
    if (!attachment_id) {
      return;
    }
  }
  const data = JSON.stringify({ comment: comment.value?.data });
  socket.send(data);
  comment.value.data.text = "";
  comment.value.data.attachment = null;
}

async function loadComments(page: number, filter: string = "") {
  try {
    const response = await fetch(
      `${BACKEND_URL}/comments/?page=${page}&ordering=${filter}`,
      {
        cache: "no-cache",
      },
    );
    if (!response.ok) {
      throw new Error(`Response status: ${response.status}`);
    }

    const json = await response.json();

    comments.value = json.results;
    pages.value = json.total_pages;
    currentPage.value = page;
  } catch (error: any) {
    console.error(error.message);
  }
}

function updateComments(filter: string | null, reversed: boolean) {
  loadComments(
    currentPage.value,
    filter ? `${reversed ? "-" : ""}${filter}` : "",
  );
}

onMounted(() => {
  loadComments(currentPage.value);
});

function cleanFileErrors() {
  fileErrors.value = null;
}

provide("fileErrors", {
  fileErrors,
  cleanFileErrors,
});
</script>

<template>
  <main class="flex max-h-svh flex-col">
    <div class="bg-base-200 grid place-items-center p-4 space-y-4">
      <CommentButton class="btn btn-primary">Add Comment</CommentButton>
      <Filters @change="updateComments" />
    </div>
    <InputForm @send="handleMessage" ref="comment" />
    <div class="overflow-x-auto">
      <ul class="list bg-base-100 rounded-box shadow-md">
        <Comment v-for="data in comments" :key="data.id" :data />
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
    <Toasts />
  </main>
</template>
