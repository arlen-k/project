<!--
 * @Description: 
 * @Version: 2.0
 * @Autor: 作者博客：www.arlen.top
 * @Date: 2021-11-16 16:44:15
 * @LastEditors: Seven
 * @LastEditTime: 2021-12-08 10:23:14
-->
<template>
  <div>
    <div id="container"></div>
  </div>
</template>

<script>
import * as THREE from "three";
// import { OrbitControls } from "three/examples/jsm/controls/OrbitControls.js";
// import { color } from "echarts";
export default {
  data() {
    return {
      camera: null,
      scene: null,
      renderer: null,
      mesh: null,
      controls: null,
    };
  },
  mounted() {
    this.init();
    // this.animate();
  },
  methods: {
    //初始化
    init() {
      var scene = new THREE.Scene();
      /*
       * 创建网格模型
       */
      var geometry = new THREE.SphereGeometry(60, 40, 40); //创建一个球体几何对象
      //   var geometry = new THREE.BoxGeometry(100, 100, 100); //创建一个立方体几何对象Geometry
      var material = new THREE.MeshLambertMaterial({
        color: 0x00ff00,
      }); //材质对象Material

      var mesh = new THREE.Mesh(geometry, material); //网格模型对象Mesh
      scene.add(mesh); //网格模型添加到场景中
      /**
       * 光源设置
       */
      //点光源
      var point = new THREE.PointLight(0xffffff);
      point.position.set(400, 200, 300); //点光源位置
      scene.add(point); //点光源添加到场景中
      //环境光
      var ambient = new THREE.AmbientLight(0x444444);
      scene.add(ambient);
      // console.log(scene)
      // console.log(scene.children)
      /**
       * 相机设置
       */
      var width = window.innerWidth; //窗口宽度
      var height = window.innerHeight; //窗口高度
      var k = width / height; //窗口宽高比
      var s = 500; //三维场景显示范围控制系数，系数越大，显示的范围越大
      //创建相机对象
      var camera = new THREE.OrthographicCamera(-s * k, s * k, s, -s, 1, 1000);
      camera.position.set(200, 300, 200); //设置相机位置
      camera.lookAt(scene.position); //设置相机方向(指向的场景对象)
      /**
       * 创建渲染器对象
       */
      var renderer = new THREE.WebGLRenderer();
      renderer.setSize(width, height); //设置渲染区域尺寸
      renderer.setClearColor(0xb9d3ff, 1); //设置背景颜色
      document.body.appendChild(renderer.domElement); //body元素中插入canvas对象
      //执行渲染操作   指定场景、相机作为参数
        renderer.render(scene, camera);
    //   function render() {
    //     console.log(123);
    //     renderer.render(scene, camera); //执行渲染操作
    //     mesh.rotateY(0.1);//每次绕y轴旋转0.01弧度
    //   }
      //间隔20ms周期性调用函数fun,20ms也就是刷新频率是50FPS(1s/20ms)，每秒渲染50次
    //   setInterval(()=>{
    //       render()
    //   }, 20);
      //   this.scene = new THREE.Scene();
      //   //网格模型添加到场景中
      //   let geometry = new THREE.BoxGeometry(0.2, 0.2, 0.2);
      //   let material = new THREE.MeshNormalMaterial({
      //     color: "white",
      //   });
      //   this.mesh = new THREE.Mesh(geometry, material);
      //   this.scene.add(this.mesh);

      //   /**
      //    * 相机设置
      //    */
      //   let container = document.getElementById("container");
      //   this.camera = new THREE.PerspectiveCamera(
      //     70,
      //     container.clientWidth / container.clientHeight,
      //     0.01,
      //     10
      //   );
      //   this.camera.position.z = 1;

      //   /**
      //    * 创建渲染器对象
      //    */
      //   this.renderer = new THREE.WebGLRenderer({ antialias: true });
      //   this.renderer.setSize(container.clientWidth, container.clientHeight);
      //   container.appendChild(this.renderer.domElement);

      //   //创建控件对象
      //   this.controls = new OrbitControls(this.camera, this.renderer.domElement);
    },

    // 动画
    animate() {
      requestAnimationFrame(this.animate);
      this.mesh.rotation.x += 0.01;
      this.mesh.rotation.y += 0.02;
      this.renderer.render(this.scene, this.camera);
    },
  },
};
</script>

<style>
#container {
  position: absolute;
  width: 100%;
  height: 100%;
}
</style>