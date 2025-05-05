export interface CommentObject {
  id: number;
  parent?: number;
  username: string;
  email: string;
  text: string;
  datetime_created: string;
  datetime_edited: string;
  attachment: string | null;
  children: CommentObject[];
}
export interface CommentRequest {
  username: string;
  email: string;
  text: string;
  homepage?: string;
  parent?: number;
  attachment: File | null;
}

export type ToastEvent = {
  type: "info" | "success" | "warning" | "error";
  message: string;
};

export type NewCommentEvent = {
  parent?: CommentObject;
};
export type Events = {
  toast: ToastEvent;
  new_comment: NewCommentEvent;
};

export interface FilterInterface {
  name: "username" | "email" | "datetime_created";
  display: string;
  active: boolean;
}
