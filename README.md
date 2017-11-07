# bqb_ev

> bqb=表情包，e=electron，v=vue

### release
release里可以直接下载mac版客户端

### 功能说明
- 第一个panel是搜索页，0是页数，任何时候都需要填页数。
- 第二个panel是上传页，如果图片在服务器上已有相似图片（基于imagehash，详见[bqb_web](https://github.com/dpy1123/bqb_web)项目）并不会上传，页面会列出unsaved file，console中会打出详细信息。
- 在搜索结果的图片上单击，可以复制图片到剪贴板。（如果想支持gif复制，请python3启动一个[gif4wx.py](https://github.com/dpy1123/gif4wx)）
- cmd+shift+c 可以呼出debug控制台。


#### Build Setup
``` bash
# install dependencies
npm install
# serve with hot reload at localhost:9080
npm run dev
# build electron application for production
npm run build
```

---
This project was generated with [electron-vue](https://github.com/SimulatedGREG/electron-vue)@[de85f81](https://github.com/SimulatedGREG/electron-vue/tree/de85f81890c01500113738bfe57bef136f9fbf52) using [vue-cli](https://github.com/vuejs/vue-cli). Documentation about the original structure can be found [here](https://simulatedgreg.gitbooks.io/electron-vue/content/index.html).
