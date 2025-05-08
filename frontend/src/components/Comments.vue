<template>
  <div class="bg-base-200 place-items-center p-4 flex px-8 flex-wrap">
    <CommentButton class="btn btn-primary me-auto">Add Comment</CommentButton>
    <Filters @change="updateComments" />
  </div>
  <InputForm @send="handleMessage" ref="inputForm" />
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
</template>
<script setup lang="ts">
import api from "../scripts/api.ts";
import { WEBSOCKET_URL } from "../scripts/config";
import { emitter, loading } from "../scripts/events";
import type {
  CommentObject,
  SocketMessage,
  FormErrors,
} from "../scripts/interfaces.ts";
import Comment from "./Comment.vue";
import CommentButton from "./CommentButton.vue";
import Filters from "./Filters.vue";
import InputForm from "./InputForm.vue";
import { provide, ref, useTemplateRef } from "vue";

const comments = ref<CommentObject[]>([]);
const pages = ref<number>(0);
const currentPage = ref<number>(1);

const inputForm = useTemplateRef("inputForm");

const formErrors = ref<FormErrors>({});

let socket: WebSocket | null;

function webSocketClose() {
  emitter.emit("toast", {
    type: "warning",
    message: "Socket disconnected. Reload to try again.",
  });
}

function webSocketMessage(message: { data: string }) {
  const response: SocketMessage = JSON.parse(message.data);

  formErrors.value = {};

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
      formErrors.value = response.body;
      break;
  }
}

function webSocketConnect() {
  api
    .post("/api/auth/generate_otp/")
    .then((response) => {
      const token = response.data.token;
      socket = new WebSocket(`${WEBSOCKET_URL}/comments?token=${token}`);

      socket.addEventListener("open", () => {
        console.log("WebSocket connected!");
      });
      socket.addEventListener("close", webSocketClose);
      socket.addEventListener("message", webSocketMessage);
    })
    .catch(() => {
      socket = null;
    });
}

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

async function uploadFile(file: File): Promise<number | null> {
  loading.value = true;

  return api
    .put("/api/attachments/upload/", file, {
      headers: {
        "Content-Disposition": `attachment; filename=${file.name}`,
      },
    })
    .then((response) => {
      return response.data.id;
    })
    .catch((error) => {
      if (error.response) {
        formErrors.value.attachment = error.response.data.detail;
        return null;
      }
      emitter.emit("toast", { type: "error", message: error.message });
      return null;
    })
    .finally(() => {
      loading.value = false;
    });
}

async function handleMessage() {
  if (!inputForm.value || !socket) return;

  formErrors.value = {};

  let attachment_id: number | null = null;
  if (inputForm.value.data.attachment) {
    attachment_id = await uploadFile(inputForm.value.data.attachment);
    if (!attachment_id) {
      return;
    }
  }
  const data = JSON.stringify({
    comment: { ...inputForm.value.data, attachment: attachment_id },
  });
  socket.send(data);
}

function loadComments(page: number, filter: string = "") {
  loading.value = true;
  api
    .get(`/api/comments/?page=${page}&ordering=${filter}`, {
      headers: {
        "Cache-Control": "no-cache, no-store, must-revalidate",
        Pragma: "no-cache",
        Expires: "0",
      },
    })
    .then((response) => {
      comments.value = response.data.results;
      pages.value = response.data.total_pages;
      currentPage.value = page;
    })
    .catch((error) => {
      emitter.emit("toast", { type: "error", message: error.message });
    })
    .finally(() => {
      loading.value = false;
    });
}

function updateComments(filter: string | null, reversed: boolean) {
  loadComments(
    currentPage.value,
    filter ? `${reversed ? "-" : ""}${filter}` : "",
  );
}

webSocketConnect();
loadComments(currentPage.value);

provide("formErrors", formErrors);
</script>
