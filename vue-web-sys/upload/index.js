const config = require('./config.js')
const shell = require('shelljs')
const path = require('path');
let Client = require('ssh2-sftp-client');
// 打包 npm run build
const compileDist = async () => {
  if(shell.exec(`npm run build`).code==0) {
    console.log("打包成功")
  }
}

async function connectSSh() {
  let sftp = new Client();
  sftp.connect({
    host: config.ip, // 服务器 IP
    port: config.port,
    username: config.username,
    password: config.password
  }).then(() => {
    console.log("删除完成");
    return sftp.rmdir(config.rmpath, true);
  }).then(() => {
    // 上传文件
    console.log("开始上传")
    return sftp.uploadDir(path.resolve(__dirname, '../dist'), config.path);
  }).then((data) => {
    console.log("上传完成");
    sftp.end();
  }).catch((err) => {
    console.log(err, '失败');
    sftp.end();
  });
}
async function runTask() {
  await compileDist()     //打包完成
  await connectSSh()      //提交上传
}
runTask()