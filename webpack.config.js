const path = require("path");

module.exports = {
  entry: {
    index: "./js/index.js",
    editor: "./js/editor.js",
  },
  output: {
    filename: "[name].bundle.js",
    path: path.resolve(__dirname, "./static")
  }
};
