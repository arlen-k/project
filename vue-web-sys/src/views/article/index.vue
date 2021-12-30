<template>
  <div class="home">
    <div class="seaBox">
      <el-select v-model="para.state" placeholder="请选择">
        <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value">
        </el-option>
      </el-select>
      <el-input class="seaInput" v-model="para.name" placeholder="请输入内容"></el-input>
      <el-button type="primary" @click="seaBtn">搜索</el-button>
      <el-button type="primary" @click="add">新增</el-button>
    </div>
    <el-table :data="tableData">
      <el-table-column label="序号" type="index" width="50">
      </el-table-column>
      <el-table-column prop="name" label="文章名称"> </el-table-column>
      <el-table-column prop="imgUrl" label="图片">
        <template slot-scope="scope">
          <img class="uploadImg" :src="scope.row.url" alt="暂无">
        </template>
      </el-table-column>
      <el-table-column prop="time" label="日期"> </el-table-column>
      <el-table-column fixed="right" label="操作" width="100">
        <template slot-scope="scope">
          <el-button type="text" @click="handleClick(scope.row)" size="small">编辑</el-button>
          <el-button type="text" @click="deletBtn(scope.row)" size="small">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    <pagination @change="change" :total="total" />
  </div>
</template>

<script>
  import { getArtList, deleteArt, httpImg } from '@/api'
  import pagination from '@/components/pagination'
  import { typeList } from '@/utils/config'
  export default {
    components: {
      pagination,
    },
    data() {
      return {
        options: typeList,
        dialogVisible: false,
        tableData: [],
        total: 0,
        content: '',
        imgUrl: '',
        para: {
          page: 1,
          size: 10,
          name: '',
        },
        item: '',
        imageUrl: '',
      }
    },
    mounted() {
      this.getList()
    },
    methods: {
      seaBtn() {
        this.para.page = 1
        this.getList()
      },
      add() {
        this.$router.push('/articleInfo')
      },
      deletBtn(row) {
        this.$confirm('确认删除？')
          .then((_) => {
            deleteArt({ id: row.id }).then((res) => {
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
          .catch((_) => { })
      },
      handleClick(row) {
        this.$router.push({ path: '/articleInfo', query: { id: row.id } })
      },
      getList() {
        getArtList(this.para).then((res) => {
          if (res.code == 200) {
            this.tableData = res.data.data.map(data => {
              data.url = httpImg + data.imgUrl
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

  .uploadImg {
    max-width: 100px;
  }

  .label {
    margin-bottom: 20px;

    .message {
      width: 80%;
    }
  }
</style>
<style>
  .uploadImg {
    border-radius: 4px;
    width: 100%;
  }

  .avatar-uploader .el-upload {
    border: 1px dashed #d9d9d9;
    border-radius: 6px;
    cursor: pointer;
    position: relative;
    overflow: hidden;
  }

  .avatar-uploader .el-upload:hover {
    border-color: #409eff;
  }

  .avatar-uploader-icon {
    font-size: 28px;
    color: #8c939d;
    width: 178px;
    height: 178px;
    line-height: 178px;
    text-align: center;
  }

  .avatar {
    width: 178px;
    height: 178px;
    display: block;
  }
</style>