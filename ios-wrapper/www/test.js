const jsdom = require("jsdom");
const { JSDOM } = jsdom;
const dom = new JSDOM(`<!DOCTYPE html><button class="dev-btn-stack"><button onclick="navigateTo('home')"></button></button>`);
try {
  dom.window.document.querySelector('.dev-btn-stack button[onclick="navigateTo(\'home\')"]');
  console.log("Valid selector");
} catch(e) {
  console.log("Invalid selector:", e.message);
}
