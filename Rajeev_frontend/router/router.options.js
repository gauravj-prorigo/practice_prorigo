// app/router.options.js
export default {
  routes: (routes) => {
    return [
      ...routes,
      {
        path: '/blogcreate',
        name: 'blogcreate',
        component: () => import('~/components/BlogForm.vue')
      }
    ]
  }
}
