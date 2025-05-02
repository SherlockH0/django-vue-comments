<script setup>
defineProps({
  data: Object,
  child: Boolean,
});
</script>

<template>
  <li :class="{ 'ps-6 pe-0': child }" class="p-4">
    <div
      class="bg-neutral text-neutral-content mb-2 flex items-center gap-4 rounded-xl p-2 px-3"
    >
      <div class="font-bold">{{ data.username }}</div>
      <div class="text-xs">{{ data.date }}</div>
      <button class="btn btn-square btn-sm btn-ghost ms-auto">
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
      </button>
    </div>
    <p class="p-1">
      {{ data.text }}
    </p>
    <ul class="mt-6 flex flex-col">
      <Comment v-for="child in data.children" :data="child" :child="true" />
    </ul>
  </li>
</template>
