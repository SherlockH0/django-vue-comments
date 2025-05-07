<script setup lang="ts">
import Comment from "./components/Comment.vue";
import CommentButton from "./components/CommentButton.vue";
import Filters from "./components/Filters.vue";
import InputForm from "./components/InputForm.vue";
import Toasts from "./components/Toasts.vue";
import { BACKEND_URL, WEBSOCKET_URL } from "./scripts/config";
import { emitter } from "./scripts/events.ts";
import type { CommentObject, SocketEvent } from "./scripts/interfaces.ts";
import { onMounted, provide, ref, useTemplateRef } from "vue";

const comments = ref<CommentObject[]>([]);
const pages = ref(0);
const currentPage = ref(1);

const comment = useTemplateRef("comment");

const socket = new WebSocket(`${WEBSOCKET_URL}/comments`);

const fileErrors = ref<any>(null);
const formError = ref<string | null>();

socket.addEventListener("open", () => {
  console.log("WebSocket connected!");
});

function insertComment(tree: CommentObject[], newComment: CommentObject) {
  for (const node of tree) {
    if (node.id === newComment.parent) {
      node.children.unshift(newComment);
      return true;
    } else if (node.children.length) {
      if (insertComment(node.children, newComment)) return true;
    }
  }
  return false;
}

socket.addEventListener("message", (event) => {
  const response: SocketEvent = JSON.parse(event.data);
  formError.value = null;
  switch (response.type) {
    case "comment":
      if (response.body.parent === null) {
        comments.value.unshift(response.body);
      } else {
        insertComment(comments.value, response.body);
      }
      emitter.emit("clean_form", null);
      break;
    case "error":
      formError.value = response.body.error;
      break;
  }
});

async function uploadFile(file: File): Promise<number | null> {
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
  const data = JSON.stringify({
    comment: { ...comment.value.data, attachment: attachment_id },
  });
  socket.send(data);
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
provide("formError", formError);
</script>

<template>
  <main class="flex max-h-svh flex-col">
    <div class="bg-base-200 grid place-items-center p-4 space-y-4">
      <CommentButton class="btn btn-primary">Add Comment</CommentButton>
      <Filters @change="updateComments" />
    </div>
    <InputForm @send="handleMessage" ref="comment" />
    <div class="overflow-x-auto">
      <ul class="list bg-base-100 rounded-box shadow-md p-6">
        <Comment v-for="data in comments" :key="data.id" :data :depth="0" />
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
