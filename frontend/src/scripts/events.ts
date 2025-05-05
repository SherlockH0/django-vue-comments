import type { Events } from "./interfaces";
import mitt from "mitt";

export const emitter = mitt<Events>();
