/**
 * Created by LZH on 2017/4/29.
 */
   // common variables
var iBytesUploaded = 0;
var iBytesTotal = 0;
var iPreviousBytesLoaded = 0;
var iMaxFilesize = 10485760; // 10MB
var oTimer = 0;
var sResultFileSize = '';

//时间格式化
function secondsToTime(secs) {
    var hr = Math.floor(secs / 3600);
    var min = Math.floor((secs - (hr * 3600))/60);
    var sec = Math.floor(secs - (hr * 3600) -  (min * 60));

    if (hr < 10) {hr = "0" + hr; }
    if (min < 10) {min = "0" + min;}
    if (sec < 10) {sec = "0" + sec;}
    if (hr) {hr = "00";}
    return hr + ':' + min + ':' + sec;
};
//图片大小格式化
function bytesToSize(bytes) {
    var fileSize = 0;
    if (bytes > 1024 * 1024) {
        fileSize = (Math.round(bytes * 100 / (1024 * 1024)) / 100).toString() + 'MB';
    }
    else {
        fileSize = (Math.round(bytes * 100 / 1024) / 100).toString() + 'KB';
    }
    return fileSize
};

function fileSelected() {

    // hide different warnings
    document.getElementById('upload_response').style.display = 'none';
    document.getElementById('error').style.display = 'none';
    document.getElementById('error1').style.display = 'none';
    document.getElementById('error2').style.display = 'none';
    document.getElementById('abort').style.display = 'none';
    document.getElementById('warnsize').style.display = 'none';

    //在readFile中，我们首先获取file对象，然后通过file的type属性来检测文件类型，我们当然只允许选择图像类型的文件，然后我们new一个FileReader实例，并调用readAsDataURL方法来读取选中的图像文件，最后在onload事件中，获取到成功读取的文件内容，并以插入一个img节点的方式显示选中的图片。
    // 获取文件
    var oFile = document.getElementById('image_file').files[0];
    //创建FileReader对象
    var oReader = new FileReader();
    //检查文件大小，超出大小直接返回
    if (oFile.size > iMaxFilesize) {
        document.getElementById('warnsize').style.display = 'block';
        return;
    }
// 检查是否支持FileReader对象
    if (typeof oReader != 'undefined') {
　　　　var acceptedTypes = {
　　　　　　'image/png': true,
　　　　　　'image/jpeg': true,
　　　　　　'image/gif': true
　　　　};
        oReader.onload = function (event) {

            //检查是否为可预览的图片类型
    　　　　if (acceptedTypes[ oFile.type] === true) {
                 // 获取 img标签
                var oImage = document.getElementById('preview');
                 // e.target.result contains the DataURL which we will use as a source of the image
                oImage.src = event.target.result;
        　　　　oImage.onload = function () { // binding onload event
                // we are going to display some custom image information here
                    sResultFileSize = bytesToSize(oFile.size);
                    document.getElementById('fileinfo').style.display = 'block';
                    document.getElementById('filename').innerHTML = 'Name: ' + oFile.name;
                    document.getElementById('filesize').innerHTML = 'Size: ' + sResultFileSize;
                    document.getElementById('filetype').innerHTML = 'Type: ' + oFile.type;
                    document.getElementById('filedim').innerHTML = 'Dimension: ' + oImage.naturalWidth + ' x ' + oImage.naturalHeight;
            };
            }
            else {
                document.getElementById('error1').style.display = 'block';
            }
　　    };
    }

    else{
          document.getElementById('error').style.display = 'block';
        }
    // read selected file as DataURL
    oReader.readAsDataURL(oFile);//FileReader接口提供了一个异步的API，通过这个API可以从浏览器中异步访问文件系统中的数据。因此，FileReader接口可以读取文件中的数据，并将读取的数据放入到内存中去。通过FileReader接口中的readAsDataURL()方法可以获取API异步读取的文件数据，另存为数据URL;将该URL绑定到img标签的src属性上，就可以实现图片的上传预览效果了
}
//文件上传
function startUploading() {
    // cleanup all temp states
    iPreviousBytesLoaded = 0;
    document.getElementById('upload_response').style.display = 'none';
    document.getElementById('error').style.display = 'none';
    document.getElementById('error1').style.display = 'none';
    document.getElementById('error2').style.display = 'none';
    document.getElementById('abort').style.display = 'none';
    document.getElementById('warnsize').style.display = 'none';
    document.getElementById('progress_percent').innerHTML = '';
    var oProgress = document.getElementById('progress');
    oProgress.style.display = 'block';
    oProgress.style.width = '0px';

    //获取要提交的数据
    //var vFD = document.getElementById('upload_form').getFormData(); // for FF3
    var vFD = new FormData(document.getElementById('upload_form'));//这种方式创建的FormData对象会自动将form中的表单值也包含进去，包括文件内容也会被编码之后包含进去。

    //创建一个XMLHttpRequest对象，并添加监听事件，最后send our data
    var oXHR = new XMLHttpRequest();
    oXHR.upload.addEventListener('progress', uploadProgress, false);
    oXHR.addEventListener('load', uploadFinish, false);
    oXHR.addEventListener('error', uploadError, false);
    oXHR.addEventListener('abort', uploadAbort, false);
    oXHR.open('POST', '/upload');
    oXHR.send(vFD);

    // set inner timer
    oTimer = setInterval(doInnerUpdates, 300);
}


