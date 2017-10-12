import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/test',
      name: 'landing-page',
      component: require('@/components/LandingPage').default
    },
    {
      path: '/list',
      name: 'list',
      component: require('@/components/List').default
    },
    {
      path: '/upload',
      name: 'upload',
      component: require('@/components/Upload').default
    },
    {
      path: '*',
      redirect: '/list'
    }
  ]
})
