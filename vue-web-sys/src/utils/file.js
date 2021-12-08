import { getUpload } from '../api/index'
// 富文本 配置
export default {
    toolbar: `formatselect | code | preview | bold italic strikethrough forecolor backcolor | 
    link image | alignleft aligncenter alignright alignjustify  | 
    numlist bullist outdent indent`,
    height: '400px',
    width: '100%',
    // template autosave save imagetools
    plugins:
        'preview paste importcss searchreplace autolink directionality code visualblocks visualchars fullscreen image link media codesample table charmap hr pagebreak nonbreaking anchor toc insertdatetime advlist lists wordcount textpattern noneditable help charmap quickbars emoticons',
    imagetools_cors_hosts: ['picsum.photos'],
    // save  print template 工具被隐藏
    // 撤销次数,默认无限次
    custom_undo_redo_levels: 30,
    // 行高 5.5版本后支持
    lineheight_formats: '1 1.1 1.2 1.3 1.4 1.5 2',
    // 字体
    font_formats:
        '宋体=simsun,serif;' +
        '仿宋=FangSong,serif;' +
        '新宋体=NSimSun,serif;' +
        '黑体=SimHei,serif;' +
        '楷体=KaiTi,serif;' +
        '微软雅黑=Microsoft YaHei,Helvetica Neue,PingFang SC,sans-serif;' +
        '隶书=LiSu,serif;' +
        '幼圆=YouYuan,serif;' +
        '华文细黑=STXihei,serif;' +
        '华文楷体=STKaiti,serif;' +
        '华文宋体=STSong,serif;' +
        // 默认字体
        'Andale Mono=andale mono,times; Arial=arial,helvetica,sans-serif; Arial Black=arial black,avant garde; Book Antiqua=book antiqua,palatino; Comic Sans MS=comic sans ms,sans-serif; Courier New=courier new,courier; Georgia=georgia,palatino; Helvetica=helvetica; Impact=impact,chicago; Symbol=symbol; Tahoma=tahoma,arial,helvetica,sans-serif; Terminal=terminal,monaco; Times New Roman=times new roman,times; Trebuchet MS=trebuchet ms,geneva; Verdana=verdana,geneva; Webdings=webdings; Wingdings=wingdings,zapf dingbats',
    // 字号
    // fontsize_formats: '8pt 10pt 12pt 14pt 18pt 24pt 36pt',
    toolbar_sticky: false,
    image_advtab: true,
    importcss_append: true,
    file_picker_callback(callback, _value, meta) {
    },
    template_cdate_format: '[Date Created (CDATE): %m/%d/%Y : %H:%M:%S]',
    template_mdate_format: '[Date Modified (MDATE): %m/%d/%Y : %H:%M:%S]',
    image_caption: true,
    quickbars_selection_toolbar:
        'bold italic | quicklink h2 h3 blockquote quickimage quicktable',
    noneditable_noneditable_class: 'mceNonEditable',
    toolbar_mode: 'sliding',
    // contextmenu: 'link image imagetools table',
    // skin: 'oxide-dark',
    // content_css: 'dark' ,
    content_style: 'body { font-family: Microsoft YaHei; font-size:14px } img { display: block;max-width: 100%;height: auto; }',
    language: 'zh_CN',
    language_url: '/upload/supermarket-common/zh_CN.js',
    // 支持本地图片上传
    powerpaste_allow_local_images: true,
    images_reuse_filename: true,
    media_live_embeds: true,
    images_upload_handler: (blobInfo, success, failure) => {
        const blob= blobInfo.blob();
        let params = new FormData()
        params.append('file',blob)
        getUpload(params).then(res=>{
            success(res.result)
        },err=>{
            failure('上传失败:'+err)
        })
    },
    media_poster: false,
    media_alt_source: false,
    // video_template_callback(data) {
    //   return `<video src="${data.source}" width="${data.width}" height="${data.height}" ${(data.poster ? ` poster="${data.poster}"` : '')} controls="controls"></video>`;
    // },
}