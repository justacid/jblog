import * as MarkdownIt from "markdown-it";
import * as hljs from "highlightjs";

document.addEventListener("DOMContentLoaded", function() {
  let tags = document.getElementById("edit-tags");
  let title = document.getElementById("edit-title");
  let post = document.getElementById("edit-text");
  let prev_title = document.getElementById("preview-title");
  let preview = document.getElementById("preview-markdown");

  const renderer = MarkdownIt({
    typographer: true,
    highlight: function(str, lang) {
      if (lang && hljs.getLanguage(lang)) {
        try {
          return hljs.highlight(lang, str).value;
        } catch (__) {}
      }
      return "";
    }
  });

  tags.oninput = function() {
    this.style.height = "";
    this.style.height = this.scrollHeight + "px";
  };

  post.oninput = function() {
    this.style.height = "";
    this.style.height = this.scrollHeight + "px";
    preview.innerHTML = renderer.render(post.value);
  };

  title.oninput = function() {
    this.style.height = "";
    this.style.height = this.scrollHeight + "px";
    prev_title.innerHTML = "<h1 id='prev-title'>" + title.value + "</h1>";
  };

  tags.oninput();
  title.oninput();
  post.oninput();
});
