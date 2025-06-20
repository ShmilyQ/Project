import { createStore } from 'vuex'
import auth from './modules/auth'
import warehouse from './modules/warehouse'
import product from './modules/product'
import inventory from './modules/inventory'
import order from './modules/order'

export default createStore({
  modules: {
    auth,
    warehouse,
    product,
    inventory,
    order
  }
})