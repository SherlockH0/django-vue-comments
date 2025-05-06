<script setup lang="ts">
import type { CommentObject } from "../scripts/interfaces";
import CommentButton from "./CommentButton.vue";
import { format } from "date-fns";
import { computed, ref } from "vue";
import VueEasyLightbox from "vue-easy-lightbox";

const props = defineProps<{
  data: CommentObject;
  depth: number;
}>();

const lightboxVisible = ref<boolean>(false);
const open = ref<boolean>(props.depth < 3);

function onLightboxShow() {
  lightboxVisible.value = true;
}

const date = computed(() => {
  const date = new Date(props.data.datetime_created);
  return format(date, "kk:mm, dd.MM.yy");
});
</script>

<template>
  <li :class="{ 'ps-6 pe-0 last-of-type:pb-0': depth > 0 }" class="p-4">
    <div
      class="bg-neutral text-neutral-content mb-2 flex items-center gap-4 rounded-xl p-2 px-3"
    >
      <div class="font-bold">{{ data.username }}</div>
      <div class="italic">{{ data.email }}</div>
      <div class="text-xs">
        {{ date }}
      </div>
      <div class="ms-auto">
        <button
          class="btn btn-square btn-sm btn-ghost"
          :class="{ 'btn-active': !open }"
          v-if="data.children.length !== 0"
          @click="open = !open"
        >
          <svg
            v-if="open"
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            viewBox="0 0 24 24"
          >
            <path
              fill="none"
              stroke="currentColor"
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="m8 14l4-4l4 4"
            />
          </svg>
          <svg
            v-else
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            viewBox="0 0 24 24"
          >
            <path
              fill="none"
              stroke="currentColor"
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="m16 10l-4 4l-4-4"
            />
          </svg>
        </button>
        <CommentButton
          class="btn btn-square btn-sm btn-ghost ms-3"
          :parent="data"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="16"
            height="16"
            viewBox="0 0 24 24"
          >
            <path
              fill="none"
              stroke="currentColor"
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M7 13L3 9m0 0l4-4M3 9h13a5 5 0 0 1 0 10h-5"
            />
          </svg>
        </CommentButton>
      </div>
    </div>
    <p class="p-1" v-html="data.text"></p>
    <template v-if="data.attachment">
      <template v-if="data.attachment.image">
        <vue-easy-lightbox
          :visible="lightboxVisible"
          :imgs="data.attachment.url"
          @hide="lightboxVisible = false"
        >
          <template v-slot:close-btn="{ close }">
            <button
              @click="close"
              class="btn btn-square absolute right-4 top-4"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="24"
                height="24"
                viewBox="0 0 24 24"
              >
                <path
                  fill="none"
                  stroke="currentColor"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="m18 18l-6-6m0 0L6 6m6 6l6-6m-6 6l-6 6"
                />
              </svg>
            </button>
          </template>
          <template v-slot:toolbar="{ toolbarMethods }">
            <div
              class="absolute w-full bottom-0 grid grid-flow-col justify-center pb-5 gap-3"
            >
              <div class="join">
                <button
                  class="join-item btn btn-square"
                  @click="toolbarMethods.zoomIn"
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="24"
                    height="24"
                    viewBox="0 0 24 24"
                  >
                    <path
                      fill="none"
                      stroke="currentColor"
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M7 10h3m0 0h3m-3 0V7m0 3v3m5 2l6 6m-11-4a7 7 0 1 1 0-14a7 7 0 0 1 0 14"
                    />
                  </svg>
                </button>
                <button
                  class="join-item btn btn-square"
                  @click="toolbarMethods.zoomOut"
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="24"
                    height="24"
                    viewBox="0 0 24 24"
                  >
                    <path
                      fill="none"
                      stroke="currentColor"
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M7 10h6m2 5l6 6m-11-4a7 7 0 1 1 0-14a7 7 0 0 1 0 14"
                    />
                  </svg>
                </button>
              </div>
              <div class="join">
                <button
                  class="join-item btn btn-square"
                  @click="toolbarMethods.rotateLeft"
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="24"
                    height="24"
                    viewBox="0 0 24 24"
                  >
                    <path
                      fill="none"
                      stroke="currentColor"
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M7 13L3 9m0 0l4-4M3 9h13a5 5 0 0 1 0 10h-5"
                    />
                  </svg>
                </button>
                <button
                  class="join-item btn btn-square"
                  @click="toolbarMethods.rotateRight"
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="24"
                    height="24"
                    viewBox="0 0 24 24"
                  >
                    <path
                      fill="none"
                      stroke="currentColor"
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="m17 13l4-4m0 0l-4-4m4 4H8a5 5 0 0 0 0 10h5"
                    />
                  </svg>
                </button>
              </div>
            </div>
          </template>
        </vue-easy-lightbox>
        <div class="avatar cursor-pointer" @click="onLightboxShow">
          <div class="w-24 rounded">
            <img :src="data.attachment.url" />
          </div>
        </div>
      </template>
      <template v-else>
        <a role="button" :href="data.attachment.url" class="btn">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            viewBox="0 0 24 24"
          >
            <path
              fill="none"
              stroke="currentColor"
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M12 12v6m0 0l3-2m-3 2l-3-2m4-13H8.2c-1.12 0-1.68 0-2.108.218a2 2 0 0 0-.874.874C5 4.52 5 5.08 5 6.2v11.6c0 1.12 0 1.68.218 2.108a2 2 0 0 0 .874.874c.427.218.987.218 2.105.218h7.606c1.118 0 1.677 0 2.104-.218c.377-.192.683-.498.875-.874c.218-.428.218-.986.218-2.104V9m-6-6c.286.003.466.014.639.055q.308.075.578.24c.202.124.375.297.72.643l3.126 3.125c.346.346.518.518.642.72q.165.271.24.578c.04.173.051.354.054.639M13 3v2.8c0 1.12 0 1.68.218 2.108a2 2 0 0 0 .874.874c.427.218.987.218 2.105.218h2.802m0 0H19"
            />
          </svg>
          {{ data.attachment.name }}
        </a>
      </template>
    </template>
    <ul v-show="open" class="mt-6 flex flex-col">
      <Comment
        v-for="child in data.children"
        :key="child.id"
        :data="child"
        :parent="data.id"
        :child="true"
        :depth="depth + 1"
      />
    </ul>
  </li>
</template>
