<template>
<div class="pane">
    <div id='uploader'>
        <input type="file" multiple class="input-file" accept="image/png,image/jpeg,image/gif" v-on:change="select">
        <button class="btn btn-large" v-on:click="upload">upload!</button>
        progress: <span>{{progress | numfixed(2)}}</span>%
    </div>

    <div id="unsaved-list" v-show="unsaved_files.length>0">
        unsaved: 
        <div v-for="file in unsaved_files" >
            <span>{{file.name}} [{{Math.round(file.size/1024)}} k] </span>   
        </div>
    </div>   

    <div id="update-list" class="list-group">
        <div v-for="file in selected_files" class="list-group-item" :id="file.name">
            <img class="img media-object pull-left">
            <div class="media-body">
                <span>{{file.name}} [{{Math.round(file.size/1024)}} k] </span>
            </div>
        </div>
    </div>    
</div>       
</template>

<script>
const host = require('../config').host  
// var axios = require('axios')   

var batch_size = 10

// Build a worker from an anonymous function body
var blobURL = URL.createObjectURL( new Blob([ '(',
    function(){
        //Long-running work here
        onmessage = function(event) {
            var files = event.data.files
            for (var i = 0; i < files.length; i++) {
                var file = files[i]
                var reader = new FileReader()
                reader.readAsDataURL(file)  
                reader.onload = (function(index) {
                    return function(event){
                        img_base64_str = event.target.result
                        postMessage({'index': index, 'data_url': img_base64_str})         
                    }
                })(i) 
            }
        }
    }.toString(),
')()' ], { type: 'application/javascript' } ) )

var worker = new Worker(blobURL)
//var worker = new Worker(__dirname+'/../libs/pic_loader.js')
worker.onmessage = function(event){
    var index = event.data.index
    var img_base64_str = event.data.data_url
    // console.log(index)
    var img = document.querySelector('.list-group-item:nth-child('+(index+1)+')').querySelector('img')
    resize_img(img_base64_str, img, 100)  
}
worker.onerror = function(e){
    console.log('err: ' + e.message)
    worker.terminate()
}
function resize_img(img_base64_str, img, size_limit){
    var type = img_base64_str.slice(11, img_base64_str.indexOf(';')) //data:image/gif;base64,...
    if(type=='gif'){ //gif不缩放，直接给原来的base64str
        img.src = img_base64_str
    }else{
        var canvas = document.createElement('canvas')
        canvas.width = size_limit
        canvas.height = size_limit
        var ctx = canvas.getContext('2d')
        ctx.clearRect(0, 0, size_limit, size_limit)
        var tmp_img = document.createElement('img')
        tmp_img.src = img_base64_str
        tmp_img.onload = function() {
            var w = tmp_img.width
            var h = tmp_img.height
            var r = w/h
            if(r>=1)
                ctx.drawImage(tmp_img, 0, (size_limit -size_limit/r)/2, size_limit, size_limit/r)
            else
                ctx.drawImage(tmp_img, (size_limit -size_limit*r)/2, 0, size_limit*r, size_limit)
            img.src = canvas.toDataURL(type)
        }      
    }
}

export default {
    name: 'upload',
    data: () => {
        return {
            progress: 0,
            selected_files: [],
            upload_results: [],
            unsaved_files: []
        }
    },
    methods: {
        select: function(event) {
            var files = event.target.files
            if (files.length < 1) return
            this.selected_files = files
            this.progress = 0
            this.upload_results = []
            this.unsaved_files = []
            worker.postMessage({'files': files})
        },
        upload: function() {
            this.progress = 0
            this.upload_results = []
            this.unsaved_files = []

            var files = this.selected_files
            var batch_number = Math.ceil(files.length / batch_size)
            var reast = files.length % batch_size
            
            if(batch_number > 1) {
                for (var i = 0; i < batch_number-1; i++) {
                    var form_data = new FormData()
                    for (var j = 0; j < batch_size; j++) {
                        var file = files[i*batch_size+j]
                        form_data.append(file.name, file)
                    }
                    this.$http.post(host+'/uploads', form_data)
                    .then(function(resp){
                        this.upload_results.push(resp.data)
                        this.progress = this.upload_results.length/batch_number * 100
                    })   
                    // var instance = axios.create()
                    // instance.post(host+'/uploads', form_data).then(function(resp){
                    //     this.upload_results.push(resp.data.data)
                    //     this.progress = this.upload_results.length/batch_number * 100
                    // })           
                }
            }
            if(reast > 0) {
                var form_data = new FormData()
                for (var j = 0; j < reast; j++) {
                    var file = files[batch_size*(batch_number-1)+j]
                    form_data.append(file.name, file)
                }
                this.$http.post(host+'/uploads', form_data)
                .then(function(resp){
                    this.upload_results.push(resp.data)
                    this.progress = this.upload_results.length/batch_number * 100
                })
                // var instance = axios.create()
                // instance.post(host+'/uploads', form_data).then(function(resp){
                //     this.upload_results.push(resp.data.data)
                //     this.progress = this.upload_results.length/batch_number * 100
                // })
            }   
        }
    },
    watch: {
        'progress': function(val, old_val) {
            if(val < 100) return
            var saved = []
            var unsaved = []
            for(var i=0; i<this.upload_results.length; i++){
                var result = this.upload_results[i]
                saved = saved.concat(result.data.file_saved)
                unsaved = unsaved.concat(result.data.file_unsaved)
            }
            

            var unsaved_files = []
            var file_names = unsaved.map((e)=>e.filename)
            for(var i=0; i<this.selected_files.length; i++){
                var file = this.selected_files[i]
                if(file_names.indexOf(file.name)>-1){
                    unsaved_files.push(file)
                }
            }
            this.unsaved_files = unsaved_files

            console.log(unsaved_files.map((e)=>e.path))
        }
    },
    filters: {
        numfixed: function (value, keep_digit) {
            return isNaN(value)? value: value.toFixed(keep_digit)
        }
    }
}
</script>

<style>
.input-file {
    display: inline-block;
    padding: 4px 10px;
}
.list-group-item img {
    width: 100px;
}
</style>
