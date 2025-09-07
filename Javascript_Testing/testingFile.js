import homePage from './homePage.js';

let page1 = homePage
let page2 = homePage

console.log(page1.tabs.add)
console.log(page2.tabs.add)

page1.tabs.add = "Added"

console.log(page1.tabs.add)
console.log(page2.tabs.add)