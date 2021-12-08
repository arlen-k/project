<template>
  <div>
    <el-form
      :model="ruleForm"
      :rules="rules"
      ref="ruleForm"
      label-width="100px"
      class="demo-ruleForm"
    >
      <el-form-item label="文章标题" prop="name">
        <el-input v-model="ruleForm.name"></el-input>
      </el-form-item>
      <el-form-item label="是否显示" prop="show">
        <el-switch v-model="ruleForm.show"></el-switch>
      </el-form-item>
      <el-form-item label="标题图" required>
        <el-upload
          class="avatar-uploader"
          :action="upUrl"
          :show-file-list="false"
          :on-success="handleAvatarSuccess"
          :headers="headers"
          :before-upload="beforeAvatarUpload"
        >
          <img v-if="imageUrl" :src="imageUrl" class="avatar" />
          <i v-else class="el-icon-plus avatar-uploader-icon"></i>
        </el-upload>
      </el-form-item>

      <el-form-item label="文章类型" prop="type">
        <el-radio-group v-model="ruleForm.type">
          <el-radio v-for="item in options" :key="item.value" :label="item.value">{{item.label}}</el-radio>
        </el-radio-group>
      </el-form-item>
      <el-form-item label="文章内容" prop="content">
        <tinymce v-model="ruleForm.content" :height="300" />
      </el-form-item>
      <el-form-item label="备注">
        <el-input type="textarea" v-model="ruleForm.remake"></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="submitForm('ruleForm')"
          >提交</el-button
        >
        <el-button @click="$router.go(-1)">返回</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>
<script>
import { addArtic, artInfo, editArt, httpImg, upUrl } from "@/api";
import Tinymce from "@/components/Tinymce";
import {typeList} from '@/utils/config'
export default {
  components: {
    Tinymce,
  },
  data() {
    return {
      options:typeList,
      upUrl: upUrl,
      headers: {
        token: sessionStorage.token,
      },
      ruleForm: {
        name: "",
        show: true,
        type: '',
        content: "",
        remake: "",
        imgUrl: "",
      },
      imgUrl: "",
      imageUrl: "",
      rules: {
        name: [{ required: true, message: "请输入文章标题", trigger: "blur" }],
        type: [
          {
            required: true,
            message: "请至少选择一个文章类型",
            trigger: "change",
          },
        ],
        content: [{ required: true, message: "请输入文章", trigger: "blur" }],
      },
    };
  },
  mounted() {
    const { id } = this.$route.query;
    if (id) this.info(id);
  },
  methods: {
    info(id) {
      artInfo({ id: id }).then((res) => {
        if (res.code == 200) {
          this.ruleForm = res.data
          this.ruleForm.type = this.ruleForm.type
          this.ruleForm.show = this.ruleForm.show == 1 ? true : false
          this.imageUrl = httpImg + res.data.imgUrl
          this.imgUrl = res.data.imgUrl
        }
      })
    },
    handleAvatarSuccess(res, file) {
      this.imgUrl = res.data.name;
      this.imageUrl = URL.createObjectURL(file.raw);
    },
    beforeAvatarUpload(file) {
      const isJPG = file.type === "image/jpeg" || "image/png";
      const isLt2M = file.size / 1024 / 1024 < 2;

      if (!isJPG) {
        this.$message.error("上传头像图片只能是 JPG 格式!");
      }
      if (!isLt2M) {
        this.$message.error("上传头像图片大小不能超过 2MB!");
      }
      return isJPG && isLt2M;
    },
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          let data = this.ruleForm;
          data.show = data.show ? 1 : 0;
          data.imgUrl = this.imgUrl;
          if (this.$route.query.id) {
            data.id = this.$route.query.id;
            editArt(data).then((res) => {
              if (res.code == 200) {
                this.$router.go(-1);
              }
            });
            return;
          }
          addArtic(data).then((res) => {
            if (res.code == 200) {
              this.$router.go(-1);
            }
          });
        } else {
          console.log("error submit!!");
          return false;
        }
      });
    },
    resetForm(formName) {
      this.$refs[formName].resetFields();
    },
  },
};
</script>