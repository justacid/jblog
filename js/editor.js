import * as MarkdownIt from "markdown-it";
import * as hljs from "highlightjs";

document.addEventListener("DOMContentLoaded", function() {
  let title = document.getElementById("input-title");
  let textarea = document.getElementById("edit-text");
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

  textarea.oninput = function() {
    this.style.height = "";
    this.style.height = this.scrollHeight + "px";

    const markdown = renderer.render(textarea.value);
    prev_title.innerHTML = "<h1 id='prev-title'>" + title.value + "</h1>";
    preview.innerHTML = markdown;
  };

  title.oninput = function() {
    textarea.oninput();
  };
  textarea.oninput();
});
