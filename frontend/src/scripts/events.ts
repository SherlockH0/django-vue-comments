import type { Events } from "./interfaces";
import mitt from "mitt";
import { ref } from "vue";

export const emitter = mitt<Events>();
export const loading = ref<boolean>(false);
