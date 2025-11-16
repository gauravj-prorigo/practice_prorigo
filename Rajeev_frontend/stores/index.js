
export const state = () => ({
  tasks: [] 
})

export const mutations = {
  ADD_TASK(state, task) {
    state.tasks.push(task)
  },
  TOGGLE_TASK(state, taskId) {
    const task = state.tasks.find(t => t.id === taskId)
    if (task) task.completed = !task.completed
  },
  DELETE_TASK(state, taskId) {
    state.tasks = state.tasks.filter(t => t.id !== taskId)
  }
}

export const actions = {
  addTask({ commit }, task) {
    commit('ADD_TASK', task)
  },
  toggleTask({ commit }, taskId) {
    commit('TOGGLE_TASK', taskId)
  },
  deleteTask({ commit }, taskId) {
    commit('DELETE_TASK', taskId)
  }
}

export const getters = {
  allTasks(state) {
    return state.tasks
  },
  completedTasks(state) {
    return state.tasks.filter(t => t.completed)
  },
  pendingTasks(state) {
    return state.tasks.filter(t => !t.completed)
  }
}
