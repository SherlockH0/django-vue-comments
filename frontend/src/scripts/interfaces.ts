export interface CommentObject {
  id: number;
  parent: number | null;
  user: {
    username: string;
    email: string;
  };
  text: string;
  datetime_created: string;
  datetime_edited: string;
  attachment: {
    url: string;
    image: boolean;
    name: string;
  } | null;
  children: CommentObject[];
}

export type CommentMessage = {
  type: "comment";
  body: CommentObject;
};

export interface FormErrors {
  text?: string[];
  captcha?: string[];
  attachment?: string[];
}

type FormErrorMessage = {
  type: "error";
  body: FormErrors;
};

export type SocketMessage = CommentMessage | FormErrorMessage;

export interface CommentRequest {
  text: string;
  parent?: number;
  attachment: File | null;
  captcha_code: string;
  captcha_hashkey: string;
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
  loading: boolean;
  new_comment: NewCommentEvent;
  clean_form: null;
};

export interface FilterInterface {
  name: string;
  display: string;
  active: boolean;
}
