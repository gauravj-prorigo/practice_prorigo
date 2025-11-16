// plugins/toast.client.ts
import Toast from 'vue-toastification'
import 'vue-toastification/dist/index.css'
export default defineNuxtPlugin((nuxtApp) => {
  nuxtApp.vueApp.use(Toast, {
    position: 'top-right',
    timeout: 2500,
    pauseOnHover: true,
    draggable: true,
  })
})
