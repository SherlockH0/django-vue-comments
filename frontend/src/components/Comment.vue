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
          <Icon v-if="open" icon="ci:caret-down-md" width="24" height="24" />
          <Icon v-else icon="ci:caret-up-md" width="24" height="24" />
        </button>
        <CommentButton
          class="btn btn-square btn-sm btn-ghost ms-3"
          :parent="data"
        >
          <Icon icon="ci:arrow-undo-up-left" width="16" height="16" />
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
              <Icon icon="ci:close-circle" width="24" height="24" />
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
                  <Icon
                    icon="ci:magnifying-glass-plus"
                    width="24"
                    height="24"
                  />
                </button>
                <button
                  class="join-item btn btn-square"
                  @click="toolbarMethods.zoomOut"
                >
                  <Icon
                    icon="ci:magnifying-glass-minus"
                    width="24"
                    height="24"
                  />
                </button>
              </div>
              <div class="join">
                <button
                  class="join-item btn btn-square"
                  @click="toolbarMethods.rotateLeft"
                >
                  <Icon icon="ci:arrow-undo-up-left" width="24" height="24" />
                </button>
                <button
                  class="join-item btn btn-square"
                  @click="toolbarMethods.rotateRight"
                >
                  <Icon icon="ci:arrow-undo-up-right" width="24" height="24" />
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
        <a
          role="button"
          :href="data.attachment.url"
          class="btn"
          target="_blank"
        >
          <Icon icon="ci:file-download" width="24" height="24" />
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
<script setup lang="ts">
import type { CommentObject } from "../scripts/interfaces";
import CommentButton from "./CommentButton.vue";
import { Icon } from "@iconify/vue";
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
