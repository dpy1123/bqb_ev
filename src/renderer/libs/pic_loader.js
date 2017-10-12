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