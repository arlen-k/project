/*
 * @Description: 
 * @Version: 2.0
 * @Autor: 作者博客：www.arlen.top
 * @Date: 2021-07-06 10:02:20
 * @LastEditors: Seven
 * @LastEditTime: 2021-11-16 16:54:42
 */
import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

export const routes = [
  {
    path: '/',
    redirect: "blog",
  },{
    path:'/blog',
    name: 'blog',
    component: () => import('../views/blog'),
    meta: {
      title: "博客",
    }
  },
  {
  path: '/',
  component: () => import('../views/index.vue'),
  children:[{
    path: '/home',
    name: 'home',
    component: () => import('../views/article'),
    meta: {
      title: "文章列表",
      navigation:true
    }
  },{
    path:'/articleInfo',
    name: 'articleInfo',
    component: () => import('../views/article/info'),
    meta: {
      title: "文章添加",
    }
  },{
    path: '/msg',
    name: 'msg',
    component: () => import('../views/msg'),
    meta: {
      title: "消息中心",
      navigation:true
    }
  },{
    path:'/bigData',
    name: 'bigData',
    component: () => import('@/views/bigData'),
    meta: {
      title: "大数据",
      navigation:true
    }
  },{
    path:'/video',
    name:'video',
    component: () => import('@/views/video'),
    meta: {
      title: "视频",
      navigation:true
    }
  }]
},{
  path: '/login',
  name: 'login',
  component: () => import('../views/login')
},{
  path: "*",
  redirect: "/blog"
}]

const router = new VueRouter({
  mode: "hash", //history
  routes
})

export default router