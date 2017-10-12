<template>
<div class="pane">
     <div class="list-group">
        <div class="list-group-header">
                <input class="input-text" type="text" v-model='queryStr'>
                <button class="btn btn-large" v-on:click="query">search</button>

                <input class="input-text" type="text" v-model='p'>
            </div>
        </div>
        <div id="query-list" class="list-group">
            <div v-for="res in queryResult" class="list-group-item" :id="res._id">
                <img :src="res.url" class="img media-object pull-left" v-on:click="copy($event, res)" crossorigin="anonymous">
                <div class="media-body">
                    <input :value="res.tags" class="input-text">
                    <button class="btn btn-large" v-on:click="update(res)">update_tags</button>
                </div>
            </div>
        </div>
    </div>
</div>    
</template>

<script>
    const host = require('../config').host
    const {gif2clipboard, jpg2clipboard} = require('../libs/clipboard')
    export default {
        name : 'list',
        data: () => {
            return {
                p: 0,
                queryStr: '',
                queryResult: []
            }
        },
        methods: {
            query: function(e) {
                this.$http.get(host+'/imgs', {'params' : {'p': this.p, 'size': 10, 'q': this.queryStr}})
                .then((resp) => {
                    var imgs = resp.data.data.list
                    imgs.forEach(function(element) {
                        element.url = host+element.url
                    }, this);
                    this.queryResult = imgs
                })
            },
            copy: (event, img) => {
                if (img.suffix == '.gif')
                    gif2clipboard(img._id)
                else
                    jpg2clipboard(event)
            },
            update: function(img) {
                var tags = document.getElementById(img._id).querySelector('input').value.replace('，',',').split(',')
                this.$http.post(host+'/imgs/'+img._id, {'tags': tags})
                .then((resp) => {
                    console.log(resp.data.msg)
                })
            }
        }
    }
</script>

<style>
.list-group-item img {
    width: 100px;
}
</style>
