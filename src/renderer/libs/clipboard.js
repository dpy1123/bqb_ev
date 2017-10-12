const exec = require('child_process').exec
const {clipboard, nativeImage} = require('electron')

export function gif2clipboard(img_id){  
    console.log('cmd: python3 '+__dirname+'/client_script.py '+img_id)
    exec('python3 '+__dirname+'/client_script.py '+img_id, {shell: '/bin/bash'}, function(error, stdout, stderr){
            
        if(error) {
            console.error('error: ' + stderr)
            return
        }
        console.log('stdout: \n' + stdout)
    })
}

export function jpg2clipboard(event) {
    let img = event.target
    var canvas = document.createElement('canvas')
    var ctx = canvas.getContext('2d')
    canvas.height = img.naturalHeight
    canvas.width = img.naturalWidth
    ctx.drawImage(img, 0, 0)
    var dataURL = canvas.toDataURL()
    clipboard.writeImage(nativeImage.createFromDataURL(dataURL))
    console.log('copied!')
}