function doInnerUpdates() { // we will use this function to display upload speed
    var iCB = iBytesUploaded;
    var iDiff = iCB - iPreviousBytesLoaded;

    // if nothing new loaded - exit
    if (iDiff == 0)
        return;

    iPreviousBytesLoaded = iCB;
    iDiff = iDiff * 2;
    var iBytesRem = iBytesTotal - iPreviousBytesLoaded;
    var secondsRemaining = iBytesRem / iDiff;

    // update speed info
    var iSpeed = iDiff.toString() + 'B/s';
    if (iDiff > 1024 * 1024) {
        iSpeed = (Math.round(iDiff * 100/(1024*1024))/100).toString() + 'MB/s';
    } else if (iDiff > 1024) {
        iSpeed =  (Math.round(iDiff * 100/1024)/100).toString() + 'KB/s';
    }

    document.getElementById('speed').innerHTML = iSpeed;
    document.getElementById('remaining').innerHTML = '| ' + secondsToTime(secondsRemaining);
}

function uploadProgress(e) { // upload process in progress
    if (e.lengthComputable) {
        iBytesUploaded = e.loaded;
        iBytesTotal = e.total;
        var iPercentComplete = Math.round(e.loaded * 100 / e.total);
        var iBytesTransfered = bytesToSize(iBytesUploaded);

        document.getElementById('progress_percent').innerHTML = iPercentComplete.toString() + '%';
        document.getElementById('progress').style.width = (iPercentComplete * 4).toString() + 'px';
        document.getElementById('b_transfered').innerHTML = iBytesTransfered;
        if (iPercentComplete == 100) {
            var oUploadResponse = document.getElementById('upload_response');
            oUploadResponse.innerHTML = '<h1>Please wait...processing</h1>';
            oUploadResponse.style.display = 'block';
        }
    } else {
        document.getElementById('progress').innerHTML = 'unable to compute';
    }
}

function uploadFinish(e) { // upload successfully finished
    var oUploadResponse = document.getElementById('upload_response');
    oUploadResponse.innerHTML = e.target.responseText;
    oUploadResponse.style.display = 'block';

    document.getElementById('progress_percent').innerHTML = '100%';
    document.getElementById('progress').style.width = '400px';
    document.getElementById('filesize').innerHTML = sResultFileSize;
    // document.getElementById('remaining').innerHTML = '| 00:00:00';

    clearInterval(oTimer);
}

function uploadError(e) { // upload error
    document.getElementById('error2').style.display = 'block';
    clearInterval(oTimer);
}

function uploadAbort(e) { // upload abort
    document.getElementById('abort').style.display = 'block';
    clearInterval(oTimer);
}