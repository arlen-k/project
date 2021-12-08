<template>
  <div class="home">
    <div class="seaBox">
      <el-button type="primary" @click="add">新增</el-button>
      <el-input
        class="seaInput"
        v-model="para.content"
        placeholder="请输入内容"
      ></el-input>
      <el-button type="primary" @click="seaBtn">搜索</el-button>
    </div>
    <el-table :data="tableData">
      <el-table-column label="序号" type="index" width="50">
      </el-table-column>
      <el-table-column prop="name" label="姓名"> </el-table-column>
      <el-table-column prop="imgUrl" label="图片"> 
         <template slot-scope="scope">
            <img class="uploadImg" :src="scope.row.url" alt="暂无">
        </template>
      </el-table-column>
      <el-table-column prop="time" label="日期"> </el-table-column>
      <el-table-column prop="content" label="内容"> </el-table-column>
      <el-table-column fixed="right" label="操作" width="100">
        <template slot-scope="scope">
          <el-button type="text" @click="handleClick(scope.row)" size="small"
            >编辑</el-button
          >
          <el-button type="text" @click="deletBtn(scope.row)" size="small"
            >删除</el-button
          >
        </template>
      </el-table-column>
    </el-table>
    <el-dialog
      title="提示"
      :modal-append-to-body="false"
      :visible.sync="dialogVisible"
      width="30%"
      @before-close="dialogVisible=false"
    >
     <el-form label-width="80px" class="demo-ruleForm"  >
      <el-form-item label="留言" prop="name">
        <el-input class="message" v-model="content" placeholder="请输入内容"></el-input>
      </el-form-item>
      <el-form-item label="图片" prop="show">
        <el-upload
        class="avatar-uploader"
        action="/member/photo/upload"
        :show-file-list="false"
        :on-success="handleAvatarSuccess"
        :before-upload="beforeAvatarUpload"
        :headers="headers"
      >
        <img v-if="imageUrl" :src="imageUrl" class="avatar" />
        <i v-else class="el-icon-plus avatar-uploader-icon"></i>
      </el-upload>
      </el-form-item>
    </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="addList">确 定</el-button>
      </span>
    </el-dialog>
    <pagination @change="change" :total="total" />
  </div>
</template>

<script>
import { getMsgList, addmessage, deleteMsg, editMsg,httpImg } from '@/api'
import pagination from '@/components/pagination'
export default {
  components: {
    pagination,
  },
  data() {
    return {
      headers: {"token":sessionStorage.token},
      dialogVisible: false,
      tableData: [],
      total: 0,
      content: '',
      imgUrl: '',
      para: {
        page: 1,
        size: 10,
        content: '',
      },
      item: '',
      imageUrl: '',
    }
  },
  mounted() {
    this.getList()
  },
  methods: {
    seaBtn(){
      this.para.page = 1
      this.getList()
    },
    handleAvatarSuccess(res, file) {
      this.imgUrl = res.data.name
      this.imageUrl = URL.createObjectURL(file.raw)
    },
    beforeAvatarUpload(file) {
      const isJPG = file.type === 'image/jpeg'
      const isLt2M = file.size / 1024 / 1024 < 2

      if (!isJPG) {
        this.$message.error('上传头像图片只能是 JPG 格式!')
      }
      if (!isLt2M) {
        this.$message.error('上传头像图片大小不能超过 2MB!')
      }
      return isJPG && isLt2M
    },
    add() {
      this.dialogVisible = true
      this.item = ''
      this.imageUrl = ''
      this.imgUrl = ''
      this.content = ''
    },
    deletBtn(row) {
      this.$confirm('确认删除？')
        .then((_) => {
          deleteMsg({ id: row.id }).then((res) => {
            if (res.code == 200) {
              this.$message({
                message: '删除成功',
                type: 'success',
              })
              this.para.page = 1
              this.getList()
            }
          })
        })
        .catch((_) => {})
    },
    addList() {
      if (this.item != '') {
        let data = {
          content: this.content,
          id: this.item.id,
          imgUrl: this.imgUrl,
        }
        editMsg(data).then((res) => {
          if (res.code == 200) {
            this.reset()
          }
        })
        return
      }
      let par = {
        name: sessionStorage.userName,
        content: this.content,
        imgUrl: this.imgUrl,
      }
      addmessage(par).then((res) => {
        if (res.code == 200) {
          this.reset()
        }
      })
    },
    reset() {
      this.dialogVisible = false
      this.content = ''
      this.item = ''
      this.getList()
    },
    handleClose() {
      this.item = ''
      this.content = ''
    },
    handleClick(row) {
      this.item = row
      this.content = row.content
      this.imgUrl = row.imgUrl // 参数
      this.imageUrl = row.url // 展示
      this.dialogVisible = true
    },
    getList() {
      getMsgList(this.para).then((res) => {
         if (res.code == 200) {
            this.tableData = res.data.data.map(data=>{
              data.url = httpImg+data.imgUrl
              return data
            })
            this.total = res.data.total
         }
      })
    },
    change(page) {
      this.para.page = page
      this.getList()
    },
  },
}
</script>

<style lang="scss" scoped>
.seaBox {
  text-align: right;
  .seaInput {
    width: 200px;
    margin: 0 20px;
  }
}
.uploadImg{
    max-width: 100px;
}
.label{
  margin-bottom: 20px;
  .message{
    width: 80%;
  }
}

</style>
 