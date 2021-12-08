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
      <el-table-column prop="cover_pic" label="图片"> 
        <template slot-scope="scope">
          <img class="uploadImg" :src="scope.row.cover_pic" alt="暂无">
        </template>
      </el-table-column>
      <el-table-column prop="pub_date" label="日期"> </el-table-column>
      <el-table-column prop="view_counter" label="播放量"> </el-table-column>
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
      width="40%"
      @before-close="dialogVisible=false"
    >
     <el-form label-width="100px" class="demo-ruleForm"  >
      <el-form-item label="名称" prop="name">
        <el-input class="message" v-model="item.name" placeholder="请输入名称" ></el-input>
      </el-form-item>
      <el-form-item label="封面图链接" prop="cover_pic">
         <el-input class="message" v-model="item.cover_pic" placeholder="请输入封面图" maxlenth='150'></el-input>
      </el-form-item>
      <el-form-item label="分类" prop="classify">
         <el-input class="message" v-model="item.classify" placeholder="请输入分类" maxlenth='150'></el-input>
      </el-form-item>
        <el-form-item label="主演" prop="actor">
         <el-input class="message" v-model="item.actor" placeholder="请输入主演" maxlenth='150'></el-input>
      </el-form-item>
       <el-form-item label="播放链接" prop="url">
         <el-input class="message" v-model="item.url" placeholder="请输入封面图" maxlenth='150'></el-input>
      </el-form-item>
       <el-form-item label="简介" prop="desc">
         <el-input class="message" :rows="7" type="textarea" v-model="item.desc" placeholder="请输入简介" maxlenth='5555'></el-input>
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
import { getVideoList, deleteVideo, editVideo,addvideo } from '@/api'
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
      item:{
        name:'',
        cover_pic:'',
        classify:'',
        actor:'',
        url:'',
        desc:''
      },
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
      // this.item = {
      //   name:'',
      //   cover_pic:'',
      //   classify:'',
      //   actor:'',
      //   url:'',
      //   desc:''
      // }
      // this.imageUrl = ''
      // this.imgUrl = ''
      // this.content = ''
    },
    deletBtn(row) {
      this.$confirm('确认删除？')
        .then((_) => {
          deleteVideo({ id: row.id }).then((res) => {
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
      if (this.item.id) {
        editVideo(this.item).then((res) => {
          if (res.code == 200) {
            this.reset()
          }
        })
        return
      }
    
      addvideo(this.item).then((res) => {
        if (res.code == 200) {
          this.reset()
        }
      })
    },
    reset() {
      this.dialogVisible = false
      this.getList()
    },
    handleClick(row) {
      this.item = row
      this.dialogVisible = true
    },
    getList() {
      getVideoList(this.para).then((res) => {
         if (res.code == 200) {
            this.tableData = res.data.data.map(data=>{
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
 