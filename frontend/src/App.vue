<template>
  <Transition>
    <div
      class="absolute inset-0 h-svh grid place-items-center bg-black/30 z-50"
      v-if="loading"
    >
      <span class="loading loading-spinner loading-xl"></span>
    </div>
  </Transition>
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

<script setup lang="ts">
import Comment from "./components/Comment.vue";
import CommentButton from "./components/CommentButton.vue";
import Filters from "./components/Filters.vue";
import InputForm from "./components/InputForm.vue";
import Toasts from "./components/Toasts.vue";
import { BACKEND_URL, WEBSOCKET_URL } from "./scripts/config";
import { emitter } from "./scripts/events.ts";
import type {
  CommentObject,
  SocketMessage,
  FormErrors,
} from "./scripts/interfaces.ts";
import { onMounted, provide, ref, useTemplateRef } from "vue";

const comments = ref<CommentObject[]>([]);
const pages = ref<number>(0);
const currentPage = ref<number>(1);
const loading = ref<boolean>(false);

const comment = useTemplateRef("comment");

const socket = new WebSocket(`${WEBSOCKET_URL}/comments`);

const fileErrors = ref<any>(null);
const defaultErrors = {
  username: [],
  email: [],
  text: [],
  captcha: [],
  homepage: [],
};
const formErrors = ref<FormErrors>(defaultErrors);

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
  const response: SocketMessage = JSON.parse(event.data);

  formErrors.value = { ...defaultErrors };

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
      for (const key in response.body) {
        formErrors.value[key] = response.body[key];
      }
      break;
  }
});

async function uploadFile(file: File): Promise<number | null> {
  loading.value = true;
  try {
    const response = await fetch(`${BACKEND_URL}/api/attachments/upload/`, {
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
    emitter.emit("toast", { type: "error", message: error.message });
    return null;
  } finally {
    loading.value = false;
  }
}

async function handleMessage() {
  if (!comment.value) return;

  formErrors.value = { ...defaultErrors };

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
  loading.value = true;
  try {
    const response = await fetch(
      `${BACKEND_URL}/api/comments/?page=${page}&ordering=${filter}`,
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
    emitter.emit("toast", { type: "error", message: error.message });
  } finally {
    loading.value = false;
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

emitter.on("loading", (state) => {
  loading.value = state;
});

function cleanFileErrors() {
  fileErrors.value = null;
}

provide("fileErrors", {
  fileErrors,
  cleanFileErrors,
});
provide("formErrors", formErrors);
</script>

<style>
/* we will explain what these classes do next! */
.v-enter-active,
.v-leave-active {
  transition: opacity 0.5s ease;
}

.v-enter-from,
.v-leave-to {
  opacity: 0;
}
</style>
